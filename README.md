Exit with Esc, then run:

aplay -D plughw:2,0 /usr/share/sounds/alsa/Front_Center.wav

Then run:

speaker-test -D plughw:2,0 -t wav

Then run:

espeak --stdout "hello" | aplay -D plughw:2,0


Before running, test these in order

python3 -c "from picrawler import Picrawler; print('ok')"

espeak "hello"

cd ~/picrawler/examples

sudo python3 move.py

Then run your file: sudo python3 corner_game.py
