import os
import re
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
# from datetime import datetime, timedelta
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
restricted_channel_id = 1280670129939681357
meep_server_id = 1129622683546554479

@bot.event
async def on_ready():
    print("Bot Commands up and running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    # bot.loop.create_task(check_reminders())
    await bot.change_presence(activity=discord.CustomActivity(name='umm', emoji='😳'))

# Dice Roller
@bot.tree.command(name="roll")
@app_commands.describe(dice="Roll dice using the format 'XdY+Z'")
async def roll(interaction: discord.Interaction, dice: str):
    # Acknowledge the interaction immediately with a placeholder message
    await interaction.response.send_message('Rolling...')

    await asyncio.sleep(1)

    dice_pattern = re.compile(r'(\d*)d(\d+)([+-]\d+)?')
    match = dice_pattern.match(dice)

    if not match:
        await interaction.edit_original_response(content="Invalid dice format. Roll dice using the format 'XdY+Z'.")
        return

    num_dice = int(match.group(1)) if match.group(1) else 1
    dice_size = int(match.group(2))
    dice_modifier = int(match.group(3)) if match.group(3) else 0

    rolls = [random.randint(1, dice_size) for _ in range(num_dice)]
    total = sum(rolls) + dice_modifier

    roll_details = f"Rolls: {', '.join(map(str, rolls))}"

    if dice_modifier:
        roll_details += f" with modifier {dice_modifier}"

    result = f"{interaction.user.mention} rolled {num_dice}d{dice_size}{match.group(3) or ''}: {roll_details}. Total: {total}"

    # Edit the original message with the result
    await interaction.edit_original_response(content=result)

# Secret rolls for the DM
@bot.tree.command(name="dmroll")
@app_commands.describe(dice="Roll dice using the format 'XdY+Z'")
async def roll(interaction: discord.Interaction, dice: str):
    # Acknowledge the interaction immediately with a placeholder message
    await interaction.response.send_message('Rolling...', ephemeral=True)

    await asyncio.sleep(1)

    dice_pattern = re.compile(r'(\d*)d(\d+)([+-]\d+)?')
    match = dice_pattern.match(dice)

    if not match:
        await interaction.edit_original_response(content="Invalid dice format. Roll dice using the format 'XdY+Z'.", ephemeral=True)
        return

    num_dice = int(match.group(1)) if match.group(1) else 1
    dice_size = int(match.group(2))
    dice_modifier = int(match.group(3)) if match.group(3) else 0

    rolls = [random.randint(1, dice_size) for _ in range(num_dice)]
    total = sum(rolls) + dice_modifier

    roll_details = f"Rolls: {', '.join(map(str, rolls))}"

    if dice_modifier:
        roll_details += f" with modifier {dice_modifier}"

    result = f"{interaction.user.mention} rolled {num_dice}d{dice_size}{match.group(3) or ''}: {roll_details}. Total: {total}"

    # Edit the original message with the result
    await interaction.edit_original_response(content=result)

# Whisper command to tell only one person something
@bot.tree.command(name="whisper")
@app_commands.describe(target="The player to send a secret message to", message="The secret message to send")
async def whisper(interaction: discord.Interaction, target: discord.User, message: str):
    # Send a secret message to the target player
    await target.send(f"{interaction.user.mention} whispers: {message}")
    # Let the whisperer know the message was sent
    await interaction.response.send_message(f"Whisper sent to {target.mention}", ephemeral=True)



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id == restricted_channel_id:
        return    



# Meep Specific Commands
    # Do not return anything message is if not in the meep server
    if message.guild.id != meep_server_id:
        return
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
    # Return a message after mentioning rrisky
    if any(trigger in message.content.lower() for trigger in ['rrisky', 'risky', '<@332537342705401856>']):
        response = random.choice(rrisky_responses)
        await message.channel.send(response)
    # Return a message after mentioning david
    if any(trigger in message.content.lower() for trigger in ['david', 'flare', '<@125063361196064768>']):
        response = random.choice(david_responses)
        await message.channel.send(response)
    # Return a picture of dylans foot after someone says toe
    if message.content == 'toe': 
        if random.random() > 0.9:
            response = 'https://i.imgur.com/SsbFqbv.png'
        else:
            response = 'https://i.imgur.com/H8u43Up.png'
        await message.channel.send(response)
    # Return a message if json is mentioned
    if any(trigger in message.content.lower() for trigger in ['json']):
        response = f'<@{382370044144779265}> has been summoned.'
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
    # Return a message only to specific channel if someone says crazy
    if message.channel.id == 1283271970900938833: 
        if any(trigger in message.content.lower() for trigger in ['crazy']):
            response = 'Crazy? I was crazy once, They locked me in a room, a rubber room, a rubber room with rats, and rats make me crazy.'
            await message.channel.send(response)
    # 0.01% chance to send a random compliment
    if message:
        if random.random() < 0.99:
            return
        
        response = random.choice(random_compliments)
        await message.channel.send(response)


# Run the bot with the token
bot.run(TOKEN)
