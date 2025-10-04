import azure.cognitiveservices.speech as speechsdk
import genanki
import random
import os
import re
import gpt
from datetime import date

speech_key = ""
service_region = "eastus"

def createOutputPath():
	today = str(date.today())
	newpath = r'./out/' + today
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	return newpath

def createDeck(source, out):
    media_files = []
    model = genanki.Model(
        1607392319,
        'Chinese Audio Model',
        fields=[
            {'name': 'FrontAudio'},
            {'name': 'BackAudio'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{FrontAudio}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{BackAudio}}',
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

    for sentence_dir in os.listdir(source):
        card_dir = os.path.join(source, sentence_dir)
        if not os.path.isdir(card_dir):
            continue

        sentence_path = os.path.join(card_dir, "sentence.mp3")
        word_path = os.path.join(card_dir, "word.mp3")
        explanation_path = os.path.join(card_dir, "explanation.mp3")

        if not (os.path.exists(sentence_path) and os.path.exists(word_path) and os.path.exists(explanation_path)):
            continue

        # Create unique flat filenames
        flat_sentence_filename = f"sentence_{sentence_dir}.mp3"
        flat_word_filename = f"word_{sentence_dir}.mp3"
        flat_explanation_filename = f"explanation_{sentence_dir}.mp3"

        # Copy files to flat structure
        flat_sentence_path = os.path.join(source, flat_sentence_filename)
        flat_word_path = os.path.join(source, flat_word_filename)
        flat_explanation_path = os.path.join(source, flat_explanation_filename)

        os.rename(sentence_path, flat_sentence_path)
        os.rename(word_path, flat_word_path)
        os.rename(explanation_path, flat_explanation_path)

        # Anki tags
        sentence_tag = f"[sound:{flat_sentence_filename}]"
        word_tag = f"[sound:{flat_word_filename}]"
        explanation_tag = f"[sound:{flat_explanation_filename}]"

        note = genanki.Note(
            model=model,
            fields=[
                sentence_tag,
                word_tag + "<br>" + explanation_tag
            ]
        )
        deck.add_note(note)

        media_files.extend([
            flat_sentence_path,
            flat_word_path,
            flat_explanation_path
        ])

    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(out)
    print(f"✅ Anki deck created: {out}")


def createCardPath(path, s):
	newpath = f"{path}/{s}"
	print(newpath)
	if not os.path.exists(newpath):
		os.makedirs(newpath)
		print(newpath)
	return newpath

def translate(path, pair):
	sentence = pair[0]
	word = pair[1]
	speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
	speech_config.speech_synthesis_voice_name = selectVoice()

	card_path = createCardPath(path, sentence)

	output_path_sentence = card_path + "/sentence.mp3"
	audio_output = speechsdk.audio.AudioOutputConfig(filename= output_path_sentence)
	synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)
	result_sentence = synthesizer.speak_text_async(sentence).get()
	if result_sentence.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
	    print(f"Saved: {output_path_sentence}")
	else:
	    print(f"Error: {result_sentence.reason}")

	output_path_word = card_path + "/word.mp3"
	audio_output = speechsdk.audio.AudioOutputConfig(filename= output_path_word)
	synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)
	result_word = synthesizer.speak_text_async(word).get()
	if result_word.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
	    print(f"Saved: {output_path_word}")
	else:
	    print(f"Error: {result_word.reason}")

	gpt_client = gpt.setup()
	text = gpt.get_definition(gpt_client, word, sentence)
	generateEnglishAudio(card_path, text)

def generateEnglishAudio(path, text):
	speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
	speech_config.speech_synthesis_voice_name = "en-US-AndrewNeural"

	output_path_explanation = path + "/explanation.mp3"
	audio_output = speechsdk.audio.AudioOutputConfig(filename= output_path_explanation)
	synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)
	result = synthesizer.speak_text_async(text).get()
	if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
	    print(f"Saved: {output_path_explanation}")
	else:
	    print(f"Error: {result.reason}")

def selectVoice():
	voices = [
	    "zh-CN-XiaoxiaoNeural",
	    "zh-CN-YunxiNeural",
	    "zh-CN-XiaochenNeural",
	    "zh-CN-XiaomengNeural",
	    "zh-CN-XiaomoNeural",
	    "zh-CN-XiaoqiuNeural",
	    "zh-CN-XiaoruiNeural",
	    "zh-CN-XiaoshuangNeural",
	    "zh-CN-XiaoxuanNeural",
	    "zh-CN-XiaoyanNeural",
	    "zh-CN-YunzeNeural",
	]
	return random.choice(voices)

def read(input):
	with open(input) as file:
		lines = [line.strip() for line in file if line.strip()]
		pairs = list(zip(lines[::2], lines[1::2]))
	return pairs

def writeFile(pairs, path):
	if not os.path.exists(path):
		os.makedirs(path)
	with open(path + '/input.txt', "a") as f:
		for p in pairs:
			f.write(p[0] + "\n")
			f.write(p[1] + "\n")

def run():
	pairs = read("input.txt")
	path = createOutputPath()
	print(path)
	writeFile(pairs, path)
	for p in pairs:
		translate(path, p)
	today = str(date.today())
	createDeck(path, f"{path}/deck-{today}.apkg")

run()

