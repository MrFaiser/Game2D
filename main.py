import itertools
import json
import math
import time
from pathlib import Path
from datetime import datetime

import pygame
import pygame as pg
import sys
from random import choice, random
from os import path

from pygame import surface

import settings
import sprites
from file_manager import *
from settings import *
from sprites import *
from npc_settings import *
from savefiles import *
from tilemap import *
# HUD functions
try:
    hp = read_file("save", "hp")
    st = read_file("save", "stamina")
except:
    hp = 20
    st = 20


def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    if hp <= 150:
        BAR_LENGTH = 140
    elif hp <= 500:
        BAR_LENGTH = 400
    else:
        BAR_LENGTH = hp * 0.8

    BAR_HEIGHT = 30
    fill = pct * BAR_LENGTH
    back_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
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
    pg.draw.rect(surf, LIGHT_GREY, back_rect)
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

def draw_player_stamina(surf, x, y, pct, down):
    if pct < 0:
        pct = 0
    if st <= 150:
        BAR_LENGTH = 140
    elif st <= 500:
        BAR_LENGTH = 400
    else:
        BAR_LENGTH = st * 0.8

    BAR_HEIGHT = 22.5
    fill = pct * BAR_LENGTH
    back_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct >= 1:
        col = BLUE
    elif pct < 0.2 :
        col = RED
    else:
        col = LiGHT_BLUE
    if down:
        col = GREY
    pg.draw.rect(surf, LIGHT_GREY, back_rect)
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
        #screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
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
        self.chat_background = pg.image.load(path.join(img_folder, 'chat_background.png')).convert_alpha()
        self.chat_background_s = pg.transform.scale(self.chat_background, (WIDTH-20, 150))
        self.chat_box = pg.image.load(path.join(img_folder, 'chat_box.png')).convert_alpha()
        self.chat_box_s = pg.transform.scale(self.chat_box, (WIDTH, 150))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))

        self.mob_img = {}
        self.mob_img["zombie"] = pg.image.load(path.join(img_folder, MOBS["zombie"]["mob_img"])).convert_alpha()
        self.mob_img["zombie_strong"] = pg.image.load(path.join(img_folder, MOBS["zombie_strong"]["mob_img"])).convert_alpha()

        self.npc_img = {}
        self.npc_img["npc"] = pg.image.load(path.join(img_folder, NPCS["npc"]["npc_img"])).convert_alpha()
        self.npc_img["npc_gun"] = pg.image.load(path.join(img_folder, NPCS["npc_gun"]["npc_img"])).convert_alpha()

        #Player Stats Start
        self.coins = read_file("save","coins")
        self.xp_lvl = read_file("save","xp")
        self.xp_points = read_file("save", "xp_points")
        self.ammo = read_file("save", "pistol_ammo")
        self.compas_lvl = read_file("save", "compas_lvl")
        self.compas_all = read_file("save", "compas_all")
        self.current_level = read_file("save", "current_level")
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

    def new(self, level):
        # Write Save File
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
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
            #Crate Player
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            #Create Npc
            if tile_object.name == 'npc':
                self.npc = Npc(self, obj_center.x, obj_center.y, "npc")
            if tile_object.name == 'npc_gun':
                self.npc = Npc(self, obj_center.x, obj_center.y, "npc_gun")
            #Create Mob
            if tile_object.name == 'zombie':
                self.mob = Mob(self, obj_center.x, obj_center.y, "zombie")
            if tile_object.name == 'zombie_strong':
                self.mob = Mob(self, obj_center.x, obj_center.y, "zombie_strong")
            #Create wall
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            #Create Item
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
        self.shop = False
        self.night = False
        self.lvl_fin = False
        self.compas_is_used = False
        self.level_selectet = False
        self.buy_cooldown = False
        self.show_hp = read_file("save","UPGRADE_LEVEL_show_player_hp")
        self.health_pack = read_file("save","health_pack")
        self.effects_sounds['level_start'].play().set_volume(0.2)
        self.info_update()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        time_start_item_respawn = time.time()
        time_start_auto_reg = time.time()
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                if not self.shop:
                    self.update()

                    #Start loop Item Respawn
                    time_now = time.time()
                    if (time_now - time_start_item_respawn) >= ITEM_RESPAWN_TIME:
                        time_start_item_respawn = time.time()
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
                    if self.player.auto_reg_up >= 1:
                        if (time_now - time_start_auto_reg) >= self.player.auto_reg_up:
                            if self.player.health < self.player.max_health:
                                time_start_auto_reg = time.time()
                                self.player.add_health(self.player.auto_reg_amount)
                                write_file("save", "hp", self.player.health)
                    #loop reg end
                    # Buy cooldown start
                    if self.buy_cooldown == True:
                        if(time_now - self.time_start_buy_cooldown >= 5):
                            self.time_start_buy_cooldown = time.time()
                            self.buy_cooldown = False
                    # Buy cooldown end

            pg.display.flip()
            self.draw()
            if self.lvl_fin:
                self.lvl_completed()

    def quit(self):
        pg.quit()
        sys.exit()

    def info_update(self):
        self.ammo = read_file("save", self.player.weapon+"_ammo")
        self.coins = read_file("save", "coins")
        self.xp_lvl = read_file("save", "xp")
        self.player.health = read_file("save", "hp")
        self.player.max_health = read_file("save", "max_hp")
        self.player.auto_reg_up = read_file("save", "auto_reg_time")
        self.player.auto_reg_amount = read_file("save", "auto_reg_amount")

        print("info update", time.time())

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
                if read_file("save", "current_level") >= 1:
                    hit.kill()
                    self.enter_level_from_home("lvl1.tmx")
            elif hit.type == "doorlvl2":
                if read_file("save", "current_level") >= 2:
                    hit.kill()
                    self.enter_level_from_home("lvl2.tmx")
            elif hit.type == "doorlvl3":
                if read_file("save", "current_level") >= 3:
                    hit.kill()
                    self.enter_level_from_home("lvl3.tmx")
            elif hit.type == "doorlvl4":
                if read_file("save", "current_level") >= 4:
                    hit.kill()
                    self.enter_level_from_home("lvl4.tmx")
            elif hit.type == "doorlvl5":
                if read_file("save", "current_level") >= 5:
                    hit.kill()
                    self.enter_level_from_home("lvl5.tmx")
            elif hit.type == "doorlvl6":
                if read_file("save", "current_level") >= 6:
                    hit.kill()
                    self.enter_level_from_home("lvl6.tmx")
            elif hit.type == "doorlvl7":
                if read_file("save", "current_level") >= 7:
                    hit.kill()
                    self.enter_level_from_home("lvl7.tmx")
            elif hit.type == "doorlvl8":
                if read_file("save", "current_level") >= 8:
                    hit.kill()
                    self.enter_level_from_home("lvl8.tmx")
            elif hit.type == "doorlvl9":
                if read_file("save", "current_level") >= 9:
                    hit.kill()
                    self.enter_level_from_home("lvl9.tmx")
            elif hit.type == "doorlvl10":
                if read_file("save", "current_level") >= 10:
                    hit.kill()
                    self.enter_level_from_home("lvl10.tmx")


            if hit.type == 'health' and self.player.health < self.player.max_health:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(self.health_pack)
                self.info_update()
            if hit.type == "pistol":
                hit.kill()
                self.effects_sounds["gun_pickup"].play()
                self.player.weapon = "pistol"
                self.get_ammo()
                self.info_update()
            if hit.type == "shotgun":
                hit.kill()
                self.effects_sounds["gun_pickup"].play()
                self.player.weapon = "shotgun"
                self.get_ammo()
                self.info_update()
            if hit.type == "sniper":
                hit.kill()
                self.effects_sounds["gun_pickup"].play()
                self.player.weapon = "sniper"
                self.get_ammo()
                self.info_update()
            if hit.type == "rifle":
                hit.kill()
                self.effects_sounds["gun_pickup"].play()
                self.player.weapon = "rifle"
                self.get_ammo()
                self.info_update()

            self.buy_upgrade(hit)

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
            self.player.pos += vec(MOBS[zombie_type]["mob_knockback"], 0).rotate(self.player.rot)#+180)
