"""Welcome to the Irisya libs file.
This project and this file is totally open-source and subject to the GPL-3.0 license.
You can use these libraries for your projects but please credit Irisya.
You can also fork the whole project on GitHub to better support us.
Here is a quick documentation of the functions available in the library:
  - ask_gpt(messages, api_key, model="gpt-3.5-turbo)
    > Arguments:
       messages: list of messages in format: [{"role": "user", "content": "your message"}]
    > api_key: your API key for ChatGPT
    > model: the language model used in your request.
   > Allows you to send a request to ChatGPT and receive its response.
  - hear()
   > Arguments: none
   > Listen to what comes into the microphone, and send it back.
- process_request(): Function used in the code, so we won't give any description, it's up to you :)"""

import openai
import speech_recognition as sr
from playsound import playsound
from gtts import gTTS

def ask_gpt(messages, api_key, model="gpt-3.5-turbo"):    
    openai.api_key = api_key

    completion = openai.ChatCompletion.create(
        model=model, 
        messages=messages
    )
    result = completion['choices'][0]['message']['content']
    return result

def hear(lang):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language=lang)
        return text.lower()
    except sr.UnknownValueError:
        print('Impossible to understand.')

def process_request(request):
    try:
        request_processed = request.split('#')
        return request_processed[1]
    except:
        return False

def check_triggers(string, triggers):
    for trigger in triggers:
        if trigger in string:
            return True
    return False

def say_audio(text, language, slowly):
    audio = gTTS(text=text, lang=language, slow=slowly)
    audio.save("audio/audio.mp3")
    playsound('audio/audio.mp3')