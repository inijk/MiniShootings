from ast import If
from threading import stack_size
import pygame
import sys
import time
import random
import math
import tkinter as tk

white = (225,225,225)
black = (0,0,0)

img_bb = pygame.image.load("white-full.png")
img_wb = pygame.image.load("black-full.png")
img_jiji = pygame.image.load("jiji.png")
img_jiji = pygame.transform.scale(img_jiji,[300,300])
img_jiji2 = pygame.image.load("jiji2.png")
img_jiji2 = pygame.transform.scale(img_jiji2,[325,325])
img_jiji3 = pygame.image.load("jiji3.png")
img_jiji3 = pygame.transform.scale(img_jiji3,[350,350])

screen_width = 640
screen_height = 640
speed = 10
idx =-1
tmr = 0
hp = 100
st = 200
px = 320 #プレイヤーのX座標
py = screen_height-130 #プレイヤーのY座標
cx = 320
cy = 475
bx = 0 #弾のX座標
by = 0 #弾のY座標
space = 0
gamescene = 0
BULLET_MAX = 100
BULLET2_MAX = 100
bull_n = 0
bull_x =[0]*BULLET_MAX
bull_y =[0]*BULLET_MAX
bull_f =[False]*BULLET_MAX
bull2_n = 0
bull2_x =[0]*BULLET2_MAX
bull2_y =[0]*BULLET2_MAX
bull2_f =[False]*BULLET2_MAX
b_f = 5
e1_hp = 150
lv = 1
e1_x = 200
e1_y = 0
e1_f = [False]
e1_0 = random.uniform(40, 280)
e_damage = 0
color = black
a_s = "ぴえん"
replay = 0
e_s = 10

def set_bullet():#弾のスタン*+*バイ
    global bull_n
    bull_f[bull_n] = True
    bull_x[bull_n] = px-16
    bull_y[bull_n] = py-32
    bull_n = (bull_n+1)%BULLET_MAX

def move_bullet(screen):#弾を飛ばす
    font_b = pygame.font.SysFont("simsun", 20)
    b1 = font_b.render("あ", True, (color))
    hit = font_b.render("１",True,(225,0,0))
    for i in range(BULLET_MAX):
        global e1_x,e1_y,e1_hp,e_damage,a_s,st
        if bull_f[i] == True:
            bull_y[i] = bull_y[i] - 32
            screen.blit(b1,[bull_x[i]+50,bull_y[i]])
            if e1_x+200 > bull_x[i] and e1_x < bull_x[i] and e1_y+200 > bull_y[i] and e1_y < bull_y[i]:
                e1_hp= e1_hp - 1
                if a_s == "ぱおん":
                    a_s = "ぴえん"
                screen.blit(hit,[random.uniform(e1_x+50,e1_x+200),random.uniform(e1_y+75,e1_y+375)])
            if bull_y[i] < 0 or bull_x == px and bull_y == py:
                bull_f[i] = False

def move_player(screen,key):
    global px,py,space,st,speed,b_f,hp,screen_height
    font_player = pygame.font.SysFont("simsun", 25)
    #hp = 100
    if key[pygame.K_UP] == 1:     
        py = py - speed
        if py < 20:
            py = 20
    if key[pygame.K_DOWN] == 1:
        py = py + speed
        if py > screen_height-20:
            py = screen_height-20
    if key[pygame.K_LEFT] == 1:
        px = px - speed
        if px < 20:
            px = 20
    if key[pygame.K_RIGHT] == 1:
        px = px + speed
        if px > 530:
            px = 530
    
    if key[pygame.K_LCTRL] == 1 and st >0 or key[pygame.K_RCTRL] == 1 and st >0:
        speed = 30
        st = st - 1.5
        b_f = 2
     
    else:
        st = st + 0.1
        speed = 10
        b_f = 5

    if key[pygame.K_z] == 1 and st >0:
        st = st - 1
        hp = hp + 0.5

    else:
        st = st +0.1
    
    space = (space+1)*key[pygame.K_SPACE]
    if space%b_f == 1: #5フレーム毎に弾を飛ばす
        set_bullet()

    p1 = font_player.render("（ ´_ゝ`）", True, (color))
    screen.blit(p1, (px-16,py-16))
    
