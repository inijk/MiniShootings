import pygame
import sys
import random
import math

red = (255,0,0) #カラー変数
green = (0,255,0)
lightgreen = (0,200,200)
blue = (0,0,255)
yellow = (255,255,0)
white = (255,255,255)
black = (0,0,0)
idx = 0 #システム変数
stage = 0
timer = 0
HEIGHT = 600
B_WIDTH = 100
WIDTH = HEIGHT - B_WIDTH
SCORE = 0
PLAYTIME = 0
shot_bool = 0
shot_time = 0
flamerate = 600
bg_color = white
px = WIDTH/2 #プレーヤー変数
py = HEIGHT-200
p_hp_max = 100
p_hp = p_hp_max
p_speed = 0.5
p_size = 25
hit = False
status = 0
p_invincible = 0
p_color = green
weapon = 0
overheat = 0
breaktime =0
BREAK = False
combo = 0
bx = 0 #弾変数
by = 0
bullet_time = 0
b_inter = 0
b_oh = 0
b_size = 5
b_sp = 5
b_atk = 1
BULLET_MAX = 100
bull_n = 0
bull_x =[0]*BULLET_MAX
bull_y =[0]*BULLET_MAX
bullet_angle =[0]*BULLET_MAX
bull_mx = [0]*BULLET_MAX
bull_my = [0]*BULLET_MAX
bull_bx = [0]*BULLET_MAX
bull_by = [0]*BULLET_MAX
bull_bbx = [0]*BULLET_MAX
bull_bby = [0]*BULLET_MAX
bull_bc = [0]*BULLET_MAX
bull_f =[False]*BULLET_MAX
bound_max = 5
mouse_x = None
mouse_y = None
ex = 0 #敵変数
ey = 0
ENEMY_MAX = 200
ENEMY_BULLET = 1
ebull_n = 0
ebull_x =[0]*ENEMY_MAX
ebull_y =[0]*ENEMY_MAX
ebull_a = [0]*ENEMY_MAX
e_size = [0]*ENEMY_MAX
ebull_hit = [0]*ENEMY_MAX
ebull_hp = [0]*ENEMY_MAX
ebull_angle = [0]*ENEMY_MAX
enemy_ang = [0]*ENEMY_MAX
ebull_f =[False]*ENEMY_MAX
ebull_f2 = [False]*ENEMY_MAX
e_list = [0]*ENEMY_MAX
e_speed = [0]*ENEMY_MAX
e_type = [0]*ENEMY_MAX
en_speed = 0.125
etype = 1
e_count = 0
enemy_time = 0
e_cooltime = 0.5
boss_hp = 0 #ボス変数
boss_type = 0
boss_x = 0
boss_y = 0
boss_inter = 0
boss_size = 100
boss_move = 0

class Player:
    def move_player(screen,key,mouse):
        global px,py,p_speed,p_size,space,bullet_time,overheat
        global status,p_hp,p_invincible,p_color,combo,breaktime
        global b_inter,b_oh,b_size,shot_bool,shot_time,weapon
        global BREAK,WIDTH,HEIGHT,PLAYTIME
        if key[pygame.K_UP] == 1 or key[pygame.K_w] == 1:
            py = py - p_speed
            if py < 0:
                py = 0
        if key[pygame.K_DOWN] == 1 or key[pygame.K_s] == 1:
            py = py + p_speed
            if py > HEIGHT - B_WIDTH - p_size:
                py = HEIGHT - B_WIDTH - p_size
        if key[pygame.K_LEFT] == 1 or key[pygame.K_a] == 1:
            px = px - p_speed
            if px < 0:
               px = 0
        if key[pygame.K_RIGHT] == 1 or key[pygame.K_d] == 1:
            px = px + p_speed
            if px > WIDTH - p_size :
                px = WIDTH - p_size
        if key[pygame.K_SPACE] == 1 or mouse[0]:
            shot_bool = 1
        else: shot_bool = 0
        shot_time = (shot_time+1)*shot_bool
        if status != 1:
            #if weapon == 0:b_inter = 100
            if shot_time%b_inter == 1:
                Bullet.set_bullet()
                overheat += b_oh
        if shot_time%5 == 1 and status == 1:
            overheat -= 0.1
            if p_invincible == 0:
                p_color = red
        if key[pygame.K_SPACE] != 1:
            if int(PLAYTIME/10)%10 == 1 and overheat > 0:
                overheat -= 0.1
        if int(PLAYTIME/10)%10 == 1 and BREAK == False:
            breaktime -= breaktime/200 + 0.1
        if overheat >= 100:
            status = 1
            p_color = red
        if overheat <= 0:
            status = 0
            p_color = green
        if breaktime > 100:
            breaktime = 99
            BREAK = True
        if status == 1: p_color = red
        if BREAK == True:#Break
            if weapon == 0 and int(PLAYTIME/10)%20 == 1 and p_hp<p_hp_max:
                p_hp +=0.5
            if weapon == 1:
                p_color = yellow
                if p_invincible == 0:
                        p_invincible = flamerate
            if weapon == 2:
                p_color = lightgreen
                overheat = 0
                #breaktime += 0.005
            if weapon == 3:
                b_size = 30
            breaktime -=0.04
        if int(PLAYTIME/10)%40 == 1 and p_hp<p_hp_max/4: p_hp += 0.05
        if breaktime <= 0.1:
            BREAK = False
            p_color = green
            if weapon == 3: b_size = 15
        if p_invincible%2 == 0:#無敵状態なら点滅させる
            pygame.draw.ellipse(screen,(p_color),(px,py,p_size,p_size))
        if p_invincible > 0:
            p_invincible = p_invincible - 1#無敵時は当たり判定を無効にする
            return
        for i in range(ENEMY_MAX):
            if ebull_f[i] == True:
                w = e_size[i]
                h = e_size[i]
                r = int((w+h)/4+(32+32)/4)
                if distance(ebull_x[i],ebull_y[i],px,py) < r*r:#敵及び敵の攻撃に接触
                    p_hp = p_hp - 20#ダメージを受ける
                    if p_invincible == 0:
                        p_invincible = flamerate#無敵時間
                    ebull_f[i] = False
                    ebull_f2[i] = False
                    breaktime -= breaktime/2
                    combo = 0

