import azure.cognitiveservices.speech as speechsdk
import genanki
import random
import os
import re
from datetime import date

speech_key = ""
service_region = "eastus"

def createOutputPath():
	today = str(date.today())
	newpath = r'./' + today
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	return newpath

def createDeck(source, out):
	media_files = []
	model = genanki.Model(
	    1607392319,
	    'Chinese Audio Model',
	    fields=[
	        {'name': 'Audio'},
	        {'name': 'Text'},
	    ],
	    templates=[
	        {
	            'name': 'Card 1',
	            'qfmt': '{{Audio}}',  # Front: audio
	            'afmt': '{{FrontSide}}<hr id="answer">{{Text}}',  # Back: show text
	        },
	    ],
	    css='''
	    .card {
	      font-family: arial;
	      font-size: 24px;
	      text-align: center;
	      color: black;
	      background-color: white;
	    }
	    '''
	)
	deck = genanki.Deck(2059400110, "Audio Flashcards")
	for file in os.listdir(source):
		if file.endswith('.mp3'):
			chinese_text = os.path.splitext(file)[0]
			audio_tag = f"[sound:{file}]"
			note = genanki.Note(
				model = model,
				fields=[audio_tag, chinese_text]
			)
			deck.add_note(note)
			media_files.append(os.path.join(source, file))
	package = genanki.Package(deck)
	package.media_files = media_files
	package.write_to_file(out)
	print(f"✅ Anki deck created: {out}")



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
	today = str(date.today())
	createDeck(path, path + '/deck-' + today + '.apkg')

run()

