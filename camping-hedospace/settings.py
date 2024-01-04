# in the name of GOD

import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 468  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Zombie Crawl"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'img/tileGreen_39.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_IMG = ['img/manBlue_gun.png', 'img/manBlue_shotgun.png', 'img/manBlue_machinegun.png']
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)


#Weapon settings
BULLET_IMG = 'img/bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 600,
                     'bullet_lifetime': 450,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 20,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 400,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 6,
                      'bullet_size': 'sm',
                      'bullet_count': 12}
WEAPONS['machinegun'] = {'bullet_speed': 800,
                      'bullet_lifetime': 500,
                      'rate': 115,
                      'kickback': 150,
                      'spread': 10,
                      'damage': 7,
                      'bullet_size': 'sm',
                      'bullet_count': 1}

# Mob settings
MOB_IMG = 'img/zombie1_hold.png'
MOB_SPEEDS = [155, 105, 115, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_HIT_RATE = 700
MOB_DAMAGE = 10
MOB_DAMAGE_MED = 20
MOB_DAMAGE_HARD = 30
MOB_KNOCKBACK = 20
AVOID_RADIUS = 75
DETECT_RADIUS = 375

# Effects
MUZZLE_FLASHES = ['img/whitePuff15.png', 'img/whitePuff16.png', 'img/whitePuff17.png',
                  'img/whitePuff18.png']
SPLAT = 'img/splat red.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (600, 600)
LIGHT_MASK = "img/light_350_med.png"

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'img/health_pack.png',
               'shotgun': 'img/obj_shotgun.png',
               'machinegun': 'img/weapon_machine.png',
               'pistol': 'img/weapon_gun.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

# Sounds
BG_MUSIC = 'song/espionage.ogg'
PLAYER_HIT_SOUNDS = ['song/8.wav', 'song/9.wav', 'song/10.wav', 'song/11.wav']
ZOMBIE_MOAN_SOUNDS = ['song/brains2.wav', 'song/brains3.wav', 'song/zombie-roar-1.wav', 'song/zombie-roar-2.wav',
                      'song/zombie-roar-3.wav', 'song/zombie-roar-5.wav', 'song/zombie-roar-6.wav', 'song/zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['song/splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['song/pistol.wav'],
                 'machinegun': ['song/gun_silenced.wav'],
                 'shotgun': ['song/shotgun.wav']}
EFFECTS_SOUNDS = {'level_start': 'song/level_start.wav',
                  'health_up': 'song/health_pack.wav',
                  'gun_pickup': 'song/gun_pickup.wav'}
