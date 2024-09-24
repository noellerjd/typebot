import os
import re
import random
import asyncio
import discord
import json
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from type_generation import type_people, type_thing, type_upgrade, type_responses, brownie_responses, rrisky_responses, david_responses, random_compliments

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
restricted_channel_id = 1280670129939681357
meep_server_id = 1129622683546554479
dnd_server_id = 1286406203055935591
personal_server_id = 1288280564155027518

# Discord intents enabled
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# DM XP functions
# Store user XP
user_xp = {}

def save_xp_data():
    with open("xp_data.json", "w") as f:
        json.dump(user_xp, f)

def load_xp_data():
    global user_xp
    try:
        with open("xp_data.json", "r") as f:
            user_xp = json.load(f)
    except FileNotFoundError:
        user_xp = {}

@bot.event
async def on_ready():
    print("Bot Commands up and running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    await bot.change_presence(activity=discord.CustomActivity(name='waspman', emoji='😳'))

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

# DM specific whisper
@bot.tree.command(name="dmwhisper") 
@app_commands.describe(target="The player to send a secret message to", message="The secret message to send")
async def whisper(interaction: discord.Interaction, target: discord.User, message: str):
    guild = interaction.guild  # Get the guild where the command is used
    dm_role = discord.utils.get(guild.roles, name="DM")  # Replace 'DM' with the exact role name
    
    # Check if the target has the "DM" role
    member = guild.get_member(target.id)  # Get the target's member object
    
    if dm_role in member.roles:  # Only send if the target has the DM role
        # Send a secret message to the target player
        await target.send(f'{interaction.user.mention} has a DM specific question that they\'d like to remain private:\n\n"{message}"')
        # Let the whisperer know the message was sent
        await interaction.response.send_message(f"Whisper sent to {target.mention}", ephemeral=True)
    else:
        # Notify the user that the target is not a DM
        await interaction.response.send_message(f"{target.mention} does not have the DM role.", ephemeral=True)

# DM XP command
@bot.tree.command(name="dmxp")
@app_commands.describe(target="The player to award XP to", xp="The amount of XP to award")
async def award_xp(interaction: discord.Interaction, target: discord.User, xp: int):
    # Ensure only a DM can use this command
    if "DM" not in [role.name for role in interaction.user.roles]:
        await interaction.response.send_message ("You must be a DM to use this command", ephemeral=True)
        return

    # Award XP to specified player
    user_id = str(target.id)
    if user_id in user_xp:
        user_xp[user_id] += xp
    else: 
        user_xp[user_id] = xp
    
    # Notify player
    await target.send(f"You have been awarded {xp} XP!")

    # Confirm in interaction
    await interaction.response.send_message(f"{xp} XP awarded to {target.mention}", ephemeral=True)

    # Save xp data
    save_xp_data()

# Check XP command
@bot.tree.command(name="xp")
async def check_xp(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    xp = user_xp.get(user_id, 0)
    await interaction.response.send_message(f"You have {xp} XP.", ephemeral=True)

#  DM XP command for entire role
@bot.tree.command(name="dmxprole")
@app_commands.describe(role="The role to award XP to", xp="The amount of XP to award")
async def award_xp_to_role(interaction: discord.Interaction, role: discord.Role, xp: int):
    # Check if user is a DM
    if "DM" not in [role.name for role in interaction.user.roles]:
        await interaction.response.send_message("You must be a DM to use this command", ephemeral=True)
        return

    # Get all members with the specific role
    for member in role.members:
        user_id = str(member.id)
        if user_id in user_xp:
            user_xp[user_id] += xp
        else:
            user_xp[user_id] = xp

        # Notify the player
        await member.send(f'You have been awarded {xp} XP!')

    await interaction.response.send_message(f"{xp} XP awarded to all members with the {role.name} role!", ephemeral=True)

    save_xp_data()

# Welcome Server
@bot.event
async def on_member_join(member):
    op_nicknames = {
        328941743632547840: "Josh",
        1057523428099366932: "Cody",
        366764816888758273: "Evan",
        227241716011368450: "Testing"
    }
    op_ids = [1057523428099366932, 328941743632547840, 366764816888758273, 227241716011368450]

    # Welcome for DnD Server
    if member.guild.id == dnd_server_id:
        channel = discord.utils.get(member.guild.channels, name="welcome")
        if channel:
            welcome_text=random.choice(['Typebot thinks you\'re pretty cool 😎', 'Typebot thinks you\'ve been very naughty 😏', 'Everybody look at them!', 'Kinda cute ngl 😏'])
            await channel.send(f"Welcome, {member.mention}! {welcome_text}")
    # Welcome for personal server
    if member.guild.id == personal_server_id:
        channel = discord.utils.get(member.guild.channels, name="general")
        if channel:
            await channel.send(f"Welcome, {member.mention}!")

        if member.id in op_nicknames:
            nickname = op_nicknames[member.id]
            await member.edit(nick=nickname)
            print(f"Changed {member.name}'s nickname to {nickname}")
        
        if member.id in op_ids:
            op_role = discord.utils.get(member.guild.roles, name="Cho Bois")
            if op_role: 
                await member.add_roles(op_role)
                print(f"{member.name} is recognized as family!")

@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(payload.guild_id)
    if payload.message_id == 1286520581923016735:
        role = discord.utils.get(guild.roles, name="PCs")
        member = guild.get_member(payload.user_id)
        
        # Check if the member already has the role
        if role and role not in member.roles:
            await member.add_roles(role)
            print(f"Assigned {role.name} to {member.name}")

            # Send a message to a specific channel for the first time role assignment
            channel = guild.get_channel(1286521389309755543)
            pcs_resources = '<#1286523637658292328>'
            await channel.send(f"Welcome {member.mention} to the Player Characters! Please feel free to take a look at the channels in {pcs_resources}")

@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    if payload.message_id == 1286520581923016735:
        role = discord.utils.get(guild.roles, name="PCs")
        member = guild.get_member(payload.user_id)
        
        if role and role in member.roles:
            await member.remove_roles(role)
            print(f"Removed {role.name} from {member.name}")

# Meep Boost Check
@bot.event
async def on_member_update(before:discord.Member, after:discord.Member):
    guild = bot.get_guild(1129622683546554479)
    target_role_name="Super Meeper"
    announcement_channel_id=1223001844217810985

    if before.guild != guild:
        return
    
    target_role = discord.utils.get(guild.roles, name=target_role_name)

    if target_role not in before.roles and target_role in after.roles:
        channel = guild.get_channel(announcement_channel_id)
        await channel.send(f"{after.mention} has started boosting the server!")

    elif target_role in before.roles and target_role not in after.roles:
        channel = guild.get_channel(announcement_channel_id)
        await channel.send(f'SMH! {after.mention} has stopped boosting the server 😡')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id == restricted_channel_id:
        return    

# DND server specific commands
    if message.guild.id == dnd_server_id:
        if message.content.lower() in ['test']:
            response = 'test'
            await message.channel.send( response)

# Meep Specific Commands
    # Do not return anything message is if not in the meep server
    elif message.guild.id == meep_server_id:
        if message.content.lower() in ['daddy', 'dad', 'mommy', 'mom']:
            print(f'test')
            summon = random.choice(['<@223200575515394048>', '<@125063361196064768>', '<@332537342705401856>', '<@382370044144779265>'])
            response = f'{summon} has been summoned.'
            await message.channel.send(response)
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
    else:
        return

# Run the bot with the token
bot.run(TOKEN)
