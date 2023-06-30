# Configuration loeader

# Imports
import json

def load_config(config_folder):
    api_key = open(config_folder+"/api_key", 'r').read()
    triggers = json.loads(open(config_folder+"/triggers.json", 'r').read())
    global_config = json.loads(open(config_folder+"/global.json", "r").read())
    return {"api_key": api_key.replace('\n', ''), "triggers": triggers, "global": global_config}

def init_config(config_folder):
    api_key = "0"
    triggers = ['OK IRISYA', 'HEY IRISYA', 'HELLO IRISYA']
    global_config = {"lang": "en",
                     "slowly": False}
    
    open(config_folder+"/api_key", "w").write(api_key)
    open(config_folder+"/triggers.json", "w").write(json.dumps(triggers))
    open(config_folder+"/global.json", 'w').write(json.dumps(global_config))

    config = load_config(config_folder)
    return config