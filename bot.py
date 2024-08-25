# bot.py
import os
import random
import discord
from dotenv import load_dotenv

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

    if message.content.lower() in ['<@1137831321599746158>', 'brownie']:
        response = 'who tf is brownie?'
        await message.channel.send(response)

# Return a response after being pinged

#Old responses -- to be added in as an additional option over procedural generation if wanted. 
    # type_responses = [
    #     'Amen', 'Godbless', 'I invented transistors', 'Idris Elba feet picture high resolution Creative Commons license', 'Shroud gaming setup no socks with RGB lighting Commercial License free download 32gb ram upgrade', 'Markiplier free smiling wholesome footage no socks red background', 'How to train your dragon toothless kickflip on scooter real footage no cgi', 'Hello :)', 'Stung by wasp on big toe 8k resolution', '😈', '🐝', , 'Sasquach gaming 420 1080p 2gb ram fail complation 2029', 'I eated a bug :)',

    # ]

#Procedural Generation

    type_people = [
        'Idris Elba', 'Tyler "Ninja" Blevins', 'Bill Gates', 'Samsung 860 EVO 2.5" SSD SATA III 500GB', 'Japanese Toilet Assistant from Cars 2', 'Barry B. Benson', 'Markiplier', 'Shroud', 'Thomas Holland', 'Remy the Rat from Remy\'s Ratatouille Adventure', 'Shadow the Hedge Hog', 'Will Smith in Bad Boys 2', 'Jamie Lee Curtis from Freaky Friday', 'The Dog from Dog with a blog', '<@382370044144779265>'
    ]

    type_thing = [
        'kidney stone irl very shaky footage lots of screaming', 'virus 2024 pandemic angry scene', 'says terrible things about a very nice old man', 'calls me papa while I try to run away', 'wholesome appendicitis moment', 'suggests only they can use the sink in the restroom chaos ensues', 'big diaper diaper baby waddling diaper baby has no fingers', 'Mukbang Play Doh Modeling Compund 4.0oz x 4 pack $6.99 at walgreens', 'no shoes animated GIF stinks to high heavens', 'praying to the wrong god complation blasphemy edition', 'goes to hell aftermath god laughs', 'gaming for 3 hours straight aftermath god reaction gone wrong'
    ]
    type_upgrade = [
        'r/wholesome free video download no surveys','kickstarter video flexible funding', 'vimeo.com 2026 trailer leak 69/100 on metacritic', 'youtube.ru putin approved version', 'my dad is yelling from the other room but I can\'t tell if hes mad at me or if he\'s eating spaghetti', 'recalled 2016 Tristar AquaRug shower rugs because suction cups on the underside of the rugs fail and cause the one thing that it was supposed to prevent', 'random guy yelling at you in 2013 made you feel bad', 'justice finally enacted death penalty confirmed', 'gets away with stealing gum from the cash register I\'m mad about it alibaba.freak', 'trapped inside my computer, wont let me open microsoft edge'
    ]

    if message.content.lower() in ['type', '<@382370044144779265>']:
        def make_sentence():
            return " ".join([person(), thing(), upgrade()])

        def person():
            return random.choice(type_people)
        def thing(): 
            return random.choice(type_thing)
        def upgrade():
            return random.choice(type_upgrade)
        
        response = make_sentence()
        await message.channel.send(response)


    

# Return a picture of dylans foot after someone says toe
    if message.content == 'toe': 
        response = 'https://i.imgur.com/H8u43Up.png'
        await message.channel.send(response)

# A list of responsed that has a 50% chance to send after brownie sends something that isn't a link or gif in the discord chat.

    brownie_responses = [
        'Wow that was very rude what you just said.', 'who asked?', 'Not very mowful not very demure', 'SMH 💀', 'Do you kiss ur cat mom with that mouth?', 'Dylan is a known cheater who boosts his meep scores.', 'I disagree with what Brownie just said.', 'Bruh', 'I actually agree with what brownie said here.', 'Brownie actually cooked with this one.', 
        'wow, you really just said \"{browniemessage}\"?', 'Bro really just said \"{browniemessage}\".', '\"{browniemessage}\"🤓'
    ]
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
