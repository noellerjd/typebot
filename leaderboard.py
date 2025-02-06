import random
import re
import discord
import datetime
import constants as c

# Pick a real winner from Wordle Winners if there is a tie.
def wordle_winners(message):
    winners = []
    
    winner_lines = re.findall(r'<@(\d+)>', message)

    for winner_line in winner_lines:
        winners.append(winner_line)

    string_type_id = str(c.type_id)

    if string_type_id in winners and len(winners) > 1:
        return('\U0001F3C6 **__Real__ Wordle Winner Today** \U0001F3C6\n' + f'<@{c.type_id}>')

    elif len(winners) > 1:
        return('\U0001F3C6 **__Real__ Wordle Winner Today** \U0001F3C6\n' + f'<@{random.choice(winners)}>')

# Find all messages in a channel that contain 'Wordle Winners Today'
async def find_winner_data(channel):
    messages = []
    async for message in channel.history(limit=None):
        if message.author.id == c.brownie_id and 'Wordle Winners Today' in message.content:
            messages.append(message.content)
    return(messages)

# Check if a leaderboard message already exists
async def check_for_existing_leaderboard(target_channel):
    found_message = False
    async for message in target_channel.history(limit=None):
        if message.author.id == c.typebot_id:
            found_message = True
            return(message.id)
    if not found_message:
        return(False)

# Update/Create a Wordle Leaderboard based on another bots declaration
async def winner_tracking(channel_scan, target_channel):
    messages = await find_winner_data(channel_scan)

    user_ids = []
    for msg in messages:
        user_ids.extend(re.findall(r'<@(\d+)>', msg))

    winner_counts = {"user_data": {}}

    for user_id in user_ids:
        if user_id in winner_counts["user_data"]:
            winner_counts["user_data"][user_id] += 1
        else: 
            winner_counts["user_data"][user_id] = 1

    winner_list = [(user_id, count) for user_id, count in winner_counts["user_data"].items()]

    sorted_winner_list = sorted(winner_list, key=lambda x: x[1], reverse=True)

    leaderboard_text = ""
    for idx, (user_id, count) in enumerate(sorted_winner_list, start=1):
        user_mention = f"<@{user_id}>"
        leaderboard_text += f"{user_mention} - {count}\n"

    leaderboard = []

    # ? if I want to just display top 10
    # top_ten = sorted_winner_list[:10]

    for user_id, count in winner_counts["user_data"].items():
        leaderboard.append(f"<@{user_id}>: {count}")

    embed = discord.Embed(
        title = ":trophy: **WORDLE WINNERS LEADERBOARD** :trophy:",
        description=leaderboard_text,
        color=discord.Color.gold(),
        timestamp=datetime.datetime.now()
    )

    leaderboard_id = await check_for_existing_leaderboard(target_channel)

    if leaderboard_id != False:
        existing_message = await target_channel.fetch_message(leaderboard_id)
        await existing_message.edit(embed=embed)
    else:
        new_message = await target_channel.send(embed=embed)
        leaderboard_id = new_message.id