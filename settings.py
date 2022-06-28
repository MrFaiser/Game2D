import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (40, 40, 40)
GREY = (100, 100, 100)
MEDIUM_GREY = (130, 130, 120)
LIGHT_GREY = (180, 180, 180)
GREEN = (0, 255, 0)
LIGHT_GREEN = (150, 255, 150)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
DARK_RED = (100, 0, 0)
LIGHT_RED = (255, 100, 100)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (80, 80, 255)
BROWN = (106, 55, 5)
ORANGE = (255, 136, 0)
DARK_ORANGE = (155, 86, 0)
LIGHT_ORANGE = (255, 166, 50)
CYAN = (0, 255, 255)
PINK = (255, 105, 180)
PURPLE = (50, 0, 50)
LIGHT_PURPLE = (200, 0, 200)

# game settings
#True False
size = 2
if size == 1:
    WIDTH = 1920  # 16 * 64 or 32 * 32 or 64 * 16
    HEIGHT = 1080  # 16 * 48 or 32 * 24 or 64 * 12
elif size == 2:
    WIDTH = 1000  # 16 * 64 or 32 * 32 or 64 * 16
    HEIGHT = 700  # 16 * 48 or 32 * 24 or 64 * 12
elif size == 3:
    WIDTH = 500  # 16 * 64 or 32 * 32 or 64 * 16
    HEIGHT = 500  # 16 * 48 or 32 * 24 or 64 * 12

FPS = 60
TITLE = "Titelfenster lol"
BGCOLOR = BROWN

TILESIZE = 1000
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
#PLAYER_HEALTH = 20
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 300
PLAYER_IMG = 'mob/player.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 40, 40)
BARREL_OFFSET = vec(30, 10)

# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 600,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 7,
                     'bullet_size': 'lg',
                     'bullet_count': 1,
                     'ammo': 24}
WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12,
                      'ammo': 10}
WEAPONS['sniper'] = {'bullet_speed': 800,
                      'bullet_lifetime': 1000,
                      'rate': 2000,
                      'kickback': 600,
                      'spread': 0,
                      'damage': 55,
                      'bullet_size': 'lg',
                      'bullet_count': 1,
                      'ammo': 5}
WEAPONS['rifle'] = {'bullet_speed': 600,
                      'bullet_lifetime': 800,
                      'rate': 150,
                      'kickback': 300,
                      'spread': 0,
                      'damage': 15,
                      'bullet_size': 'lg',
                      'bullet_count': 1,
                      'ammo': 35}
WEAPONS['laser'] = {'bullet_speed': 1000,
                      'bullet_lifetime': 20000,
                      'rate': 5,
                      'kickback': 0,
                      'spread': 1,
                      'damage': 200,
                      'bullet_size': 'sm',
                      'bullet_count': 2,
                      'ammo': 1000}

# Mob settings
MOBS = {}
MOBS["zombie"] = {"mob_img": "mob/zombie1_hold.png",
                  "mob_speed": [150, 100, 75, 125],
                  "mob_hit_rect": pg.Rect(0, 0, 30, 30),
                  "mob_health": 100,
                  "mob_damage": 8,
                  "mob_knockback": 20,
                  "avoid_radius":20,
                  "detect_radius":400,
                  "xp_reward":10,
                  "coin_reward":1}
MOBS["zombie_strong"] = {"mob_img": "mob/zombie_strong.png",
                  "mob_speed": [200, 10],
                  "mob_hit_rect": pg.Rect(0, 0, 30, 30),
                  "mob_health": 400,
                  "mob_damage": 20,
                  "mob_knockback": 40,
                  "avoid_radius":20,
                  "detect_radius":200,
                  "xp_reward":23.8,
                  "coin_reward": 2}

NPC_INTERACT_RANGE = 100
NPCS = {}
NPCS["npc"] = {"npc_img": "mob/npc.png",
                  "npc_speed": [0],
                  "npc_hit_rect": pg.Rect(0, 0, 30, 30),
                  "npc_health": 100,
                  "npc_damage": 0,
                  "npc_knockback": 20,
                  "avoid_radius":20,
                  "detect_radius":400,
                  "xp_reward":10,
                  "coin_reward":1}
