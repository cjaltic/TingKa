import azure.cognitiveservices.speech as speechsdk
from datetime import date
import random
import os

speech_key = ""
service_region = "eastus"

def createOutputPath():
	today = str(date.today())
	newpath = r'./' + today
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	return newpath

def translate(path, text):
	speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
	speech_config.speech_synthesis_voice_name = selectVoice()

	output_path = path + '/' + text + ".mp3"

	audio_output = speechsdk.audio.AudioOutputConfig(filename= output_path)
	synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

	result = synthesizer.speak_text_async(text).get()

	if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
	    print(f"Saved: {output_path}")
	else:
	    print(f"Error: {result.reason}")

def selectVoice():
	voices = [
	    "zh-CN-XiaoxiaoNeural",
	    "zh-CN-YunxiNeural",
	    "zh-CN-XiaochenNeural",
	    "zh-CN-XiaohanNeural",
	    "zh-CN-XiaomengNeural",
	    "zh-CN-XiaomoNeural",
	    "zh-CN-XiaoqiuNeural",
	    "zh-CN-XiaoruiNeural",
	    "zh-CN-XiaoshuangNeural",
	    "zh-CN-XiaoxuanNeural",
	    "zh-CN-XiaoyanNeural",
	    "zh-CN-XiaoyouNeural",
	    "zh-CN-YunyeNeural",
	    "zh-CN-YunzeNeural"
	]
	return random.choice(voices)

def read(input):
	with open(input) as file:
		words = [word.rstrip() for word in file]
		words = list(filter(None, words))
	return words

def run():
	words = read("input.txt")
	path = createOutputPath()
	print(path)
	for w in words:
		translate(path, w)

run()

