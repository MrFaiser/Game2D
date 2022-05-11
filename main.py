import json
import time
from pathlib import Path
from datetime import datetime
import pygame as pg
import sys
from random import choice, random
from os import path

import settings
import sprites
from file_manager import *
from settings import *
from sprites import *
from savefiles import *
from tilemap import *
# HUD functions


def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    if PLAYER_HEALTH <= 150:
        BAR_LENGTH = 120
    else:
        BAR_LENGTH = PLAYER_HEALTH * 0.8
    BAR_HEIGHT = 30
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct >= 0.8:
        col = GREEN
    elif pct >= 0.5:
        col = YELLOW
    elif pct >= 0.3:
        col = ORANGE
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_line(surf, x, y,pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct >= 0.8:
        col = BLUE
    elif pct >= 0.5:
        col = YELLOW
    elif pct >= 0.3:
        col = ORANGE
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        create_file()

        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        save_folder = path.join(game_folder, 'savefiles')
        self.safe_file = path.join(save_folder, "save.txt")
        self.map_folder = path.join(game_folder, 'maps')
        self.title_font = path.join(img_folder, 'MinecraftBold-nMK1.otf')
        self.hud_font = path.join(img_folder, 'MinecraftRegular-Bmg3.otf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 200))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))

        self.mob_img = {}
        self.mob_img["zombie"] = pg.image.load(path.join(img_folder, MOBS["zombie"]["mob_img"])).convert_alpha()
        self.mob_img["zombie_strong"] = pg.image.load(path.join(img_folder, MOBS["zombie_strong"]["mob_img"])).convert_alpha()

        #Player Stats Start
        self.coins = read_file("save","COINS")
        self.ammo = read_file("save", "pistol_ammo")
        self.compas_lvl = read_file("save", "compas_lvl")
        self.compas_all = read_file("save", "compas_all")
        self.current_level = read_file("save", "CURRENT_LEVEL")
        #Player Stats End



        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (32, 32))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        for item in LVL_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, LVL_IMAGES[item])).convert_alpha()

        #lighning effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = (pg.image.load(path.join(img_folder, LIGHT_MASk)).convert_alpha())
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADUIS)
        self.light_rect = self.light_mask.get_rect()
        # Sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        pg.mixer.music.set_volume(0.02)


        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.02)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.02)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.02)
            self.player_hit_sounds.append(s)
#            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.player_step_sounds = []
        for snd in PLAYER_STEP_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.02)
            self.player_step_sounds.append(s)
#            self.player_step_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.02)
            self.zombie_hit_sounds.append(s)
#            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))


    def new(self, level):
        # Write Save File
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.items = pg.sprite.Group()
        try:
