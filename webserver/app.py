import sys

# Import Flask
from flask import Flask, render_template, redirect, request

# Edit the path
sys.path.append('.')

# Import the configuration module
import config.libs

# Load the active config
config = config.libs.Config("./config/config.json", autocreate=True)

# Init flask application
app = Flask(__name__)

# Index route
@app.route('/')
def index():
    config.reload_config()
    return render_template('index.html', config=config.config_file)

# Profil edition
@app.route('/profil/<profil>/edit')
def profil_edition(profil):
    config.reload_config()
    config_profil = config.get_config_by_profil(profil)
    return render_template('edit.html', name=profil, config=config_profil)

@app.route('/profil/<profil>/edit/get', methods=['POST'])
def edit_profil_get(profil):
    api_key = request.form.get('api_key')
    message_linux = request.form.get('message_linux')
    message_windows = request.form.get('message_windows')
    message_darwin = request.form.get('message_darwin')
    desc = request.form.get('description')
    triggers = request.form.get('triggers').split(',')
    language = request.form.get('language')

    messages = {"Linux": message_linux,
                "Windows": message_windows,
                "Darwin": message_darwin}

    config.edit_profil(profil, "api_key", api_key)
    config.edit_profil(profil, "messages", messages)
    config.edit_profil(profil, "language", language)
    config.edit_profil(profil, "triggers", triggers)
    config.edit_profil(profil, "description", desc)

    config.rewrite_config()
    config.reload_config()
    return redirect('/')

# Profil creation
@app.route('/profil/create')
def profil_create():
    return render_template('create.html')

@app.route('/profil/create/get', methods=['POST'])
def create_profil_get():
    api_key = request.form.get('api_key')
    slowly = request.form.get('slowly')
    process = request.form.get('process')
    message_linux = request.form.get('message_linux')
    message_windows = request.form.get('message_windows')
    message_darwin = request.form.get('message_darwin')
    add_trigger_with_voice = request.form.get('add_triggers_with_voice')
    description = request.form.get('description')
    triggers = request.form.get('triggers').split(',')
    name = request.form.get('name')
    language = request.form.get('language')

    if add_trigger_with_voice == "on":
        add_trigger_with_voice = True
    else:
        add_trigger_with_voice = False

    if process == "on":
        process = True
    else:
        process = False

    if slowly == "on":
        slowly = True
    else:
        slowly = False

    messages = {"Linux": message_linux,
                "Windows": message_windows,
                "Darwin": message_darwin}

    config.create_profil(
        api_key=api_key,
        slowly=slowly,
        process=process,
        messages=messages,
        voice_trigger_edition=add_trigger_with_voice,
        description=description,
        profil_name=name,
        triggers=triggers,
        language=language)

    config.rewrite_config()
    config.reload_config()
    return redirect('/')

# Profil remove
@app.route('/profil//<profil>/remove')
def remove_profil(profil):
    config.remove_profil(profil)
    config.rewrite_config()
    return redirect('/')

@app.route('/profil//<profil>/enable')
def enable_profil(profil):
    config.edit_active_profil(profil)
    config.rewrite_config()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=53582, host="127.0.0.1")