def enemy(screen):
    global e1_x,e1_y,e1_0,e1_hp,tmr,lv,color,st,hp,e_s
    font_title = pygame.font.SysFont("simsun",70)
    if lv == 1:
        tmr = tmr + 1
        if e1_hp > 0:
            screen.blit(img_jiji,(e1_x,e1_y))
            if tmr/30 == 1:
                e1_x = random.uniform(0,300)
                enemy_set()
                tmr = 0
        if e1_hp < -1:
            if tmr/30 == 5:
                e1_hp = 300
                lv = 2
                tmr = 0
                st = st + 50
                hp = hp + 50
                e_s = 20
    
    if lv == 2:
        tmr = tmr + 1
        if e1_hp > 0:
            screen.blit(img_jiji3,(e1_x,e1_y))
            if tmr/30 == 0.1:
                e1_x = random.uniform(-50,400)
                enemy_set()
                tmr = 0
        if e1_hp < -1:
            if tmr/30 == 5:
                e1_hp = 750
                lv = 3
                tmr = 0
                color = white
                st = st + 100
                hp = hp + 100
                e_s = 30
        
    
    if lv == 3:
        tmr = tmr + 1
        if e1_hp > 0:
            screen.blit(img_jiji2,(e1_x,e1_y))
            e1_x = random.uniform(-100,500)
            enemy_set()
            tmr = 0
        if e1_hp < -1:
            if tmr/30 == 5:
                e1_hp = 750
                lv = 3
                tmr = 0

def enemy_set():
    global bull2_n
    bull2_f[bull2_n] = True
    bull2_x[bull2_n] = e1_x+75
    bull2_y[bull2_n] = e1_y+100
    bull2_n = (bull2_n+1)%BULLET2_MAX

def enemy_bullet(screen):
    global px,py,hp,a_s,e_s
    font_e = pygame.font.SysFont("simsun", 25)
    e1_1 = font_e.render(a_s,True,(color))
    for i in range(BULLET2_MAX):
        if bull2_f[i] == True:
            bull2_y[i] = bull2_y[i] + e_s
            screen.blit(e1_1,[bull2_x[i]+50,bull2_y[i]])
            if px < bull2_x[i]+40 and px > bull2_x[i]-40 and py < bull2_y[i]+70 and py > bull2_y[i]-70:
                hp= hp - 1
                if a_s == "ぴえん":
                    a_s = "ぱおん"
            if bull2_y[i] > 730 :#or bull2_x == e1_x and bull2_y == e1_py:
                bull2_f[i] = False
    

