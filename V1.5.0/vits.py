import time
import threading
from gradio_client import Client
class vits():
	def __init__(self):
		try:
			self.client = Client("https://v2.genshinvoice.top/")
		except:
			print("API已炸，自动跳过个性回复初始化，并在未来10分钟内重复尝试请求连接")
			self.reconnect_thread()

	def make_sound(self,text):
		result = self.client.predict(
			text,  # str in '输入文本内容' Textbox component
			"纳西妲_ZH",
			0.2,  # float (numeric value between 0 and 1) in 'SDP Ratio' Slider component
			0.6,  # float (numeric value between 0.1 and 2) in 'Noise' Slider component
			0.8,  # float (numeric value between 0.1 and 2) in 'Noise_W' Slider component
			1,  # float (numeric value between 0.1 and 2) in 'Length' Slider component
			"ZH",  # str (Option from: ['ZH', 'JP', 'EN', 'mix', 'auto']) in 'Language' Dropdown component
			None,
			# "https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav",	# str (filepath on your computer (or URL) of file) in 'Audio prompt' Audio component
			"Howdy!",  # str in 'Text prompt' Textbox component
			"Text Prompt",  # str in 'Prompt Mode' Radio component
			fn_index=0
		)
		return result[1]

	def reconnect(self):
		for _ in range(10):
			try:
				self.client = Client("https://v2.genshinvoice.top/")
				print("连接成功")
			except:
				print("请求失败")
				time.sleep(60)

	def reconnect_thread(self):
		t = threading.Thread(target=self.reconnect)
		t.start()