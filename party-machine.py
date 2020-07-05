# https://pypi.org/project/PyGetWindow/
import pygetwindow as gw

# https://github.com/ponty/pyscreenshot/
import pyscreenshot as ImageGrab

# https://pypi.org/project/PyScreeze/
import pyscreeze

import os
import serial
import yaml
import time

from PIL import Image

import pytesseract

config_file = "config.yaml"


def check_for_enemy():
    # marker_location = pyscreeze.locateCenterOnScreen(
    #     "img/enemy/enemy_top.png", grayscale=True
    # )
    enemy_name = get_enemy_name()

    if enemy_name == "":
        # print("Enemy not detected!")
        return False
    else:
        return True


def get_enemy_name():
    enemyScreen = ImageGrab.grab(bbox=(630, 30, 890, 48))
    enemyScreen.save("img_out/enemy_name.png")
    im = Image.open("img_out/enemy_name.png")
    # im = Image.open(enemyScreen)
    return pytesseract.image_to_string(im)


if os.path.exists(config_file) is False:
    print(config_file + " Not found!")
    quit()

with open(config_file, "r") as file:
    config_list = yaml.full_load(file)

arduino_port = config_list["port"]
arduino_baud = config_list["baud"]

arduinoSerial = serial.Serial(arduino_port, arduino_baud)

fiestaWindow = gw.getWindowsWithTitle("FiestaOnline")[0]
fiestaWindow.restore()
fiestaWindow.moveTo(0, 0)
fiestaWindow.activate()

time.sleep(2)

# For troubleshooting
# fiestaScreen = ImageGrab.grab(bbox=(0, 0, fiestaWindow.width, fiestaWindow.height))
# fiestaScreen.save("img_out/game_window.png")


while 1:
    arduinoSerial.write(b"q")
    time.sleep(1)

    if check_for_enemy() == True:
        while check_for_enemy():
            arduinoSerial.write(b"r")
            time.sleep(1)
        arduinoSerial.write(b"u")
        time.sleep(1)
        arduinoSerial.write(b"u")
        time.sleep(1)

        arduinoSerial.write(b"i")
        time.sleep(4)
        arduinoSerial.write(b"i")
