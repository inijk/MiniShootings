from calendar import c, weekday
from pathlib import PureWindowsPath
import random
import time
import sys
import pygame
import pygame.mixer
from pygame.locals import *

FRAMERATE = 60
SURFACE = Rect(0, 0, 720, 480)
p_speed = 1
C_RANGE = 40
BGM_SOUND = 0.2

tmr_c = 0
tmr_t = 0
c_c = 0
c_c_c = 0

black = (0,0,0)
white = (255,255,255)
surface_color = black
scr =pygame.Surface((720,480),flags=pygame.SRCALPHA)
scr_a = 0

map = []

idx = -1
gamemode = 0
help = "こんにちは"
px = 0
py = 0
pw = 0 #↑↓←→

class Player(pygame.sprite.Sprite):
    def __init__(self,p_x,p_y,carsol,attack,ground):
        pygame.sprite.Sprite.__init__(self)
        super(Player, self).__init__()
        self.images = list()
        for i in range(1, 13):
            number_str = str(i)
            if len(number_str) == 1:
                number_str =number_str
            self.images.append(pygame.image.load('player/player' + number_str + '.png').convert_alpha())
        self.index = 0
        self.index_t = 0
        self.way = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(20), int(35)))
        self.p_x = p_x
        self.p_y = p_y
        self.carsol = carsol
        self.attack = attack
        self.ground = ground

    def move(self,key):
        global p_speed,px,py,pw
        key = pygame.key.get_pressed()
        self.rect.x=self.p_x
        self.rect.y=self.p_y
        px = self.p_x
        py = self.p_y

        if key[pygame.K_w] == 1 or key[pygame.K_UP] == 1:
            pw = 1
            if map[py-1][px] != 9:
                self.p_y = self.p_y - p_speed
            if self.index_t > 1/p_speed*20:
                self.index += 1
                self.index_t = 0
            if self.index > 8 or self.index < 6:
                self.index = 6
            self.index_t += 1

        if key[pygame.K_s] == 1:
            pw = 2
            if map[py+1][px] != 9:
                self.p_y = self.p_y + p_speed
            if self.index_t > 1/p_speed*20:
                self.index += 1
                self.index_t = 0
            if self.index > 5 or self.index < 3:
                self.index = 3
            self.index_t += 1

        if key[pygame.K_a] == 1:
            pw = 3
            if map[py][px-1] != 9:
                self.p_x = self.p_x - p_speed
            if self.index < 3 and self.index_t > 1/p_speed*20:
                self.index += 1
                self.index_t = 0
            if self.index > 2 :
                self.index = 0
            self.index_t += 1

        if key[pygame.K_d] == 1:
            pw = 4
            if map[py][px+1] != 9:
                self.p_x = self.p_x + p_speed
            if self.index_t > 1/p_speed*20:
                self.index += 1
                self.index_t = 0
            if self.index >11  or self.index < 9:
                self.index = 9
            self.index_t += 1

        if key[pygame.K_LCTRL] == 1:
            p_speed = 2
        else:
            p_speed = 1
        
        if self.p_x < 0:
            self.p_x = 700
        if self.p_x > 710:
            self.p_x = 10
        if self.p_y < 0:
            self.p_y = 450
        if self.p_y > 460:
            self.p_y = 0

    def draw(self, surface):
        global px,py
        px = self.p_x
        py = self.p_y
        self.image = self.images[self.index]
        self.image = pygame.transform.scale(self.image, (int(20), int(35)))
        surface.blit(self.image, self.rect)

class Carsol(pygame.sprite.Sprite):
    def __init__(self,name,x,y,c_x,c_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(name).convert_alpha()
        width  = self.image.get_width()
        height = self.image.get_height()
 
        ### 四角形オブジェクト生成
        self.rect = Rect(x, y, width, height)
        self.image = pygame.transform.scale(self.image, (35, 25))
        self.c_x = c_x
        self.c_y = c_y


    def move(self,key):
        global tmr_c,c_c,c_c_c,idx,gamemode
        key = pygame.key.get_pressed()
        self.rect.x=self.c_x
        self.rect.y=self.c_y
        if key[pygame.K_UP] == 1 and tmr_c > 30:
            self.c_y = self.c_y - C_RANGE
            if idx == 0:
                self.c_x -= 30
                gamemode -=1
            tmr_c = 0
        if key[pygame.K_DOWN] == 1 and tmr_c > 30:
            self.c_y = self.c_y + C_RANGE
            if idx == 0:
                self.c_x += 30
                gamemode +=1
            tmr_c = 0
        if idx == 0:
            if self.c_y < 305: 
                self.c_y = 305
                self.c_x = 380
                if gamemode <0:
                    gamemode = 0
            if self.c_y > 425: 
                self.c_y = 425 
                self.c_x = 470
                if gamemode > 3:
                    gamemode = 3

        #self.rect = self.rect.clamp(SURFACE)
        tmr_c += 1
        if c_c <= 120 and c_c_c == 0:
            self.c_x += 0.2
            c_c += 1
        if c_c == 120 and c_c_c == 0:
            c_c = 0
            c_c_c = 1
        if c_c <= 120 and c_c_c == 1:
            self.c_x -= 0.2
            c_c += 1
        if c_c == 120 and c_c_c == 1:
            c_c = 0
            c_c_c = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,e_x,e_y,attack):
        global px,py
        pygame.sprite.Sprite.__init__(self)
        super(Enemy, self).__init__()
        self.images = list()
        for i in range(1, 2):
            number_str = str(i)
            if len(number_str) == 1:
                number_str =number_str
            self.images.append(pygame.image.load('enemy/enemy' + number_str + '.png').convert_alpha())
        self.e_x = e_x
        self.e_y = e_y
        self.attack = attack
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def move(self):
        global px,py

    def draw(self,surface):
        self.image = self.images[self.index]
        surface.blit(self.image, self.rect)

