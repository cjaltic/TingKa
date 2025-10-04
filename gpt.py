import openai
from openai import OpenAI

def setup():
	client = OpenAI(api_key="")
	return client

def get_definition(client, word, sentence):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": (
                "I will give you a Chinese text and a word from that text."
                "Explain what the word means in English (not the sentence, the word)."
                "Don't just give an English translation; actually explain what the word means"
                " in a similar manner to how the word would be explained in a Chinese-to-Chinese"
                " dictionary for native Chinese speakers, but in English.  Avoid using direct "
                "English equivalents of the word.  Explain 100 percent in English, without using any"
                " Chinese.  If there are multiple meanings, only explain the 'core meaning' of"
                " the word (not just what the word means in this particular sentence)"
                "  Since the result will be fed directly to a text-to-speech program, so don't"
                " repeat the word itself, Do not say the word.  Do not say 'means', 'refers to' or "
                "any intro like 'the word is...'and skip introductory comments like 'I will explain X' "
                "Just start explaining straight away.  Explain the entire thing in one sentence."
                "  Try to make the explanation as intuitive as possible, using plain language.  "
                "Keep the explanation short (around 15 words max, but less if that isn't needed)"
            )},
            {"role": "user", "content": f"{sentence}, {word}"}
        ]
    )
    return response.choices[0].message.content

# client = setup()
# x = get_definition(client, "培养", "学校应该从小培养学生的独立思考能力。")
# print(x)






