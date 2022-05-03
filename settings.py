import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
ORANGE = (255, 136, 0)
CYAN = (0, 255, 255)


# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)

# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 50,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1,
                     'ammo': 9}
WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 50,
                      'bullet_size': 'sm',
                      'bullet_count': 12,
                      'ammo': 10}
WEAPONS['sniper'] = {'bullet_speed': 800,
                      'bullet_lifetime': 1000,
                      'rate': 2000,
                      'kickback': 600,
                      'spread': 0,
                      'damage': 99,
                      'bullet_size': 'lg',
                      'bullet_count': 1,
                      'ammo': 5}

# Mob settings
MOBS = {}
MOBS["zombie"] = {"mob_img": "zombie1_hold.png",
                  "mob_speed": [150, 100, 75, 125],
                  "mob_hit_rect": pg.Rect(0, 0, 30, 30),
                  "mob_health": 100,
                  "mob_damage": 10,
                  "mob_knockback": 20,
                  "avoid_radius":20,
                  "detect_radius":400,
                  "coin_reward":1}

MOBS["zombie_strong"] = {"mob_img": "zombie_strong.png",
                  "mob_speed": [1000, 10],
                  "mob_hit_rect": pg.Rect(0, 0, 30, 30),
                  "mob_health": 1000,
                  "mob_damage": 800,
                  "mob_knockback": 200,
                  "avoid_radius":20,
                  "detect_radius":400,
                  "coin_reward": 2}



# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
SPLAT = 'whitePuff16 - Kopie.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
NIGHT_COLOR = (30, 30, 30)
LIGHT_RADUIS = (500, 500)
LIGHT_MASk = "light_350_soft.png"



# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Maps
#CURRENT_LEVEL = 0
MAPS = []
MAPS = ["lvl_tut.tmx", "home.tmx",
        "lvl1.tmx", "home.tmx",
        "lvl2.tmx", "home.tmx",
        "lvl3.tmx", "home.tmx",
        ]

# Items
ITEM_IMAGES = {'health': 'health_pack.png',
               "door": "door.png",
               "shotgun": "shotgun.png",
               "sniper": "sniper.png"}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

# Sounds
BG_MUSIC = 'rubedo.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'sniper': ['shotgun.wav']
                 }
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  "gun_pickup": "gun_pickup.wav"}