import json
import os
# from tokenize import Token
import discord
import requests
# import nltk
import random
import pymongo
from dotenv import load_dotenv

# databse work
try:
  myclient = pymongo.MongoClient("mongodb://localhost/discordData")
  print("connected to MongoDb")
except:
  print("cannot connect to the mongoDB")

mydb = myclient["myDatabase"]
print(myclient.list_database_names())

client = discord.Client()

# "load_dotenv" is used to load the ".env" file to the environment variables
# after using "load_dotenv" you can just think that ".env" file is in this very file, here but HIDDEN
load_dotenv('.env')
# you can access the variables of ".env" file using "os.getenv" and naming the variable of the .env file as the parameter
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

# This one is used in the 4th event of "on_message" Function
f = open('data.json','r')
DATA = json.load(f)



@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')
  #"client.guilds" contains [<Guild id=935196937462890526 name='Bot Family' shard_id=None chunked=False member_count=3>]
  for guild in client.guilds:
    if guild.name == GUILD:
      break
  
  print(f'{client.user} is connected to {guild.name} server \nServer ID is {guild.id} ')


@client.event
async def on_message(message):
    if message.author == client.user:
      return

    if message.content.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)

    msg = message.content
    msgs = msg.lower()
    if any(word in msgs for word in DATA['sad_word']):
      await message.channel.send(random.choice(DATA['starter_encouragement']))
      f.close()
    

    if any(word in msgs for word in DATA['bad_Words']):
      await message.channel.send('Please Refrain from using Bad Words')
      f.close()


@client.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(f'Welcome {member.name}! to our discord server. \n The admin here mainly make simple bots, Don\'t take him too seriously \n InFact what you reading is written by him \n Well anyway you have the right to deploy your bots here ENjOY' )


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

# def update_encouragement()    


client.run(TOKEN)


# # word.tokenize will make an array and each word of the below sentence will be its elements(hopefully)
# sentence = """sad depressed unhappy miserable die javascript dissappoint bitter java C++"""
# sad_word = nltk.word_tokenize(sentence)