#            self.map = TiledMap(path.join(self.map_folder, MAPS[read_file("save", "CURRENT_LEVEL")]))
            self.map = TiledMap(path.join(self.map_folder, level))
        except:
            self.map = TiledMap(path.join(self.map_folder, "home.tmx"))
            print("enter home")
            #write_file("save","CURRENT_LEVEL", self.current_level-1)

        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                self.mob = Mob(self, obj_center.x, obj_center.y, "zombie")
            if tile_object.name == 'zombie_strong':
                self.mob = Mob(self, obj_center.x, obj_center.y, "zombie_strong")
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in LVL_LIST:
                t = tile_object.name
                tt = t.replace("doorlvl", "")
                if tt == "door_auto":
                    Item(self, obj_center, tile_object.name)
                elif int(tt) <= self.current_level:
                    Item(self, obj_center, tile_object.name)
            if tile_object.name in ITEM_LIST:
                Item(self, obj_center, tile_object.name)


        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = False
        self.lvl_fin = False
        self.compas_is_used = False
        self.level_selectet = False
        self.effects_sounds['level_start'].play().set_volume(0.2)
        self.info_update()


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        time_start = time.time()
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
                #Start loop Item Respawn
                time_now = time.time()
                if (time_now - time_start) >= ITEM_RESPAWN_TIME:
                    time_start = time.time()
                    hits = self.items

                    for hit in hits:
                        for item in ITEM_LIST:
                            hit.kill()

                    for tile_object in self.map.tmxdata.objects:
                        obj_center = vec(tile_object.x + tile_object.width / 2,
                                         tile_object.y + tile_object.height / 2)
                        if tile_object.name in ITEM_LIST:
                            Item(self, obj_center, tile_object.name)
                        if tile_object.name in LVL_LIST:
                            t = tile_object.name
                            tt = t.replace("doorlvl", "")
                            if tt == "door_auto":
                                Item(self, obj_center, tile_object.name)
                            elif int(tt) <= self.current_level:
                                Item(self, obj_center, tile_object.name)
                    #Loop End Item Respawn
                # loop reg start
                if (time_now - time_start) >= ITEM_RESPAWN_TIME:
                    pass
                #loop reg end
            pg.display.flip()
            self.draw()
            if self.lvl_fin:
                self.lvl_completed()


    def quit(self):
        pg.quit()
        sys.exit()

    def info_update(self):
        self.ammo = read_file("save", self.player.weapon+"_ammo")
        self.coins = read_file("save", "COINS")
        print(time.time())

    def get_ammo(self):
        write_file("save", self.player.weapon + "_ammo",
        read_file("save", self.player.weapon + "_ammo") + WEAPONS[self.player.weapon]["ammo"])

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        #game over
        if len(self.mobs) == 0:
            mapname = Path(self.map.tmxdata.filename).stem
            if mapname != "home":
                self.lvl_fin = True
                # self.playing = False
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == "door_auto":
                hit.kill()
                self.home_completed()
            elif hit.type == "doorlvl1":
                if read_file("save", "CURRENT_LEVEL") >= 1:
                    hit.kill()
                    self.enter_level_from_home("lvl1.tmx")
            elif hit.type == "doorlvl2":
                if read_file("save", "CURRENT_LEVEL") >= 2:
                    hit.kill()
                    self.enter_level_from_home("lvl2.tmx")


            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == "pistol":
                hit.kill()
                self.effects_sounds["gun_pickup"].play()
                self.player.weapon = "pistol"
                self.get_ammo()
            if hit.type == "shotgun":
                hit.kill()
                self.effects_sounds["gun_pickup"].play()
                self.player.weapon = "shotgun"
                self.get_ammo()
            if hit.type == "sniper":
                hit.kill()
                self.effects_sounds["gun_pickup"].play()
                self.player.weapon = "sniper"
                self.get_ammo()
            if hit.type == "rifle":
                hit.kill()
                self.effects_sounds["gun_pickup"].play()
                self.player.weapon = "rifle"
                self.get_ammo()

            self.info_update()

        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        zombie_type = ""
        for hit in hits:
            hits = pg.sprite.groupcollide(self.mobs, self.players, False, False)
            for mob in hits:
                zombie_type = mob.type

            if random() < 0.4:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOBS[zombie_type]["mob_damage"]
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOBS[zombie_type]["mob_knockback"],0).rotate(-self.player.rot+180)
#
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)


    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)

                ###
                if sprite.type == "zombie" or sprite.type == "zombie_strong":
                    pg.draw.line(self.screen, ORANGE, self.camera.apply(self.player).center,
                                         self.camera.apply(sprite).center, 2)
                ###

        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        #USE ITEMS
        if self.compas_is_used:
            self.use_compas()
        #USE ITEMS


        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        #Fog
        if self.night:
            self.render_fog()

        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text("HP: {}".format(self.player.health) + " / {}".format(PLAYER_HEALTH), self.hud_font, 15, DARK_GREY, 15, 25, align="w")
        self.draw_text("Zombies: {}".format(len(self.mobs)), self.hud_font, 30, DARK_GREEN, 10, 55, align="w")
        self.draw_text("Coins: {}".format(self.coins), self.hud_font, 30, ORANGE, 10, 85, align="w")
        self.draw_text("Weapon: {}".format(self.player.weapon) + " x {}".format(self.ammo), self.hud_font, 30, DARK_GREY, 10, 115, align="w")
     #   self.draw_text("Ammo: {}".format(ammo) , self.hud_font, 30, DARKGREY, 10, 140, align="w")

        self.draw_text("FPS {:.2f}".format(self.clock.get_fps()), self.hud_font, 20, LIGHT_GREY, WIDTH - 50, 10,align="center")

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
            self.draw_text("press Esc to play", self.hud_font, 105, GREEN, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()

    def use_compas(self):
        dist_all = []
        for sprite in self.all_sprites:
            if sprite.type == "zombie" or sprite.type == "zombie_strong":
                dist = self.player.pos - sprite.pos
                dist_all.append(dist.length())
                dist_all.sort()
                if self.compas_all:
                    pg.draw.line(self.screen, ORANGE, self.camera.apply(self.player).center,
                                     self.camera.apply(sprite).center, 2)
        for sprite in self.all_sprites:
            dist = self.player.pos - sprite.pos
            for k in range(self.compas_lvl):
                try:
                    if dist.length() == dist_all[k]:
                        if sprite.type == "zombie":
                            pg.draw.line(self.screen, ORANGE, self.camera.apply(self.player).center,
                                             self.camera.apply(sprite).center, 2)
                        elif sprite.type == "zombie_strong":
                                pg.draw.line(self.screen, RED, self.camera.apply(self.player).center,
                                             self.camera.apply(sprite).center, 2)
                except:
                    pass


    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F1:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night
                if event.key == pg.K_0:
                    self.info_update()
                    write_file("save", "COINS", read_file("save","COINS")+2)
                    self.coins = read_file("save", "COINS")
                    print("+2 Coins")
                    self.get_ammo()
                    self.player.health = 1000
                if event.key == pg.K_1:
                    if read_file("save", "pistol_ammo") >= 0:
                        self.player.weapon = "pistol"
                    pass
                if event.key == pg.K_2:
                    if read_file("save", "shotgun_ammo") >= 0:
                        self.player.weapon = "shotgun"
                    pass
                if event.key == pg.K_3:
                    if read_file("save", "sniper_ammo") >= 0:
                        self.player.weapon = "sniper"
                    pass
                if event.key == pg.K_4:
                    if read_file("save", "rifle_ammo") >= 0:
                        self.player.weapon = "rifle"
                    pass
                if event.key == pg.K_5:
                    if read_file("save", "laser_ammo") >= 0:
                        self.player.weapon = "laser"
                    pass
                if event.key == pg.K_6:
                    self.compas_is_used = not self.compas_is_used
                if event.key == pg.K_7:
                    pass
                if event.key == pg.K_8:
                    print(8)
                    pass
                if event.key == pg.K_9:
                    pass



    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("START GAME", self.title_font, 100, YELLOW, WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press ENTER to start", self.hud_font, 75, LIGHT_GREY, WIDTH / 2, HEIGHT * 3 / 4, align="center")

        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED, WIDTH/2, HEIGHT/2, align="center")
        self.draw_text("Press ENTER to start", self.hud_font, 75, LIGHT_GREY, WIDTH/2, HEIGHT*3/4, align="center")

        pg.display.flip()

        self.wait_for_key()
        self.new("home.tmx")

    def lvl_completed(self):
        self.screen.fill(BLACK)
        self.draw_text("LEVEL DONE", self.title_font, 100, GREEN, WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press ENTER to go Home", self.hud_font, 75, LIGHT_GREY, WIDTH / 2, HEIGHT * 3 / 4, align="center")

        pg.display.flip()
        self.wait_for_key()
        if not self.level_selectet:
            self.current_level = read_file("save", "CURRENT_LEVEL") + 1
            write_file("save", "CURRENT_LEVEL", self.current_level)

        self.new("home.tmx")

    def home_completed(self):
        self.screen.fill(BLACK)
        self.draw_text("Let's Go!", self.title_font, 100, BROWN, WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press ENTER to Fight!", self.hud_font, 75, LIGHT_GREY, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        self.compas_lvl = read_file("save", "compas_lvl")
        self.compas_all = read_file("save", "compas_all")

        pg.display.flip()
        self.wait_for_key()

        try:
            self.new(MAPS[read_file("save", "CURRENT_LEVEL") + 1])
        except:
            self.new("home.tmx")

    def enter_level_from_home(self, level):
        self.screen.fill(DARK_GREY)
        self.draw_text("Let's Go!", self.title_font, 100, BROWN, WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press ENTER to Fight!", self.hud_font, 75, LIGHT_GREY, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        self.compas_lvl = read_file("save", "compas_lvl")
        self.compas_all = read_file("save", "compas_all")

        pg.display.flip()
        self.wait_for_key()
        self.new(level)
        self.level_selectet = not self.level_selectet

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                        waiting = False


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new("home.tmx")
    g.run()
    g.show_go_screen()
