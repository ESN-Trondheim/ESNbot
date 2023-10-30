cd /opt/ESNbot
# "^C" is ctrl+c
# "^M" is enter, necessary so that commands will run instead of just writing to console.
screen -S esnbot stuff "^C" #ctrl+c to stop python script
screen -S esnbot stuff "deactivate^M"
screen -XS esnbot quit
git pull
screen -dmS esnbot
screen -S esnbot -X stuff ". env/bin/activate^M"
screen -S esnbot -X stuff "pip install -r requirements.txt^M"
screen -S esnbot -X stuff "python3 esnbot/main.py^M"
screen -S esnbot -X multiuser on