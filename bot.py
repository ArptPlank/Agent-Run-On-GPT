import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from connect_with_gpt import gpt
from sound import sound
import threading
from PIL import Image
gpt = gpt()
sound = sound()
is_sound = False
def send(tag = 0):
    if tag == 0:
        text = entry.get("0.0", "end")
        entry.delete("0.0", "end")
        text = text.strip("\n")
        text = f"用户：{text}\n\n"
        text_box.config(state="normal")
        text_box.insert("end", text)
        text_box.config(state="disabled")
        text = text_box.get("0.0", "end")
        gpt.chat(text)
        text_box.config(state="normal")
        text_box.insert("end", "GPT：")
        text_box.config(state="disabled")
        sentense = ""
        lable = [",","，","。","！","？",".","!","?"]
        index = 0
        gpt.index = 0
        while gpt.is_chat:
            if gpt.is_finish and len(gpt.delta) == 0:
                gpt.is_chat = False
                gpt.is_finish = False
                gpt.delta = []
                text_box.config(state="normal")
                text_box.insert("end", "\n\n")
                text_box.config(state="disabled")
            elif len(gpt.delta) > 0:
                text_box.config(state="normal")
                text_box.insert("end", gpt.delta[0])
                text_box.config(state="disabled")
                if any(gpt.delta[0] == variant for variant in lable) and is_sound:
                    t = threading.Thread(target=gpt.get_real_sound,args=(sentense,index))
                    t.start()
                    index += 1
                    sentense = ""
                else:
                    sentense += gpt.delta[0]
                gpt.delta.pop(0)
    elif tag == 1:
        text = text_box.get("0.0", "end")
        gpt.chat(text)
        text_box.config(state="normal")
        text_box.insert("end", "GPT：")
        text_box.config(state="disabled")
        sentense = ""
        lable = ["。", "！", "？", ".", "!", "?"]
        index = 0
        gpt.index = 0
        while gpt.is_chat:
            if gpt.is_finish and len(gpt.delta) == 0:
                gpt.is_chat = False
                gpt.is_finish = False
                gpt.delta = []
                text_box.config(state="normal")
                text_box.insert("end", "\n\n")
                text_box.config(state="disabled")
            elif len(gpt.delta) > 0:
                text_box.config(state="normal")
                text_box.insert("end", gpt.delta[0])
                text_box.config(state="disabled")
                if any(gpt.delta[0] == variant for variant in lable) and is_sound:
                    t = threading.Thread(target=gpt.get_real_sound,args=(sentense,index))
                    t.start()
                    index += 1
                    sentense = ""
                else:
                    sentense = sentense + gpt.delta[0]
                gpt.delta.pop(0)

def send_thread(tag = 0):
    t = threading.Thread(target=send,args=(tag,))
    t.start()
def secect_gpt3():
    gpt.model_for_chat = "gpt-3.5-turbo"

def secect_gpt4():
    gpt.model_for_chat = "gpt-4-0314"

def open_month():
    global is_sound
    is_sound = True

def close_month():
    global is_sound
    is_sound = False

def stop_record():
    sound_path = sound.stop_record()
    text = sound.get_text(sound_path)
    text_box.config(state="normal")
    text_box.insert("end", f"用户：{text}\n\n")
    text_box.config(state="disabled")
    send_thread(tag=1)
def stop_record_thread(event):
    t = threading.Thread(target=stop_record)
    t.start()
def show():
    image = Image.open("pay.png")
    image.show()
def pay():
    t = threading.Thread(target=show)
    t.start()
root = tk.Tk()
root.title("ChatGPT V1.0.0")
root.geometry("700x800")
title = tk.Label(root,font=("宋体",32),fg="blue",text="ChatGPT")
title.place(x=250,y=10,anchor='nw')
button_pay = tk.Button(root,font=("宋体",20),fg="green",width=10,height=1,text="打赏",command=pay)
button_pay.place(x=500,y=25,anchor='nw')
text_box = tk.Text(root,font=("宋体",15),fg="black",width=63,height=20)
text_box.place(x=35,y=100,anchor='nw')
text_box.config(state="disabled")
entry = tk.Text(root,font=("宋体",20),fg="black",width=45,height=4)
entry.place(x=35,y=550,anchor='nw')
button_send = tk.Button(root,font=("宋体",20),fg="black",width=10,height=1,text="发送",command=send_thread)
button_send.place(x=28,y=700,anchor='nw')
button_speak = tk.Button(root,font=("宋体",20),fg="black",width=10,height=1,text="语音")
button_speak.place(x=200,y=700,anchor='nw')
choose_model = tk.StringVar(value="gpt-3.5-turbo")
is_open = tk.IntVar(value=0)
rl_1 = tk.Radiobutton(root, text='GPT3.5', variable=choose_model, value="gpt-3.5-turbo",font=("宋体",20),command=secect_gpt3)
rl_1.place(x=400,y=700,anchor='nw')
rl_2 = tk.Radiobutton(root, text='GPT4', variable=choose_model, value="gpt-4-0314",font=("宋体",20),command=secect_gpt4)
rl_2.place(x=400,y=730,anchor='nw')
rl_3 = tk.Radiobutton(root, text='语音回复', variable=is_open, value=1,font=("宋体",20),command=open_month)
rl_3.place(x=520,y=700,anchor="nw")
rl_4 = tk.Radiobutton(root, text="", variable=is_open, value=0,font=("宋体",20),command=close_month)
rl_4.place(x=520,y=730,anchor="nw")
button_speak.bind("<Button-1>",sound.start_record)
button_speak.bind("<ButtonRelease-1>",stop_record_thread)
root.mainloop()
