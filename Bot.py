import discord
import random
import asyncio
from datetime import datetime
import pytz

client = discord.Client()

@client.event
async def on_ready():
    print(f'Wir sind eingeloggt als {client.user}')

# Replace with the channel ID
CHANNEL_ID = channel_ID
# Set Berlin time zone
BERLIN_TIMEZONE = pytz.timezone('Europe/Berlin')
client = discord.Client()

async def clean_channel():
    channel = client.get_channel(CHANNEL_ID)
    try:
        # Get the last 100 messages
        messages = await channel.history(limit=100).flatten()
        
        # Check if there are new messages (except the first one)
        if len(messages) > 1:
            # Lösche alle Nachrichten
            await channel.purge(limit=None)

            # Determine the current time and date in Berlin
            berlin_time = datetime.now(BERLIN_TIMEZONE)
            formatted_datetime = berlin_time.strftime("%d.%m.%Y um %H:%M:%S")

            # Send a message with date and time
            await channel.send(f"Kanal wurde am {formatted_datetime} bereinigt!")
        else:
            print("Keine neuen Nachrichten zum Löschen gefunden.")

    except discord.errors.Forbidden:
        print("Keine Berechtigung zum Löschen von Nachrichten.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

    async def clean_channel_at_specific_time(hour, minute):
        while True:
            now = datetime.now(BERLIN_TIMEZONE)
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            # If the current time is already above the target time,
            # the target time is postponed to the next day
            if now > target_time:
                target_time += timedelta(days=1)

            # Wait until the target time is reached
            await asyncio.sleep((target_time - now).total_seconds())

            # Call the actual cleaning function
            await clean_channel()

            # Wait a second before looping again (optional)
            await asyncio.sleep(1)

    # Example: Clean the channel daily at 3:00 a.m. and 3:00 p.m
    await asyncio.create_task(clean_channel_at_specific_time(14, 22))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Hier kannst du weitere Befehle hinzufügen
    if message.content.startswith('!ping'):
        await message.channel.send('Pong!')

    elif message.content.startswith('!dice'):
        await message.channel.send(f'You have a {random.randint(1, 6)} diced!')

    elif message.content.startswith('!hilfe'):
        await message.channel.send("Available commands:\n!ping: Ping response\n!dice: Rolls a 6-sided die\n!help: Displays this help\n!V: The current version of the bot". file=discord.File('Picture.jpg'))

    elif message.content.startswith('!Test'):
        await message.channel.send('Test LINK -> https://alphagames.info', file=discord.File('tbot.jpg'))

    elif message.content.startswith('command1'):
        await message.channel.send('message 1', file=discord.File('Picture1.jpg'))

    elif message.content.startswith('!command2'):
        await message.channel.send('message 2', file=discord.File('Picture2.jpg'))

    elif message.content.startswith('!command3'):
        await message.channel.send('message 3', file=discord.File('Picture3.jpg'))

@client.event
async def on_ready():
    print(f'Onlein {client.user}')
    while True:
        await clean_channel()

# Replace 'your_bot_token' with your actual bot token
client.run('your_bot_token')
