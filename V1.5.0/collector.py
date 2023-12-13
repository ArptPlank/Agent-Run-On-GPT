import pygame
import os
import time
import threading
class collector():
    def __init__(self):
        #待被播放音频路径
        self.sound_path = []
        #待被删除音频路径
        self.delete_sound_path = []
        self.delete_all_file("mp3")
        self.delete_all_file("output_sound")
        self.index = 0
        pygame.init()
        t = threading.Thread(target=self.start)
        t.start()

    def add_sound(self,sound_path,index):
        self.sound_path.append({"path":sound_path,"play_time":None,"index":index})
    def play_sound(self):
        while True:
            if len(self.sound_path) > 0:
                sound_path = self.pop_index(self.index)
                if sound_path != None:
                    print(sound_path)
                    pygame.mixer.init()
                    pygame.mixer.music.load(sound_path["path"])
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pass
                    sound_path["play_time"] = time.time()
                    pygame.mixer.quit()
                    self.delete_sound_path.append(sound_path)
                    self.index += 1
            self.delete_sound()

    def delete_sound(self):
        if len(self.delete_sound_path) > 0:
            for index,path in enumerate(self.delete_sound_path):
                if time.time() - path["play_time"] > 3:
                    try:
                        os.remove(path["path"])
                        del self.delete_sound_path[index]
                    except:
                        pass


    def start(self):
        self.play_sound()

    def delete_all_file(self,folder_path):
        # 遍历文件夹中的所有文件并删除
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):  # 只删除文件，不包括文件夹
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    def pop_index(self,index):
        for i,path in enumerate(self.sound_path):
            if index == path["index"]:
                return path
        return None