class Bullet:
    def set_bullet():#弾のスタンバイ
        global bull_n,b_speed,b_sp,p_size
        bull_f[bull_n] = True
        bull_x[bull_n] = px + p_size/2
        bull_y[bull_n] = py + p_size/2
        bull_mx[bull_n] ,bull_my[bull_n] = pygame.mouse.get_pos()
        bull_bx[bull_n] = False
        bull_by[bull_n] = False
        bull_bbx[bull_n] = 0
        bull_bby[bull_n] = 0             
        bull_bc[bull_n] = 0
        bull_n = (bull_n+1)%BULLET_MAX
        b_speed = b_sp 
        mouse_x,mouse_y = pygame.mouse.get_pos()
        bullet_angle[bull_n-1] = math.atan2(
            mouse_y - py - p_size/2,
            mouse_x - px - p_size/2
        )

    def move_bullet(screen):#弾を飛ばす
        global bull_mx,bull_x,bull_bx,bull_bbx,bull_bby
        #font00 = pygame.font.SysFont("hg正楷書体pro", 25) #フォント、テキスト設定
        #text00 = font00.render("💩", True, (black))
        for i in range(BULLET_MAX):
            if bull_f[i] == True:
                if bull_x[i] < b_size or bull_x[i] > WIDTH - b_size:
                    if bull_bx[i] == True:
                        bull_bx[i] = False
                        bull_bbx[i] = 1
                    if bull_bx[i] == False and bull_bbx[i] == 0: 
                        bull_bx[i] = True
                    if bull_bc[i] == 0:
                        bull_bx[i] = True
                    bull_bc[i] += 1
    
                if bull_y[i] < b_size or bull_y[i] > HEIGHT - B_WIDTH - b_size:
                    if bull_by[i] == True:
                        bull_by[i] = False
                        bull_bby[i] = 1
                    if bull_by[i] == False and bull_bby[i] == 0: 
                        bull_by[i] = True
                    if bull_bc[i] == 0:
                        bull_by[i] = True
                    bull_bc[i] += 1
                if bull_bx[i] == True:#x跳ね返り
                    bull_mx[i] = -b_speed * math.cos(bullet_angle[i])
                if bull_by[i] == True:#y跳ね返り
                    bull_my[i] = -b_speed * math.sin(bullet_angle[i])
                if bull_bx[i] == False:
                    bull_mx[i] = b_speed * math.cos(bullet_angle[i])
                if bull_by[i] == False:
                    bull_my[i] = b_speed * math.sin(bullet_angle[i])
                if bull_bc[i] > bound_max:
                    bull_f[i] = False
                bull_x[i] =bull_x[i] + bull_mx[i]/3
                bull_y[i] =bull_y[i] + bull_my[i]/3
                pygame.draw.ellipse(screen,(black),(bull_x[i],bull_y[i],b_size,b_size))

