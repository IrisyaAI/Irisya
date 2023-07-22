import sys
import os
import librarys.libs as libs
import config.libs as config_lib
import time
import platform
from playsound import playsound
from gtts import gTTS

config = config_lib.Config('./config/config.json', autocreate=True)
active_profil_name = config.get_config()['active_profil']
active_profil = config.get_config_by_profil(active_profil_name)

libs.say_audio("Welcome to Irisya. The active profil is "+active_profil_name, active_profil['language'], active_profil['slowly'])

libs.say_audio("I am ready to help you. Say 'ok Irisia' to talk with me.", active_profil['language'], active_profil['slowly'])

last_request = 0

while True:
    config.reload_config()
    try:
        user_said = libs.hear(lang=active_profil['language'])
        if libs.check_triggers(user_said.upper(), active_profil['triggers']):
            # Remove "ok willo" from the request
            prompt = user_said.split("ok willow")[-1].strip()

            history = [{"role": "user", "content": active_profil['messages'][platform.system()].format(request=prompt)}]

            # Blip sound
            playsound('audio/blip.mp3')
            

            print('[LOG] Sending to ChatGPT... ')
            # Get the ChatGPT response.
            result = libs.ask_gpt(history, active_profil['api_key'])

            print('[LOG] Result: '+result)
            if libs.process_request(result) == "_":
                print('[LOG] Starting a process... ({process})'.format(process=result.split('#')[-1]))
                os.system(result.split('#')[-1])
            elif libs.process_request(result) == "!":
                config['triggers'] = config_lib.create_trigger("./config", result.split('#')[-1])
            else:
                # Say the response
                libs.say_audio(result, active_profil['language'], active_profil['slowly'])


                # End bilp
                playsound('audio/blip.mp3')

                # Init the last request.
                last_request = time.time()
        
                history.append({"role": "assistant", "content": result})

            last_request = time.time()


        elif time.time() - last_request <= 30:
            prompt = user_said

            # Add request to history
            history.append({"role": "user", "content": prompt})
            
            # Blip sound
            playsound('audio/blip.mp3')

            # Get the ChatGPT response.
            result = libs.ask_gpt(history, active_profil['api_key'])

            if result == "":
                print('[LOG] The user asked to be quiet. Ignore the instruction.')
            else:
                if libs.process_request(result) == "_":
                    libs.say_audio(result, active_profil['language'], active_profil['slowly'])
                    os.system(result.split('#')[-1])
                else:
                    # Say the response.
                    libs.say_audio(result, active_profil['language'], active_profil['slowly'])

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
