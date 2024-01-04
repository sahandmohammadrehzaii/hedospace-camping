# in the name of GOD

import cx_Freeze
import os
import sys

os.environ['TCL_LIBRARY'] = "C:\\Users\\tmstani23\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\tmstani23\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tk8.6"

executables = [cx_Freeze.Executable("main.py")]
excludes = ['Tkinter']
files = ['img/manBlue_gun.png', 'img/manBlue_machinegun.png', 'img/manBlue_shotgun.png', 'img/bullet.png', 'img/zombie1_hold.png', 'img/whitePuff15.png', 
    'img/whitePuff16.png', 'img/whitePuff17.png', 'img/whitePuff18.png', 'img/splat red.png', "img/light_350_med.png", 'img/health_pack.png', 
    'img/obj_shotgun.png', 'img/weapon_machine.png','img/weapon_gun.png', 'img/tileGreen_39.png', 'img/spritesheet_tiles.png', 'song/espionage.ogg', 
    'song/8.wav', 'song/9.wav', 'song/10.wav', 'song/11.wav', 'song/brains2.wav', 'song/brains3.wav', 'song/zombie-roar-1.wav', 'song/zombie-roar-2.wav', 
    'song/zombie-roar-3.wav', 'song/zombie-roar-5.wav', 'song/zombie-roar-6.wav', 'song/zombie-roar-7.wav', 'song/splat-15.wav', 'song/gun_silenced.wav', 
    'song/pistol.wav', 'song/shotgun.wav', 'song/level_start.wav', 'song/health_pack.wav', 'song/gun_pickup.wav', "tmx/level1.tmx", "tmx/l2.tmx", "tmx/level3.tmx", 
    'font/Shabnam.woff', 'font/Shabnam.woff', "attributions.txt", "img/icon.png"]
includes = ["settings", "sprites", "tilemap"]
cx_Freeze.setup(
    name = "hedospace",
    options = {"build_exe": {"packages": ["pygame", "os", "sys", "pytmx","pytweening", "itertools"], 'excludes': excludes, 'includes': includes, "include_files": files}},
    description ="hedospace",
    executables = executables
)

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)