class Enemy:
    def set_enemy(x,y,a,enemy,speed,etype):
        global ebull_n
        if etype == 2:
            e_hp = 5
        else: e_hp = 1
        while True:
            if ebull_f[ebull_n] == False:
                ebull_f[ebull_n] = True
                ebull_x[ebull_n] = x
                ebull_y[ebull_n] = y
                ebull_a[ebull_n] = a
                ebull_hp[ebull_n] = e_hp
                e_list[ebull_n] = enemy
                e_speed[ebull_n] = speed
                e_type[ebull_n] = etype
                e_size[ebull_n] = 15
                ebull_hit[ebull_n] = False
                break
            ebull_n = (ebull_n+1)%ENEMY_MAX
        enemy_ang[ebull_n] = math.atan2(
            py + p_size/2 - y,
            px + p_size/2 - x
        )

    def move_enemy(screen):
        global idx,px,py,p_hp,hit,SCORE,breaktime,combo,status,e_count,BREAK
        for i in range(ENEMY_MAX):
            if ebull_f[i] == True:
                if ebull_f[i] == True:
                    ebull_angle[i] = math.atan2(
                        py + p_size/2 - ebull_y[i] - e_size[i]/2,
                        px + p_size/2 - ebull_x[i] - e_size[i]/2)
                    if e_type[i] == 0:
                        e_size[i] = 15
                        ebull_x[i] = ebull_x[i] + e_speed[i]*math.cos(ebull_angle[i])
                        ebull_y[i] = ebull_y[i] + e_speed[i]*math.sin(ebull_angle[i])
                    if e_type[i] == 1:
                        e_size[i] = 15
                        ebull_x[i] = ebull_x[i] + e_speed[i]*math.cos(enemy_ang[i])*5
                        ebull_y[i] = ebull_y[i] + e_speed[i]*math.sin(enemy_ang[i])*5
                    if e_type[i] == 2:
                        e_size[i] = 30
                        ebull_x[i] = ebull_x[i] + e_speed[i]*math.cos(enemy_ang[i])*0.3
                        ebull_y[i] = ebull_y[i] + e_speed[i]*math.sin(enemy_ang[i])*0.3
                if ebull_x[i] < -40 or ebull_x[i] > WIDTH or ebull_y[i] < -40 or ebull_y[i] > HEIGHT:#画面外に敵が消える
                    ebull_f[i] = False
                    ebull_f2[i] = False
                if e_list[i] != ENEMY_BULLET:
                    w = e_size[i]
                    h = e_size[i]
                    r = int((w+h)/4)+8
                    for n in range(BULLET_MAX):
                        if bull_f[n] == True and distance(ebull_x[i]+e_size[i]/2,ebull_y[i]+e_size[i]/2,bull_x[n]+b_size/2,bull_y[n]+b_size/2)<r*r:
                            if not (weapon == 1 or weapon == 3):
                                bull_f[n] = False
                            ebull_hp[i] -= b_atk/3
                            combo +=0.5
                            if ebull_hp[i] <= 0:
                                ebull_f[i] = False
                                ebull_f2[i] = False
                                ebull_x[i] = WIDTH
                                ebull_y[i] = HEIGHT
                                e_count += 1 #e_type[i]
                                combo += e_type[i]
                            if BREAK == False:
                                if weapon == 2:
                                    breaktime += 0.1+0.1*combo
                                else: breaktime += 7+1.1*combo
                            SCORE += 100
                pygame.draw.ellipse(screen,(blue),(ebull_x[i]-2.5,ebull_y[i]-2.5,e_size[i],e_size[i]))

class Boss:
    def set_boss(boss_type):
        global boss_hp,boss_x,boss_y,boss_size,boss_move,text_boss
        if boss_type == 0:
            boss_hp = 100
            boss_size = 30
            boss_x = 200
            boss_y = 50
            boss_move = 0
            font_boss = pygame.font.SysFont("hg正楷書体pro",boss_size)
            text_boss = font_boss.render("(ﾟДﾟ*)ﾉ", True, (black))
        if boss_type == 1:
            boss_hp = 150
            boss_size = 30
            boss_x = 200
            boss_y = 50
            boss_move = 0
            font_boss = pygame.font.SysFont("hg正楷書体pro",boss_size)
            text_boss = font_boss.render("щ(゜ロ゜щ)", True, (black))
    def move_boss(screen):
        global combo,breaktime,boss_hp,idx,boss_x,boss_move,etype
        if boss_type == 0:
            if boss_move == 0: 
                boss_x += 0.5
                if PLAYTIME%flamerate/7 == 1:
                    Enemy.set_enemy(boss_x+boss_size*3.5/2,boss_y+boss_size,90,0,en_speed,0)
            if boss_move == 1: 
                boss_x -= 0.5
                if PLAYTIME%flamerate/2 == 1:
                    Enemy.set_enemy(boss_x+boss_size*3.5/2,boss_y+boss_size,90,0,en_speed,1)
            if boss_x >= WIDTH -boss_size*3.5: boss_move = 1
            if boss_x <= 0: boss_move = 0
            for n in range(BULLET_MAX):
                        if bull_f[n] == True and bull_x[n]+b_size  >= boss_x and bull_x[n] <= boss_x + boss_size*3.5 and bull_y[n] <= boss_y + boss_size and bull_y[n]+b_size >= boss_y:
                            if weapon == 0 or weapon == 2:
                                bull_f[n] = False
                                if BREAK == False:
                                    if weapon == 0:
                                        combo +=1
                                        breaktime += 7+int(0.75*combo)
                                    if weapon == 2:
                                        breaktime += 0.015+0.075*combo
                                        combo += b_atk
                            else:
                                combo += b_atk*0.075
                                if BREAK == False:
                                    breaktime += 0.05+1.1*combo
                            boss_hp -= b_atk
                            
            pygame.draw.rect(screen,(red),(70,7,boss_hp*3.7,15))
            screen.blit(text_boss,(boss_x,boss_y))
        if boss_hp <= 0:
            idx = 2
            

