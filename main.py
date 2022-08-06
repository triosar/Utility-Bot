import requests
import os
#from ro_py import users
#from ro_py.users import User
import discord
from dotenv import load_dotenv
from keep_alive import *
#import random
import time
from humanfriendly import format_timespan
from discord.ext import commands
from replit import db
import io
import contextlib
from discord.utils import get
from discord import Webhook, AsyncWebhookAdapter
#import aiohttp
import logging
from trello import TrelloApi
import asyncio
from ro_py import Client
#import traceback
import logging
from flask import request

serverlist = [] # server names
slist = [] #server objects
blacklist = [] # bot blacklist

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='>',intents=intents)

logging.basicConfig(filename='log.txt', format='%(filename)s: %(message)s',level=logging.ERROR)

load_dotenv()
DISCTOKEN = os.getenv('DISCORD_TOKEN')
#RS = os.getenv('ROBLOSECURITY') # not needed
#TRELLO_APP_KEY = os.getenv('TRELLO_APP_KEY') # not needed

TWwebhook = os.getenv('WEBHOOK')

# bot function definitions

async def checkQ():
  while True:
    await asyncio.sleep(1)
    fileq = open("log.txt","r")
    for x in fileq:
      if x.startswith("`System"):
        toSend = x
      else:
        toSend = "```py\n"+x+"```"
      bot.loop.create_task((bot.get_channel(903626137001918484)).send(toSend))
    fileq.close()
    open('log.txt', 'w').close()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="some flies. | Prefix is '>'!"))
    channel = bot.get_channel(903626137001918484)
    embedVar2 = discord.Embed(title="Bot connected to Discord",description=f'Bot successfully connected to Discord at {time.asctime()}.',color=0x0090ff)
    embedVar2.set_footer(text="Hello world | FrogBot")
    await channel.send(embed=embedVar2)

    for server in bot.guilds:
      serverlist.append(str(server))
      slist.append(server)
      #await server.leave() #activate this to leave all servers
    await checkQ()

@bot.event
async def on_message(message):

  if message.author == bot.user:
    return

  if (message.webhook_id):
    # ignore webhook posts
    return

  if message.channel.type is discord.ChannelType.private:
    channel = bot.get_channel(903627366302109697)
    user = str(message.author.id)
    user = "<@"+user+">"

    embedVar = discord.Embed(title="New Froggo DM", description="",color=0x0090ff)

    embedVar.add_field(name="Username:", value=(user), inline=False)
    embedVar.add_field(name="Message:",value = message.content,inline=False)
      
    await channel.send(embed=embedVar)
  if str(message.author.id) not in blacklist:
    await bot.process_commands(message)

@bot.command()
async def say(ctx,*args):
  if str(ctx.message.author) != "puptaco#3335":
    return
  await ctx.send(' '.join(args))
  await ctx.message.delete()
  
  
@bot.command()
async def bloxsearch(ctx,*args):
  
#initiate bloxlink search
  blox_key = os.getenv('BLOXKEY')
  baseURL = "https://v3.blox.link/developer/discord/"
  discID = args[0] # the discord id provided
  discID = str(discID)
  reqURL = baseURL + discID
  r = requests.get(reqURL,headers={"api-key":blox_key})
  print(r)
  r = r.json() # make it accessible as a dict
  print(r)
  await ctx.send("Bloxlink JSON: "+str(r))
  if not r["success"]: # if the request failed
    await ctx.send("The Bloxlink lookup failed.")
  else:
    try:
      link = "https://www.roblox.com/users/"+r["user"]["primaryAccount"]+"/profile"
      embedVar = discord.Embed(title="Bloxlink Lookup", description="",color=000000)
      embedVar.add_field(name="Discord User", value="<@"+str(discID)+">", inline=False)
      roblox = Client()
      try:
        user = await roblox.get_user(int(r["user"]["primaryAccount"]))
      except:
        await ctx.send("Boblox hecked up :(")
        return
      currentName = user.name
      embedVar.add_field(name="Username", value=currentName, inline=False)
      embedVar.add_field(name="Profile Link", value=link, inline=False)
      await ctx.send(embed=embedVar)
    except:
      await ctx.send("This user is not verified with Bloxlink")
    
#########################################################

#iniate rover search
  baseURL = "https://verify.eryn.io/api/user/"
  discID = args[0] # the discord id provided
  discID = str(discID)
  reqURL = baseURL + discID
  r = requests.get(reqURL)
  r = r.json() # make it accessible as a dict
  await ctx.send("Rover JSON: "+str(r))
  if r["status"] == "error": # if the request failed
    errorText = r["error"]
    await ctx.send("The Rover lookup failed.\nError reason is:")
    toSend = "`"+errorText+"`"
    await ctx.send(toSend)
  else:
    link = "https://www.roblox.com/users/"+str(r["robloxId"])+"/profile"
    embedVar = discord.Embed(title="Rover Lookup", description="",color=0xBD222A)
    embedVar.add_field(name="Discord User", value="<@"+str(discID)+">", inline=False)
    roblox = Client()
    try:
      user = await roblox.get_user(int(r["robloxId"]))
    except:
      await ctx.send("Boblox hecked up :(")
      return
    currentName = user.name
    embedVar.add_field(name="Username", value=currentName, inline=False)
    embedVar.add_field(name="Profile Link", value=link, inline=False)
    await ctx.send(embed=embedVar)

@bot.command()
async def postweb(ctx):
  url = TWwebhook
  data = {
    "content" : "ALERT!!!! AMOGUS HAS BEEN DISCOVERED IN THE NOVA SECURITY TRAINING FACILITY!"
  }
  try:
    result = requests.post(url, json = data)
    await ctx.send("pass")
    await ctx.send(str(result))
  except:
    await ctx.send("bonk")
    await ctx.send(str(result))


@bot.command()
async def eval(ctx, *, code):
    if (ctx.message.author.id) != 314394344465498122:
      await ctx.send("Denied.")
      return
    str_obj = io.StringIO() #Retrieves a stream of data
    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        return await ctx.send(f"```{e.__class__.__name__}: {e}```")
    await ctx.send(f'```{str_obj.getvalue()}```')

@app.route("/post", methods=['POST'])
def posturl():
  data = request.get_json()
  result = requests.post(TWwebhook, json = data)
  return

keep_alive()
try:
  bot.run(DISCTOKEN)
except:
    file = open("log.txt","a+")
    file.write("`System: Container had to restart because current container rate-limited.` <@314394344465498122>\n")
    file.close()
    os.system("kill 1")