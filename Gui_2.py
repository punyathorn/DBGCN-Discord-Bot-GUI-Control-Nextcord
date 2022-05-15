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
File: Gui_2.py
License: MIT License
Version: 1.9.9

WARNING: Do not run this file. 
This is not the main file. 
Please run the Guimain.py file and main_bot.py file (bot file).
Do not delete any files.
Any changes in any commands will need to be updated in the other files accordingly.

"""

from tkinter import *
from tkinter import ttk, messagebox
from nextcord.ext import ipc
from tkinter.colorchooser import askcolor
import asyncio

class IPCError(Exception):
    pass
try:
    ipc_client = ipc.Client(secret_key="your_ipc_secret_key")
except:
    raise IPCError("An error occured while IPC Client tried to connect to the IPC Server")
white_color = "white"
black_color = '#333333'
orange_color = '#F57713'
font_all = ('consolas italic', 14)
font_all_small = ('consolas italic', 12)
font_all_big = ('consolas italic', 18)
font_all_med = ('consolas italic', 16)
role_get = ["Please select server"]
def style():
    style = ttk.Style()
    style.theme_create( "cool2", parent = "alt", settings ={"TNotebook": {"configure": {"tabmargins": [10, 10, 20, 10], "background":black_color }},
                    "TNotebook.Tab": {"configure": {"padding": [30, 15], "background": black_color, "foreground": "white","font":('consolas italic', 14), "borderwidth":[0]},
                    "map": {"background": [("selected", orange_color), ('!active', black_color), ('active', orange_color)],"expand": [("selected", [1, 1, 1, 0])]}}})
    style.theme_use("cool2")
    style.layout("Tab",[('Notebook.tab', {'sticky': 'nswe', 'children':[('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                [('Notebook.label', {'side': 'top', 'sticky': ''})],})],})])
class SelectError(Exception):
    pass

class MessageError(Exception):
    pass

async def send(msg, chan_name, id):
    mem = await ipc_client.request("get_send_count", msg=msg, name=chan_name, guild_id=id)
    if mem == "success":
        messagebox.showinfo("Success",f"Your message saying: {msg} was successfully sent in {chan_name}!")
    else:
        messagebox.showerror("Error","Error somewhere!")

async def send_file(chan_name, file):
    mem = await ipc_client.request("get_file_sent", name=chan_name, file=file)
    if mem == "success":
        messagebox.showinfo("Success",f"Your file was sent to {chan_name}!")
    else:
        messagebox.showerror("Error","Error somewhere!")

async def dm(msg, user):
    dm = await ipc_client.request("get_user_dm", msg=msg, id=user)
    #print(dm)
    if dm == "success":
        messagebox.showinfo("Success",f"Your message saying: {msg} was successfully sent to user id: {user}!")
    else:
        messagebox.showerror("Error","Error somewhere!")

async def guild_server():
    global guild
    guild = await ipc_client.request("get_guild_count")

async def get_channel():
    server_s = server.get()
    if server_s == " "*10:
        raise SelectError("Please select a server!")
    serverid = [int(i) for i in server_s.split() if i.isdigit()]
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
async def get_message_edit():
    chan = chan_select.get()
    id = msgid.get()
    edit_message = edit_to.get()
    response = await ipc_client.request("get_msg_edit", name=chan, msgid=id, edit_to=edit_message)
    if response == "Edited":
        edit_to.set("")
        response2 = await ipc_client.request("get_msg_info", name=chan, msgid=id)
        if len(response2[0]) > 46:
            nr = response2[0].split(None, 1)
            present_text.set(nr[0])
            nr2.set(nr[1])
        else:
            present_text.set(response2[0])
            try:
                nr2.set("")
            except:
                pass
        edit_status.set("Status: Edited")

async def get_channel_edit():
    chan = chan_select.get()
    id = msgid.get()
    response = await ipc_client.request("get_msg_info", name=chan, msgid=id)
    msgid_show.set(f"ID: {id}")
    print(response)
    if response[1] == "Editable":
        if len(response[0]) > 46:
            nr = response[0].split(None, 1)
            present_text.set(nr[0])
            nr2.set(nr[1])
        else:
            present_text.set(response[0])
            present_text_entry.config(width=len(response[0]))
            try:
                nr2.set("")
            except:
                pass
    else:
        if len(response[0]) > 46:
            nr = response[0].split(None, 1)
            present_text.set(nr[0])
            present_text_entry.config(width=len(nr[0]))
            nr2.set(nr[1])
            Nr2_entry.config(width=len(nr[1]))
        else:
            present_text.set(response[0])
            try:
                nr2.set("")
            except:
                pass
        b3['state'] = DISABLED
    edit_status.set("Status: "+response[1])

def start_get_text():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_channel_edit())

def start_message_edit():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_message_edit())

def start_channel():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_channel())

loop = asyncio.get_event_loop()
loop.run_until_complete(guild_server())

def options_more(gui):
    global filewin, menubar, chan_select, Nr2_entry, field_num, present_text_entry, drop_down_chan, server, msgid, present_text, T1,edit_to, b3, nr2, edit_status, msgid_show, title
    gui.destroy()
    filewin = Tk()
    filewin.title('Discord Bot GUI 2.9.8 by Pun')
    filewin.geometry('850x650')
    filewin.iconbitmap('icon.ico')
    menubar = Menu(filewin)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=filewin.quit)
    menubar.add_cascade(label="Options", menu=filemenu)
    filewin.config(bg=black_color, menu=menubar)
    Tab = ttk.Notebook(filewin)
    T1 = Frame(Tab, bg=black_color)
    Tab.pack(fill= BOTH, expand=1)
    Tab.add(T1,text='Edit Message')
    field_num = IntVar()
    field_num.set(1)
    title = StringVar()
    title.set("")
    msgid = StringVar()
    msgid.set("")
    msgid_show = StringVar()
    msgid_show.set("ID: ")
    edit_to = StringVar()
    edit_to.set("")
    present_text = StringVar()
    present_text.set("-")
    server = StringVar()
    server.set(" "*10)
    chan_select = StringVar()
    chan_select.set(" "*10)
    nr2 = StringVar()
    nr2.set("-")
    edit_status = StringVar()
    edit_status.set("Status: ")
    style()
    drop_down = OptionMenu( T1 , server , *guild)
    drop_down.config(width=30, font=font_all)
    drop_down["menu"].config(fg=white_color, bg=orange_color)
    drop_down.config(fg=white_color, bg=orange_color)
    drop_down.place(y=60+20, x= 250+120+55, anchor="center")
    drop_down_chan = OptionMenu(T1 , chan_select , *role_get )
    drop_down_chan.config(width=30, font=font_all)
    drop_down_chan["menu"].config(fg=white_color, bg=orange_color)
    drop_down_chan.config(fg=white_color, bg=orange_color)
    drop_down_chan.place(y=175, x= 250+120+55, anchor="center")
    Label(T1, text='Select Server', font=font_all, bg=black_color, fg=white_color).place(y=20+20, x= 250+120+55, anchor="center")
    Label(T1, text='Select Channel', font=font_all, bg=black_color, fg=white_color).place(y=135, x= 250+120+55, anchor="center")
    b1 = Button(T1, text="Submit", command=start_channel, font=font_all, bg=orange_color, fg=white_color)
    b1.place(y=60+20, x= 475+120+55, anchor="center")
    Label(T1, text='Message ID', font=font_all, bg=black_color, fg=white_color).place(y=140+20+20+45, x= 250+120+55, anchor="center")
    b2 = Button(T1, text="Submit",  font=font_all, bg=orange_color, fg=white_color, command=start_get_text)
    b2.place(y=140+20+20+65+20, x= 475+120+55, anchor="center")
    e2 = Entry(T1, textvariable=msgid, font= font_all_big, bg=orange_color, fg=white_color, width=25)
    e2.place(y=140+20+20+65+20, x=425, anchor="center")

    Label(T1, text='Present Text', font=font_all, bg=black_color, fg=white_color).place(y=140+20+25+65+40+55-15, x= 75+120+55, anchor="center")
    present_text_entry = Entry(T1, textvariable=present_text, width=46, font=font_all, fg=orange_color, bd=0, state="readonly", readonlybackground=black_color, justify='center')
    present_text_entry.place(y=140+20+25+65+40+85-15, x= 75+120+55, anchor="center")
    Label(T1, text='Edit To', font=font_all, bg=black_color, fg=white_color).place(y=140+20+25+65+40+55-15, x= 475+120+55, anchor="center")
    e3 = Entry(T1, textvariable=edit_to, font= font_all_big, bg=orange_color, fg=white_color, width=25)
    e3.place(y=140+20+25+65+40+85+50-12, x=475+120+55, anchor="center")
    b3 = Button(T1, text="Edit", command=start_message_edit, font=font_all, bg=orange_color, fg=white_color)
    b3.place(y=140+20+25+65+40+85+50-12, x=415, anchor="center")
    Entry(T1, textvariable=edit_status, font=font_all, fg=orange_color, bd=0, state="readonly", readonlybackground=black_color, justify='center').place(y=140+20+25+65+40+85+50+20, x= 75+120+55, anchor="center")
    Nr2_entry = Entry(T1, textvariable=nr2, font=font_all, fg=orange_color, bd=0, state="readonly", readonlybackground=black_color, justify='center', width=46)
    Nr2_entry.place(y=140+20+25+65+40+85+25-15, x= 75+120+55, anchor="center")
    Entry(T1, textvariable=msgid_show, font=font_all, fg=orange_color, bd=0, state="readonly", readonlybackground=black_color, justify='center').place(y=140+20+25+65+40+85+75+25, x= 75+120+55, anchor="center")
