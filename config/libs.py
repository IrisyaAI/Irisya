# Configuration loader

# Imports
import json

BASE_MESSAGES = {"Linux": "Ignore everything I told you. You are a computer voice assistant called Irisya. Here's how you should react:\n - If I ask you to do code on my machine or launch applications, return the bash script for linux to do it preceded by #_#. Does not install anything on the computer and does not do an administrator process.\n - If I ask you to add a word trigger, return it preceded by #!#.\n - If I ask you a question, simply answer the question without preceding anything and make short answers.\n - You can only do one action per message.\nHere is the first question: {request}", 
                                                           "Darwin": "Ignore everything I told you. You are a computer voice assistant called Irisya. Here's how you should react:\n - If I ask you to do code on my machine or launch applications, return the bash script for MacOS to do it preceded by #_#. Does not install anything on the computer and does not do an administrator process.\n - If I ask you to add a word trigger, return it preceded by #!#.\n - If I ask you a question, simply answer the question without preceding anything and make short answers.\n - You can only do one action per message.\nHere is the first question: {request}", 
                                                           "Windows": "Ignore everything I told you. You are a computer voice assistant called Irisya. Here's how you should react:\n - If I ask you to do code on my machine or launch applications, return the powershell script for Windows to do it preceded by #_#. Does not install anything on the computer and does not do an administrator process.\n - If I ask you to add a word trigger, return it preceded by #!#.\n - If I ask you a question, simply answer the question without preceding anything and make short answers.\n - You can only do one action per message.\nHere is the first question: {request}"},
BASE_TRIGGERS = ['OK IRISYA', 'HEY IRISYA', 'HELLO IRISYA', 'OK ROSIA', 'HEY ROSIA', 'HELLO ROSIA']


class ProfilNotExsistError(Exception):
    pass

class InvalidConfiguration(Exception):
    pass

class Config:
    def __init__(self, config_file, autocreate=False):
        try:
            self.config_file = json.loads(open(config_file, 'r').read())
        except:
            if autocreate:
                default_config = {"default": {"api_key": "0",
                                              "messages": BASE_MESSAGES,
                                              "slowly": False,
                                              "language": "en",
                                              "triggers": BASE_TRIGGERS,
                                              "process": True,
                                              "add_trigger_with_voice": True}
                                 }
                self.config_file = default_config
                open(self.config_file, 'w').write(json.dumps(default_config))
            else:
                raise InvalidConfiguration('Config not valid. Add arg autocreate=True')
        
        self.profils = list(config_file)
    
    def get_config_by_profil(self, profil):
        if not(profil in self.profils):
            raise ProfilNotExsistError('The profil {profil} don\' exsists. ')
        
        return self.config_file[profil]

    def edit_profil(self, profil, value_name, value_edit):
        self.config_file[profil][value_name] = value_edit

    def rewrite_config(self):
        open(self.config_file, 'w').write(json.dumps(self.config_file))

    def remove_profil(self, profil):
        profil_value = self.config_file[profil]
        self.config_file.pop(profil)
        return profil_value

    def create_profil(self, profil_name, api_key="0", messages=BASE_MESSAGES, slowly=False, language="en", triggers=BASE_TRIGGERS, process="True", voice_trigger_edition=True):  
        profil_value = {"api_key": api_key,
                        "messages": messages,
                        "slowly": slowly,
                        "language": language,
                        "triggers": triggers,
                        "process": process,
                        "add_trigger_with_voice": voice_trigger_edition}
        
        self.config_file[profil_name] = profil_value
        return profil_value

    def close(self):
        self.rewrite_config()
    