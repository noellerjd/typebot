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

# Server IDs
meep_server_id = 1129622683546554479
dnd_server_id = 1286406203055935591
personal_server_id = 1288280564155027518

# Channel IDs
restricted_channel_id = 1280670129939681357
wordle_channel_id = 1326175839884148867
dev_channel_id = 1137836224040673331
bot_testing_channel_id = 1276648666928779458
dnd_test_channel_id = 1335728540418576385
dnd_general_channel_id = 1286406204976791629
meep_leaderboard_channel = 1282365851001163786

# User IDs
brownie_id = 1137831321599746158
type_id = 382370044144779265
rrisky_id = 332537342705401856
flare_id = 125063361196064768
bungoh_id = 223200575515394048

# Discord intents enabled
intents = discord.Intents.default()
intents.message_content = True 
intents.members = True

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# XP Thresholds
level_thresholds = {
    1: 0,
    2: 300,
    3: 900,
    4: 2700,
    5: 6500,
    6: 14000,
    7: 23000,
    8: 34000,
    9: 48000,
    10: 64000,
    11: 85000,
    12: 100000,
    13: 120000,
    14: 140000,
    15: 165000,
    16: 195000,
    17: 225000,
    18: 265000,
    19: 305000,
    20: 355000
}

# DM XP functions
# Store user XP
user_xp = {}
user_level = {}

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

def get_user_level(xp):
    # Return level based on their xp
    for level, threshold in sorted(level_thresholds.items(), reverse=True):
        if xp >= threshold:
            return level
    return 1 # default to level 1 if below threshold

@bot.event
async def on_ready():
    print("Bot Commands up and running!")
    load_winner_data()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    await bot.change_presence(activity=discord.CustomActivity(name="Don't type 'toe'", emoji='😳'))

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

    # Check for level up
    current_xp = user_xp[user_id]
    current_level = user_level.get(user_id, 1)
    new_level = get_user_level(current_xp)

    if new_level > current_level:
        user_level[user_id] = new_level
        # Notify user of level up
        await target.send(f"🎉 Congratulations! You've leveled up to level {new_level}! 🎉")

    # Confirm in interaction
    await interaction.response.send_message(f"{xp} XP awarded to {target.mention}", ephemeral=True)

    # Save xp data
    save_xp_data()

