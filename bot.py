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

# from dnd_data import races
from dnd_data import races, classes, backgrounds
races_list = ", ".join(races)

# Create an Intents object with the intents you want to enable
intents = discord.Intents.default()
intents.message_content = True  # Enable the message_content intent if you want to listen to messages

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
restricted_channel_id = 1280670129939681357

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

# DnD Character Creator 
active_character_creation = {}

# Start Creation
@bot.tree.command(name="create_character")
async def create_character(interaction: discord.Interaction):
    races_list = ", ".join(races)
    await interaction.response.send_message(f"Welcome to Typebot character creation! Please choose a race from the following: {races_list}. Type 'cancel' at any time to exit or 'back' to return to the previous step.", ephemeral=True)
    active_character_creation[interaction.user.id] = {"step": "race", "previous_step": None}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id == restricted_channel_id:
        return    
    user_id = message.author.id

    # Character Creation
    if user_id in active_character_creation:
        current_step = active_character_creation[user_id]["step"]

        # Allow user to cancel
        if message.content.lower() == "cancel":
            del active_character_creation[user_id]
            await message.channel.send("Character creation has been cancelled.")
            return
        
        # Allow user to go back to the previous step
        if message.content.lower() == "back":
            previous_step = active_character_creation[user_id].get("previous_step")
            if previous_step:
                active_character_creation[user_id]["step"] = previous_step
                await message.channel.send(f"Returning to the previous step: {previous_step}. Please make your selection again.")
                if previous_step == "race":
                    races_list = ", ".join(races)
                    await message.channel.send(f"Please choose a race from the following: {races_list}")
                elif previous_step == "subrace":
                    subraces = active_character_creation[user_id]["subraces"]
                    subrace_list = ", ".join(subraces.keys())
                    await message.channel.send(f"Please choose a subrace from the following: {subrace_list}")
                elif previous_step == "class":
                    class_list = ", ".join(classes.keys())
                    await message.channel.send(f"Please choose a class from the following: {class_list}")
                elif previous_step == "background":
                    background_list = ", ".join(backgrounds.keys())
                    await message.channel.send(f"Please choose a background from the following: {background_list}")
                return

        # Step 1: Race Selection
        if current_step == "race":
            race_choice = message.content.capitalize()

            if race_choice in races:
                race_data = races[race_choice]
                response = f"You chose **{race_choice}**.\n\n*{race_data['description']}*\n\n**Traits:**\n" \
                + "\n".join([f"{key}: {', '.join(value) if isinstance(value, list) else value}" for key, value in race_data["traits"].items() if key != "subrace"])

                response += "\nType 'confirm' to proceed or select another race."
                await message.channel.send(response)
                active_character_creation[user_id]["race"] = race_choice
                active_character_creation[user_id]["previous_step"] = "race"  # Set the previous step
                active_character_creation[user_id]["step"] = "confirm_race"

            else:
                await message.channel.send(f"Invalid race. Please choose a valid race: {races_list}")

        # Step 2: Confirm Race or Select Another Race
        elif current_step == "confirm_race":
            if message.content.lower() == "confirm":
                race_choice = active_character_creation[user_id]["race"]
                race_data = races[race_choice]

                # Check if the race has subraces
                if "subrace" in race_data["traits"]:
                    subraces = race_data["traits"]["subrace"]
                    subrace_list = ", ".join(subraces.keys())
                    response = f"Race confirmed! Now choose a subrace from the following: {subrace_list}"
                    await message.channel.send(response)
                    active_character_creation[user_id]["subraces"] = subraces
                    active_character_creation[user_id]["previous_step"] = "confirm_race"  # Update previous step
                    active_character_creation[user_id]["step"] = "subrace"
                else:
                    # No subraces, proceed to class selection
                    class_list = ", ".join(classes.keys())
                    await message.channel.send(f"Race confirmed! Now choose a class from the following: {class_list}")
                    active_character_creation[user_id]["previous_step"] = "confirm_race"  # Update previous step
                    active_character_creation[user_id]["step"] = "class"

            elif message.content.capitalize() in races:
                race_choice = message.content.capitalize()
                race_data = races[race_choice]
                response = f"You chose **{race_choice}**.\n\n*{race_data['description']}*\n\n**Traits:**\n" \
                + "\n".join([f"{key}: {', '.join(value) if isinstance(value, list) else value}" for key, value in race_data["traits"].items() if key != "subrace"])

                response += "\nType 'confirm' to proceed or select another race."
                await message.channel.send(response)
                active_character_creation[user_id]["race"] = race_choice

            else:
                await message.channel.send(f"Invalid input. Type 'confirm' to proceed or select another race.")

        # Step 3: Subrace Selection (if applicable)
        elif current_step == "subrace":
            # Normalize subrace input
            subrace_choice = message.content.capitalize()

            if subrace_choice in active_character_creation[user_id]["subraces"]:
                subrace_data = active_character_creation[user_id]["subraces"][subrace_choice]
                response = f"You chose **{subrace_choice}**.\n\n*{subrace_data['ability increase']}*\n\n**Special Trait**: {subrace_data['race increase']}"
                await message.channel.send(response + "\nType 'confirm' to proceed or select another subrace.")
                
                # Store subrace selection
                active_character_creation[user_id]["subrace"] = subrace_choice
                active_character_creation[user_id]["previous_step"] = "subrace"  # Update previous step
                active_character_creation[user_id]["step"] = "confirm_subrace"
            else:
                subraces = active_character_creation[user_id]["subraces"]
                subrace_list = ", ".join(subraces.keys())
                await message.channel.send(f"Invalid subrace. Please choose from the following: {subrace_list}")

        # Step 4: Confirm Subrace or Choose Another
        elif current_step == "confirm_subrace":
            if message.content.lower() == "confirm":
                class_list = ", ".join(classes.keys())
                await message.channel.send(f"Subrace confirmed! Now choose a class from the following: {class_list}")
                active_character_creation[user_id]["step"] = "class"
            else:
                subraces = active_character_creation[user_id]["subraces"]
                subrace_list = ", ".join(subraces.keys())
                await message.channel.send(f"Invalid input. Please type 'confirm' or choose another subrace: {subrace_list}")

        # Step 5: Class Selection
        elif current_step == "class":
            class_choice = message.content.capitalize()

            if class_choice in classes:
                class_data = classes[class_choice]
                response = f"You chose **{class_choice}**.\n\n*{class_data['description']}*\n\n**Primary Ability:** {class_data['abilities']['primary']}\n**Secondary Ability:** {class_data['abilities']['secondary']}"
                await message.channel.send(response + "\nType 'confirm' or select another class.")
                active_character_creation[user_id]["class"] = class_choice
                active_character_creation[user_id]["step"] = "confirm_class"
            else:
                await message.channel.send(f"Invalid class. Please choose a valid class: {', '.join(classes.keys())}")

        # Step 6: Confirm Class or Select Another Class
        elif current_step == "confirm_class":
            if message.content.lower() == "confirm":
                background_list = ", ".join(backgrounds.keys())
                await message.channel.send(f"Class confirmed! Now choose a background from the following: {background_list}")
                active_character_creation[user_id]["step"] = "background"
            elif message.content.capitalize() in classes:
                class_choice = message.content.capitalize()
                class_data = classes[class_choice]
                response = f"You chose **{class_choice}**.\n\n*{class_data['description']}*\n\n**Primary Ability:** {class_data['abilities']['primary']}\n**Secondary Ability:** {class_data['abilities']['secondary']}"
                await message.channel.send(response + "\nType 'confirm' or select another class.")
                active_character_creation[user_id]["class"] = class_choice
            else:
                await message.channel.send(f"Invalid input. Type 'confirm' to proceed or select another class.")

        # Step 7: Background Selection
        elif current_step == "background":
            background_choice = message.content.capitalize()

            if background_choice in backgrounds:
                background_data = backgrounds[background_choice]
                response = f"You chose **{background_choice}**.\n\n*{background_data['description']}*\n\n**Skills:** {', '.join(background_data['skills'])}"
                await message.channel.send(response + "\nType 'confirm' or select another background.")
                active_character_creation[user_id]["background"] = background_choice
                active_character_creation[user_id]["step"] = "confirm_background"
            else:
                await message.channel.send(f"Invalid background. Please choose a valid background: {', '.join(backgrounds.keys())}")

        # Step 8: Confirm Background or Select Another Background
        elif current_step == "confirm_background":
            if message.content.lower() == "confirm":
                final_data = active_character_creation[user_id]
                subrace = final_data['subrace']
                subrace_data = final_data['subraces'][subrace]
                print(f'{subrace_data}')

                await message.channel.send(f"Character creation complete!\n\n**Race**: {final_data['race']}\n**Subrace**: {final_data['subrace']}\n**Race traits**: \nAbility Score Increase: {subrace_data['ability increase']}\n {subrace_data['race increase']}\n**Class**: {final_data['class']}\n**Background**: {final_data['background']}")
                del active_character_creation[user_id]  # Clean up after character creation is complete
            elif message.content.capitalize() in backgrounds:
                background_choice = message.content.capitalize()
                background_data = backgrounds[background_choice]
                response = f"You chose **{background_choice}**.\n\n*{background_data['description']}*\n\n**Skills:** {', '.join(background_data['skills'])}"
                await message.channel.send(response + "\nType 'confirm' or select another background.")
                active_character_creation[user_id]["background"] = background_choice
            else:
                await message.channel.send(f"Invalid input. Type 'confirm' to proceed or select another background.")

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