def distance(x1,y1,x2,y2):
    return ((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))

def reset():
    global px,py,p_speed,p_size,timer,bullet_time,overheat
    global status,p_hp,p_invincible,p_color,combo,breaktime
    global bull_mx,bull_x,bull_bx,bull_bbx,bull_bby,bull_f
    global bull_n,b_speed,b_size,ebull_f,ebull_f2,e_count
    global boss_hp
    global SCORE,WIDTH,HEIGHT,PLAYTIME
    px = WIDTH/2 #プレーヤー変数
    py = HEIGHT-200
    p_hp_max = 100
    p_hp = p_hp_max
    p_speed = 0.5
    p_size = 25
    p_color = green
    e_count = 0
    bull_f =[False]*BULLET_MAX
    ebull_f =[False]*ENEMY_MAX
    ebull_f2 = [False]*ENEMY_MAX
    #hit = False
    SCORE = 0
    timer = 0
    boss_hp = 1
    status = p_invincible = overheat = breaktime = combo = 0

def ui(screen,scr,font_score):
    global idx,p_hp,p_hp_max,bg_color
    pygame.draw.rect(screen,(black),(0,HEIGHT - B_WIDTH,WIDTH,B_WIDTH))
    pygame.draw.rect(screen,(lightgreen),(10,HEIGHT - B_WIDTH+10,p_hp*2,15))
    pygame.draw.rect(screen,(red),(10,HEIGHT - B_WIDTH+30,overheat*2,15))
    pygame.draw.rect(screen,(yellow),(10,HEIGHT - B_WIDTH+50,breaktime*2,15))
    text_score = font_score.render("SCORE:" + str(SCORE),True,(white))
    text_combo = font_score.render("COMBO:" + str(int(combo)),True,(white))
    screen.blit(text_score,(WIDTH - 220,HEIGHT - B_WIDTH+5))
    screen.blit(text_combo,(WIDTH - 220,HEIGHT - B_WIDTH+55))
    bg_color = white
    if p_hp <= p_hp_max/4:
        scr.fill((255,0,0,128))
        screen.blit(scr,(0,0))
    if BREAK == True:
        scr.fill((255,255,0,128))
        screen.blit(scr,(0,0)) 

def tip(screen,word,x,y):
    font_tip = pygame.font.SysFont("hg正楷書体pro",20)
    text = font_tip.render(word,True,(white))
    screen.blit(text(x,y))

