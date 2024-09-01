# bot.py
import os
import random
import discord
from dotenv import load_dotenv

from type_generation import type_people
from type_generation import type_thing
from type_generation import type_upgrade
from type_generation import type_responses
from type_generation import brownie_responses
from type_generation import rrisky_responses
from type_generation import david_responses


# Create an Intents object with the intents you want to enable
intents = discord.Intents.default()
intents.message_content = True  # Enable the message_content intent if you want to listen to messages

# Pass the intents when creating the Client instance
client = discord.Client(intents=intents)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

# Return who is brownie after mention

    if any(trigger in message.content.lower() for trigger in ['<@1137831321599746158>', 'brownie']):
        response = 'who tf is brownie?'
        await message.channel.send(response)

# Return a response after pinging type
#Procedural Generation moved to seprate files

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
        if 'https://' in message.content:
            return
        if random.random() < 0.25:
            return

        browniemessage = message.content
        response = random.choice(brownie_responses)
        response = response.format(browniemessage=browniemessage)

        await message.channel.send(response)


# Run the bot with the token
client.run(TOKEN)
