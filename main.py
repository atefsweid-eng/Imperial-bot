import discord
from discord import app_commands
import os
import random
import datetime
from server import stay_alive

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("Bot is ready and online!")


@tree.command(name="ping", description="Check the bot's latency")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! Latency: {latency}ms")


@tree.command(name="hello", description="Get a friendly greeting")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.display_name}! How are you doing?")


@tree.command(name="roll", description="Roll a dice")
@app_commands.describe(sides="Number of sides on the dice (default: 6)")
async def roll(interaction: discord.Interaction, sides: int = 6):
    if sides < 2:
        await interaction.response.send_message("A dice must have at least 2 sides!", ephemeral=True)
        return
    result = random.randint(1, sides)
    await interaction.response.send_message(
        f"{interaction.user.display_name} rolled a d{sides} and got **{result}**!"
    )


@tree.command(name="echo", description="Repeat a message")
@app_commands.describe(message="The message to repeat")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message)


@tree.command(name="info", description="Show bot information")
async def info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Bot Info",
        description="A simple slash command bot built with discord.py",
        color=discord.Color.blurple()
    )
    embed.add_field(name="Commands", value="/ping, /hello, /roll, /echo, /info, /help", inline=False)
    embed.set_footer(text=f"Requested by {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed)


@tree.command(name="xenon", description="Erstellt eine Xenon-Scheinwerfer Dokumentation")
@app_commands.describe(
    kunde="Name des Kunden",
    kennzeichen="Das Kennzeichen des Autos",
    farbe="Die Farbe des Xenon-Lichts",
    bild="Lade ein Bild hoch"
)
async def xenon(
    interaction: discord.Interaction,
    kunde: str,
    kennzeichen: str,
    farbe: str,
    bild: discord.Attachment
):
    mitarbeiter = interaction.user
    embed = discord.Embed(title="Xenon-Scheinwerfer Dokumentation", color=discord.Color.green())
    embed.add_field(name="Kunde", value=kunde, inline=True)
    embed.add_field(name="Kennzeichen", value=kennzeichen, inline=True)
    embed.add_field(name="Xenon-Farbe", value=farbe, inline=True)
    embed.add_field(name="Bearbeitet von", value=mitarbeiter.mention, inline=False)
    embed.set_image(url=bild.url)
    zeit = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    embed.set_footer(text=f"Dokumentations-ID: #239 • {zeit}")
    await interaction.response.send_message(embed=embed)


@tree.command(name="stance", description="Erstellt eine Stance-Tuning Dokumentation")
@app_commands.describe(
    kunde="Name des Kunden",
    kennzeichen="Das Kennzeichen des Autos",
    bild="Lade ein Bild hoch"
)
async def stance(
    interaction: discord.Interaction,
    kunde: str,
    kennzeichen: str,
    bild: discord.Attachment
):
    mitarbeiter = interaction.user
    embed = discord.Embed(title="Stance-Tuning Dokumentation", color=discord.Color.dark_magenta())
    embed.add_field(name="Kunde", value=kunde, inline=True)
    embed.add_field(name="Kennzeichen", value=kennzeichen, inline=True)
    embed.add_field(name="Bearbeitet von", value=mitarbeiter.mention, inline=True)
    embed.set_image(url=bild.url)
    zeit = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    embed.set_footer(text=f"Dokumentations-ID: #340 • {zeit}")
    await interaction.response.send_message(embed=embed)


@tree.command(name="abmelden", description="Melde dich für einen Zeitraum ab")
@app_commands.describe(
    grund="Warum meldest du dich ab?",
    von="Startdatum (z.B. 01.05.)",
    bis="Enddatum (z.B. 10.05.)"
)
async def abmelden(interaction: discord.Interaction, grund: str, von: str, bis: str):
    user = interaction.user
    embed = discord.Embed(
        title="📝 Neue Abmeldung",
        color=discord.Color.red(),
        description=f"Der User {user.mention} hat sich abgemeldet."
    )
    embed.add_field(name="📅 Von", value=von, inline=True)
    embed.add_field(name="📅 Bis", value=bis, inline=True)
    embed.add_field(name="📋 Grund", value=grund, inline=False)
    await interaction.response.send_message(embed=embed)


@tree.command(name="help", description="Show all available commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Help - Available Commands",
        color=discord.Color.green()
    )
    embed.add_field(name="/ping", value="Check the bot's latency", inline=False)
    embed.add_field(name="/hello", value="Get a friendly greeting", inline=False)
    embed.add_field(name="/roll [sides]", value="Roll a dice (default: 6 sides)", inline=False)
    embed.add_field(name="/echo <message>", value="Repeat your message", inline=False)
    embed.add_field(name="/info", value="Show bot information", inline=False)
    embed.add_field(name="/xenon", value="Erstellt einen Xenon-Eintrag (Kunde, Kennzeichen, Farbe, Bild)", inline=False)
    embed.add_field(name="/stance", value="Erstellt einen Stance-Eintrag (Kunde, Kennzeichen, Bild)", inline=False)
    embed.add_field(name="/abmelden", value="Melde dich für einen Zeitraum ab (Grund, Von, Bis)", inline=False)
    embed.add_field(name="/help", value="Show this help message", inline=False)
    await interaction.response.send_message(embed=embed)


token = os.environ.get("DISCORD_BOT_TOKEN")
if not token:
    print("ERROR: DISCORD_BOT_TOKEN environment variable is not set.")
    exit(1)

stay_alive()
client.run(token, reconnect=True)