NPCS["npc_gun"] = {"npc_img": "mob/npc_gun.png",
                  "npc_speed": [0],
                  "npc_hit_rect": pg.Rect(0, 0, 30, 30),
                  "npc_health": 400,
                  "npc_damage": 20,
                  "npc_knockback": 40,
                  "avoid_radius":20,
                  "detect_radius":200,
                  "xp_reward":23.8,
                  "coin_reward": 2}
NPCS["npc_quest_boy"] = {"npc_img": "mob/npc_quest_boy.png",
                  "npc_speed": [0],
                  "npc_hit_rect": pg.Rect(0, 0, 30, 30),
                  "npc_health": 400,
                  "npc_damage": 20,
                  "npc_knockback": 40,
                  "avoid_radius":20,
                  "detect_radius":200,
                  "xp_reward":23.8,
                  "coin_reward": 2}


# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
SPLAT = 'blood_splat.png'
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
NPC_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1


# Items
ITEM_LIST = []
ITEM_LIST= ['health',
            "max_health_up", "health_pack_up", "auto_reg_up", "auto_reg_amount", "show_player_hp",
            "pistol", "shotgun", "sniper", "rifle"]
ITEM_IMAGES = {'health': 'item/health_pack.png',

               "max_health_up": "item/max_health_up.png",
               "health_pack_up": "item/health_pack_up.png",
               "auto_reg_up": "item/auto_reg_up.png",
               "auto_reg_amount": "item/auto_reg_amount.png",
               "show_player_hp": "item/show_player_hp.png",

               "pistol": "item/pistol.png",
               "shotgun": "item/shotgun.png",
               "sniper": "item/sniper.png",
               "rifle": "item/rifle.png",
               "laser": "item/laser.png"}

# Maps
#CURRENT_LEVEL = 0
MAPS = []
MAPS = ["lvl_tut.tmx",
        "lvl1.tmx",
        "lvl2.tmx",
        "lvl3.tmx",
        "lvl4.tmx",
        "lvl5.tmx",
        "lvl6.tmx",
        "lvl7.tmx",
        "lvl8.tmx",
        "lvl9.tmx",
        "lvl10.tmx",
        "lvl11.tmx",
        ]

# Levels
LVL_LIST = []
LVL_LIST= ["door_auto",
           "doorlvl1",
           "doorlvl2",
           "doorlvl3",
           "doorlvl4",
           "doorlvl5",
           "doorlvl6",
           "doorlvl7",
           "doorlvl8",
           "doorlvl9",
           "doorlvl10",
           "doorlvl11"]
LVL_IMAGES = {'door_auto': 'doors/door_enter.png',
               "doorlvl1": "doors/doorlvl1.png",
               "doorlvl2": "doors/doorlvl2.png",
               "doorlvl3": "doors/doorlvl3.png",
               "doorlvl4": "doors/doorlvl4.png",
               "doorlvl5": "doors/doorlvl5.png",
               "doorlvl6": "doors/doorlvl6.png",
               "doorlvl7": "doors/doorlvl7.png",
               "doorlvl8": "doors/doorlvl8.png",
               "doorlvl9": "doors/doorlvl9.png",
               "doorlvl10": "doors/doorlvl10.png",
               "doorlvl11": "doors/doorlvl10.png"}



#HEALTH_PACK_AMOUNT = 20
ITEM_RESPAWN_TIME = 3*60
BOB_RANGE = 20
BOB_SPEED = 0.6

# Sounds
BG_MUSIC = 'calm2.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
PLAYER_STEP_SOUNDS = ['step1.ogg', 'step2.ogg', 'step3.ogg', 'step4.ogg', 'step5.ogg', 'step6.ogg']

ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']

ZOMBIE_HIT_SOUNDS = ['splat-15.wav']

WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'sniper': ['shotgun.wav'],
                 'rifle': ['pistol.wav'],
                 'laser': ['pistol.wav']
                 }

EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  "gun_pickup": "gun_pickup.wav"}

# TEXT
START_TEXT = "START GAME"
OPTION_TEXT = "OPTION"
QUIT_TEXT = "LEAVE"