class Ground(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        super(Ground, self).__init__()
        self.images = list()
        for i in range(1, 2):
            number_str = str(i)
            if len(number_str) == 1:
                number_str =number_str
        self.images.append(pygame.image.load('bg/bg' + number_str + '.png').convert_alpha())
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def draw(self, surface):
        self.image = pygame.transform.scale(self.image, (int(50), int(100)))
        self.image = self.images[self.index]
        surface.blit(self.image, self.rect)

class Attack(pygame.sprite.Sprite):
    def __init__(self,name,x,y,a_x,a_y):
        global pw,px,py
        pygame.sprite.Sprite.__init__(self)
        self.images = list()
        for i in range(1, 5):
            number_str = str(i)
            if len(number_str) == 1:
                number_str =number_str
            self.images.append(pygame.image.load('slash/slash' + number_str + '.png').convert_alpha())
        '''
        width = 50
        height = 50
        '''
        self.image = self.images[pw+1]
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (int(35), int(35)))
        self.a_x = px
        self.a_y = py
        self.ax = 0
        self.ay = 0
        self.image_center_position = (a_x,a_y+35)
        self.image_angle = 0
        self.attack_t = 0

    def rotate_center_image(self):
        global pw
        #self.image_angle = 180
        rot_image = pygame.transform.rotate(self.image, self.image_angle)
        rot_rect = rot_image.get_rect()
        rot_rect.center = self.image_center_position # 中心位置を設定(移動)

        self.image = rot_image
        self.rect = rot_rect

    def attack(self,key,surface):
        global px,py,pw
        self.image = pygame.transform.scale(self.image, (self.ax, int(35)))
        if key[pygame.K_SPACE] == 1:
            self.attack_t +=1
            if self.attack_t < 60:
                surface.blit(self.image, self.rect)
        else:
            self.attack_t = 0

def help_message(surface):
    global help,gamemode,idx
    font_help = pygame.font.SysFont("yumincho", 15)
    text_help = font_help.render("Help："+help,True,(black))
    if idx == 0:
        if gamemode == 0:
            help = "開発中…"
        if gamemode == 1:
            help = "開発中…"
        if gamemode == 2:
            help = "操作の練習を行います"
        if gamemode == 3:
            help = "操作の設定を行います"
        surface.blit(text_help,(0,460))

def main():
    global idx, gamemode, surface_color,scr,scr_a, tmr_t,help
    pygame.init()
    pygame.mixer.init()
    surface = pygame.display.set_mode(SURFACE.size)
    clock = pygame.time.Clock()
    carsol = Carsol("yubi.png",0,0,380,305)
    attack = Attack("slash.png",0,0,100,100)
    ground = Ground(0,0)
    enemy = Enemy(0,0,attack)
    player = Player(240,200,carsol,attack,ground)

    font_title = pygame.font.SysFont("yumincho" ,100)
    font_menu = pygame.font.SysFont("yumincho", 30)
    text_title = font_title.render("UnKnown",True,(black))
    text_newgame = font_menu.render("NewGame",True,(black))
    text_loadgame = font_menu.render("LoadGame",True,(black))
    text_practice = font_menu.render("Practice",True,(black))
    text_options = font_menu.render("Options",True,(black))
    while True:
        clock.tick(120)
        surface.fill(surface_color)
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]==1:
                pygame.quit()
                sys.exit()

        if idx == -1:
            idx = 0
            pygame.mixer.music.load("Moment.mp3")
            pygame.mixer.music.set_volume(BGM_SOUND) #読み込み
            pygame.mixer.music.play(-1)
        
        if idx == 0:
            surface.blit(scr,(0,0))
            surface.blit(text_title,(80,60))
            surface.blit(text_newgame,(450,300))
            surface.blit(text_loadgame,(480,340))
            surface.blit(text_practice,(510,380))
            surface.blit(text_options,(540,420))
            scr.fill((255,255,255,scr_a))
            tmr_t += 1
            if key[pygame.K_SPACE] == 1:
                if scr_a < 225  :
                    scr_a = 225
                    tmr_t = 0
                if scr_a > 224 and tmr_t > 60:
                    pygame.mixer.music.stop()
                    if gamemode == 2:
                        idx = 1
                        #
                        # time.sleep(3)
                tmr_t = 0
            if scr_a < 255:
                scr_a += 0.5
            if scr_a > 224:
                carsol.move(key)
                carsol.draw(surface)
                help_message(surface)

        if idx == 1:
            player.move(key)
            player.draw(surface)
            attack.rotate_center_image()
            attack.attack(key,surface)
            ground.draw(surface)
            #enemy.move()
            #enemy.draw(surface)
        
        pygame.display.update()

def exit():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":

    main()