import pygame
import pygame as pg
import math
from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect
import pytweening
import pytweening as tween
from itertools import chain
from file_manager import *

vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.players
        pg.sprite.Sprite.__init__(self, self.groups)
        self.type = "player"
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.sprint_speed = read_file("save","sprint_speed")
        self.stamina = read_file("save","stamina")
        self.max_stamina = read_file("save","max_stamina")
        self.stamina_reg = read_file("save","stamina_reg")
        self.stamina_cost = read_file("save","stamina_cost")
        self.health = read_file("save","hp")
        self.auto_reg_up = read_file("save","UPGRADE_LEVEL_auto_reg_up_time")
        self.auto_reg_amount = read_file("save","UPGRADE_LEVEL_auto_reg_amount")
        self.max_health = read_file("save","max_hp")
        self.weapon = 'pistol'
        self.damaged = False
        self.out_of_stamina = False
        self.sprinting = False

    def get_keys(self):
        global test
        global down
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        snd = choice(self.game.player_step_sounds)
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
            if random() < 0.008:
                snd.play()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
            if random() < 0.08:
                snd.play()
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            if random() < 0.016:
                snd.play()
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
            if random() < 0.016:
                snd.play()
        if keys[pg.K_SPACE]:
            self.shoot()

        #Rennen & Audauer
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            if self.stamina > 0:
                if self.out_of_stamina == False:
                    self.vel = vec(PLAYER_SPEED * self.sprint_speed, 0).rotate(-self.rot)
                    self.stamina = self.stamina - self.stamina_cost
                    self.sprinting =True
                    if self.stamina <= 0:
                        self.out_of_stamina = True
                        self.sprinting = False
        else:
            self.sprinting = False
        if self.stamina < self.max_stamina:
            if self.sprinting == False:
                self.stamina = self.stamina + self.stamina_reg
                if self.out_of_stamina == True:
                    if self.stamina >= self.max_stamina:
                        self.sprinting = False
                        self.out_of_stamina = False
                        self.stamina = self.max_stamina
        else:
            self.stamina = self.max_stamina
            self.out_of_stamina = False
        #Sound stop
        if snd.get_num_channels() > 1:
            snd.stop()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            if read_file("save", self.weapon+"_ammo") > 0:
            #if now - self.last_shot > WEAPONS[self.weapon]['rate']:
                write_file("save", self.weapon+"_ammo", read_file("save", self.weapon+"_ammo") - 1)
                self.game.info_update()
                self.last_shot = now
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
                for i in range(WEAPONS[self.weapon]['bullet_count']):
                    spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                    Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]["damage"])
                    snd = choice(self.game.weapon_sounds[self.weapon])
                    if snd.get_num_channels() > 2:
                        snd.stop()
                    snd.play()
                MuzzleFlash(self.game, pos)


    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 2)

    def update(self):
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.damaged:
            try:
                self.image.fill((255, 0, 132, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        write_file("save","hp", self.health)

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img[type].copy()
        #EDIT-----------------------------------
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.type = type
        self.name = type
        self.hit_rect = MOBS[self.type]["mob_hit_rect"].copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOBS[self.type]["mob_health"]
        self.speed = choice(MOBS[self.type]["mob_speed"])
        self.target = game.player


    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < MOBS[self.type]["avoid_radius"]:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < MOBS[self.type]["detect_radius"]**2:

            if random() < 0.008:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img[self.type], self.rot)

            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center

 #           if self.pos.x >= WIDTH:
#                print(self.pos.x-WIDTH)

#            print(self.pos.x)

           #pg.draw
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            write_file("save", "coins", read_file("save", "coins") + MOBS[self.type]["coin_reward"])
            self.game.info_update()
            self.game.get_xp(MOBS[self.type]["xp_reward"])


    def draw_health(self):
        pct = MOBS[self.type]["mob_health"]
        if self.health >= pct * 0.8:
            col = GREEN
        elif self.health >= pct * 0.3:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOBS[self.type]["mob_health"])
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOBS[self.type]["mob_health"]:
            pg.draw.rect(self.image, col, self.health_bar)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.type = "bullet"
        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        #spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = "obstacle"
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = "muzzle"
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1