def main():
    global idx,cx,cy,hp,st,e1_hp,tmr,screen_height,screen_width
    global lv,px,py,e1_y,e1_x,color,replay
    pygame.init()
    pygame.display.set_caption("普通のシューティングゲーム")
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont("simsun",70)
    font = pygame.font.SysFont("simsun", 40)
    font_h = pygame.font.SysFont("simsun",20) 
    font_n = pygame.font.SysFont("arial", 25)
    text_load = font.render("Now Loading",True,(white))
    text_carsol = font.render("=>",True,(color))

    while True:
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE]==1:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(30)

        if idx == -1:
            idx = 0
            #pygame.mixer.music.load("bgm/moment.wav")
            #pygame.mixer.music.play(-1)
        
        if idx==0:
            if  key[pygame.K_SPACE] == 1 or key[pygame.K_RETURN] == 1 :
                screen.fill(black)
                screen.blit(text_load, (0,screen_height-45))
                pygame.display.update()
                time.sleep(1)
                idx = 0.5
            if key[pygame.K_c] == 1:
                idx = 0.25

            if key[pygame.K_UP]==1 or key[pygame.K_LEFT]==1:
                if cy ==525:
                    cx = 320
                    cy = 475
                if cy == 575:
                    cx = 350
                    cy = 525
            
            if key[pygame.K_DOWN]==1 or key[pygame.K_RIGHT]==1:
                if cy == 475:
                    cx = 350
                    cy = 525
                if cy == 525:
                    cx = 380
                    cy = 575
                      
            screen.fill(white)
            text1 = font_title.render("普通の", True, (color))
            text5 = font_title.render("シューティング", True, (color))
            text2 = font_title.render("ゲーム", True, (color))
            res = font.render("雑魚過ぎて", True, (color))
            res2 = font.render("死んだ回数w  " + str(replay), True, (color))
            help1 = font_h.render("[SPACE]:Start", True, (color))
            help2 = font_h.render("[C]:Option", True, (color))
            screen.blit(text1, (40,30))
            screen.blit(text2, (40,170))
            screen.blit(text5, (40,100))
            screen.blit(help1, (0,screen_height-30))
            screen.blit(help2, (0,screen_height-60))
            if replay >0:
                screen.blit(res, (0,screen_height-355))
                screen.blit(res2, (0,screen_height-280))
            #screen.blit(text_carsol,(cx,cy))
        if idx == 0.25:
            if key[pygame.K_a] == 1:
                idx = 0
            screen.fill(white)
            text1 = font_title.render("普通の", True, (color))
            text5 = font_title.render("シューティング", True, (color))
            text2 = font_title.render("ゲーム", True, (color))
            res = font.render("雑魚過ぎて", True, (color))
            screen.blit(text1, (40,30))
            screen.blit(text2, (40,170))
            screen.blit(text5, (40,100))
        if idx == 0.5:
            idx = 1
            #pygame.mixer.music.load("OneDrive/ドキュメント/phython/シューティング/bgm/カービィ.wav")
            #pygame.mixer.music.play(-1)
        if idx == 1:
            if lv == 1 or 2:
                screen.fill(white)
            if lv == 3 :
                screen.fill(black)
            text_hp = font_n.render("HP  "+str(math.floor(hp)),True,(color))
            screen.blit(text_hp,(0,0))
            text_ehp = font_n.render("HP  "+str(e1_hp),True,(color))
            screen.blit(text_ehp,(550,0))
            text_ehp = font_n.render("Lv  "+str(lv),True,(color))
            screen.blit(text_ehp,(550,30))
            text_st = font_n.render("ST  "+str(math.floor(st)),True,(color))
            screen.blit(text_st,(0,30))
            text_st = font_n.render("TMR  "+str(b_f),True,(color))
            screen.blit(text_st,(0,60))
            help2 = font_h.render("[SPACE]:撃つ", True, (color))
            help3 = font_h.render("[Ctrl]:バースト", True, (color))
            help4 = font_h.render("[Z]:回復", True, (color))
            help = font_h.render("[Arrow]:移動", True, (color))
            screen.blit(help,(0,screen_height-120))
            screen.blit(help2,(0,screen_height-90))
            screen.blit(help3,(0,screen_height-60))
            screen.blit(help4,(0,screen_height-30))
            move_player(screen,key)
            move_bullet(screen)
            enemy(screen)
            enemy_bullet(screen)
            if hp<1:
                idx =2
                hp = 0
        
        if idx == 2:
            screen.fill(black)
	    #pygame.mixer.music.load("カービィ.wav")
	    #pygame.mixer.music.stop(-1)
            text_gameover = font_title.render("GAMEOVER",True,(white))
            screen.blit(text_gameover,(screen_width/4,screen_height/2))
            text_www = font_n.render("WWW",True,(white))
            screen.blit(text_www,(random.uniform(0, 501),random.uniform(0, 700)))
            text_zako = font.render("雑魚乙w",True,(white))
            help5 = font_h.render("[R]:リスタート", True, (white))
            screen.blit(help5,(0,screen_height-30))
            screen.blit(text_zako,(random.uniform(0, 501),random.uniform(0, screen_height-30)))
            screen.blit(text_zako,(random.uniform(0, 501),random.uniform(0, screen_height-30)))
            screen.blit(text_www,(random.uniform(0, 501),random.uniform(0, screen_height-30)))
            screen.blit(text_www,(random.uniform(0, 501),random.uniform(0, screen_height-30)))
            screen.blit(text_www,(random.uniform(0, 501),random.uniform(0, screen_height-30)))
            if key[pygame.K_r]==1 :
                idx=-1
                tmr = 0
                hp = 100
                st = 200
                px = 320 #プレイヤーのX座標
                py = screen_height-130 #プレイヤーのY座標
                cx = 320
                cy = 475
                e1_hp = 150
                lv = 1
                e1_x = 200
                e1_y = 0
                color = black
                replay = replay + 1

if __name__ == "__main__":
    main()