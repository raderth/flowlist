from flask import Flask, render_template, request, jsonify, redirect, url_for
import shelve
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import requests
import threading
import queue
import asyncio
import aiohttp
import json

message_queue = queue.Queue()
APPLICATIONS_KEY = "applications"
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

def set(key, value):
  with shelve.open('mydb') as db:
      db[key] = value

def get(key):
  with shelve.open('mydb') as db:
      return db.get(key)
  

##### Configuration initiation #####
refresh_commands = False
if not get("server"):
   set("server",input("Minecraft server URL: "))
   refresh_commands = True
if not get("whitelist"):
   user_input = input("Whitelist command (username is added on the end later): ")
   if user_input[:1] == " ":
      user_input = user_input[:-1]
   set("whitelist",user_input)
if not get("ban"):
   user_input = input("Ban command (username is added on the end later): ")
   if user_input[:1] == " ":
      user_input = user_input[:-1]
   set("ban",user_input)
if not get("token"):
   set("token", input("Discord bot token: "))

if not get("managed_roles"):
    set("managed_roles", [])

##### WEB #####
    
app = Flask(__name__)

@app.route('/panel', methods=['GET', 'POST'])
def save_items():
    if request.method == 'POST':
      items = request.json
      print("Received items:", items)
      set('items', items)
      return jsonify({"status": "success"})
    elif request.args.get('code') == 'XPAat7my219H2lxT1auHpSyGTNJRhV0c':
      items = get('items')
      return render_template('panel.html', items=items or [])
    return "<h1>404 not found</h1>"

text = '<input class="small_text" name={} placeholder="{}" required>'
textbox = '<textarea class="textarea" name="{}" placeholder="{}" rows="1" style="resize: none; overflow: hidden;"></textarea>'
checkbox = '<div class="checkbox"><label>{}</label><input type="checkbox" name={} /></div>'

@app.route('/form')
def form():
  items = get('items')
  content = '<input class="small_text" name="in_game_name" placeholder="In game name" required>'
  for item in items:
    replaced = item["label"].replace(" ", "_")
    if item["type"] == "text":
      content += text.format(replaced, item["label"])
    elif item["type"] == "textbox":
      content += textbox.format(replaced, item["label"])
    elif item["type"] == "checkbox":
      content += checkbox.format(item["label"], replaced)
    
  return render_template("index.html", content=content)

TEST_USERNAME = "admin"
TEST_PASSWORD = 'lGGN2ZEfmL'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
  if request.method == 'POST':
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == TEST_USERNAME and password == TEST_PASSWORD:
        return jsonify({"status": "success", "message": 'XPAat7my219H2lxT1auHpSyGTNJRhV0c'}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401
  return render_template("admin.html")

CLIENT_ID = "1272584635674530005"
CLIENT_SECRET = "rs54yY5bxPimT_56hlm0Uw-R2vuWRxR4"
REDIRECT_URI = "http://143.47.234.184/"

@app.route('/')
def oauth_callback():
    code = request.args.get('code')
    if not code:
       return redirect("https://discord.com/oauth2/authorize?client_id=1272584635674530005&response_type=code&redirect_uri=http%3A%2F%2F143.47.234.184%2F&scope=identify", code=302)

    # Exchange the code for a token
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    print(response.status_code)

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']

        # Fetch the user's info
        user_response = requests.get('https://discord.com/api/users/@me', headers={
            'Authorization': f'Bearer {access_token}'
        })
        print(user_response.status_code)
        if user_response.status_code == 200:
            user_info = user_response.json()
            user_id = user_info['id']

            # Send the user ID to your Discord bot
            #message_queue.put(int(user_id))


            return redirect(f"{url_for('form')}?code={user_id}", code=302)
        else:
            return "Failed to fetch user information."
    else:
        return "Authorization failed."
    
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    message_queue.put(data)
    return jsonify({"status": "success"}), 200

@app.route('/success')
def success():
    return "Success"


##### BOT #####

async def process_message_queue():
    while True:
        try:
            data = message_queue.get_nowait()
            print(data)
            await send_confirmation_message(data)
        except queue.Empty:
            await asyncio.sleep(1)
    
class ApplicationView(View):
    def __init__(self, data, message_id):
        super().__init__(timeout=None)
        self.data = data
        self.message_id = message_id

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, custom_id="accept")
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_response(interaction, "Accepted", discord.Color.green())
        await self.send_post_request(self.data, "accepted")

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red, custom_id="deny")
    async def deny_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_response(interaction, "Denied", discord.Color.red())
        await self.send_post_request(self.data, "denied")

    async def handle_response(self, interaction, status, color):
        player_name = self.data.get('name', 'Player')
        response_embed = discord.Embed(title=f"{status}!", description=f"{player_name} was {status.lower()}!", color=color)
        await interaction.response.edit_message(embed=response_embed, view=None)
        
        # Remove the application from the database
        applications = json.loads(get(APPLICATIONS_KEY) or '{}')
        applications.pop(str(self.message_id), None)
        set(APPLICATIONS_KEY, json.dumps(applications))

    async def send_post_request(self, data, status):
        json_data = {**data, "status": status}
        print(f"Sending POST request with data: {json.dumps(json_data)}")
        # Implement actual HTTP POST request here

