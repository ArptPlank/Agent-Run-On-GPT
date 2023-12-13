import os
import tkinter as tk
from tkinter import scrolledtext,messagebox
from ttkbootstrap.constants import *
from connect_with_gpt import gpt
from sound import sound
import threading
from PIL import Image
from collector import collector
collector = collector()
gpt = gpt(collector=collector)
sound = sound(gpt=gpt)
is_sound = 0
can_write = True
def send(tag = 0):
    global can_write
    if can_write:
        can_write = False
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
            lable = [",", "，", "。", "！", "？", ".", "!", "?"]
            while gpt.is_chat:
                if gpt.is_finish and len(gpt.delta) == 0:
                    gpt.is_chat = False
                    gpt.is_finish = False
                    gpt.delta = []
                    text_box.config(state="normal")
                    text_box.insert("end", "\n\n")
                    text_box.config(state="disabled")
                    can_write = True
                elif len(gpt.delta) > 0:
                    text_box.config(state="normal")
                    text_box.insert("end", gpt.delta[0])
                    text_box.config(state="disabled")
                    if any(gpt.delta[0] == variant for variant in lable) and (is_sound == 1 or is_sound == 2):
                        t = threading.Thread(target=gpt.get_real_sound, args=(sentense, is_sound))
                        t.start()
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
                    can_write = True
                    if any(gpt.delta[0] == variant for variant in lable) and (is_sound == 1 or is_sound == 2):
                        t = threading.Thread(target=gpt.get_real_sound, args=(sentense, tag))
                        t.start()
                        sentense = ""
                    else:
                        sentense = sentense + gpt.delta[0]
                    gpt.delta.pop(0)
    else:
        messagebox.showinfo("注意", "前一消息仍未回复完")
def send_thread(tag = 0):
    t = threading.Thread(target=send,args=(tag,))
    t.start()
def secect_gpt3():
    gpt.model_for_chat = "gpt-3.5-turbo"

def secect_gpt4():
    gpt.model_for_chat = "gpt-4-0314"

def open_mouth():
    global is_sound
    is_sound = 1

def close_mouth():
    global is_sound
    is_sound = 0

def open_with_nxd():
    global is_sound
    is_sound = 2
    messagebox.showinfo("注意", "该API接口为社区大佬的免费接口不保证百分之百可用")

def secect_gpt3_thread():
    t = threading.Thread(target=secect_gpt3)
    t.start()

def secect_gpt4_thread():
    t = threading.Thread(target=secect_gpt4)
    t.start()
def open_mouth_thread():
    t = threading.Thread(target=open_mouth)
    t.start()
def close_mouth_thread():
    t = threading.Thread(target=close_mouth)
    t.start()

def open_with_nxd_thread():
    t = threading.Thread(target=open_with_nxd)
    t.start()

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
def clean():
    text_box.config(state="normal")
    text_box.delete("0.0","end")
    text_box.config(state="disabled")
root = tk.Tk()
root.title("ChatGPT V1.0.0")
root.geometry("700x800")
title = tk.Label(root,font=("宋体",32),fg="blue",text="ChatGPT")
title.place(x=250,y=10,anchor='nw')
button_pay = tk.Button(root,font=("宋体",20),fg="green",width=10,height=1,text="清空",command=clean)
button_pay.place(x=50,y=25,anchor='nw')
button_pay = tk.Button(root,font=("宋体",20),fg="green",width=10,height=1,text="打赏",command=pay)
button_pay.place(x=500,y=25,anchor='nw')
text_box = scrolledtext.ScrolledText(root,font=("宋体",15),fg="black",width=63,height=20)
text_box.place(x=35,y=100,anchor='nw')
text_box.config(state="disabled")
entry = scrolledtext.ScrolledText(root,font=("宋体",15),fg="black",width=63,height=6)
entry.place(x=35,y=550,anchor='nw')
button_send = tk.Button(root,font=("宋体",20),fg="black",width=10,height=1,text="发送",command=send_thread)
button_send.place(x=28,y=700,anchor='nw')
button_speak = tk.Button(root,font=("宋体",20),fg="black",width=10,height=1,text="语音")
button_speak.place(x=200,y=700,anchor='nw')
choose_model = tk.StringVar(value="gpt-3.5-turbo")
is_open = tk.IntVar(value=0)
rl_1 = tk.Radiobutton(root, text='GPT3.5', variable=choose_model, value="gpt-3.5-turbo",font=("宋体",20),command=secect_gpt3_thread)
rl_1.place(x=400,y=700,anchor='nw')
rl_2 = tk.Radiobutton(root, text='GPT4', variable=choose_model, value="gpt-4-0314",font=("宋体",20),command=secect_gpt4_thread)
rl_2.place(x=400,y=730,anchor='nw')
rl_3 = tk.Radiobutton(root, text='语音回复', variable=is_open, value=1,font=("宋体",20),command=open_mouth_thread)
rl_3.place(x=520,y=700,anchor="nw")
rl_4 = tk.Radiobutton(root, text="文字回复", variable=is_open, value=0,font=("宋体",20),command=close_mouth_thread)
rl_4.place(x=520,y=730,anchor="nw")
rl_4 = tk.Radiobutton(root, text="个性回复", variable=is_open, value=2,font=("宋体",20),command=open_with_nxd_thread)
rl_4.place(x=520,y=760,anchor="nw")
button_speak.bind("<Button-1>",sound.start_record)
button_speak.bind("<ButtonRelease-1>",stop_record_thread)
root.mainloop()
