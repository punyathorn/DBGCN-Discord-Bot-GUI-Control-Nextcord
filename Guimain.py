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
File: Guimain.py
License: MIT License
Version: 1.9.9

FYI: This is the main GUI file.
Gui_2.py is not the main file, main_bot.py is the main bot file, and the Guimain.py is the main GUI file.
Please run this file and main_bot.py file (bot file).
Do not delete any files.
Any changes in any commands will need to be updated in the other files accordingly.

"""

from tkinter import *
from tkinter import messagebox, ttk, filedialog as fd
import asyncio
from Gui_2 import *

gui = Tk()
gui.title('Discord Bot GUI 3.1.7 by Pun')
gui.geometry('850x550')
gui.iconbitmap('icon.ico')
style()

message= StringVar()
dm_msg= StringVar()
drop = StringVar()
drop.set(" "*10)
drop_server2= StringVar()
drop_server2.set(" "*10)
drop_server3 = StringVar()
drop_server3.set(" "*10)
drop_server4 = StringVar()
drop_server4.set(" "*10)
chan_select = StringVar()
chan_select.set(" "*10)
role_select = StringVar()
role_select.set(" "*10)
user_select = StringVar()
user_select.set(" "*10)
member_in_role = StringVar()
member_in_role.set("Role Members")
purge_channel = StringVar()
purge_channel.set(" "*10)
purge_chan = StringVar()
purge_chan.set(" "*10)
purge_num = StringVar()
purge_num.set(" "*10)
notbot_var = StringVar()
notbot_var.set("-")
member_var = StringVar()
member_var.set("-")
online_var = StringVar()
online_var.set("-")
offline_var = StringVar()
offline_var.set("-")
dnd_var = StringVar()
dnd_var.set("-")
idle_var = StringVar()
idle_var.set("-")
bot_var = StringVar()
bot_var.set("-")
role_var = StringVar()
role_var.set("-")
membercount_var = StringVar()
membercount_var.set("-")


Tab = ttk.Notebook(gui)
T1 = Frame(Tab, bg=black_color)
T2 = Frame(Tab, bg=black_color)
T3 = Frame(Tab, bg=black_color)
T4 = Frame(Tab, bg=black_color)
T5 = Frame(Tab, bg=black_color)
Tab.pack(fill= BOTH, expand=1)
Tab.add(T1,text='Purge')
Tab.add(T2,text='Member Count')
Tab.add(T3,text='Member Role')
Tab.add(T4,text="DM Messaging")
Tab.add(T5,text="Send Message")

drop_down_role = OptionMenu(T3 , role_select , *role_get)
drop_down_role.config(width=30, font=font_all)
drop_down_role["menu"].config(fg=white_color, bg=orange_color)
drop_down_role.config(fg=white_color, bg=orange_color)
drop_down_role.place(y=140+20+25, x= 250+120+55, anchor="center")
drop_down_chan = OptionMenu(T5 , chan_select , *role_get )
drop_down_chan.config(width=30, font=font_all)
drop_down_chan["menu"].config(fg=white_color, bg=orange_color)
drop_down_chan.config(fg=white_color, bg=orange_color)
drop_down_chan.place(y=140+20+25, x= 250+120+55, anchor="center")
drop_down_chan5 = OptionMenu(T1 , purge_chan , *role_get )
drop_down_chan5.config(width=30, font=font_all)
drop_down_chan5["menu"].config(fg=white_color, bg=orange_color)
drop_down_chan5.config(fg=white_color, bg=orange_color)
drop_down_chan5.place(y=140+20+25, x= 250+120+55, anchor="center")
drop_down_role5 = OptionMenu(T3 , member_in_role , *role_get )
drop_down_role5.config(width=20, font=font_all)
drop_down_role5["menu"].config(fg=white_color, bg=orange_color)
drop_down_role5.config(fg=white_color, bg=orange_color)
drop_down_role5.place(y=260+20, x= 350+120+55, anchor="center")

menubar = Menu(gui)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Options", menu=filemenu)
filemenu.add_command(label="More", command=lambda: options_more(gui))
filemenu.add_separator()

filemenu.add_command(label="Exit", command=gui.quit)

gui.config(bg=black_color, menu=menubar)

async def get_channel_member():
    server = drop_server2.get()
    if server == " "*10:
        raise SelectError("Please select a server!")
    serverid = [int(i) for i in server.split() if i.isdigit()]
    serverid = str(serverid).strip('[')
    serverid = serverid.strip(']')
    serverid = int(serverid)
    member = await ipc_client.request("get_member_count", guild_id=int(serverid))
    online_var.set(str(member[1]))
    member_var.set(str(member[0]))
    offline_var.set(str(member[2]))
    dnd_var.set(str(member[3]))
    idle_var.set(str(member[4]))
    bot_var.set(str(member[5]))
    notbot_var.set(str(member[6]))

def select_file(): 
    filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=(("All Files", "*.*"),))
    chan_name = chan_select.get()
    if chan_name == " "*10:
        raise SelectError("Please select a channel!")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_file(chan_name, filename))
    message.set('') 
    chan_select.set('')
    drop.set('')

def start_send():
    guild = drop.get()
    serverid = [int(i) for i in guild.split() if i.isdigit()]
    serverid = str(serverid).strip('[')
    serverid = serverid.strip(']')
    serverid = int(serverid)
    msg = message.get()
    chan_name = chan_select.get()
    drop_down_chan["menu"].delete(0, "end")
    if chan_name == " "*10:
        raise SelectError("Please select a channel!")
    elif msg == "":
        raise MessageError("Please input a message!")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send(msg,chan_name, serverid))
    # loop.close()
    # loop.stop()
    message.set('') 
    chan_select.set('')
    drop.set('')
    #HERE HERE HERE

def start_dm():
    msg = dm_msg.get()
    user = user_select.get()
    userid = [int(i) for i in user.split() if i.isdigit()]
    userid = str(userid).strip('[')
    userid = userid.strip(']')
    userid = int(userid)
    if msg == "":
        raise MessageError("Please input a message!")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dm(msg, userid))
    # loop.close()
    # loop.stop()
    dm_msg.set('')
    user_select.set('')
    drop_server4.set('')

async def get_channel():
    server = drop.get()
    if server == " "*10:
        raise SelectError("Please select a server!")
    serverid = [int(i) for i in server.split() if i.isdigit()]
    serverid = str(serverid).strip('[')
    serverid = serverid.strip(']')
    serverid = int(serverid)
    #print(len(server))
    chan = await ipc_client.request("get_chan_count", guild_id= serverid)
    drop_down_chan["menu"].delete(0, "end")
    for item in chan:
        drop_down_chan["menu"].add_command(
            label=item,
            command=lambda value=item: chan_select.set(value)
        )
    

def start_channel():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_channel())

async def get_purge_channel():
    server = purge_channel.get()
    if server == " "*10:
        raise SelectError("Please select a server!")
    serverid = [int(i) for i in server.split() if i.isdigit()]
    serverid = str(serverid).strip('[')
    serverid = serverid.strip(']')
    serverid = int(serverid)
    #print(len(server))
    chan = await ipc_client.request("get_chan_count", guild_id= serverid)
    #HERE HERE HERE
    drop_down_chan5["menu"].delete(0, "end")
    for item in chan:
        drop_down_chan5["menu"].add_command(
            label=item,
            command=lambda value=item: purge_chan.set(value)
        )

def start_purge_channel():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_purge_channel())

async def get_purging():
    chan_purging = purge_chan.get()
    server = purge_channel.get()
    serverid = [int(i) for i in server.split() if i.isdigit()]
    serverid = str(serverid).strip('[')
    serverid = serverid.strip(']')
    serverid = int(serverid)
    number = purge_num.get()
    purge_channel.set('')
    purge_chan.set('')
    purge_num.set('')
    drop_down_chan5["menu"].delete(0, "end")
    if chan_purging == " "*10:
        raise SelectError("Please select a channel!")
    elif number == " "*10:
        raise SelectError("Please select an amount to purge!")
    chan = await ipc_client.request("get_purge_channel", name= chan_purging, amount=str(int(number)), guild_id=serverid)
    if chan == "success":
        messagebox.showinfo("Success",f"Successfully purged {number} message(s) in {chan_purging}!")
    else:
        messagebox.showerror("Error","Error somewhere!")


def start_purge():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_purging())

l15=Label(T2, textvariable=idle_var, font=font_all, bg=black_color, fg=orange_color)
l15.place(y=265+20, x= 75+120+55, anchor="center")
l16=Label(T2, textvariable=bot_var, font=font_all, bg=black_color, fg=orange_color)
l16.place(y=265+20, x= 200+120+55, anchor="center")
l14=Label(T2, textvariable=dnd_var, font=font_all, bg=black_color, fg=orange_color)
l14.place(y=165+20, x= 475+120+55, anchor="center")
l13=Label(T2, textvariable=offline_var, font=font_all, bg=black_color, fg=orange_color)
l13.place(y=165+20, x= 325+120+55, anchor="center")
l12=Label(T2, textvariable=online_var, font=font_all, bg=black_color, fg=orange_color)
l12.place(y=165+20, x= 200+120+55, anchor="center")
l11 = Label(T2, textvariable=member_var, font=font_all, bg=black_color, fg=orange_color)
l11.place(y=165+20, x= 75+120+55, anchor="center")
l17=Label(T2, textvariable=notbot_var, font=font_all, bg=black_color, fg=orange_color)
l17.place(y=265+20, x= 325+120+55, anchor="center")

def start_member():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_channel_member())

async def get_role():
    role_select.set("")
    member_in_role.set("Role Members")
    server = drop_server3.get()
    if server == " "*10:
        raise SelectError("Please select a server!")
    serverid = [int(i) for i in server.split() if i.isdigit()]
    serverid = str(serverid).strip('[')
    serverid = serverid.strip(']')
    serverid = int(serverid)
    role_get = await ipc_client.request("get_role_count", guild_id= serverid)
    drop_down_role["menu"].delete(0, "end")
    for item in role_get:
        drop_down_role["menu"].add_command(
            label=item,
            command=lambda value=item: role_select.set(value)
        )
    

def start_role():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_role())

async def get_member_role():
    member_in_role.set("")
    role = role_select.get()
    if role == " "*10:
        raise SelectError("Please select a role!")
    server = drop_server3.get()
    if server == " "*10:
        raise SelectError("Please select a server!")
    serverid = [int(i) for i in server.split() if i.isdigit()]
    serverid = str(serverid).strip('[')
    serverid = serverid.strip(']')
    serverid = int(serverid)
    role_member = await ipc_client.request("get_member_role", guild_id= serverid, role=role)

    role_var.set(role)
    membercount_var.set(str(role_member[1]))
    all_role_member = role_member[0]
    if all_role_member == []:
        all_role_member=["Empty Role"]
    #HERE HERE HERE
    drop_down_role5["menu"].delete(0, "end")
    for item in all_role_member:
        drop_down_role5["menu"].add_command(
            label=item,
            command=lambda value=item: member_in_role.set(value)
        )

l31=Label(T3, textvariable=role_var, font=font_all, bg=black_color, fg=orange_color)
l31.place(y=265+20, x= 125+100, anchor="center")
l32=Label(T3, textvariable=membercount_var, font=font_all, bg=black_color, fg=orange_color)
l32.place(y=365+20, x= 125+100, anchor="center")

def start_member_role():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_member_role())

async def get_user():
    user_select.set("")
    server = drop_server4.get()
    if server == " "*10:
        raise SelectError("Please select a server!")
    serverid = [int(i) for i in server.split() if i.isdigit()]
    serverid = str(serverid).strip('[')
    serverid = serverid.strip(']')
    serverid = int(serverid)
    #print(len(server))
    user = await ipc_client.request("get_user_count", guild_id= serverid)
    drop_down_user["menu"].delete(0, "end")
    for item in user:
        drop_down_user["menu"].add_command(
            label=item,
            command=lambda value=item: user_select.set(value)
        )

drop_down_user = OptionMenu(T4 , user_select , *role_get )
drop_down_user.config(width=30, font=font_all)
drop_down_user["menu"].config(fg=white_color, bg=orange_color)
drop_down_user.config(fg=white_color, bg=orange_color)
drop_down_user.place(y=140+20+25, x= 250+120+55, anchor="center")

def start_user():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_user())

#Tab5
Label(T5, text='Select Server', font=font_all, bg=black_color, fg=white_color).place(y=20+20, x= 250+120+55, anchor="center")
Label(T5, text='Select Channel', font=font_all, bg=black_color, fg=white_color).place(y=100+20+25, x= 250+120+55, anchor="center")
Label(T5, text='Text to send', font=font_all, bg=black_color, fg=white_color).place(y=180+20+25, x= 250+120+55, anchor="center")
drop_down = OptionMenu( T5 , drop , *guild)
drop_down.config(width=30, font=font_all)
drop_down["menu"].config(fg=white_color, bg=orange_color)
drop_down.config(fg=white_color, bg=orange_color)
drop_down.place(y=60+20, x= 250+120+55, anchor="center")
b1 = Button(T5, text="Submit", command=start_channel, font=font_all, bg=orange_color, fg=white_color)
b1.place(y=60+20, x= 475+120+55, anchor="center")
tr = Entry(T5, font=font_all_big, textvariable=message, bg=orange_color, fg=white_color, width=30)
tr.place(y=220+20+25, x= 250+120+55, anchor="center")
b2 = Button(T5, text="send", command=start_send, font=font_all, bg=orange_color, fg=white_color)
b2.place(y=260+20+45, x= 250+65+55, anchor="center")
b3 = Button(T5, text="send file", command=select_file, font=font_all, bg=orange_color, fg=white_color)
b3.place(y=260+20+45, x= 250+175+55, anchor="center")

#Tab2
Label(T2, text='Select Server', font=font_all, bg=black_color, fg=white_color).place(y=20+20, x= 250+120+55, anchor="center")
drop_down2 = OptionMenu( T2 , drop_server2 , *guild)
drop_down2.config(width=30, font=font_all)
drop_down2["menu"].config(fg=white_color, bg=orange_color)
drop_down2.config(fg=white_color, bg=orange_color)
drop_down2.place(y=60+20, x= 250+120+55, anchor="center")
b1_2 = Button(T2, text="Submit", command=start_member, font=font_all, bg=orange_color, fg=white_color)
b1_2.place(y=60+20, x= 475+120+55, anchor="center")
Label(T2, text='All Members', font=font_all, bg=black_color, fg=white_color).place(y=145, x= 75+120+55, anchor="center")
Label(T2, text='Online', font=font_all, bg=black_color, fg=white_color).place(y=125+20, x= 200+120+55, anchor="center")
Label(T2, text='Offline', font=font_all, bg=black_color, fg=white_color).place(y=125+20, x= 325+120+55, anchor="center")
Label(T2, text='Dnd', font=font_all, bg=black_color, fg=white_color).place(y=125+20, x= 475+120+55, anchor="center")
Label(T2, text='Idle', font=font_all, bg=black_color, fg=white_color).place(y=225+20, x= 75+120+55, anchor="center")
Label(T2, text='Bots', font=font_all, bg=black_color, fg=white_color).place(y=225+20, x= 200+120+55, anchor="center")
Label(T2, text='Members', font=font_all, bg=black_color, fg=white_color).place(y=225+20, x= 325+120+55, anchor="center")

#Tab3
Label(T3, text='Select Server', font=font_all, bg=black_color, fg=white_color).place(y=20+20, x= 250+120+55, anchor="center")
Label(T3, text='Select Role', font=font_all, bg=black_color, fg=white_color).place(y=100+20+25, x= 250+120+55, anchor="center")
drop_down3 = OptionMenu(T3 , drop_server3 , *guild)
drop_down3.config(width=30, font=font_all)
drop_down3["menu"].config(fg=white_color, bg=orange_color)
drop_down3.config(fg=white_color, bg=orange_color)
drop_down3.place(y=60+20, x= 250+120+55, anchor="center")
b1_3 = Button(T3, text="Submit", command=start_role, font=font_all, bg=orange_color, fg=white_color)
b1_3.place(y=60+20, x= 475+120+55, anchor="center")
b2_3 = Button(T3, text="Submit", command=start_member_role, font=font_all, bg=orange_color, fg=white_color)
b2_3.place(y=140+20+25, x= 475+120+55, anchor="center")
Label(T3, text='Role Name', font=font_all, bg=black_color, fg=white_color).place(y=225+20, x= 125+100, anchor="center")
Label(T3, text='Members', font=font_all, bg=black_color, fg=white_color).place(y=325+20, x= 125+100, anchor="center")
Label(T3, text='Role Members', font=font_all, bg=black_color, fg=white_color).place(y=225+20, x= 350+120+55, anchor="center")

#Tab4
Label(T4, text='Select Server', font=font_all, bg=black_color, fg=white_color).place(y=20+20, x= 250+120+55, anchor="center")
Label(T4, text='Select User', font=font_all, bg=black_color, fg=white_color).place(y=100+20+25, x= 250+120+55, anchor="center")
Label(T4, text='Text to send', font=font_all, bg=black_color, fg=white_color).place(y=180+20+25, x= 250+120+55, anchor="center")
drop_down_4 = OptionMenu( T4 , drop_server4 , *guild)
drop_down_4.config(width=30, font=font_all)
drop_down_4["menu"].config(fg=white_color, bg=orange_color)
drop_down_4.config(fg=white_color, bg=orange_color)
drop_down_4.place(y=60+20, x= 250+120+55, anchor="center")
b1_4 = Button(T4, text="Submit", command=start_user, font=font_all, bg=orange_color, fg=white_color)
b1_4.place(y=60+20, x= 475+120+55, anchor="center")
tr_4 = Entry(T4, font=font_all_big, textvariable=dm_msg, bg=orange_color, fg=white_color, width=30)
tr_4.place(y=220+20+25, x= 250+120+55, anchor="center")
b1_4 = Button(T4, text="Send", command=start_dm, font=font_all, bg=orange_color, fg=white_color)
b1_4.place(y=260+20+45, x= 250+120+55, anchor="center")

#Tab1
Label(T1, text='Select Server', font=font_all, bg=black_color, fg=white_color).place(y=20+20, x= 250+120+55, anchor="center")
Label(T1, text='Select Channel', font=font_all, bg=black_color, fg=white_color).place(y=100+20+25, x= 250+120+55, anchor="center")
drop_down = OptionMenu( T1 , purge_channel , *guild)
drop_down.config(width=30, font=font_all)
drop_down["menu"].config(fg=white_color, bg=orange_color)
drop_down.config(fg=white_color, bg=orange_color)
drop_down.place(y=60+20, x= 250+120+55, anchor="center")
b5_1 = Button(T1, text="Submit", command=start_purge_channel, font=font_all, bg=orange_color, fg=white_color)
b5_1.place(y=60+20, x= 475+120+55, anchor="center")
purge_num_list = ['1','5','10','20']
Label(T1, text='Purge Number', font=font_all, bg=black_color, fg=white_color).place(y=180+20+25, x= 250+120+55, anchor="center")
drop_down_purge = OptionMenu(T1 , purge_num , *purge_num_list)
drop_down_purge.config(width=15, font=font_all)
drop_down_purge["menu"].config(fg=white_color, bg=orange_color)
drop_down_purge.config(fg=white_color, bg=orange_color)
drop_down_purge.place(y=220+20+25, x= 250+120+55, anchor="center")
b5_1 = Button(T1, text="Purge", command=start_purge, font=font_all, bg=orange_color, fg=white_color)
b5_1.place(y=220+20+25, x= 475+120+55, anchor="center")
gui.mainloop()