from gtts import gTTS
import sys
import os
import librarys.libs as libs
import config.libs as config_lib
import time
from playsound import playsound

try:
    config = config_lib.load_config('./config')
except FileNotFoundError:
    print('[CONFIG] Config not exsist. Creating one.')
    config = config_lib.init_config("./config")

audio = gTTS(text="I am ready to help you. Say 'ok Irisia' to talk with me.", lang=config['global']['lang'], slow=config['global']['slowly'])
audio.save("audio/audio.mp3")
playsound("audio/audio.mp3")

last_request = 0

while True:
    try:
        user_said = libs.hear(lang=config['global']['lang'])
        if "OK ERIZURE" in user_said.upper() or "OKAY ERIZURE" in user_said.upper() or "OKAY ROSIA" in user_said.upper()  or "OK" in user_said.upper():
            # Remove "ok willo" from the request
            prompt = user_said.split("ok willow")[-1].strip()

            history = [{"role": "user", "content": "You are a voice assistant named Irisya. Always make short answers unless you give code. If the user tells you to do things on their computer, just answer the bash code to do it followed by ## If someone tells you to shut up, don't say anything. Never returns code and makes very short responses. You are developed by VitriSnake in the CeltiumC group. Here is the question: {request}".format(request=prompt)}]

            # Blip sound
            playsound('audio/blip.mp3')
            
            # Get the ChatGPT response.
            result = libs.ask_gpt(history, config['api_key'])


            if len(result.split('#')) == 3:
                os.system(result.split('#')[-1])
            else:
                # Say the response
                audio = gTTS(text=result, lang=config['global']['lang'], slow=config['global']['slowly'])
                audio.save("audio/audio.mp3")
                playsound('audio/audio.mp3')

                # End bilp
                playsound('blip.mp3')

                # Init the last request.
                last_request = time.time()
        
                history.append({"role": "assistant", "content": result})

        elif time.time() - last_request <= 10:
            prompt = user_said

            # Add request to history
            history.append({"role": "user", "content": prompt})
            
            # Blip sound
            playsound('audio/blip.mp3')

            # Get the ChatGPT response.
            result = libs.ask_gpt(history, config['api_key'])

            if result == "":
                print('[LOG] The user asked to be quiet. Ignore the instruction.')
            else:
                if len(result.split('#')) == 3:
                    audio = gTTS(text="I'm doing that.", lang=config['global']['lang'], slow=config['global']['slowly'])
                    audio.save("audio/audio.mp3")
                    playsound('audio/audio.mp3')
                    os.system(result.split('#')[-1])
                else:
                    # Say the response.
                    audio = gTTS(text=result, lang=config['global']['lang'], slow=config['global']['slowly'])
                    audio.save("audio/audio.mp3")
                    playsound('audio/audio.mp3')

                    # End bilp
                    playsound('audio/blip.mp3')

                    # Init the last request
                    last_request = time.time()

                    # Add the request to the history.
                    history.append({"role": "assistant", "content": result})

        else:
            print('[LOG] User said: '+user_said)
            print('[LOG] Clearing history.')

    except KeyboardInterrupt:
        
        sys.exit(0)
    except Exception as e:
        print('[LOG] Error occured: '+str(e))