# Check XP command
@bot.tree.command(name="xp")
async def check_xp(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    xp = user_xp.get(user_id, 0)
    level = user_level.get(user_id, get_user_level(xp))
    await interaction.response.send_message(f"You have {xp} XP and are level {level}.", ephemeral=True)

#  DM XP command for entire role
@bot.tree.command(name="dmxprole")
@app_commands.describe(role="The role to award XP to", xp="The amount of XP to award")
async def award_xp_to_role(interaction: discord.Interaction, role: discord.Role, xp: int):
    # Check if user is a DM
    if "DM" not in [role.name for role in interaction.user.roles]:
        await interaction.response.send_message("You must be a DM to use this command", ephemeral=True)
        return

    # Get all members with the specific role
    members_awarded = []
    for member in role.members:
        user_id = str(member.id)
        if user_id in user_xp:
            user_xp[user_id] += xp
        else:
            user_xp[user_id] = xp

        members_awarded.append(member.name)

        # Check for level up
        current_xp = user_xp[user_id]
        current_level = user_level.get(user_id, 1)
        new_level = get_user_level(current_xp)
        if new_level > current_level:
            user_level[user_id] = new_level
            # Notify player of level up
            await member.send(f"🎉 Congratulations you've gained {xp} XP and you've leveled up to level {new_level}! 🎉")

    await interaction.response.send_message(f"{xp} XP awarded to all members with the {role.name} role!")

    save_xp_data()

# Welcome Server
@bot.event
async def on_member_join(member):

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

# Message reaction to change member role
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
            response = '<@1276601243292143729>'
            await message.channel.send(response)

# Meep Specific Commands
    # Do not return anything message is if not in the meep server
    elif message.guild.id == meep_server_id:
        # Pick a 'real' winner from wordle winner list
        if message.channel.id == wordle_channel_id and message.author.id == brownie_id:
            if 'Wordle Winners Today' in message.content:
                response = wordle_winners(message.content)
        # Update/Create a Wordle Leaderboard based on another bots declaration
                target_channel = message.guild.get_channel(meep_leaderboard_channel)
                if target_channel:
                    await winner_tracking(message, target_channel)
                if response:
                    await message.channel.send(response)

        # ? Incase I want to remove the 'real' winner function.
        # if message.author.id == brownie_id and message.channel.id == wordle_channel_id:
        #     if 'Wordle Winners Today' in message.content:
        #         target_channel = message.guild.get_channel(meep_leaderboard_channel)
        #         if target_channel:
        #             await winner_tracking(message, target_channel)
        # ping someone when parent is mentioned.
        if message.content.lower() in ['daddy', 'dad', 'mommy', 'mom']:
            summon = random.choice([f'<@{bungoh_id}>', f'<@{flare_id}>', f'<@{rrisky_id}>', f'<@{type_id}>'])
            response = f'{summon} has been summoned.'
            await message.channel.send(response)
        # Return a response after pinging type
        if message.content.lower() in ['type', f'<@{type_id}>']:
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
        if any(trigger in message.content.lower() for trigger in ['rrisky', 'risky', f'<@{rrisky_id}>']):
            response = random.choice(rrisky_responses)
            await message.channel.send(response)
        # Return a message after mentioning david
        if any(trigger in message.content.lower() for trigger in ['david', 'flare', f'<@{flare_id}>']):
            response = random.choice(david_responses)
            await message.channel.send(response)
        # Return a picture of dylans foot after someone says toe
        if message.content.lower() == 'toe': 
            if random.random() > 0.9:
                response = 'https://i.imgur.com/SsbFqbv.png'
            else:
                response = 'https://i.imgur.com/H8u43Up.png'
            await message.channel.send(response)
        # Return a message if json is mentioned
        if 'json' in message.content.lower():
            response = f'<@{type_id}> has been summoned.'
            await message.channel.send(response)
        # Uses a list of responses that has a 25% chance to send after brownie sends something that isn't a link or gif in the discord chat.
        if message.author.id == brownie_id:
            if any(trigger in message.content.lower() for trigger in ['https://', 'insult', 'suggestion', 'judge']) or random.random() < 0.99:
                return

            browniemessage = message.content
            response = random.choice(brownie_responses)
            response = response.format(browniemessage=browniemessage)

            await message.channel.send(response)
        # test function
        # if message.channel.id == bot_testing_channel_id and message.user.id == type_id:

        # 0.01% chance to send a random compliment
        if message:
            if random.random() < 0.99:
                return
            response = random.choice(random_compliments)
            await message.channel.send(response)

# Pick a real winner from Wordle Winners if there is a tie.
def wordle_winners(message):
    winners = []
    
    winner_lines = re.findall(r'<@(\d+)>', message)

    for winner_line in winner_lines:
        winners.append(winner_line)

    string_type_id = str(type_id)

    if string_type_id in winners and len(winners) > 1:
        return('\U0001F3C6 **__Real__ Wordle Winner Today** \U0001F3C6\n' + f'<@{type_id}>')

    elif len(winners) > 1:
        return('\U0001F3C6 **__Real__ Wordle Winner Today** \U0001F3C6\n' + f'<@{random.choice(winners)}>')

winner_data = {}
leaderboard_message_ids = {}

def save_winner_data():
    with open("winner_data.json", "w") as f:
        json.dump(winner_data, f)

def load_winner_data():
    global winner_data
    try:
        with open("winner_data.json") as f:
            content = f.read()
            if not content.strip():
                winner_data = {"user_data": {}, "message_ids":{}}
            else:
                winner_data = json.loads(content)
                if "message_ids" not in winner_data:
                    winner_data["message_ids"] = {}
    except (FileNotFoundError, json.JSONDecodeError):
        winner_data = {"user_data": {}, "message_ids": {}}


async def winner_tracking(message, target_channel):
    # load data from winner_data.json
    load_winner_data()
    # find users within the message.content
    user_ids = re.findall(r'<@(\d+)>', message.content)

    # update score within winner_data else set their score.
    for user_id in user_ids:
        if user_id in winner_data["user_data"]:
            winner_data["user_data"][user_id] += 1
        else: 
            winner_data["user_data"][user_id] = 1

    # Sort the leaderboard by score.
    sorted_leaderboard = sorted(
        winner_data["user_data"].items(), key=lambda x: x[1], reverse=True
    )

    # Establish leaderboard text
    leaderboard_text = ""
    for idx, (user_id, count) in enumerate(sorted_leaderboard, start=1):
        user_mention = f"<@{user_id}>"
        leaderboard_text += f"{idx}. {user_mention} - {count} wins\n"

    # leaderboard = []

    # # if I want to just display top 10
    # # top_ten = sorted_leaderboard[:10]


    # for user_id, count in winner_data["user_data"].items():
    #     leaderboard.append(f"<@{user_id}>: {count} time(s)")

    # leaderboard_message = ":trophy: **Wordle Winners Leaderboard** :trophy:\n" + "\n".join([f'<@{user_id}> - {count} wins' for user_id, count in sorted_leaderboard])
    # # change to ([f'<@{user_id} - {count} wins' for user_id, count in top_ten]) if only display top 10 

    # Save winner data
    save_winner_data()
    # for user_id, count in winner_data.items():
    #     leaderboard.append(f"<@{user_id}> won: {count} time(s)")

    # Format leaderboard as an embed
    embed = discord.Embed(
        title = ":trophy: **Wordle Winners Leaderboard** :trophy:",
        description=leaderboard_text,
        color=discord.Color.gold()
    )

    # establish channel for leaderboard to post to
    channel_id = str(target_channel.id)

    # Check if a embed has already been sent in channel
    # if yes, edit the existing embed
    # if no, create embed
    if channel_id in winner_data["message_ids"]:
        try:
            existing_message = await target_channel.fetch_message(winner_data["message_ids"][channel_id])
            
            await existing_message.edit(embed=embed)
        except discord.NotFound:
            new_message = await target_channel.send(embed=embed)
            winner_data["message_ids"][channel_id] = new_message.id
            save_winner_data()
    else: 
        new_message = await target_channel.send(embed=embed)
        winner_data["message_ids"][channel_id] = new_message.id
        save_winner_data()


    
# Run the bot with the token
bot.run(TOKEN)