async def send_confirmation_message(data):
    guild_id = get("guild")
    guild = discord.utils.get(bot.guilds, id=guild_id)
    
    for member in guild.members:
        if int(member.id) == int(data['code']):
            embed = discord.Embed(title="Confirmation", description="Your application has been submitted and is being carefully reviewed", color=0xffa500)
            await member.send(embed=embed)
    
    embed = discord.Embed(title="Application")
    for key, value in data.items():
        embed.add_field(name=key, value=value, inline=False)
    
    channel = bot.get_channel(get("channel"))
    message = await channel.send(embed=embed)
    
    view = ApplicationView(data, message.id)
    await message.edit(view=view)
    
    # Store the application data in the database
    applications = json.loads(get(APPLICATIONS_KEY) or '{}')
    applications[str(message.id)] = data
    set(APPLICATIONS_KEY, json.dumps(applications))

def has_managed_role():
    async def predicate(interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles]
        return any(role_id in get("managed_roles") for role_id in user_roles)
    return app_commands.check(predicate)

MINECRAFT_API_URL = get("server")

@bot.tree.command(name="whitelist", description="Whitelists a player by using the Minecraft server console.")
@app_commands.describe(username="The Minecraft username to whitelist")
@has_managed_role()
async def whitelist(interaction: discord.Interaction, username: str):
    # Send request to Minecraft plugin
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{MINECRAFT_API_URL}", json={"username": username}) as response:
            if response.status == 200:
                await interaction.response.send_message(f"Successfully whitelisted {username}")
            else:
                await interaction.response.send_message(f"Failed to whitelist {username}")

@bot.tree.command(name="ban", description="bans a player by using the minecraft server console.")
@app_commands.describe(username="The Minecraft username to ban")
@has_managed_role()
async def ban(interaction: discord.Interaction, username: str):
    # Send request to Minecraft plugin
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{MINECRAFT_API_URL}", json={"command": ""+username}) as response:
            if response.status == 200:
                await interaction.response.send_message(f"Successfully banned {username}")
            else:
                await interaction.response.send_message(f"Failed to ban {username}")

@whitelist.error
async def whitelist_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.CheckFailure):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {str(error)}", ephemeral=True)

@ban.error
async def whitelist_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.CheckFailure):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message(f"An error occurred: {str(error)}", ephemeral=True)

class ChannelSelect(discord.ui.Select):
    def __init__(self, channels):
        options = [discord.SelectOption(label=channel.name, value=str(channel.id)) for channel in channels]
        super().__init__(placeholder="Select a channel", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        channel_id = int(self.values[0])
        channel = interaction.guild.get_channel(channel_id)
        await interaction.response.send_message(f"Channel: {channel.name}\nChannel ID: {channel.id}\nServer ID: {interaction.guild.id}")

class ChannelView(discord.ui.View):
    def __init__(self, channels):
        super().__init__()
        self.add_item(ChannelSelect(channels))

@bot.tree.command(name="set", description="Sets the channel for applications")
async def get_ids(interaction: discord.Interaction):
    channels = interaction.guild.text_channels
    view = ChannelView(channels)
    await interaction.response.send_message("Please select a channel:", view=view)

@bot.tree.command(name="add", description="Add a role to the managed list")
@app_commands.checks.has_permissions(administrator=True)
async def add_role(interaction: discord.Interaction, role: discord.Role):
    if role.id not in managed_roles:
        managed_roles.append(role.id)
        await interaction.response.send_message(f"Added {role.name} to the managed roles list.")
    else:
        await interaction.response.send_message(f"{role.name} is already in the managed roles list.")

@bot.tree.command(name="remove", description="Remove a role from the managed list")
@app_commands.checks.has_permissions(administrator=True)
async def remove_role(interaction: discord.Interaction, role: discord.Role):
    if role.id in managed_roles:
        managed_roles.remove(role.id)
        await interaction.response.send_message(f"Removed {role.name} from the managed roles list.")
    else:
        await interaction.response.send_message(f"{role.name} is not in the managed roles list.")

@add_role.error
@remove_role.error
async def role_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You don't have permission to use this command. Only administrators can manage roles.", ephemeral=True)



@bot.event
async def on_ready():
    if refresh_commands:
        await bot.tree.sync()
    print(f'Logged in as {bot.user}! Commands synced.')
    # Recreate views for existing applications
    applications = json.loads(get(APPLICATIONS_KEY) or '{}')
    
    for message_id, data in applications.items():
        channel = bot.get_channel(get("channel"))
        try:
            message = await channel.fetch_message(int(message_id))
            view = ApplicationView(data, int(message_id))
            await message.edit(view=view)
        except discord.NotFound:
            # Message no longer exists, remove
            applications.pop(message_id, None)
    
    set(APPLICATIONS_KEY, json.dumps(applications))

    bot.loop.create_task(process_message_queue())

def run_bot():
  bot.run(get("token"))

if __name__ == "__main__":
  threading.Thread(target=run_bot).start()
  app.run(host='0.0.0.0', port=80)
  