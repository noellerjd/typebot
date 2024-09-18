import os
import re
import random
import asyncio
import discord
import yt_dlp as youtube_dl
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
restricted_channel_id = 1280670129939681357
meep_server_id = 1129622683546554479

print(f'YTAPIKEY {YOUTUBE_API_KEY}')

# Create an Intents object with the intents you want to enable
intents = discord.Intents.default()
intents.message_content = True  # Enable the message_content intent if you want to listen to messages

# Create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Set up YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# ffmpeg options
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
    'stderr': True  # Log FFmpeg errors to the console
}

# YouTubeDL options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'nocheckcertificate': True,  # Disable SSL checks
    'force_generic_extractor': True,  # Try forcing a more generic extractor
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# Function to get video info via YouTube API
async def get_video_info(youtube, video_id):
    try:
        request = youtube.videos().list(
            part="snippet,contentDetails",
            id=video_id
        )
        response = request.execute()
        if response['items']:
            video_info = response['items'][0]
            title = video_info['snippet']['title']
            stream_url = f"https://www.youtube.com/watch?v={video_id}"
            return title, stream_url
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching video info: {str(e)}")
        return None, None

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    pattern = re.compile(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*")
    match = pattern.search(url)
    return match.group(1) if match else None

@bot.event
async def on_ready():
    print("Bot Commands up and running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
    await bot.change_presence(activity=discord.CustomActivity(name='waspman', emoji='😳'))

# Join the voice channel
@bot.tree.command(name="join")
async def join(interaction: discord.Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        if interaction.guild.voice_client is None:
            await channel.connect()
            await interaction.response.send_message(f"Joined {channel}", ephemeral=True)
        else:
            await interaction.guild.voice_client.move_to(channel)
            await interaction.response.send_message(f"Moved to {channel}", ephemeral=True)
    else:
        await interaction.response.send_message("You're not in a voice channel.", ephemeral=True)

# Play a song from YouTube
@bot.tree.command(name="play")
@app_commands.describe(url="YouTube URL of the song to play")
async def play(interaction: discord.Interaction, url: str):
    if interaction.user.voice:
        channel = interaction.user.voice.channel

        if interaction.guild.voice_client is None:
            await channel.connect()
        else:
            await interaction.guild.voice_client.move_to(channel)

        await interaction.response.send_message(f"Fetching video info from YouTube API...", ephemeral=True)

        # Extract video ID and fetch video info
        video_id = extract_video_id(url)
        if video_id:
            title, stream_url = await get_video_info(youtube, video_id)
        else:
            await interaction.edit_original_response(content="Invalid YouTube URL.")
            return

        # If video info was retrieved
        if not title or not stream_url:
            await interaction.edit_original_response(content="Could not find video or invalid URL.")
            return

        # Attempt to use yt_dlp to extract streamable URL
        try:
            print(f"Stream URL: {stream_url}")
            data = ytdl.extract_info(stream_url, download=False)
            audio_url = data['url']
            await interaction.edit_original_response(content=f"Now playing: **{title}**")
            interaction.guild.voice_client.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))
        except youtube_dl.utils.DownloadError as e:
            print(f"yt_dlp error: {str(e)}")
            await interaction.edit_original_response(content="Could not play the video, it may be restricted.")
    else:
        await interaction.response.send_message("You're not in a voice channel.", ephemeral=True)

# Command to stop and leave
@bot.tree.command(name="stop")
async def stop(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("Disconnected from the voice channel.", ephemeral=True)
    else:
        await interaction.response.send_message("I'm not connected to a voice channel.", ephemeral=True)


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
