screen -XS esnbot quit
git pull
screen -dmS esnbot python3 esnbot/main.py
screen -S esnbot -X multiuser on