#
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def create_shop_frame(self, item, text1,text2, text3,
                          cur_lvl, cur_value, cost_to_nxt_lvl, currency,
                          value_by_next_lvl, complete_value_by_next_lvl,
                          cur_lvl_path, cur_value_path,level_after_buy, max_level_reached):
        sizeX = 200
        sizeY = 50

        #acceptX = 100
        acceptX = WIDTH/2-100-sizeX-100
        acceptY = 550

        deniedX = WIDTH/2+100
        deniedY = 550


        shopY = 50

        trennlinie = "--------------------------------------------------------------------------" \
                     "--------------------------------------------------------------------------"

        self.screen.blit(self.dim_screen, (0, 0))

        while self.shop:
            for ev in pygame.event.get():
                if ev.type == pg.QUIT:
                    self.quit()
                if max_level_reached:
                    self.draw_text(("Du das das Maximale Level erreicht!"), self.hud_font, 28, LIGHT_RED, WIDTH/2,
                                   acceptY-25, align="center")

                #erstelle butten funktion position
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    #accept
                    if acceptX <= mouse[0] <= acceptX + sizeX and acceptY <= mouse[1] <= acceptY + sizeY:
                        konto = read_file("save", currency.lower())
                        if konto >= cost_to_nxt_lvl and not max_level_reached:
                            self.shop = False
                            self.time_start_buy_cooldown = time.time()
                            print("Buy:", item.type, cost_to_nxt_lvl, currency, " from ", cur_lvl, " to ", cur_lvl+1)
                            #currency abziehen
                            write_file("save", currency.lower(), konto-cost_to_nxt_lvl)
                            #lvl aufsteigen
                            write_file("save", cur_lvl_path, level_after_buy)
                            #wert aufsteigen
                            write_file("save", cur_value_path, complete_value_by_next_lvl)

                            self.info_update()
                        elif max_level_reached:
                           pass
                        else:
                            self.draw_text(("Nicht genug " + currency), self.hud_font, 28, LIGHT_RED, acceptX + 10, acceptY-25, align="sw")

                    #denied
                    if deniedX <= mouse[0] <= deniedX + sizeX and deniedY <= mouse[1] <= deniedY + sizeY:
                        self.shop = False
                        self.time_start_buy_cooldown = time.time()


            mouse = pygame.mouse.get_pos()


            #create button sichtbar position
            #accept
            if acceptX <= mouse[0] <= acceptX + sizeX and acceptY <= mouse[1] <= acceptY + sizeY:
                pygame.draw.rect(self.screen, LIGHT_GREY, [acceptX, acceptY, sizeX, sizeY])
            else:
                pygame.draw.rect(self.screen, BLACK, [acceptX, acceptY, sizeX, sizeY])


            #denied
            if deniedX <= mouse[0] <= deniedX + sizeX and deniedY <= mouse[1] <= deniedY + sizeY:
                pygame.draw.rect(self.screen, LIGHT_GREY, [deniedX, deniedY, sizeX, sizeY])
            else:
                pygame.draw.rect(self.screen, BLACK, [deniedX, deniedY, sizeX, sizeY])



            self.draw_text("SHOP", self.title_font, 105, ORANGE, WIDTH / 2, shopY, align="center")
            self.draw_text(trennlinie, self.title_font, 10, LIGHT_GREY, WIDTH / 2, shopY+50, align="center")

            #write text
            self.draw_text(text1, self.hud_font, 50, LIGHT_GREY, WIDTH/2, shopY + 100, align="center")
            self.draw_text(text2, self.hud_font, 55, CYAN, WIDTH/2, shopY + 150, align="center")
            self.draw_text(text3, self.hud_font, 50, LIGHT_GREY, WIDTH/2, shopY + 200, align="center")

            #write values
            self.draw_text(("Aktuelle Stufe: " + "{}".format(round(cur_lvl))), self.hud_font, 35, YELLOW, acceptX, shopY + 300, align="nw")
            self.draw_text("{}".format(round(cur_value,2)), self.hud_font, 35, CYAN, acceptX, shopY + 330, align="nw")

            self.draw_text("-->", self.hud_font, 35, CYAN, WIDTH / 2, shopY + 300, align="n")
            self.draw_text("{} ".format(cost_to_nxt_lvl) + currency, self.hud_font, 35, ORANGE, WIDTH / 2, shopY + 330, align="n")
            self.draw_text("{}".format(round(value_by_next_lvl,2)), self.hud_font, 35, PINK, WIDTH / 2, shopY + 360, align="n")

            self.draw_text(("Naechste Stufe: " + "{}".format(round(cur_lvl + 1))), self.hud_font, 35, YELLOW, deniedX, shopY + 300, align="nw")
            self.draw_text("{}".format(round(complete_value_by_next_lvl,2)), self.hud_font, 35, CYAN, deniedX, shopY + 330, align="nw")


            #write answer
            self.draw_text(trennlinie, self.title_font, 10, LIGHT_GREY, WIDTH / 2, acceptY-10, align="center")
            self.draw_text("Kaufen", self.hud_font, 40, GREEN, acceptX + 30, acceptY, align="nw")
            self.draw_text("Ablehnen", self.hud_font, 40, RED, deniedX + 10, deniedY, align="nw")
            pg.display.update()


    def buy_upgrade(self, item):
        if self.buy_cooldown == False:
            if item.type == "max_health_up":
                self.buy_cooldown = True
                self.shop = True
                max_level = 100

                text1 = "Möchtest du deine \n"
                text2 = "Maximale Gesundheit"
                text3 = "\n verbessern?"


                cur_lvl_path = "UPGRADE_LEVEL_max_health_up"
                cur_lvl = read_file("save", "UPGRADE_LEVEL_max_health_up")

                cur_value_path = "max_hp"
                cur_value = read_file("save", "max_hp")

                cost_to_nxt_lvl = (cur_lvl * math.pi) + cur_lvl * (cur_lvl/15)
                cost_to_nxt_lvl = round(cost_to_nxt_lvl)

                currency = "XP"

                value_by_next_lvl = (cur_lvl*2+1)*0.2378+(cur_lvl*2.5)
                complete_value_by_next_lvl = cur_value + value_by_next_lvl
                level_after_buy = cur_lvl + 1

                if cur_lvl == max_level:
                    self.create_shop_frame(item, text1, text2, text3, max_level, 0, 0, currency,
                                           0, 0, cur_lvl_path, cur_value_path,
                                           0, True)
                else:
                    self.create_shop_frame(item, text1, text2, text3, cur_lvl, cur_value, cost_to_nxt_lvl, currency,
                                           value_by_next_lvl, complete_value_by_next_lvl, cur_lvl_path, cur_value_path,
                                           level_after_buy, False)
            if item.type == "health_pack_up":
                self.buy_cooldown = True
                self.shop = True
                max_level = 100

                text1 = "Möchtest du die \n"
                text2 = "Erste-Hilfe Packs"
                text3 = "\n verbessern?"

                cur_lvl_path = "UPGRADE_LEVEL_health_pack_up"
                cur_lvl = read_file("save", "UPGRADE_LEVEL_health_pack_up")

                cur_value_path = "health_pack"
                cur_value = read_file("save", "health_pack")

                cost_to_nxt_lvl = (cur_lvl * 2.2) + 1
                cost_to_nxt_lvl = round(cost_to_nxt_lvl)
                currency = "XP"
                value_by_next_lvl = 5
                complete_value_by_next_lvl = cur_value + value_by_next_lvl
                level_after_buy = cur_lvl + 1

                if cur_lvl == max_level:
                    self.create_shop_frame(item, text1, text2, text3, max_level, 0, 0, currency,
                                           0, 0, cur_lvl_path, cur_value_path,
                                           0, True)
                else:
                    self.create_shop_frame(item, text1, text2, text3, cur_lvl, cur_value, cost_to_nxt_lvl, currency,
                                           value_by_next_lvl, complete_value_by_next_lvl, cur_lvl_path, cur_value_path,
                                           level_after_buy, False)
            if item.type == "auto_reg_up":
                self.buy_cooldown = True
                self.shop = True
                max_level = 100

                text1 = "Möchtest du deine \n"
                text2 = "Regerations Geschwindigkeit"
                text3 = "\n verbessern?"

                cur_lvl_path = "UPGRADE_LEVEL_auto_reg_up_time"
                cur_lvl = read_file("save", "UPGRADE_LEVEL_auto_reg_up_time")

                cur_value_path = "auto_reg_time"
                cur_value = read_file("save", "auto_reg_time")


                cost_to_nxt_lvl = (cur_value*0.5) * cur_value+(cur_lvl*2)
                cost_to_nxt_lvl = round(cost_to_nxt_lvl)
                currency = "XP"
                value_by_next_lvl = 6.5-(cur_lvl/17)*(cur_lvl/100)

                complete_value_by_next_lvl = value_by_next_lvl
                level_after_buy = cur_lvl+1
                if cur_lvl == max_level:
                    self.create_shop_frame(item, text1, text2, text3, max_level, 0, 0, currency,
                                           0, 0, cur_lvl_path, cur_value_path,
                                           0, True)
                else:
                    self.create_shop_frame(item, text1, text2, text3, cur_lvl, cur_value, cost_to_nxt_lvl, currency,
                                           value_by_next_lvl, complete_value_by_next_lvl, cur_lvl_path, cur_value_path,
                                           level_after_buy, False)
            if item.type == "auto_reg_amount":
                self.buy_cooldown = True
                self.shop = True
                max_level = 100

                text1 = "Möchtest du deine \n"
                text2 = "Regerations Kraft"
                text3 = "\n verbessern?"

                cur_lvl_path = "UPGRADE_LEVEL_auto_reg_amount"
                cur_lvl = read_file("save", "UPGRADE_LEVEL_auto_reg_amount")

                cur_value_path = "auto_reg_amount"
                cur_value = read_file("save", "auto_reg_amount")


                cost_to_nxt_lvl = (cur_value*0.3) *cur_value/2+(cur_lvl*2.5)
                cost_to_nxt_lvl = round(cost_to_nxt_lvl)
                currency = "XP"
                value_by_next_lvl = 1.5+(cur_lvl*0.77)+(cur_lvl/100)

                complete_value_by_next_lvl = value_by_next_lvl
                level_after_buy = cur_lvl+1

                if cur_lvl == max_level:
                    self.create_shop_frame(item, text1, text2, text3, max_level, 0, 0, currency,
                                           0, 0, cur_lvl_path, cur_value_path,
                                           0, True)
                else:
                    self.create_shop_frame(item, text1, text2, text3, cur_lvl, cur_value, cost_to_nxt_lvl, currency,
                                           value_by_next_lvl, complete_value_by_next_lvl, cur_lvl_path, cur_value_path,
                                           level_after_buy, False)
            if item.type == "show_player_hp":
                self.buy_cooldown = True
                self.shop = True
                max_level = 1

                text1 = "Möchtest du deine \n"
                text2 = "HP in Zahlen "
                text3 = "\n anzeigen lassen?"

                cur_lvl_path = "UPGRADE_LEVEL_show_player_hp"
                cur_lvl = read_file("save", "UPGRADE_LEVEL_show_player_hp")

                cur_value_path = "auto_reg_amount"
                cur_value = read_file("save", "auto_reg_amount")

                cost_to_nxt_lvl = 25
                cost_to_nxt_lvl = round(cost_to_nxt_lvl)
                currency = "XP"
                value_by_next_lvl = 1

                complete_value_by_next_lvl = value_by_next_lvl
                level_after_buy = cur_lvl+1
                if cur_lvl == max_level:
                    self.create_shop_frame(item, text1, text2, text3, max_level, 0, 0, currency,
                                           0, 0, cur_lvl_path, cur_value_path,
                                           0, True)
                else:
                    self.create_shop_frame(item, text1, text2, text3, cur_lvl, cur_value, cost_to_nxt_lvl, currency,
                                           value_by_next_lvl, complete_value_by_next_lvl, cur_lvl_path, cur_value_path,
                                           level_after_buy, False)

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
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.rect), 1)

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
        draw_player_health(self.screen, 10, 10, self.player.health / self.player.max_health)
        if self.show_hp == 1:
            self.draw_text("HP: {}".format(round(self.player.health, 2)) + " / {}".format(round(self.player.max_health,2)), self.hud_font, 15, BLACK, 15, 25, align="w")
        draw_player_stamina(self.screen, 10, 45, self.player.stamina / self.player.max_stamina, self.player.out_of_stamina)
        if self.show_hp == 1:
            self.draw_text("ST: {}".format(round(self.player.stamina, 2)) + " / {}".format(self.player.max_stamina), self.hud_font, 15, WHITE, 15, 55, align="w")

        self.draw_text("Weapon: {}".format(self.player.weapon) + " x {}".format(self.ammo), self.hud_font, 30,DARK_GREY, 10, 100, align="w")
        self.draw_text("Zombies: {}".format(len(self.mobs)), self.hud_font, 30, DARK_GREEN, 10, 130, align="w")
        self.draw_text("Coins: {}".format(self.coins), self.hud_font, 30, ORANGE, 10, 160, align="w")
        self.draw_text("XP lvl: {}".format(self.xp_lvl) , self.hud_font, 30, YELLOW, 10, 190, align="w")

        self.draw_text("FPS {:.2f}".format(self.clock.get_fps()), self.hud_font, 20, BLACK, WIDTH - 50, 10,align="center")

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
            self.draw_text("press Esc to play", self.hud_font, 105, GREEN, WIDTH / 2, HEIGHT * 3 / 4, align="center")

        pg.display.flip()

