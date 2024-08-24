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
    # meep_responses = [
    #     'plink', 'mow', 'buh',
    # ]
# Return who is brownie after mention
    if message.content == '<@1137831321599746158>':
        response = 'who tf is brownie?'
        await message.channel.send(response)
    if message.content == 'brownie':
        response = 'who tf is brownie?'
        await message.channel.send(response)
    if message.content == 'Brownie':
        response = 'who tf is brownie?'
        await message.channel.send(response)

# Return a response after being pinged
    # type_responses = [
    #     'Amen', 'Godbless', 'I invented transistors', 'Idris Elba feet picture high resolution Creative Commons license', 'Shroud gaming setup no socks with RGB lighting Commercial License free download 32gb ram upgrade', 'Markiplier free smiling wholesome footage no socks red background', 'How to train your dragon toothless kickflip on scooter real footage no cgi', 'Hello :)', 'Stung by wasp on big toe 8k resolution', '😈', '🐝', , 'Sasquach gaming 420 1080p 2gb ram fail complation 2029', 'I eated a bug :)',

    # ]

    type_people = [
        'Idris Elba', 'Tyler "Ninja" Blevins', 'Bill Gates', 'Samsung 860 EVO 2.5" SSD SATA III 500GB', 'Japanese Toilet Assistant from Cars 2', 'Barry B. Benson', 'Markiplier', 'Shroud', 'Thomas Holland', 'Remy the Rat from Remy\'s Ratatouille Adventure', 'Shadow the Hedge Hog', 'Will Smith in Bad Boys 2', 'Jamie Lee Curtis from Freaky Friday', 'The Dog from Dog with a blog', '<@382370044144779265>'
    ]

    type_thing = [
        'kidney stone irl very shaky footage lots of screaming', 'virus 2024 pandemic angry scene', 'says terrible things about a very nice old man', 'calls me papa while I try to run away', 'wholesome appendicitis moment', 'suggests only they can use the sink in the restroom chaos ensues', 'big diaper diaper baby waddling diaper baby has no fingers', 'Mukbang Play Doh Modeling Compund 4.0oz x 4 pack $6.99 at walgreens', 'no shoes animated GIF stinks to high heavens', 'praying to the wrong god complation blasphemy edition', 'goes to hell aftermath god laughs', 'gaming for 3 hours straight aftermath god reaction gone wrong'
    ]
    type_upgrade = [
        'r/wholesome free video download no surveys','kickstarter video flexible funding', 'vimeo.com 2026 trailer leak 69/100 on metacritic', 'youtube.ru putin approved version', 'my dad is yelling from the other room but I can\'t tell if hes mad at me or if he\'s eating spaghetti', 'recalled 2016 Tristar AquaRug shower rugs because suction cups on the underside of the rugs fail and cause the one thing that it was supposed to prevent', 'random guy yelling at you in 2013 made you feel bad', 'justice finally enacted death penalty confirmed', 'gets away with stealing gum from the cash register I\'m mad about it alibaba.freak', 'trapped inside my computer, wont let me open microsoft edge'
    ]

    if 'Type' in message.content:
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

        # response = random.choice(type_responses) 
        # await message.channel.send(response)
    if 'type' in message.content:
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

    if '<@382370044144779265>' in message.content:
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


# All commands below have a 75% chance to be successful
    if random.random() < 0.25:
        # print(f'{random.random()}')
        return


    # if message.content == 'Plink':
    #     response = 'plink'
    #     await message.channel.send(response)
    # if message.content == 'mow':
    #     response = 'mow'
    #     await message.channel.send(response)
    # if message.content == 'Mow':
    #     response = 'mow'
    #     await message.channel.send(response)
    # if message.content == 'buh':
    #     response = 'buh'
    #     await message.channel.send(response)
    # if message.content == 'Buh':
    #     response = 'buh'
    #     await message.channel.send(response)


    # if 'type' in message.content:
    #     response = random.choice(type_responses) 
    #     await message.channel.send(response)

    # if message.content == 'test':
    #     response = message.author.id
    #     await message.channel.send(response)


    brownie_responses = [
        'Wow that was very rude what you just said.', 'who asked?', 'Not very mowful not very demure', 'SMH 💀', 'Do you kiss ur cat mom with that mouth?', 'Dylan is a known cheater who boosts his meep scores.', 'I disagree with what Brownie just said.', 'Bruh', 'I actually agree with what brownie said here.', 'Brownie actually cooked with this one.', 
        'wow, you really just said \"{browniemessage}\"?', 'Bro really just said \"{browniemessage}\".', '\"{browniemessage}\"🤓'
    ]
    if message.author.id == 1137831321599746158:
        if 'https://' in message.content:
            return
        browniemessage = message.content
        response = random.choice(brownie_responses)
        response = response.format(browniemessage=browniemessage)

        await message.channel.send(response)


# Run the bot with the token
client.run(TOKEN)
