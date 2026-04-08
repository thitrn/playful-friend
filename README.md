✅ What you need to do on your Mac
1. Connect to the Raspberry Pi via SSH

Open Terminal on your Mac:

ssh pi@<raspberry-pi-ip>

Example:

ssh pi@192.168.1.45

👉 If you don’t know the IP:

arp -a

or check your router / ask your prof (since they said routers are being set up)

2. Once connected → NOW you’re “inside” the Pi

You’ll see something like:

pi@raspberrypi:~ $

👉 From here, run ALL the install commands I gave you earlier
(This is the important part — you're no longer on your Mac)

3. Install modules (run on Pi, not Mac)
sudo apt update
sudo apt upgrade
git clone -b v2.0 https://github.com/sunfounder/robot-hat.git --depth 1
cd robot-hat
sudo python3 install.py
git clone https://github.com/sunfounder/vilib.git --depth 1
cd vilib
sudo python3 install.py
git clone https://github.com/sunfounder/picrawler.git --depth 1
cd picrawler
sudo python3 setup.py install
4. Run your code FROM your Mac (but on Pi)

You can:

write code on Mac (VS Code)
then upload OR directly SSH and run

Run:

python3 your_file.py

Then run your file: sudo python3 corner_game.py


sudo python3 green_game.py