############################################################
    def truncate(self, n, decimals=0):
        multiplier = 10 ** decimals
        return int(n * multiplier) / multiplier

##################################
    def get_xp(self, xp):
        xp_needed = (24 + ((self.xp_lvl) * (self.xp_lvl / 100)) * 2.8)
        self.xp_points = self.xp_points + xp
        for i in range(int(self.truncate((self.xp_points) / xp_needed))):
            self.xp_lvl = self.xp_lvl + 1
            self.xp_points = self.xp_points % xp_needed
            xp_needed = (24 + ((self.xp_lvl) * (self.xp_lvl / 100)) * 2.8)

            write_file("save", "xp", self.xp_lvl)
            write_file("save", "xp_points", self.xp_points)


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

    def dialogue(self, npcType, color):
        self.npc_chat = []
        for chat in NPCS_CHAT[npcType]:
            self.npc_chat.append(chat)

        textGroup = choice(self.npc_chat)
        text = NPCS_CHAT[npcType][textGroup]

        #Nametag
        blackBarRectPos = (40, HEIGHT - 200)
        blackBarRectSize = (300, 50)
        pygame.draw.rect(self.screen, GREY, pygame.Rect(blackBarRectPos, blackBarRectSize))
        self.draw_text(npcType, self.hud_font, 40, PINK, 55, HEIGHT-200, align="nw")

        #Background
        blackBarRectPos = (20, HEIGHT - 150)
        blackBarRectSize = (WIDTH - 40, 120)
        pygame.draw.rect(self.screen, DARK_GREY,pygame.Rect(blackBarRectPos, blackBarRectSize))


        def blit_text(surface, text, pos, font, color=color):
            words = [word.split(' ') for word in text.splitlines()]
            space = font.size(' ')[0]
            max_width, max_height = surface.get_size()
            x, y = pos
            for line in words:
                for word in line:
                    word_surface = font.render(word, 0, color)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= max_width:
                        x = pos[0]
                        y += word_height
                    surface.blit(word_surface, (x, y))
                    x += word_width + space
                x = pos[0]
                y += word_height

        font = pygame.font.Font(self.hud_font, 30)

        continues = True
        while continues:
            self.clock.tick(FPS)
            pygame.event.pump()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_e:
                        continues = False
            pygame.display.flip()
            blit_text(self.screen, text, (40, HEIGHT-140), font)

    def nearest_npc(self):
        dist_all = []
        dist_all_type = {}
        for sprite in self.all_sprites:
            if sprite.type == "npc" or sprite.type == "npc_gun":
                dist = self.player.pos - sprite.pos
                dist_all.append(dist.length())
                dist_all_type[dist.length()] = sprite.type

        try:
            nearest_npc = dist_all[0]
            for v in dist_all:
                if v < nearest_npc:
                    nearest_npc = v
            if nearest_npc <= NPC_INTERACT_RANGE:
                print("start dialoge")
                return dist_all_type[nearest_npc]
        except:
            pass

    def events(self):
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
                if event.key == pg.K_o:
                    self.show_go_screen()
                if event.key == pg.K_e:
                    print("interact")
                    try:
                        self.dialogue(self.nearest_npc(), CYAN)
                    except:
                        print("Kein NPC in der Nähe!")
                if event.key == pg.K_c:
                    pass
                if event.key == pg.K_n:
                    self.night = not self.night
                if event.key == pg.K_0:
                    self.info_update()
                    write_file("save", "coins", read_file("save","coins")+2)
                    self.coins = read_file("save", "coins")
                    print("+2 Coins")
                    self.get_ammo()
                    self.player.max_health = 1000
                    self.player.health = 1000
                    self.player.max_stamina = 1000
                    self.player.stamina = 1000
                if event.key == pg.K_1:
                    if read_file("save", "pistol_ammo") >= 0:
                        self.player.weapon = "pistol"
                        self.ammo = read_file("save", self.player.weapon+"_ammo")
                    pass
                if event.key == pg.K_2:
                    if read_file("save", "shotgun_ammo") >= 0:
                        self.player.weapon = "shotgun"
                        self.ammo = read_file("save", self.player.weapon+"_ammo")
                    pass
                if event.key == pg.K_3:
                    if read_file("save", "sniper_ammo") >= 0:
                        self.player.weapon = "sniper"
                        self.ammo = read_file("save", self.player.weapon+"_ammo")
                    pass
                if event.key == pg.K_4:
                    if read_file("save", "rifle_ammo") >= 0:
                        self.player.weapon = "rifle"
                        self.ammo = read_file("save", self.player.weapon+"_ammo")
                    pass
                if event.key == pg.K_5:
                    if read_file("save", "laser_ammo") >= 0:
                        self.player.weapon = "laser"
                        self.ammo = read_file("save", self.player.weapon+"_ammo")
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
            self.current_level = read_file("save", "current_level") + 1
            write_file("save", "current_level", self.current_level)

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
            self.new(MAPS[read_file("save", "current_level") + 1])
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
