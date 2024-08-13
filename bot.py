import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import os

intents = discord.Intents.default()
bot = commands.Bot(intents=intents)

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

bot.run(os.environ['KEY'])
