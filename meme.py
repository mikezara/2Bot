# The dumb onw with inside jokes
import discord
from discord.ext import commands
import asyncio
import heapq
import random
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import urllib.request

description = "A multi-purpose bot"

_2B = commands.Bot(command_prefix='2b ', description=description)

OWNER_ID = "132142420044414976"


@_2B.event
async def on_ready():
    print('Logged in as')
    print(_2B.user.name)
    print(_2B.user.id)
    print('------')
    for member in _2B.get_all_members():
        print(str(member) + " - " + str(member.id))


@_2B.command(pass_context=True)
async def wordcount(ctx):
    """Usage: 2b wordcount @[user] - Returns that user's most used words (common words are ignored)"""
    wordcount_ignored = open('wordcount_ignored.txt', 'r')
    wordcount_ignored_list = wordcount_ignored.read().split()

    words_dict = {}

    wordcount_user = ctx.message.clean_content[13:]

    mentioned_user = ctx.message.mentions[0]

    async for user_message in _2B.logs_from(ctx.message.channel, limit=1000):
        if user_message.author == mentioned_user:
            words_list = user_message.clean_content.split()
            for word in words_list:
                if word not in wordcount_ignored_list and "@" not in word:
                    if word in words_dict:
                        words_dict[word] += 1
                    else:
                        words_dict[word] = 1

    fav_words = heapq.nlargest(10, words_dict, key=words_dict.get)

    wordcount_ignored.close()

    await _2B.say(wordcount_user + '\'s top 10 words are: ' + str(', '.join(fav_words)))


@_2B.command(pass_context=True)
async def mostpopular(ctx):
    """Returns the user who has the most @ mentions"""
    mentions_dict = {}

    for member in _2B.get_all_members():
        mentions_dict[member] = 0

    async for message in _2B.logs_from(ctx.message.channel, limit=1000):
        for member in mentions_dict:
            if member.mentioned_in(message):
                mentions_dict[member] += 1

    most_popular = max(mentions_dict, key=mentions_dict.get)

    await _2B.say("The most popular user in this channel is " + most_popular.display_name + ", with "
                  + str(mentions_dict[most_popular]) + " mentions.")


@_2B.command(pass_context=True)
async def quote(ctx):
    """Usage: 2b quote @[user] - Returns a random quote from that user"""
    quote_attributed_to = ctx.message.clean_content[10:]
    quotelist = []

    mentioned_user = ctx.message.mentions[0]

    async for possible_quote in _2B.logs_from(ctx.message.channel, limit=1000):
        if ctx.message.content != "" and possible_quote.author == mentioned_user:
            quotelist.append(possible_quote.content)

    randomizer = random.randrange(len(quotelist))

    await _2B.say('"' + quotelist[randomizer] + '" - ' + quote_attributed_to)


@_2B.command()
async def rattleofftheformula():
    await _2B.say("V 👞 U 👞 DASH 👞 MINUS 👞 U 👞 V 👞 DASH 👞")
    await asyncio.sleep(0.5)
    await _2B.say("ALLOVERVSQUARED")


@_2B.command(pass_context=True)
async def ideal(ctx):
    """Usage: 2b ideal @[user] - Generates an ideal gf meme using random quotes"""
    name = ctx.message.clean_content[10:]

    mentioned_user = ctx.message.mentions[0]
    quotelist = []

    async for possible_quote in _2B.logs_from(ctx.message.channel, limit=1000):
        if possible_quote.content != "" and possible_quote.author == mentioned_user \
                and len(possible_quote.clean_content) <= 24 \
                and "2b" not in possible_quote.clean_content \
                and "!mugi" not in possible_quote.clean_content:
            quotelist.append('"' + possible_quote.clean_content + '"')

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    url = mentioned_user.avatar_url
    local = 'avatar.jpg'
    urllib.request.urlretrieve(url, local)

    avatar_img = Image.open('avatar.jpg', 'r')
    avatar_img = avatar_img.resize((54, 54), Image.ANTIALIAS)

    positions = [(20, 300), (250, 190), (580, 550), (70, 600), (170, 700)]

    img = Image.open("1000-800.png").convert('RGB')
    draw = ImageDraw.Draw(img)

    font1 = ImageFont.truetype("cour.ttf", 52)
    font2 = ImageFont.truetype("cour.ttf", 28)

    draw.text((100, 0), name + " GF", (0, 0, 0), font=font1)

    if len(quotelist) >= 5:
        randomizer = random.sample(range(len(quotelist)), 5)
        for i in range(5):
            draw.text(positions[i], quotelist[randomizer[i]], (0, 0, 0), font=font2)
    elif len(quotelist) < 5:
        randomizer = random.sample(range(len(quotelist)), len(quotelist))
        for i in range(len(quotelist)):
            draw.text(positions[i], quotelist[randomizer[i]], (0, 0, 0), font=font2)

    img.paste(avatar_img, (475, 325))

    img.save('gf-out.jpg')

    await _2B.send_file(ctx.message.channel, 'gf-out.jpg')


@_2B.command(pass_context=True)
async def boysitstimetologoff(ctx):
    """Only I can use this"""

    if ctx.message.author.id == OWNER_ID:
        await _2B.say("Logging off...")
        await _2B.close()


_2B.run('Mzc0MTYwNTUzMDg3NTk4NTky.DNdPsg.kL4PPzQ1UwQamrZtmJ47G3d-IN4')

