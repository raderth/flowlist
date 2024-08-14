from flask import Flask, render_template, request, jsonify
import shelve
import os
import threading
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def set(key, value):
  with shelve.open('mydb') as db:
      db[key] = value

def get(key):
  with shelve.open('mydb') as db:
      return db.get(key)
  
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
textbox = '<span placeholder="{}" class="textarea" role="textbox" contenteditable></span>'
checkbox = '<div class="checkbox"><label>{}</label><input type="checkbox" name={} /></div>'

def main():
  items = get('items')
  content = ""
  for item in items:
    if item["type"] == "text":
      content += text.format(item["label"], item["label"])
    elif item["type"] == "textbox":
      content += textbox.format(item["label"])
    elif item["type"] == "checkbox":
      content += checkbox.format(item["label"], item["label"])
    
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

    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info['access_token']

        # Fetch the user's info
        user_response = requests.get('https://discord.com/api/users/@me', headers={
            'Authorization': f'Bearer {access_token}'
        })

        if user_response.status_code == 200:
            user_info = user_response.json()
            user_id = user_info['id']

            # Send the user ID to your Discord bot
            bot.loop.create_task(send_confirmation_message(user_id))

            return main()
        else:
            return "Failed to fetch user information."
    else:
        return "Authorization failed."
    
async def send_confirmation_message(user_id):
    channel = bot.get_channel(837786954128687157)
    await channel.send(f"User with ID {user_id} has successfully authorized.")

def run_flask():
  app.run(host='0.0.0.0', port=80, debug=True)

##### BOT #####


@bot.tree.command(name="embed_with_button", description="Sends an embed with a button.")
async def embed_with_button(interaction: discord.Interaction):
    embed = discord.Embed(title="Example Application", description="This is an embed with a button and stuff.")

    button = Button(label="Accept", style=discord.ButtonStyle.green)
    button2 = Button(label="Deny", style=discord.ButtonStyle.red)

    async def button_callback(interaction):
        response_embed = discord.Embed(title="Accepted!", description="player name was accepted!", color=discord.Color.green())
        await interaction.response.edit_message(embed=response_embed, view=None)
        
    async def button2_callback(interaction):
        response_embed = discord.Embed(title="Denied!", description="player name was denied!", color=discord.Color.red())
        await interaction.response.edit_message(embed=response_embed,view=None)

    button.callback = button_callback
    button2.callback = button2_callback

    view = View()
    view.add_item(button)
    view.add_item(button2)

    await interaction.response.send_message(embed=embed, view=view)

@bot.event
async def on_ready():
    #await bot.tree.sync()
    print(f'Logged in as {bot.user}! Commands synced.')

if __name__ == "__main__":
  threading.Thread(target=run_flask).start()
  bot.run('MTI3MjU4NDYzNTY3NDUzMDAwNQ.GyCbE7.CpA43YTQuY7Xve7SScg-HHu_Ku_6yZlBb5ip1I')
  