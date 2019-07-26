import discord
from discord.ext import commands
import asyncio
import os
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True)

with open('chatbot.txt','r', encoding='utf8', errors = 'ignore') as fin:
    raw = fin.read().lower()

sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

BOT_PREFIX = os.environ['prefix']
TOKEN = os.environ['token']

bot = commands.Bot(command_prefix=BOT_PREFIX)

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response

@bot.event
async def on_ready():
    print("The bot is ready")
    await bot.change_presence(activity=discord.Game(name="Making a bot"))

@bot.event
async def on_message(message):
    channel = message.channel
    if message.author == bot.user:
        return
    if message.content == "hello":
        await channel.send("Hello!")
    if message.content == "what is god?":
        await channel.send("God is a painful abstract voice.")
        time.sleep(2)
        await channel.send("How can we love god if we don't know if he exists?")
        time.sleep(2)
        await channel.send('"If you gaze long enough into an abyss, the abyss will gaze back into you"')
        time.sleep(2)
        await channel.send("\tFriedrich Nietzsche")
    if message.content == "time":
        await channel.send(datetime.datetime.now())
    await bot.process_commands(message)

@bot.command()
async def echo(ctx, *, content:str):
    await ctx.send(content)

@bot.command()
async def smashmouth(ctx):
    await ctx.send("Somebody once told me the world is gonna roll me I ain't the sharpest tool in the shed")

@bot.command()
async def time(ctx):
    await ctx.send(datatime.datetime.now)

@bot.command()
async def opm(ctx):
    await ctx.send("\n⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀")
    await ctx.send("\n⣴⠿⠏⠀⠀⠀⠀⠀⠀⢳⡀⠀⡏⠀⠀⠀⠀⠀⢷")
    await ctx.send("\n⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀⠀⠀⠀ ⡇")
    await ctx.send("\n⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿⠀⣸⠀⠀OK⠀ ⡇")
    await ctx.send("\n⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀⣿⠀⢹⠀⠀⠀⠀⠀ ⡇")
    await ctx.send("\n⠙⢿⣯⠄⠀⠀⠀⢀⡀⠀⠀⡿⠀⠀⡇⠀⠀⠀⠀⡼")
    await ctx.send("\n⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀⠀⠘⠤⣄⣠⠞⠀")
    await ctx.send("\n⢸⣷⡦⢤⡤⢤⣞⣁ ")
    await ctx.send("\n⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀⠀")
    await ctx.send("\n⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿")
    await ctx.send("\n⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀⠀⣄⢸")
    await ctx.send("\n⣿⣿⣧⣀⣿.........⣀⣰⣏⣘⣆⣀⠀")

@bot.command()
async def talk(ctx):
    flag = True
    await ctx.send("My name is Marvin. I can talk to you!")
    while(flag==True):
        user_response = mesage.channel
        user_response = message.channel.lower()
        if (user_response != 'bye'):
            if (user_response == 'thanks' or user_response == 'thank you'):
                flag = False
                await ctx.send("ROBO: You are welcome..")
            else:
                if (greeting(user_response) != None):
                    await ctx.send(greeting(user_response))
                else:
                    print(end="")
                    print(response(user_response))
                    sent_tokens.remove(user_response)
        else:
            flag = False
            print("Bye! take care..")


bot.run(TOKEN)