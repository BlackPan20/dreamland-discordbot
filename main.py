import discord
import os
import asyncio
from server import keep_alive



intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

server_status = "ausgeschaltet"  # Server ist anfangs ausgeschaltet
admin_only_mode = False  # Start with all users allowed

async def update_nickname():
    """Updates the bot's nickname based on server status."""
    global server_status
    for guild in bot.guilds:
        for member in guild.members:
            if member == bot.user:
                if server_status == "ausgeschaltet":
                    await member.edit(nick="DreamlandBot[STOP]")
                else:
                    await member.edit(nick="DreamlandBot")
                break

@bot.event
async def on_message(msg):
    global server_status
    global admin_only_mode

    if msg.author == bot.user:
        return

    print('[New message]', msg.content)

    # Check for admin commands
    if msg.content.lower() == '/admin-only':
        if msg.author.guild_permissions.administrator:  # Check if user is admin
            admin_only_mode = not admin_only_mode  # Toggle admin mode
            await msg.channel.send(f"Admin-only mode is now {'on' if admin_only_mode else 'off'}.")
        else:
            await msg.channel.send("You do not have permission to use this command.")
        return  # Stop processing further commands

    # Only process commands from admins if admin-only mode is on
    if admin_only_mode and not msg.author.guild_permissions.administrator:
        return

    # Antworten auf "Hallo" und "Tschüss"
    if msg.content.lower() == 'hallo':
        await msg.channel.send('Hallo!')
    elif msg.content.lower() == 'tschüss':
        await msg.channel.send('Tschüss, bis zum nächsten Mal!')

    # Server-Management-Befehle
    elif msg.content.lower() == '/start-server':
        if server_status == "läuft":
            await msg.channel.send("Der Server läuft bereits.")
        else:
            server_status = "läuft"
            await msg.channel.send("Der Server wurde gestartet.")
            await update_nickname()  # Update nickname after starting
    elif msg.content.lower() == '/stop-server':
        server_status = "ausgeschaltet"
        await msg.channel.send("Der Server wurde gestoppt.")
        await update_nickname()  # Update nickname after stopping
    elif msg.content.lower() == '/server-status':
        await msg.channel.send(f"Der Server ist momentan {server_status}.")

    # Info command
    elif msg.content.lower() == '/info':
        commands = [
            "/start-server",
            "/stop-server",
            "/server-status",
            "/flip-coin",
            "/roll-dice",
            "/fun-fact",
            "/admin-only" 
        ]
        await msg.channel.send(f"Verfügbare Befehle: {', '.join(commands)}")

    # Weitere coole Features
    elif msg.content.lower() == '/flip-coin':
        outcome = "Kopf" if os.urandom(1)[0] > 127 else "Zahl"
        await msg.channel.send(f"Die Münze zeigt: {outcome}.")
    elif msg.content.lower() == '/roll-dice':
        import random
        dice_roll = random.randint(1, 6)
        await msg.channel.send(f"Du hast eine {dice_roll} geworfen.")
    elif msg.content.lower() == '/fun-fact':
        facts = [
            "Wusstest du, dass Honig niemals schlecht wird?",
            "Das Herz eines Blauwals ist so groß wie ein Auto.",
            "Eine Schnecke kann bis zu drei Jahre schlafen.",
            "Der längste Flug eines Huhns dauerte 13 Sekunden.",
            "Im Weltraum gibt es keine Geräusche."
        ]
        await msg.channel.send(random.choice(facts))
    else:
        await msg.channel.send("Entschuldigung, ich verstehe den Befehl nicht. Versuche es mit /start-server, /stop-server, /server-status, /flip-coin, /roll-dice oder /fun-fact.")




@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Dreamland"))
    await update_nickname()  # Update nickname on startup
keep_alive()
bot.run(os.environ['DISCORD_TOKEN'])