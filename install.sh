echo "Installation de Willow. "
echo "Nous allons commencer l'installation".

sudo apt-get install portaudio19-dev python3 python3-pip
pip3 install -r requirements.txt

echo "Tout est terminé. S'il y a une erreur, vous pouvez nous la soumettre sur Github. "
python3 app.py
