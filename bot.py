import os
import re
import random
import json
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta
from dotenv import load_dotenv

from type_generation import type_people, type_thing, type_upgrade, type_responses, brownie_responses, rrisky_responses, david_responses, random_compliments

# Create an Intents object with the intents you want to enable
intents = discord.Intents.default()
intents.message_content = True  # Enable the message_content intent if you want to listen to messages

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

## Remind functionality 

# Get the directory where bot.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to the reminders.json file
REMINDERS_FILE = os.path.join(BASE_DIR, 'reminders.json')

# Check that there is a reminders.json file
def ensure_reminders_file_exists():
    if not os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, 'w') as f:
            json.dump([], f)

# Load saved reminders 
def load_reminders():
    ensure_reminders_file_exists()
    with open(REMINDERS_FILE, 'r') as f:
        return json.load(f)
    
# Store reminder to json    
def store_reminder(user_id, reminder_time, message, message_link):
    reminders = load_reminders()
    reminders.append({
        'user_id': user_id, 
        'reminder_time': reminder_time.isoformat(), 
        'message': message,
        'message_link': message_link  # Store the link to the previous message
    })
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f)

def parse_duration(duration):
    time_pattern = re.compile(r'((?P<years>\d+)y)?((?P<months>\d+)mo)?((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?((?P<seconds>\d+)s)?')
    match = time_pattern.fullmatch(duration)
    if not match:
        return None
    return {name: int(value) for name, value in match.groupdict(default='0').items()}

def calculate_reminder_time(time_params):
    now = datetime.now()
    reminder_time = now + timedelta(days=time_params['days'], seconds=time_params['seconds'], minutes=time_params['minutes'], hours=time_params['hours'])
    reminder_time = reminder_time.replace(year=reminder_time.year + time_params['years'])
    month = reminder_time.month + time_params['months']
    if month > 12:
        reminder_time = reminder_time.replace(year=reminder_time.year + 1, month=month - 12)
    else:
        reminder_time = reminder_time.replace(month=month)
    return reminder_time

#  Checks reminders every minute
async def check_reminders():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now = datetime.now()
        reminders = load_reminders()
        updated_reminders = []
        for reminder in reminders:
            reminder_time = datetime.fromisoformat(reminder['reminder_time'])
            if now >= reminder_time:
                user = await bot.fetch_user(reminder['user_id'])
                message_link = reminder.get('message_link', '')
                await user.send(f"Reminder: {reminder['message']}\nHere is the original message: {message_link}")
                # Do not add this reminder to updated_reminders, effectively removing it
            else:
                updated_reminders.append(reminder)
        
        # Save the updated reminders list, which excludes sent reminders
        with open(REMINDERS_FILE, 'w') as f:
            json.dump(updated_reminders, f)
        
        await asyncio.sleep(60)


@bot.event
async def on_ready():
    print("Bot Commands up and running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    bot.loop.create_task(check_reminders())
    await bot.change_presence(activity=discord.CustomActivity(name='umm', emoji='😳'))

# Reminder Command        
@bot.tree.command(name="remindme")
@app_commands.describe(duration="e.g. '1y 2mo 3d 4h 5m 6s", message="Reminder message")
async def remindme(interaction: discord.Interaction, duration: str, message: str):
    time_params = parse_duration(duration)
    if time_params is None: 
        await interaction.response.send_message("Invalid time format! Please try something like `2mo`, or `5m6s` etc.", ephemeral=True)
        return
    
    # Fetch recent messages to find the most recent message before the command
    channel = interaction.channel
    messages = [msg async for msg in channel.history(limit=50)]  # Increased limit to get more context
    
    prev_message = None
    for msg in messages:
        if msg.created_at < interaction.created_at:
            prev_message = msg
            break
    
    message_link = prev_message.jump_url if prev_message else None
    
    reminder_time = calculate_reminder_time(time_params)
    store_reminder(interaction.user.id, reminder_time, message, message_link)
    await interaction.response.send_message(f'Reminder set for {reminder_time}', ephemeral=True)

# Example code
# @bot.tree.command(name="say")
# @app_commands.describe(thing_to_say="what should I say?")
# async def say(interaction: discord.Interaction, thing_to_say: str):
#     await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")

restricted_channel_id = 1280670129939681357

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id == restricted_channel_id:
            return
    # Return who is brownie after mention
    # if any(trigger in message.content.lower() for trigger in ['<@1137831321599746158>', 'brownie']):
    #     response = 'who tf is brownie?'
    #     await message.channel.send(response)

    # Return a response after pinging type
    if message.content.lower() in ['type', '<@382370044144779265>']:
        def make_sentence():
            return " ".join([person(), thing(), upgrade()])

        def person():
            return random.choice(type_people)
        def thing(): 
            return random.choice(type_thing)
        def upgrade():
            return random.choice(type_upgrade)
        
        if random.random() < 0.333:

            response = random.choice(type_responses)
        else:
            response = make_sentence()

        await message.channel.send(response)

    if any(trigger in message.content.lower() for trigger in ['rrisky', 'risky', '<@332537342705401856>']):
        response = random.choice(rrisky_responses)
        await message.channel.send(response)

    if any(trigger in message.content.lower() for trigger in ['david', 'flare', '<@125063361196064768>']):
        response = random.choice(david_responses)
        await message.channel.send(response)

    # Return a picture of dylans foot after someone says toe
    if message.content == 'toe': 
        response = 'https://i.imgur.com/H8u43Up.png'
        await message.channel.send(response)

    # Uses a list of responses that has a 25% chance to send after brownie sends something that isn't a link or gif in the discord chat.
    if message.author.id == 1137831321599746158:

        if any(trigger in message.content.lower() for trigger in ['https://', 'insult', 'suggestion', 'judge']):
            return
        if random.random() < 0.99:
            return

        browniemessage = message.content
        response = random.choice(brownie_responses)
        response = response.format(browniemessage=browniemessage)

        await message.channel.send(response)

    if message.channel.id == 1283271970900938833: 
        if any(trigger in message.content.lower() for trigger in ['crazy']):
            response = 'Crazy? I was crazy once, They locked me in a room, a rubber room, a rubber room with rats, and rats make me crazy.'
            await message.channel.send(response)

    if message:
        if random.random() < 0.99:
            return
        
        response = random.choice(random_compliments)
        await message.channel.send(response)


# Run the bot with the token
bot.run(TOKEN)