def main():
    global idx,flamerate,enemy_time,p_hp,overheat,combo
    global WIDTH,HEIGHT,SCORE,PLAYTIME,white,p_hp_max
    global e_cooltime,stage,en_speed,weapon,screen,timer
    global b_inter,b_oh,bound_max,b_size,b_sp,b_atk,etype
    pygame.init() #システム設定
    pygame.display.set_caption("タダサバイバー")
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    scr =pygame.Surface((WIDTH,HEIGHT),flags=pygame.SRCALPHA)
    clock = pygame.time.Clock()
    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    key_time = flamerate
    font_title = pygame.font.SysFont("hg正楷書体pro", 70) #フォント、テキスト設定
    font_result = pygame.font.SysFont("ocraextended", 70)
    font_score = pygame.font.SysFont("ocraextended",35)
    font_text = pygame.font.SysFont("ocraextended",20)
    font_tutorial = pygame.font.SysFont("hg正楷書体pro",20)
    font_help = pygame.font.SysFont("hg正楷書体pro",18)
    text_title = font_title.render("タダサバイバー", True, (white))
    text_gameover = font_result.render("GAMEOVER",True,(white))
    text_clear = font_result.render("CLEAR",True,(black))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or key[pygame.K_ESCAPE] == 1 and key[pygame.K_LSHIFT] == 1:
                pygame.quit()
                sys.exit()
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        if idx == 0:#title
            bg_color = black
            screen.blit(text_title,(text_title.get_rect(center=(WIDTH//2, HEIGHT//2-100))))
            if int(PLAYTIME*3/flamerate)%4 == 1:
                help_color = black
            else: help_color = white
            text_begin = font_text.render("Press space or return to play.",True,(help_color))
            screen.blit(text_begin,(text_begin.get_rect(center=(WIDTH//2, HEIGHT//2 -28))))
            if key[pygame.K_SPACE] == 1 or key[pygame.K_RETURN] == 1:
                idx = 0.1
                key_time = 0
        if idx == 0.1:#stage select
            bg_color = black
            screen.blit(text_title,(text_title.get_rect(center=(WIDTH//2, HEIGHT//2-100))))
            text_ss = font_text.render("Select a stage.",True,(white))
            screen.blit(text_ss,(text_ss.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))))
            if key_time == flamerate/4 and stage < 10 and (key[pygame.K_RIGHT] == 1 or key[pygame.K_d]) == 1: 
                    key_time = 0
                    stage += 1
            if key_time == flamerate/4 and stage >= 1 and (key[pygame.K_LEFT] == 1 or key[pygame.K_a]) == 1:
                stage -= 1
                key_time = 0
            if key_time > flamerate/4: key_time = flamerate/4
            if stage <=10 and key_time == flamerate/4 and (key[pygame.K_SPACE] == 1 or key[pygame.K_RETURN] == 1):
                idx = 0.2
                key_time = 0
            if stage == 0:
                text_tip = font_tutorial.render("※チュートリアル 敵を20体倒すとクリア",True,(white))
                tutorial = 0
            if stage == 1:
                text_tip = font_tutorial.render("敵を30体倒すとクリア",True,(white))
            if stage == 2:
                text_tip = font_tutorial.render("敵を50体倒すとクリア",True,(white))
            if stage == 3:
                text_tip = font_tutorial.render("1分間逃げ切るとクリア",True,(white))
            if stage == 4:
                text_tip = font_tutorial.render("Overheatなしで30体倒すとクリア",True,(white))
            if stage == 5:
                text_tip = font_tutorial.render("BOSSを倒すとクリア",True,(white))
            if stage == 6:
                text_tip = font_tutorial.render("100体倒すとクリア",True,(white))
            if stage == 7:
                text_tip = font_tutorial.render("1分間逃げ切るとクリア",True,(white))
            if stage == 8:
                text_tip = font_tutorial.render("200体倒すとクリア",True,(white))
            if stage == 9:
                text_tip = font_tutorial.render("BOSSを倒すとクリア",True,(white))
            if stage == 10:
                text_tip = font_tutorial.render("頑張ればクリア",True,(white))
            if not stage <= 10: 
                text_tip = font_tutorial.render("開発中…",True,(white))
            if key_time == flamerate/4 and key[pygame.K_ESCAPE] == 1:
                key_time = 0
                idx = 0
            key_time += 1
            if key_time > flamerate/4: key_time = flamerate/4
            text_stage = font_score.render("Stage " + str(stage),True,(white))
            screen.blit(text_tip,(text_tip.get_rect(center=(WIDTH//2, HEIGHT-50))))
            screen.blit(text_stage,(text_stage.get_rect(center=(WIDTH//2, HEIGHT//2 + 160))))
        if idx == 0.2:#weapon select
            bg_color = black
            if key_time == flamerate/4 and weapon < 5 and (key[pygame.K_RIGHT] == 1 or key[pygame.K_d]) == 1: 
                key_time = 0
                weapon += 1
            if key_time == flamerate/4 and weapon >= 1 and (key[pygame.K_LEFT] == 1 or key[pygame.K_a]) == 1:
                weapon -= 1
                key_time = 0
            if (weapon <= 3) and key_time == flamerate/4 and (key[pygame.K_SPACE] == 1 or key[pygame.K_RETURN] == 1):
                key_time = 0
                bg_color = white
                if stage < 1:
                    tutorial = 0
                    idx = 0.5
                else: idx = 1
                if stage == 5:
                    Boss.set_boss(0)
                if stage == 9:
                    Boss.set_boss(1)
                if stage == 10:
                    Boss.set_boss(0)
                    Boss.set_boss(1)
            if weapon == 0:
                text_tip = font_tutorial.render("弾が3回跳ね返り,Break状態になるとHPが回復します",True,(white))
                text_tip1 = font_text.render("Bound x3",True,(white))
                text_tip2 = font_text.render("Normal",True,(white))
                text_tip3 = font_text.render("Healing",True,(white))
                b_inter = 100
                b_oh = 2
                bound_max = 5
                b_size = 6
                b_sp = 5
                b_atk = 3
            if weapon == 1:
                text_tip = font_tutorial.render("弾が貫通し,Break状態になると無敵状態になります",True,(white))
                text_tip1 = font_text.render("Penetrate",True,(white))
                text_tip2 = font_text.render("Large",True,(white))
                text_tip3 = font_text.render("Invincible",True,(white))
                b_inter = 130
                b_oh = 3
                bound_max = 0
                b_size = 5
                b_sp = 6
                b_atk = 1
            if weapon == 2:
                text_tip = font_tutorial.render("連結した弾を放ち,Break時にOverheatを全回復します。",True,(white))
                text_tip1 = font_text.render("Beam",True,(white))
                text_tip2 = font_text.render("Large",True,(white))
                text_tip3 = font_text.render("Cooltime",True,(white))
                b_inter = 2
                b_oh = 0.2
                bound_max = 0
                b_size = 4
                b_sp = 4
                b_atk = 0.15
            if weapon == 3:
                text_tip = font_tutorial.render("大きく遅い弾を放ち,Break時に弾が大きくなります。",True,(white))
                text_tip1 = font_text.render("Slow",True,(white))
                text_tip2 = font_text.render("Large",True,(white))
                text_tip3 = font_text.render("Big&Huge",True,(white))
                b_inter = 170
                b_oh = 7
                bound_max = 20
                b_size = 15
                b_sp = 0.75
                b_atk = 0.05
            if weapon == 5:
                text_tip = font_tutorial.render("速度、大きさなどすべてがランダムな武器です",True,(white))
                text_tip1 = font_text.render("Random",True,(white))
                text_tip2 = font_text.render("Random",True,(white))
                text_tip3 = font_text.render("Random",True,(white))
                b_inter = random.randint(80,140)
                b_oh = random.randint(0,5)
                bound_max = random.randint(0,5)
            if not (weapon <= 3 or weapon == 5): 
                text_tip = font_tutorial.render("開発中…",True,(white))
                text_tip1 = font_text.render("???",True,(white))
                text_tip2 = font_text.render("???",True,(white))
                text_tip3 = font_text.render("???",True,(white))
            if key_time == flamerate/4 and key[pygame.K_ESCAPE] == 1:
                key_time = 0
                idx = 0.1
            text_weapon = font_text.render("Weapon " + str(weapon),True,(white))
            text_ws = font_text.render("Select your weapon.",True,(white))
            text_wt1 = font_text.render("BulletType :",True,(white))
            text_wt2 = font_text.render("OverHeat   :",True,(white))
            text_wt3 = font_text.render("BreakSkill :",True,(white))
            screen.blit(text_wt1,(WIDTH//2-140, HEIGHT//2 + 122))
            screen.blit(text_wt2,(WIDTH//2-140, HEIGHT//2 + 144))
            screen.blit(text_wt3,(WIDTH//2-140, HEIGHT//2 + 166))
            screen.blit(text_tip1,(WIDTH//2+20, HEIGHT//2 + 122))
            screen.blit(text_tip2,(WIDTH//2+20, HEIGHT//2 + 144))
            screen.blit(text_tip3,(WIDTH//2+20, HEIGHT//2 + 166))
            screen.blit(text_ws,(text_ws.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))))
            screen.blit(text_weapon,(text_weapon.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))))
            screen.blit(text_tip,(text_tip.get_rect(center=(WIDTH//2, HEIGHT-50))))
            screen.blit(text_title,(text_title.get_rect(center=(WIDTH//2, HEIGHT//2-100))))
            key_time += 1
            if key_time > flamerate/4: key_time = flamerate/4
        if idx == 0.5:#tutorial
            Player.move_player(screen,key,mouse)
            ui(screen,scr,font_score)
            if tutorial == 0:
                text1 = font_tutorial.render("矢印、WASDで移動",True,(black))
                if key_time == flamerate/4 and key[pygame.K_RETURN] == 1:
                    key_time = 0
                    tutorial = 1
                if key_time == flamerate/4 and key[pygame.K_ESCAPE] == 1:
                    idx = 0.2
            if tutorial == 1:
                text1 = font_tutorial.render("[SPACE]でマウスの方向に弾を撃つ",True,(black))
                text2 = font_tutorial.render("打ち続けると赤いゲージ(OverHeat)が貯まり、",True,(black))
                text3 = font_tutorial.render("MAXになるとゲージがなくなるまで弾を撃てなくなる",True,(black))
                screen.blit(text2,(0,23))
                screen.blit(text3,(0,46))
                Bullet.move_bullet(screen)
                if key_time == flamerate/4 and key[pygame.K_RETURN] == 1:
                    key_time = 0
                    tutorial = 2
                    e_cooltime = flamerate/2
            if tutorial == 2:
                text1 = font_tutorial.render("敵を撃つと黄色いゲージ(Break)とComboが貯まる",True,(black))
                text2 = font_tutorial.render("MAXになるとBreak状態となる",True,(black))
                text3 = font_tutorial.render("敵に触れるとHP,Break,Comboは減少する",True,(black))
                screen.blit(text2,(0,23))
                screen.blit(text3,(0,46))
                Bullet.move_bullet(screen)
                Enemy.move_enemy(screen)
                if key_time == flamerate/4 and key[pygame.K_RETURN] == 1:
                    key_time = 0
                    tutorial = 3
                if e_cooltime > flamerate/2 and int(PLAYTIME/flamerate)%5 == 1:
                    e_cooltime = 0
                    en_speed = etype = 0
                    Enemy.set_enemy(random.randint(0,WIDTH),150,90,0,en_speed,etype)
                e_cooltime += 1
            if tutorial == 3:
                text1 = font_tutorial.render("チュートリアルは終了です",True,(black))
                text2 = font_tutorial.render("早速、敵を20体倒してみましょう",True,(black))
                screen.blit(text2,(0,23))
                Bullet.move_bullet(screen)
                etype = 0
                if key_time == flamerate/4 and key[pygame.K_RETURN] == 1:
                    key_time = 0
                    tutorial = 2
                    e_cooltime = 0
                    idx = 1
                    reset()
            if weapon == 5:
                b_inter = random.randint(80,140)
                b_oh = random.randint(0,5)
                bound_max = random.randint(1,6)
                b_size = random.randint(2,30)
            if int(PLAYTIME*2/flamerate)%2 == 1:
                help_color = white
            else: help_color = black
            text = font_help.render("エンターキーで次に進む",True,(help_color))
            screen.blit(text,(7,HEIGHT-22))
            screen.blit(text1,(0,0))
            if key_time == flamerate/4 and key[pygame.K_ESCAPE] == 1:
                key_time = 0
                tutorial -= 1
            key_time += 1
            if key_time > flamerate/4: key_time = flamerate/4
            #screen.blit(text,(0,38))
        if idx == 1:#game
            help_color = white
            if stage == 0:
                e_cooltime = 2
                goal_score = 20
                text = font_help.render("敵を"+str(goal_score-e_count)+"体倒す",True,(help_color))
            if stage == 1:
                e_cooltime = 1
                goal_score = 30
                text = font_help.render("敵を"+str(goal_score-e_count)+"体倒す",True,(help_color))
            if stage == 2:
                e_cooltime = 0.75
                goal_score = 50
                text = font_help.render("敵を"+str(goal_score-e_count)+"体倒す",True,(help_color))
            if stage == 3:
                e_cooltime = 0.3
                goal_score = 100000
                text = font_help.render("残り"+str(60-int(timer))+"秒耐える",True,(help_color))
                if timer > 60:
                    key_time = 0
                    idx = 2
            if stage == 4:
                e_cooltime = 0.65
                goal_score = 30
                text = font_help.render("敵を"+str(goal_score-e_count)+"体倒す(OH禁止)",True,(help_color))
                if overheat >= 100:
                    key_time = 0
                    idx = 3
            if stage == 5:
                e_cooltime = 100000
                goal_score = 10000000
                text = font_help.render("BOSS敵を倒す",True,(help_color))
                text_bh = font_help.render("BOSS:",True,(black))
                screen.blit(text_bh,(5,5))
                Boss.move_boss(screen)
            if stage == 6:
                e_cooltime = 0.4
                goal_score = 100
                text = font_help.render("敵を"+str(goal_score-e_count)+"体倒す",True,(help_color))
                if enemy_time%int(flamerate*e_cooltime*3) == 1:
                    for i in range(5):
                        Enemy.set_enemy(random.randint(0,WIDTH),-10,90,0,en_speed,1)
            if stage == 7:
                e_cooltime = 0.3
                goal_score = 100000
                overheat = 100
                text = font_help.render("残り"+str(60-int(timer))+"秒耐える",True,(help_color))
                if enemy_time%int(flamerate*e_cooltime*4) == 1:
                    for i in range(3):
                        Enemy.set_enemy(random.randint(0,WIDTH),-10,90,0,en_speed,1)
                if timer > 60:
                    key_time = 0
                    idx = 2
            if stage == 8:
                e_cooltime = 0.2
                goal_score = 200
                text = font_help.render("敵を"+str(goal_score-e_count)+"体倒す",True,(help_color))
                if enemy_time%int(flamerate*e_cooltime*4) == 1:
                    for i in range(5):
                        Enemy.set_enemy(random.randint(0,WIDTH),-10,90,0,en_speed,1)
            if stage == 9:
                goal_score = 10000000
                text = font_help.render("BOSS敵を倒す",True,(help_color))
                text_bh = font_help.render("BOSS:",True,(black))
                screen.blit(text_bh,(5,5))
                Boss.move_boss(screen)
            if stage == 10:
                goal_score = 10000000
                e_cooltime = 0.1
                text = font_help.render("BOSS敵を倒す",True,(help_color))
                text_bh = font_help.render("BOSS:",True,(black))
                screen.blit(text_bh,(5,5))
                Boss.move_boss(screen)
                if enemy_time%int(flamerate*e_cooltime*4) == 1:
                    for i in range(10):
                        Enemy.set_enemy(random.randint(0,WIDTH),-10,90,0,en_speed,1)
            if enemy_time%int(flamerate*e_cooltime)==1 and (stage < 5 or (stage > 5 and stage != 9)):
                if stage == 0:
                    etype = 1
                    en_speed = 0.05
                if stage < 3:
                    ENEMY_MAX = 100
                    etype = 0
                elif stage < 5:
                    ENEMY_MAX = 100
                    etype = 1
                elif (stage < 9) and stage != 5:
                    etype = 0
                    ENEMY_MAX = 200
                    if random.randint(0,5) > 3:
                        etype = 1
                    if random.randint(0,5) == 3:
                        etype = 2
                    if random.randint(0,5) < 3:
                        etype = 0
                if stage == 10:
                    ENEMY_MAX = 250
                    if random.randint(0,5) > 3:
                        etype = 1
                    if random.randint(0,5) == 3:
                        etype = 2
                    if random.randint(0,5) < 3:
                        etype = 0
                Enemy.set_enemy(random.randint(0,WIDTH),-10,90,0,en_speed,etype)
            if weapon == 5:
                b_inter = random.randint(80,140)
                b_oh = random.randint(0,5)
                bound_max = random.randint(1,6)
                b_size = random.randint(2,30)
            if e_count >= goal_score: 
                key_time = 0
                idx = 2
            if p_hp <= 0: 
                key_time = 0
                idx = 3
            if e_cooltime >= 20: e_cooltime=0.75
            if key_time == flamerate/4 and key[pygame.K_ESCAPE] == 1:
                key_time = 0
                reset()
                idx = 0.2
            key_time += 1
            if key_time > flamerate/4: key_time = flamerate/4
            Player.move_player(screen,key,mouse)
            Bullet.move_bullet(screen)
            Enemy.move_enemy(screen)
            ui(screen,scr,font_score)
            screen.blit(text,(7,HEIGHT-22))
            enemy_time +=1
            timer += 1/flamerate 
        if idx == 2:#clear
            screen.blit(text_clear,(text_clear.get_rect(center=(WIDTH//2, HEIGHT//2))))
            if int(PLAYTIME*3/flamerate)%4 == 1:
                help_color = white
            else: help_color = black
            text_begin = font_text.render("Press space or return to back.",True,(help_color))
            screen.blit(text_begin,(text_begin.get_rect(center=(WIDTH//2, HEIGHT//2 +50))))
            key_time += 1
            if key_time > flamerate/4: key_time = flamerate/4
            if key_time == flamerate/4 and (key[pygame.K_ESCAPE] or key[pygame.K_RETURN] or key[pygame.K_SPACE] == 1):
                reset()
                idx = 0.1
        if idx == 3:#gameover
            screen.blit(text_gameover,(text_gameover.get_rect(center=(WIDTH//2, HEIGHT//2))))
            bg_color = black
            if int(PLAYTIME*3/flamerate)%4 == 1:
                help_color = black
            else: help_color = white
            text_begin = font_text.render("Press space or return to back.",True,(help_color))
            screen.blit(text_begin,(text_begin.get_rect(center=(WIDTH//2, HEIGHT//2 +50))))
            key_time += 1
            if key_time > flamerate/4: key_time = flamerate/4
            if key_time == flamerate/4 and (key[pygame.K_ESCAPE] or key[pygame.K_RETURN] or key[pygame.K_SPACE] == 1):
                reset()
                idx = 0.1
        
        if key[pygame.K_i] == 1:print(idx)
        PLAYTIME += 1
        pygame.display.update() #システム処理
        screen.fill(bg_color)
        clock.tick(flamerate)
        
if __name__ == "__main__":
    main()