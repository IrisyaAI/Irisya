# Configuration loader

# Imports
import json
import ipdb

BASE_MESSAGES = {"Linux": "Ignore everything I told you. You are a computer voice assistant called Irisya. Here's how you should react:\n - If I ask you to do code on my machine or launch applications, return the bash script for linux to do it preceded by #_#. Does not install anything on the computer and does not do an administrator process.\n - If I ask you to add a word trigger, return it preceded by #!#.\n - If I ask you a question, simply answer the question without preceding anything and make short answers.\n - You can only do one action per message.\nHere is the first question: {request}", 
                                                           "Darwin": "Ignore everything I told you. You are a computer voice assistant called Irisya. Here's how you should react:\n - If I ask you to do code on my machine or launch applications, return the bash script for MacOS to do it preceded by #_#. Does not install anything on the computer and does not do an administrator process.\n - If I ask you to add a word trigger, return it preceded by #!#.\n - If I ask you a question, simply answer the question without preceding anything and make short answers.\n - You can only do one action per message.\nHere is the first question: {request}", 
                                                           "Windows": "Ignore everything I told you. You are a computer voice assistant called Irisya. Here's how you should react:\n - If I ask you to do code on my machine or launch applications, return the powershell script for Windows to do it preceded by #_#. Does not install anything on the computer and does not do an administrator process.\n - If I ask you to add a word trigger, return it preceded by #!#.\n - If I ask you a question, simply answer the question without preceding anything and make short answers.\n - You can only do one action per message.\nHere is the first question: {request}"},
BASE_TRIGGERS = ['OK IRISYA', 'HEY IRISYA', 'HELLO IRISYA', 'OK ROSIA', 'HEY ROSIA', 'HELLO ROSIA']


class ProfilNotFoundError(Exception):
    pass

class InvalidConfiguration(Exception):
    pass

class Config:
    def __init__(self, config_file, autocreate=False):
        self.config_file_name = config_file
        
        try:
            self.config_file = json.loads(open(config_file, 'r').read())
        except FileNotFoundError:
            if autocreate == True:
                default_config = {"active_profil": "default", "profils": {"default": 
                                                                                    {"api_key": "0",
                                                                                     "messages": BASE_MESSAGES,
                                                                                     "slowly": False,
                                                                                     "language": "en",
                                                                                     "triggers": BASE_TRIGGERS,
                                                                                     "process": True,
                                                                                     "add_trigger_with_voice": True,
                                                                                     'description': "The default profil"}}}
                self.config_file = default_config
                open(self.config_file_name, 'w').write(json.dumps(default_config))
            else:
                raise InvalidConfiguration('Config not valid. Add arg autocreate=True')
        
        self.profils = list(self.config_file['profils'])
    
    def get_config(self):
        return self.config_file

    def get_config_by_profil(self, profil):
        if not(profil in self.profils):
            raise ProfilNotFoundError('The profil {profil} don\'t exsists. '.format(profil=profil))
        
        return self.config_file['profils'][profil]

    def edit_profil(self, profil, value_name, value_edit):
        self.config_file['profils'][profil][value_name] = value_edit

    def rewrite_config(self):
        open(self.config_file_name, 'w').write(json.dumps(self.config_file))

    def remove_profil(self, profil_name):
        self.config_file['profils'].pop(profil_name)
        
    def create_profil(self, profil_name, api_key="0", messages=BASE_MESSAGES, slowly=False, language="en", triggers=BASE_TRIGGERS, process="True", voice_trigger_edition=True, description="No description"):  
        profil_value =  {"api_key": api_key, "messages": messages, "slowly": slowly, "language": language, "triggers": triggers, "process": process, "add_trigger_with_voice": voice_trigger_edition, "description": description}
        
        self.config_file['profils'][profil_name] = profil_value
        return profil_value

    def close(self):
        self.rewrite_config()
        self = None
    
    def get_profil_list(self):
        return list(self.config_file['profils'])

    def get_profils_config(self):
        return self.config_file['profils']

    def edit_active_profil(self, profil):
        self.config_file['active_profil'] = profil

    def reload_config(self):
        self.config_file = json.loads(open(self.config_file_name, 'r').read())

