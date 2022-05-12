"""

MIT License

Copyright (c) 2021-present Punyathorn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Project Name: Discord-Bot-GUI-Control-Nextcord
Author: punyathorn
Github Repo: https://github.com/punyathorn/Discord-Bot-GUI-Control-Nextcord
First published:
File: main_bot.py
License: MIT License
Version: 1.9.9

FYI: This is the main bot file not the GUI file.
Gui_2.py is not the main file, this file is the main bot file, and the Guimain.py is the main GUI file.
Please run this file and Guimain.py file (GUI file).
Do not delete any files.
You can add your bot's commands here, but please leave the ipc routes commands.
Any changes in any commands will need to be updated in the other files accordingly.

"""

import nextcord
from nextcord.ext import commands, ipc

class Client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix = '[]', *args, **kwargs)
        self.ipc = ipc.Server(self, secret_key="your_ipc_secret_key") # This secrect key needs to be the same as the one at line 47 in Gui_2.py
        
    async def on_ipc_ready(self):
        print("Ipc server connected...")
        
    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="GUI")        
bot = Client(commands_prefix="[]", intents=nextcord.Intents.all(), activity=activity)

@bot.ipc.route()
async def get_chan_count(data):
    guild = bot.get_guild(data.guild_id) # get the guild object using parsed guild_id
    listofchans = []
    for chan in guild.text_channels:
        listofchans.append(f"{chan}")
    return listofchans

@bot.event
async def on_ready():
    print("[ BOT ] successfully login")


@bot.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.command()
async def invite(ctx):
    embed = nextcord.Embed(title=f"Invite {bot.user.name}", color=0xff0000, description=f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot")
    await ctx.send(embed=embed)

@bot.command()
async def gen_invite(ctx, user: nextcord.Member):
    if user.bot == True:
        embed = nextcord.Embed(title=f"Invite {user.name}", color=0xff00, description=f"https://discord.com/api/oauth2/authorize?client_id={user.id}&permissions=8&scope=bot")
        await ctx.send(embed=embed)
    else:
        embed = nextcord.Embed(title=f"This user is not a bot!", color=0xff0000, description="Can not invite a user using link!")
        await ctx.send(embed=embed)

@bot.ipc.route()
async def get_file_sent(data):
    channel = nextcord.utils.get(bot.get_all_channels(), name= data.name)
    ca = bot.get_channel(channel.id)
    await ca.trigger_typing()
    await ca.send(file=nextcord.File(r"{}".format(data.file)))
    return "success"

@bot.ipc.route()
async def get_embed_sent(data):
    channel = nextcord.utils.get(bot.get_all_channels(), name= data.name)
    embed=nextcord.Embed(title=data.title, description=data.description)
    ca = bot.get_channel(channel.id)
    await ca.send(embed=embed)
    return "success"

@bot.ipc.route()
async def get_msg_info(data):
    channel = nextcord.utils.get(bot.get_all_channels(), name= data.name)
    ca = bot.get_channel(channel.id)
    message = await ca.fetch_message(data.msgid)
    if message.author == bot.user:
        return [message.content,"Editable"]
    else:
        return [message.content,"not editable"]

@bot.ipc.route()
async def get_msg_edit(data):
    channel = nextcord.utils.get(bot.get_all_channels(), name= data.name)
    ca = bot.get_channel(channel.id)
    message = await ca.fetch_message(data.msgid)
    await message.edit(data.edit_to)
    return "Edited"

@bot.ipc.route()
async def get_role_count(data):
    guild = bot.get_guild(data.guild_id)
    listofroles = []
    for role in guild.roles:
        listofroles.append(f"{role}")
    listofroles.pop(0)
    return listofroles

@bot.ipc.route()
async def get_user_dm(data):
    user = bot.get_user(data.id)
    await user.send(data.msg)
    return "success"

@bot.ipc.route()
async def get_user_count(data):
    guild = bot.get_guild(data.guild_id) # get the guild object using parsed guild_id
    listofuser = []
    for user in guild.members:
        if user.bot == False:
            listofuser.append(f"{user.name} {user.id}")
    #print(listofuser)
    return listofuser

@bot.ipc.route()
async def get_member_role(data):
    guild = bot.get_guild(int(data.guild_id))
    role = data.role
    role_member = []
    for user in guild.members:
        for user_role in user.roles:
            if str(role) == str(user_role):
                role_member.append(user.name+user.discriminator)
    #print(role_member)
    return [role_member, len(role_member)]


@bot.ipc.route()
async def get_member_count(data):
    guild = bot.get_guild(int(data.guild_id))  # get the guild object using parsed guild_id
    #print(guild.member_count)
    online = []
    offline = []
    dnd = []
    idle = []
    bot = []
    notbot = []
    for user in guild.members:
        if str(user.status) == "online":
            online.append(user.name)
            #print(user.name, user.status,"\n")
        elif str(user.status) == "offline":
            offline.append(user.name)
            #print(user.name, user.status,"\n")
        elif str(user.status) == "dnd":
            dnd.append(user.name)
            #print(user.name, user.status,"\n")
        elif str(user.status) == "idle":
            idle.append(user.name)
            #print(user.name, user.status,"\n")
        if user.bot == True:
            bot.append(user.name)
            #print("bot",user.name,"\n")
        if user.bot == False:
            notbot.append(user.name)
            #print("not bot",user.name,"\n")
    #print("--\n\n--")
    return [guild.member_count, len(online), len(offline), len(dnd), len(idle), len(bot), len(notbot)]


@bot.ipc.route()
async def get_guild_count(data):
    listofnames = []
    for guild in bot.guilds:
        listofnames.append(f"{guild.name} {guild.id}")
    return listofnames

@bot.ipc.route()
async def get_send_count(data):
    guild = bot.get_guild(int(data.guild_id))
    channel = nextcord.utils.get(guild.text_channels, name= data.name)
    ca = bot.get_channel(channel.id)
    await ca.trigger_typing()
    await ca.send(str(data.msg))
    return str("success")

@bot.ipc.route()
async def get_purge_channel(data):
    try:
        channel = nextcord.utils.get(bot.get_all_channels(), name= data.name)
        ca = bot.get_channel(channel.id)
        await ca.purge(limit=int(data.amount))
        return str("success")
    except Exception as e:
        return e

class TokenError(Exception):
    pass

def run(token):
    if token == "#YOUR TOKEN HERE!":
        raise TokenError("Please put your bot token at line 230!")
    bot.ipc.start() # start the IPC Server
    bot.run(token)

run("ODY1NDcwMzMwOTk4MzU4MDY2.Gd5Upq.xYMptuNbrU294oBuBnVymHod5ShiIZgOYafekU")