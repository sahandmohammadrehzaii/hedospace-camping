# in the name of GOD

import pygame as pg
import sys
from random import choice, random
import os
from os import path
from settings import *
from sprites import *
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, 16, 2, 4096)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        game_folder = os.path.dirname(__file__)
        icon = pg.image.load('img/icon.png')
        pg.display.set_icon(icon)
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
        game_folder = os.path.dirname(__file__)
        self.title_font = 'font/Shabnam.woff'
        self.hud_font = 'font/Shabnam.woff'
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.player_img = []
        for pimg in PLAYER_IMG:
            self.player_img.append(pg.image.load(pimg).convert_alpha())
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(BULLET_IMG).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        self.wall_img = pg.image.load(WALL_IMG).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.mob_img = pg.image.load(MOB_IMG).convert_alpha()
        self.splat = pg.image.load(SPLAT).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(img).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(ITEM_IMAGES[item]).convert_alpha()
        
        #Lighting effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(LIGHT_MASK).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        
        # Sound loading
        pg.mixer.music.load(BG_MUSIC)
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(EFFECTS_SOUNDS[type])
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(snd)
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(snd)
            s.set_volume(0.2)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(snd))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(snd))

    def new(self, t_map, level):
        # initialize all variables and do all the setup for a new game
        self.current_level = level - 1
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(t_map)
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name in ['health', 'shotgun','machinegun', 'pistol']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night =  False


        if self.current_level == 1:
            self.night = False
        else:
            self.night = True
       
        self.effects_sounds['level_start'].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        
        #game over?
        if len(self.mobs) == 0:
            self.playing = False
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
            if hit.type == 'machinegun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'machinegun'
            if hit.type == 'pistol':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'pistol'
        # mobs hit player
        #watch video on this section
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            
            if self.current_level == 2:
                self.player.health -= MOB_DAMAGE_MED
            elif self.current_level == 3:
                self.player.health -= MOB_DAMAGE_HARD 
            else: 
                self.player.health -= MOB_DAMAGE
        
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            #for each bullet in each mob hit:
            for bullet in hits[mob]:
                #subtract damage from mob health
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        #draw light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags = pg.BLEND_MULT)

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        if self.night:
            self.render_fog()
        
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text('Zombies: {}'.format(len(self.mobs)), self.hud_font, 30, WHITE, 
                       WIDTH - 10, 10, align="ne")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align = "center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night
    
    def level_select(self, level):
        print(level)
        running = True
        
        while running:
            if level == 1:
                level += 1
                g.new('tmx/level1.tmx', level)
                g.run()
                g.show_go_screen(level)
            #add final endgame screen
            if level == 2:
                level += 1
                g.new('tmx/l2.tmx', level)
                g.run()
                g.show_go_screen(level)
            #check this code:
            if level == 3:
                level += 1
                g.new('tmx/level3.tmx', level)
                g.run()
                g.show_go_screen(level)
    
    def show_start_screen(self, level):
        self.s_screen = True
        s_screen = self.s_screen
        self.go_screen = False
        self.screen.fill(BLACK)
        
        if level == 1:
            
            self.draw_text("hedospace camping", self.title_font, 100, RED, 
                       WIDTH / 2, HEIGHT * 1/6, align="center")
            self.draw_text("Controls - Use space to shoot and p to pause.", self.title_font, 30, WHITE, 
                       WIDTH / 2, HEIGHT * 2/6, align="center")
            self.draw_text("Use w/a/s/d or up/down/left/right for movement.", self.title_font, 30, WHITE, 
                       WIDTH / 2, HEIGHT / 2, align="center")
            self.draw_text("Kill all the zombies and become the brand and understand the story of the game", self.title_font, 20, WHITE, 
                       WIDTH / 2, HEIGHT * 4/6, align="center")
            self.draw_text("Press c to continue or q to quit.", self.title_font, 40, GREEN, 
                       WIDTH / 2, HEIGHT * 5/6, align="center")
            self.draw_text("Built and designed by the GHADAAM team", self.title_font, 15, LIGHTGREY, 
                       WIDTH / 2, HEIGHT * 5.75/6, align="center")
        if level == 2:
            self.draw_text("Welcome to the new stage of the game. We hope you finish the game and discover the secrets! " + str(level), self.title_font, 20, RED, 
                       WIDTH / 2, HEIGHT * 2/6, align="center")
            self.draw_text("This level begins in night mode and the mobs are more difficult.", self.title_font, 30, WHITE, 
                       WIDTH / 2, HEIGHT / 2, align="center")
            self.draw_text("Kill all the zombies and become the brand and understand the story of the game", self.title_font, 20, WHITE, 
                       WIDTH / 2, HEIGHT * 4/6, align="center")
            self.draw_text("Press c key to continue or q to quit.", self.title_font, 40, WHITE, 
                       WIDTH / 2, HEIGHT * 5/6, align="center")
        if level == 3:
            self.draw_text("Welcome to the new stage of the game. We hope you finish the game and discover the secrets! " + str(level), self.title_font, 20, RED, 
                       WIDTH / 2, HEIGHT * 2/6, align="center")
            self.draw_text("This is the final level.  This level begins in night mode and the mobs are more difficult.", self.title_font, 20, WHITE, 
                       WIDTH / 2, HEIGHT /2, align="center")
            self.draw_text("Kill all the zombies and become the brand and understand the story of the game", self.title_font, 20, WHITE, 
                       WIDTH / 2, HEIGHT * 4/6, align="center")
            self.draw_text("Press c key to continue or q to quit.", self.title_font, 40, WHITE, 
                       WIDTH / 2, HEIGHT * 5/6, align="center")
        
        pg.display.flip()
        self.wait_for_key(level)
    
    def show_go_screen(self, level):
        self.go_screen = True
        self.s_screen = False
        self.screen.fill(BLACK)
        if len(self.mobs) == 0:
            if level == 2:
                self.draw_text("YOU WIN THE THIS LEVEL!", self.title_font, 25, RED, 
                        WIDTH / 2, HEIGHT / 2, align="center")
                self.draw_text("Press (C) button to continue the game or start again or press (Q) button to exit the game", self.title_font, 20, WHITE, 
                            WIDTH / 2, HEIGHT * 4/6, align="center")
            if level == 3:
                self.draw_text("YOU WIN THE THIS LEVEL!", self.title_font, 25, RED, 
                        WIDTH / 2, HEIGHT / 2, align="center")
                self.draw_text("Press (C) button to continue the game or start again or press (Q) button to exit the game", self.title_font, 20, WHITE, 
                            WIDTH / 2, HEIGHT * 4/6, align="center")
            if level == 4:
                self.draw_text("Congratulations, you have completed the game!", self.title_font, 25, RED, 
                        WIDTH / 2, HEIGHT * 2/6, align="center")
                self.draw_text("You finished the game and you were able to finish the story!", self.title_font, 25, RED, 
                        WIDTH / 2, HEIGHT / 2, align="center")
                self.draw_text("To exit the game, press the (Q) button and to play the level again, you must press the (R) button", self.title_font, 20, WHITE, 
                            WIDTH / 2, HEIGHT * 4/6, align="center")
        else:
            self.draw_text("Unfortunately, you lost the game and could not understand the story of the game", self.title_font, 25, RED, 
                        WIDTH / 2, HEIGHT / 2, align="center")
        
            self.draw_text("To exit the game, press the (Q) button and to play the level again, you must press the (R) button", self.title_font, 20, WHITE, 
                        WIDTH / 2, HEIGHT * 3/4, align="center")
            
        pg.display.flip()
        self.wait_for_key(level)
       
    
    def wait_for_key(self, level):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    if self.s_screen == True:
                        if event.key == pg.K_c:
                            try:
                                if len(self.mobs) == 0: 
                                    if level == 4:
                                        self.quit()
                                    if level == 3:
                                        g.level_select(level)    
                                    if level == 2:
                                        g.level_select(level)
                                        waiting = False
                            except:
                                if level == 1:
                                    g.level_select(level)
                                    waiting = False
                        if event.key == pg.K_q:
                            waiting = False
                            self.quit()
                        
                    elif self.go_screen == True:
                        if event.key == pg.K_c:
                            try:
                                if len(self.mobs) == 0: 
                                    if level == 4:
                                        self.quit()
                                    if level == 3:
                                        g.show_start_screen(level)    
                                    if level == 2:
                                        g.show_start_screen(level)
                                        waiting = False
                            except:
                                if level == 1:
                                    g.level_select(level)
                                    waiting = False
                        if event.key == pg.K_q:
                            waiting = False
                            self.quit()
                        else:
                            if event.key == pg.K_r:
                                waiting = False
                                g.level_select(level - 1)
                               
g = Game()
g.show_start_screen(1)

