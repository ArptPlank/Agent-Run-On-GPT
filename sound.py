from connect_with_gpt import gpt
import pyaudio
import wave
import time
import threading
import os
class sound():
    def __init__(self):
        self.gpt = gpt()
        self.CHUNK = 1024  # 每次读取的帧数
        self.FORMAT = pyaudio.paInt16  # 采样格式（16位）
        self.CHANNELS = 1  # 声道数
        self.RATE = 44100  # 采样率
        self.text = None
        self.is_record = False
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.delete_files_in_folder("mp3")
        self.delete_files_in_folder("output_sound")
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)
        t = threading.Thread(target=self.record)
        t.start()


    def start_record(self,event):
        self.frames = []
        self.is_record = True

    def stop_record(self):
        _frames = self.frames
        self.frames = []
        sound_path = f"mp3/{int(time.time())}.wav"
        wf = wave.open(sound_path, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(_frames))
        wf.close()
        return sound_path

    def record(self):
        start_time = time.time()
        while True:
            self.frames.append(self.stream.read(self.CHUNK))
            if time.time() - start_time > 120:
                self.frames = []
                start_time = time.time()

    def get_text(self,sound_path):
        return self.gpt.get_text_of_sound(sound_path)

    def delete_files_in_folder(self,folder_path):
        # 遍历文件夹内的所有文件
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # 删除文件
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                else:
                    print(f"{file_path} is not a file.")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

