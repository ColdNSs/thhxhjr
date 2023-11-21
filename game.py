import random
import pygame
import json
pygame.init()
class UIasset():
    def __init__(self):
        self.enemy_hp_bar = pygame.image.load("Picture/hp_bar.bmp").convert()
        self.framework = pygame.image.load("Picture/framework.png").convert()
        self.background = pygame.image.load("Picture/background.png").convert()
        self.bomb = pygame.image.load("Picture/star_green.bmp").convert()
        self.HP = pygame.image.load("Picture/star_red.bmp").convert()
        self.time_panel = pygame.image.load("Picture/time_panel.bmp").convert()
        self.framework.set_colorkey((255,255,255))
        self.bomb.set_colorkey((240,240,240))
        self.HP.set_colorkey((240,240,240))
        self.time_panel.set_colorkey("BLACK")
        self.fpsTimer = 0
    def drawBefore(self):
        screen.blit(self.background, (30, 20))
    def drawAfter(self):
        # 游戏UI背景
        screen.blit(self.framework, (0, 0))
        # 帧率显示
        if not self.fpsTimer:
            nowfps = clock.get_fps()
            if nowfps > 57:
                fpscolor = (255,255,255)
            else:
                fpscolor = (255,0,0) 
            self.fpstext = font_Arial20.render(str("{0:.2f}".format(nowfps/2 if settings["powersave"] else nowfps)), True, fpscolor)
            self.fpsTimer = 60
        screen.blit(self.fpstext, (900, 680))
        self.fpsTimer -= 1
        # 敌机血量显示
        screen.blit(pygame.transform.scale(UI.enemy_hp_bar,(max(500*baka.HP/baka.HPlist[baka.spell - 1],0),20)),(90,35))
        screen.blit(UI.time_panel,(50,22))
        # 分数显示
        screen.blit(font_Simsun20.render("   Score：{0:0>10}".format(score),True, (240, 240, 240)),(630,140))
        # 残机显示
        screen.blit(font_Simsun20.render("剩余人数：",True, (240, 240, 240)),(630,170))
        for i in range(player_Character.HP):
            screen.blit(UI.HP, (730+i*25, 170))
        # 符卡显示
        screen.blit(font_Simsun20.render("剩余符卡：",True, (240, 240, 240)),(630,200))
        for i in range(player_Character.Bomb):
            screen.blit(UI.bomb, (730+i*25, 200))
        # 擦弹数量显示
        screen.blit(font_Simsun20.render("擦弹数：{0}".format(player_CharacterImage.graze),True, (240, 240, 240)),(630,230))
        # 敌人位置显示
        screen.blit(font_Simsun16.render("| ENEMY |",True, (255, 0, 0)),(baka.rect.x,700))
        # 剩余时间显示
        self.lefttime = int((baka.spellTimeLimitList[baka.spell - 1] - baka.spelltick) / 6)
        if self.lefttime > 99:
            screen.blit(font_Arial24.render(str(int(self.lefttime / 10)),True,"BLACK"),(55,31))
            screen.blit((font_Arial24.render(".",True,"BLACK")),(79,31))
            screen.blit(font_Arial20.render(str(int(self.lefttime - int(self.lefttime / 10) * 10)),True,"BLACK"),(83,35))
        else:
            screen.blit(font_Arial24.render("0"+str(int(self.lefttime / 10)),True,"RED"),(55,31))
            screen.blit((font_Arial24.render(".",True,"RED")),(79,31))
            screen.blit(font_Arial20.render(str(int(self.lefttime - int(self.lefttime / 10) * 10)),True,"RED"),(83,35))
        showspellscore()
            # posvec：位置向量 speedvec：速度向量
class playerCharacter(pygame.sprite.Sprite): #判定点类 
    def __init__(self,radius,speed,speedMultiplier,QTElimit,attackspeed,slowattackspeed):
        super().__init__()
        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.set_colorkey('BLACK')
        self.rect = self.image.get_rect()
        self.posvec = pygame.math.Vector2(455,600)
        self.radius = radius
        self.rect.centerx = 455
        self.rect.centery = 600
        self.nowattackspeed = self.attackSpeed = attackspeed
        self.slowattackSpeed = slowattackspeed
        self.attackCoolDown = 0 
        self.speedvec = pygame.math.Vector2(0,0)
        self.speed = speed
        self.slow = 1
        self.speedMultiplier = speedMultiplier
        self.shoot = False
        self.HP = 5
        self.Bomb = 3
        self.leftspeed = 0
        self.rightspeed = 0
        self.upspeed = 0
        self.downspeed = 0
        self.invincibleTime = 0
        self.QTETime = 0
        self.QTElimit = QTElimit
        self.status = "alive"
        self.mode = 0
        self.missinthisspell = False
    def setmode(self,mode): #设置子机位置
        if mode == 1:
            player_Character.slow = self.speedMultiplier
            pygame.draw.circle(player_Character.image,'WHITE',(self.radius,self.radius),self.radius)
            pygame.draw.circle(player_Character.image,'RED',(self.radius,self.radius),self.radius,1)   
            player_CharacterJadeRight.x = 18
            player_CharacterJadeRight.y = -23
            player_CharacterJadeLeft.x = -15
            player_CharacterJadeLeft.y = -23
        if mode == 0:
            player_Character.slow = 1
            player_Character.image.fill('BLACK')
            player_CharacterJadeRight.x = 30
            player_CharacterJadeRight.y = 28
            player_CharacterJadeLeft.x = -24
            player_CharacterJadeLeft.y = 28
        self.mode = mode

    def update(self):
        if chooseCharacter == "Marisa":
            for item in bombgroup:
                item.angle += 3
                if item.angle > 360:
                    item.angle = 0
        self.speedvec.x = self.rightspeed - self.leftspeed
        self.speedvec.y = self.downspeed - self.upspeed
        if self.speedvec.length():
            self.speedvec.scale_to_length(self.speed * self.slow) #算出速度方向并乘以速度标量
            self.posvec += self.speedvec
            self.posvec.x = min(gameX + 20,self.posvec.x)
            self.posvec.x = max(40,self.posvec.x)
            self.posvec.y = min(screenY - 50,self.posvec.y)
            self.posvec.y = max(50,self.posvec.y)
            self.rect.centerx , self.rect.centery = self.posvec
        # 伪状态机
        if self.status == "alive":
            self.missCheck()
        if self.status == "dying":
            self.missCheck()
            self.QTECheck()
        if self.status == "invincible":
            self.missCheck()
            self.invincibleCheck()
        if self.status == "usebomb":
            self.Bomb -= 1
            self.missinthisspell = True
            if self.QTETime: # 决死
                self.QTETime = 0
            self.status = "bombing"
            if chooseCharacter == "Reimu":
                # 下面这段是Bing AI优化的
                # 创建一个列表，包含不同颜色的图片对象
                pictures = [player_bomb_pictures[color] for color in ["red", "orange", "yellow", "green", "blue", "purple"]]
                # 创建一个列表，包含不同的位置和参数
                positions = [(self.rect.centerx - 80, self.rect.centery - 150, 210),
                (self.rect.centerx + 80, self.rect.centery - 150, 215),
                (self.rect.centerx + 150, self.rect.centery, 220),
                (self.rect.centerx + 80, self.rect.centery + 150, 225),
                (self.rect.centerx - 80, self.rect.centery + 150, 230),
                (self.rect.centerx - 150, self.rect.centery, 235)]
                # 遍历两个列表，创建和添加每个bomb对象
                for picture, position in zip(pictures, positions):
                    mybomb = ReimuBomb(picture, pygame.math.Vector2(*position[:2]), pygame.math.Vector2(0, -0.1), position[2], 2)
                    bombgroup.add(mybomb)
            self.bombingTime = 180
        if self.status == "bombing":
            self.missCheck()
            self.bombingCheck()
        if self.shoot:
            if self.attackCoolDown - self.nowattackspeed: # 射击冷却计算
                self.attackCoolDown += 1
                return
            self.attackCoolDown = 0
            if self.slow == self.speedMultiplier: # 高低速不同类型的子弹
                self.nowattackspeed = self.attackSpeed    
                if chooseCharacter == "Reimu": # 为什么是全局变量 因为懒
                    mybullet = Bullet(0,(255,0,0),10,30,pygame.math.Vector2(player_CharacterJadeLeft.rect.x + 13,player_CharacterJadeLeft.rect.y + 10),pygame.math.Vector2(0,-40),10,0,False,pygame.math.Vector2(0,0))
                    selfBulletGroup.add(mybullet)
                    mybullet = Bullet(0,(255,0,0),10,30,pygame.math.Vector2(player_CharacterJadeRight.rect.x + 13,player_CharacterJadeLeft.rect.y + 10),pygame.math.Vector2(0,-40),10,0,False,pygame.math.Vector2(0,0))
                    selfBulletGroup.add(mybullet)
                elif chooseCharacter == "Marisa":
                    mybullet = Bullet(0,(255,255,128),10,300,pygame.math.Vector2(player_CharacterJadeLeft.rect.x + 13,player_CharacterJadeLeft.rect.y - 10),pygame.math.Vector2(0,-120),1,player_CharacterJadeLeft,False,pygame.math.Vector2(0,0))
                    selfBulletGroup.add(mybullet)
                    mybullet = Bullet(0,(255,255,128),10,300,pygame.math.Vector2(player_CharacterJadeRight.rect.x + 13,player_CharacterJadeLeft.rect.y - 10),pygame.math.Vector2(0,-120),1,player_CharacterJadeRight,False,pygame.math.Vector2(0,0))
                    selfBulletGroup.add(mybullet)
            if self.slow == 1:
                self.nowattackspeed = self.slowattackSpeed
                if chooseCharacter == "Reimu":
                    mybullet = Bullet(2,(255,255,255),10,10,pygame.math.Vector2(player_CharacterJadeLeft.rect.x + 10,player_CharacterJadeLeft.rect.y + 10),pygame.math.Vector2(0,-20),10,0,True,pygame.math.Vector2(0,0))
                    selfBulletGroup.add(mybullet)
                    mybullet = Bullet(2,(255,255,255),10,10,pygame.math.Vector2(player_CharacterJadeRight.rect.x + 10,player_CharacterJadeLeft.rect.y + 10),pygame.math.Vector2(0,-20),10,0,True,pygame.math.Vector2(0,0))
                    selfBulletGroup.add(mybullet)
                elif chooseCharacter == "Marisa":
                    mybullet = Bullet(self.bulletimage,(255,255,128),10,300,pygame.math.Vector2(player_CharacterJadeLeft.rect.x + 13,player_CharacterJadeLeft.rect.y),pygame.math.Vector2(0,-1),30,0,False,pygame.math.Vector2(0,-0.5))
                    selfBulletGroup.add(mybullet)
                    mybullet = Bullet(self.bulletimage,(255,255,128),10,300,pygame.math.Vector2(player_CharacterJadeRight.rect.x + 13,player_CharacterJadeLeft.rect.y),pygame.math.Vector2(0,-1),30,0,False,pygame.math.Vector2(0,-0.5))
                    selfBulletGroup.add(mybullet)
    
    def bombingCheck(self):
        self.bombingTime -= 1
        if chooseCharacter == "Marisa":
            mybomb = MarisaBomb(player_bomb_pictures[random.choice(["red","yellow","green"])],pygame.math.Vector2(player_Character.rect.centerx,player_Character.rect.centery - 40),pygame.math.Vector2(random.uniform(-1.5,1.5),random.uniform(-3.5,-5.5)),8)
            bombgroup.add(mybomb)
        if not self.bombingTime:
            self.status = "alive"
    
    def QTECheck(self): 
        self.QTETime -= 1
        if self.Bomb == 0: #没B直接寄
            self.QTETime = 0
        if not self.QTETime:
            self.status = "invincible"
            self.invincibleTime = 120
            self.HP -= 1
            self.missinthisspell = True
            self.clearradius = 10
            self.diecenter = self.rect.center
            self.Bomb = max(2,self.Bomb)
            pygame.draw.circle(player_Character.image,'WHITE',(5,5),5)
            pygame.draw.circle(player_Character.image,'RED',(5,5),5,1)
            self.setmode(mode=self.mode)

    def invincibleCheck(self):
        self.invincibleTime -= 1
        if 0 < self.clearradius < 600: #创造出一个以死亡点为圆心的扩大消弹的圆
            self.clearradius += 25
            for item in enemyBulletGroup:
                if (item.rect.center[0]-self.rect.center[0])**2 + (item.rect.center[1]-self.rect.center[1])**2 < self.clearradius**2:
                    sprite_disappear(item,8)
        else:
            self.clearradius = 0
        if not self.invincibleTime:
            self.status = "alive"

    def missCheck(self):
        self.iscoll = False
        for item in enemyBulletGroup:
            if pygame.sprite.collide_circle_ratio(0.5)(item,player_Character):
                self.iscoll = item
                break
        if self.iscoll:
            item.kill()
            if self.status == "alive": #活着被弹转移到决死反应时间
                self.QTETime = 10 
                self.status = "dying"
                pygame.draw.circle(player_Character.image,'RED',(5,5),5)

class playerCharacterImage(pygame.sprite.Sprite): #自机点阵图 只有擦弹相关实现在里面
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.originimage = image
        self.image.set_colorkey((240,240,240))
        self.x = x
        self.y = y
        self.graze = 0
    def update(self):
        global score
        self.rect = self.image.get_rect()
        self.rect.center = player_Character.rect.center
        for item in enemyBulletGroup:
            if pygame.sprite.collide_circle_ratio(2)(item,player_Character) and not item.alreadyGraze:
                self.graze += 1
                score += 2000
                item.alreadyGraze = True # 擦过的弹不能再擦

class playerJade(playerCharacterImage): # 子机类
    def __init__(self,image,x,y):
        super(playerJade,self).__init__(image,x,y)
        self.angle = 0
    def update(self):
        self.rect = self.image.get_rect()
        width,height = self.image.get_size()
        self.rect.x , self.rect.y = (-width / 2 + player_Character.rect.x + self.x,-height / 2 + player_Character.rect.y + self.y)
        self.image = pygame.transform.rotate(self.originimage,self.angle+1)
        self.rect = self.image.get_rect(center = self.rect.center) # 重新获取中心 避免转动问题
        self.angle += 1
        if self.angle > 360:
            self.angle = 0

class Bullet(pygame.sprite.Sprite): # 子弹类
    def __init__(self,shape,color,width,height,posvec:pygame.math.Vector2,speedvec:pygame.math.Vector2,damage,free,track,accvec:pygame.math.Vector2):
        super().__init__()
        self.origincolor = self.color = color
        self.shape = shape
        self.accvec = accvec
        self.image = pygame.Surface([width, height]) # 控制子弹类型 但是目前看来这样写下去会更加屎山
        if shape == 2:
            pygame.draw.circle(self.image,color,(width/2,height/2),width/2)
            self.image.set_colorkey('BLACK')
        elif shape == 1:
            pygame.draw.circle(self.image,color,(width/2,height/2),width/2)
            pygame.draw.circle(self.image,(color[0]+14,color[1]+14,color[2]+14),(width/2,height/2),width/3)
            pygame.draw.circle(self.image,'WHITE',(width/2,height/2),width/2-2,1)
            self.image.set_colorkey('BLACK')
        elif shape == 0:
            self.image.fill(color)
        else: 
            self.image = self.shape
        self.rect = self.image.get_rect()
        self.posvec = posvec
        self.speedvec = speedvec
        self.inputspeedvec = speedvec
        self.rect.centerx , self.rect.centery = posvec
        self.damage = damage
        self.free = free # 0产生跟随子机y轴移动的激光
        self.track = track
        self.width = width
        self.height = height
        self.alreadyGraze = False

    def update(self):
        self.posvec += self.speedvec
        self.speedvec += self.accvec
        self.rect.centerx , self.rect.centery = self.posvec # 这行及上两行实现非整数坐标
        if self.track: # 诱导弹
            self.speedvec = relative_direction(self,baka)
            self.speedvec.scale_to_length(self.inputspeedvec.length()) #速度向量转化为长度与输入速度一致
        if self.rect.x - self.width > gameX + 50 or self.rect.x < -50 or self.rect.y > screenY + 50  or self.rect.y + self.height < -50: # 出界判定
            self.kill()
        if self.free:
            self.rect.centerx = self.posvec.x = self.free.rect.centerx

class MarisaBomb(pygame.sprite.Sprite): # 抄袭自灵梦Bomb类型 别问我为什么不复用 问就是懒和不会
    def __init__(self,image,posvec:pygame.math.Vector2,speedvec:pygame.math.Vector2,damage):
        super().__init__()
        self.image = self.originimage = image
        self.rect = self.image.get_rect()
        self.posvec = posvec
        self.rect.centerx , self.rect.centery = posvec
        self.speedvec = speedvec
        self.damage = damage
        self.trigger = 0
        self.angle = 0
        self.lifetime = 240
        self.radius = 24

    def update(self):
        self.angle += 3
        if self.angle > 360:
            self.angle = 0 # 使我的星星旋转
        self.image = pygame.transform.rotate(self.originimage,self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)
        #self.posvec.x , self.posvec.y = self.rect.centerx , self.rect.centery 没这行有问题 有这行更有问题
        self.posvec += self.speedvec
        self.rect.centerx , self.rect.centery = self.posvec
        if not self.trigger:
            if pygame.sprite.collide_circle(self,baka):
                self.trigger = 1 # 击中则被触发
                baka.HP -= self.damage
            if not self.lifetime:
                self.trigger = 1
        if self.trigger: # 逐渐变大消失
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * (1 + 0.04 * self.trigger), self.image.get_height() * (1 + 0.04 * self.trigger)))
            self.trigger += 1
            self.image.set_alpha(255 - self.trigger * 10) 
        if self.trigger > 25:
            self.kill()
        if not self.lifetime: # 超过生命周期也消失
            self.kill()
        for item in enemyBulletGroup:
            if pygame.sprite.collide_circle(self,item):
                sprite_disappear(item,5)

class ReimuBomb(pygame.sprite.Sprite):
    def __init__(self,image,posvec:pygame.math.Vector2,speedvec:pygame.math.Vector2,lifetime,damage):
        super().__init__()
        self.image = self.originimage = image
        self.rect = self.image.get_rect()
        self.posvec = posvec
        self.inputvec = self.speedvec = speedvec
        self.inputspeedvec = speedvec
        self.rect.centerx , self.rect.centery = posvec
        self.damage = damage
        self.inputlifetime = self.lifetime = lifetime
        self.tracktime = 200
        self.angle = 0
        self.trigger = False
        self.image.set_alpha(0)
        self.radius = 63
    def update(self):
        if 10 > self.lifetime - self.tracktime > 0: # 10帧的逐渐出现效果
            self.image = self.originimage
            self.image.set_alpha(255 - (self.lifetime - self.tracktime) / 10 * 255)  
        if self.tracktime > self.lifetime:
            self.angle += 3
            if self.angle > 360:
                self.angle = 0 # 使我的阴阳玉旋转
            self.image = pygame.transform.rotate(self.originimage,self.angle)
            self.speedvec = (self.speedvec + relative_direction(self,baka)*3).normalize() * (self.inputspeedvec.length() + 0.08 * (self.tracktime - self.lifetime))
            self.rect = self.image.get_rect(center = self.rect.center)
            self.posvec.x , self.posvec.y = self.rect.centerx , self.rect.centery 
            self.posvec += self.speedvec
            self.rect.centerx , self.rect.centery = self.posvec
        if pygame.sprite.collide_circle_ratio(0.8)(self,baka):
            baka.HP -= self.damage
            if not self.trigger:
                self.trigger = 1 # 击中则被触发
        self.lifetime -= 1
        if self.trigger: # 逐渐变大消失
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * (1 + 0.03 * self.trigger), self.image.get_height() * (1 + 0.03 * self.trigger)))
            self.trigger += 1
            self.image.set_alpha(255 - self.trigger * 4) 
        if self.trigger > 63:
            baka.HP -= 50
            self.kill()
        if not self.lifetime: # 超过生命周期也消失
            self.kill()
        for item in enemyBulletGroup:
            if pygame.sprite.collide_circle(self,item):
                sprite_disappear(item,5)

class Enemy(pygame.sprite.Sprite):
    def __init__(self,maxHP,HP,posvec):
        super().__init__()
        self.enter_spell7 = False
        self.ice_cone_image = pygame.image.load("Picture/ice_cone.bmp").convert()
        self.ice_cone_image.set_colorkey("BLACK")
        self.shootCoolDown = (1,10,4,1,1,1,1,1,1)
        self.HPlist = (4,2500,4000,7000,3000,6000,8000,4000,4000)
        self.spellTimeLimitList = (2400,2400,2000,3000,2000,3000,3600,2000,2000)
        self.spell = 9
        self.HP = self.HPlist[self.spell - 1]
        self.image = pygame.image.load("Picture/cirno.bmp").convert()
        self.image.set_colorkey((240,240,240))
        self.rect = self.image.get_rect()
        self.maxHP = maxHP
        self.posvec = posvec 
        self.rect.centerx , self.rect.centery = self.posvec
        self.speedvec = pygame.math.Vector2(0,0)
        self.width = 59
        self.height = 74
        self.moveCoolDown = random.randint(300,600)
        self.moveCoolDownCount = 0
        self.shootCoolDownCount = 0
        self.spellcount = 10
        self.spelltick = 0
        self.enter_spell6 = False # 屎
        self.stand = False

    def update(self):
        global score
        global showspellfailedtime
        self.shootCoolDownCount += 1
        self.spelltick += 1
        if self.shootCoolDown[self.spell - 1] == self.shootCoolDownCount:
            self.shoot()
            self.shootCoolDownCount = 0
        list = pygame.sprite.spritecollide(self,selfBulletGroup,False)
        for item in list:
            self.HP -= item.damage
            if not item.free:
                item.kill()
        if self.HP < 0 or self.spelltick >= self.spellTimeLimitList[baka.spell - 1]:
            if not player_Character.missinthisspell: # 符卡收取判定
                spellscore = (self.spellTimeLimitList[baka.spell - 1] - self.spelltick) * 1000
                score += spellscore
                showspellscoredata["score"] = spellscore
                showspellscoredata["time"] = 150
            else:
                player_Character.missinthisspell = False
                showspellfailedtime = 150
            for item in enemyBulletGroup:
                sprite_disappear(item,15)
            if self.spell > self.spellcount:
                self.kill()
                return
            self.shootCoolDownCount = 0
            self.spell += 1
            self.spelltick = 0
            self.HP = self.HPlist[self.spell - 1]
        if not self.stand:
            self.moveCoolDownCount += 1
            if self.moveCoolDown == self.moveCoolDownCount:
                self.moveCoolDown = random.randint(120,300)
                self.moveCoolDownCount = 0
                self.speedvec.x = random.uniform(-2,2)
            self.posvec = self.posvec + self.speedvec
            self.posvec.x=min(gameX - 50,self.posvec.x)
            self.posvec.x=max(self.rect.width,self.posvec.x)
            self.posvec.y=min(screenY - 50,self.posvec.y)
            self.posvec.y=max(self.rect.height,self.posvec.y)
            self.rect.centerx , self.rect.centery = self.posvec

    def shoot(self):
        if self.spell == 1:
            tmp_vec1 = pygame.math.Vector2(random.uniform(-1,1),random.uniform(0,1)).normalize() * 3
            while True: # 朴实无华随机弹
                bullet = Bullet(1,((random.randint(0,240)),(random.randint(0,240)),(random.randint(0,240))),20,20,pygame.math.Vector2(self.posvec.x,self.posvec.y),tmp_vec1,1,0,0,pygame.math.Vector2(0,0))
                if not (bullet.speedvec.length() < 1): # 避免出现太慢的弹幕
                    break
            enemyBulletGroup.add(bullet)
        
        if self.spell == 2:
            if not self.spelltick % 300 < 20: 
                for i in range(-3,4,1): # 上下2*7=14条封位弹
                    bullet = Bullet(1,(100,128,240),20,20,pygame.math.Vector2(self.posvec.x,self.posvec.y),pygame.math.Vector2(i,2),1,0,0,pygame.math.Vector2(0,0))
                    enemyBulletGroup.add(bullet)
                    bullet = Bullet(1,(100,128,240),20,20,pygame.math.Vector2(self.posvec.x,self.posvec.y),pygame.math.Vector2(i,-2),1,0,0,pygame.math.Vector2(0,0))
                    enemyBulletGroup.add(bullet)
            if self.spelltick / 10 % 3: # 8颗朝下的随机弹
                for i in range(8):
                    bullet = Bullet(1,((random.randint(0,240)),(random.randint(0,240)),(random.randint(0,240))),20,20,pygame.math.Vector2(self.posvec.x,self.posvec.y),pygame.math.Vector2(random.uniform(3,-3),3),1,0,0,pygame.math.Vector2(0,0))
                    enemyBulletGroup.add(bullet)
            if self.spelltick % 120 == 0: # 1颗自机狙
                bullet = Bullet(1,(240,240,240),60,60,pygame.math.Vector2(self.posvec.x,self.posvec.y),relative_direction(self,player_Character)*5,1,0,0,pygame.math.Vector2(0,0))
                enemyBulletGroup.add(bullet)
        
        if self.spell == 3: # 大冰棱子
            bullet = Bullet(self.ice_cone_image.copy(),((random.randint(0,240)),(random.randint(0,240)),(random.randint(0,240))),40,40,pygame.math.Vector2(random.uniform(10,600),self.rect.centery - 50),pygame.math.Vector2(0,1.5),1,0,0,pygame.math.Vector2(0,0.01))
            enemyBulletGroup.add(bullet)
            if self.spelltick % 90 == 0: # 屎山偶数弹
                bullet = Bullet(1,(240,240,240),60,60,pygame.math.Vector2(self.posvec.x,self.posvec.y),relative_direction(self,player_Character).rotate(10)*8,1,0,0,pygame.math.Vector2(0,0))
                enemyBulletGroup.add(bullet)
                bullet = Bullet(1,(240,240,240),60,60,pygame.math.Vector2(self.posvec.x,self.posvec.y),relative_direction(self,player_Character).rotate(-10)*8,1,0,0,pygame.math.Vector2(0,0))
                enemyBulletGroup.add(bullet)

        if self.spell == 4:
            if self.posvec.y <= 350: # 笨蛋下压中 
                self.speedvec.y = 5
                self.isfreeze = True
                return
            elif not self.speedvec.y == 0:
                self.speedvec.y = 0
            if self.spelltick % 600 < 400:
                if self.isfreeze:
                    self.isfreeze = False
                    for item in enemyBulletGroup:
                        item.accvec = pygame.math.Vector2(random.uniform(-1,1),random.uniform(-1,1)).normalize() * random.uniform(0.1) # 解冻之后随机弹道
                # 全向随机弹
                tmp_vec1 = pygame.math.Vector2(random.uniform(-1,1),random.uniform(-1,1)).normalize()
                bullet = Bullet(1,((random.randint(0,240)),(random.randint(0,240)),(random.randint(0,240))),20,20,pygame.math.Vector2(self.posvec.x,self.posvec.y),tmp_vec1 * random.uniform(1.5,2.5),1,0,0,pygame.math.Vector2(0,0))
                enemyBulletGroup.add(bullet)
            else:
                if self.spelltick % 10 == 0 and 410 < self.spelltick % 600 < 500: # 2*⑨ = 18颗偶数弹
                    bullet = Bullet(1,(20,100,240),40,40,pygame.math.Vector2(self.posvec.x,self.posvec.y),relative_direction(self,player_Character).rotate(random.uniform(5,20))*8,1,0,0,pygame.math.Vector2(0,0))
                    enemyBulletGroup.add(bullet)
                    bullet = Bullet(1,(20,100,240),40,40,pygame.math.Vector2(self.posvec.x,self.posvec.y),relative_direction(self,player_Character).rotate(random.uniform(-5,-20))*8,1,0,0,pygame.math.Vector2(0,0))
                    enemyBulletGroup.add(bullet)
                if not self.isfreeze:  # Perfect Freeze!
                    self.isfreeze = True
                    for item in enemyBulletGroup:
                        pygame.draw.circle(item.image,(240,240,240),(item.width/2,item.height/2),item.width/2)
                        pygame.draw.circle(item.image,"WHITE",(item.width/2,item.height/2),item.width/3)
                        pygame.draw.circle(item.image,'WHITE',(item.width/2,item.height/2),item.width/2-2,1)
                        item.speedvec = pygame.math.Vector2(0,0)

        if self.spell == 5:
            if self.posvec.y > 100: 
                self.speedvec.y = -5
                return
            if self.spelltick % 30 == 0:
                for i in range(60):
                    bullet = Bullet(1,(0,100,240),20,20,pygame.math.Vector2(i * 60,0),pygame.math.Vector2(0,2),1,0,0,pygame.math.Vector2(0,0))    
                    bullet.tracktime = 181
                    enemyBulletGroup.add(bullet)
            if self.spelltick % 30 == 0: # 一定时间内的诱导弹
                bullet = Bullet(1,(240,240,240),40,40,pygame.math.Vector2(self.posvec.x,self.posvec.y),relative_direction(self,player_Character) * 2,1,0,0,pygame.math.Vector2(0,0))
                bullet.tracktime = 0
                enemyBulletGroup.add(bullet)
            for item in enemyBulletGroup:
                if item.tracktime > 150: # 超过时间就停止追踪
                    continue
                item.tracktime += 1
                directvec = relative_direction(item,player_Character)
                if 0 < item.speedvec.angle_to(directvec) < 180:
                    item.speedvec.rotate_ip(2)
                else:
                    item.speedvec.rotate_ip(-2)
        
        if self.spell == 6: # 转圈弹
            if not self.enter_spell6:
                self.speedvec = (pygame.math.Vector2(350,350) - self.posvec) / 60 # 60帧内移动到屏幕中心
                self.enter_spell6 = True
                return
            if self.spelltick < 60:
                return
            self.stand = True
            bullet = Bullet(1,(0,100,240),15,15,pygame.math.Vector2(self.posvec.x,self.posvec.y),pygame.math.Vector2(0,2).rotate(self.spelltick * 18),1,0,0,pygame.math.Vector2(0,0))    
            enemyBulletGroup.add(bullet)
            bullet = Bullet(1,(0,100,240),15,15,pygame.math.Vector2(self.posvec.x,self.posvec.y),pygame.math.Vector2(0,2).rotate(self.spelltick * 9),1,0,0,pygame.math.Vector2(0,0))    
            enemyBulletGroup.add(bullet)
            if self.spelltick % 90 == 0: # 1颗自机狙
                bullet = Bullet(1,(240,240,240),40,40,pygame.math.Vector2(self.posvec.x,self.posvec.y),relative_direction(self,player_Character)*4,1,0,0,pygame.math.Vector2(0,0))
                enemyBulletGroup.add(bullet)

        if self.spell == 7:
            if not self.enter_spell7:
                self.spell7_bulletrotate = -5
                self.stand = False
                self.speedvec = (pygame.math.Vector2(350,100) - self.posvec) / 60 # 60帧内移动回上方
                self.enter_spell7 = True
                return
            if self.spelltick < 60:
                return
            self.stand = True
            if self.spelltick % 2 == 0:
                self.posvec = pygame.math.Vector2(self.rect.centerx,self.rect.centery)
                self.speedvec = pygame.math.Vector2(0,0) # 防止弹幕修改笨蛋位置只能每帧锁定速度了
                bullet = Bullet(1,(0,100,240),20,20,baka.posvec,pygame.math.Vector2(random.uniform(-1,1),random.uniform(-1,1)).normalize() * random.uniform(4,5),1,0,0,pygame.math.Vector2(0,0))     
                bullet.tracktime = 0
                enemyBulletGroup.add(bullet)
            if self.spelltick % 2 == 1:
                self.posvec = pygame.math.Vector2(self.rect.centerx,self.rect.centery)
                bullet = Bullet(1,(0,240,100),20,20,baka.posvec,pygame.math.Vector2(random.uniform(-1,1),random.uniform(-1,1)).normalize() * random.uniform(3,4),1,0,0,pygame.math.Vector2(0,0))     
                bullet.tracktime = 0
                enemyBulletGroup.add(bullet)
                self.posvec = pygame.math.Vector2(self.rect.centerx,self.rect.centery)
                bullet = Bullet(1,(240,240,240),20,20,baka.posvec,pygame.math.Vector2(random.uniform(-1,1),random.uniform(-1,1)).normalize() * random.uniform(2,3),1,0,0,pygame.math.Vector2(0,0))     
                bullet.tracktime = 0
                enemyBulletGroup.add(bullet)
            for item in enemyBulletGroup:
                if item.tracktime > 180: # 超过时间就停止旋转
                    continue
                item.tracktime += 1
                item.speedvec.rotate_ip(self.spell7_bulletrotate)
            if self.spelltick % 480 == 0:
                self.spell7_bulletrotate = -self.spell7_bulletrotate
                for item in enemyBulletGroup:
                    item.tracktime = 999
            self.posvec = pygame.math.Vector2(self.rect.centerx,self.rect.centery)

        if self.spell == 8:
            self.stand = True
            for i in range(60):
                if self.spelltick % 15 == i: #开花旋转加速弹（?
                    tmp_speedvec = pygame.math.Vector2(0,-1).rotate(i * 24 + (self.spelltick / 5) % 360)
                    bullet = Bullet(1,(0,min(240 - self.spelltick % 240,self.spelltick % 240) * 2,240),20,20,baka.posvec + tmp_speedvec,tmp_speedvec,1,0,0,tmp_speedvec * 0.02)     
                    enemyBulletGroup.add(bullet)
                if (self.spelltick + 5) % 15 == i:
                    tmp_speedvec = pygame.math.Vector2(0,-1).rotate(i * 24 + (self.spelltick / 5) % 360)
                    bullet = Bullet(1,(0,min(240 - self.spelltick % 240,self.spelltick % 240) * 2,240),20,20,baka.posvec + tmp_speedvec,tmp_speedvec,1,0,0,tmp_speedvec * 0.04)     
                    enemyBulletGroup.add(bullet)
                if (self.spelltick + 10) % 15 == i:
                    tmp_speedvec = pygame.math.Vector2(0,-1).rotate(i * 24 + (self.spelltick / 5) % 360)
                    bullet = Bullet(1,(0,min(240 - self.spelltick % 240,self.spelltick % 240) * 2,240),20,20,baka.posvec + tmp_speedvec,tmp_speedvec,1,0,0,tmp_speedvec * 0.06)     
                    enemyBulletGroup.add(bullet)
        
        if self.spell == 8:
            self.stand = True
            for i in range(60):
                if self.spelltick % 15 == i: #开花旋转加速弹（?
                    tmp_speedvec = pygame.math.Vector2(0,-1).rotate(i * 24 + (self.spelltick / 5) % 360)
                    bullet = Bullet(1,(0,min(240 - self.spelltick % 240,self.spelltick % 240) * 2,240),20,20,baka.posvec + tmp_speedvec,tmp_speedvec,1,0,0,tmp_speedvec * 0.02)     
                    enemyBulletGroup.add(bullet)
                if (self.spelltick + 5) % 15 == i:
                    tmp_speedvec = pygame.math.Vector2(0,-1).rotate(i * 24 + (self.spelltick / 5) % 360)
                    bullet = Bullet(1,(0,min(240 - self.spelltick % 240,self.spelltick % 240) * 2,240),20,20,baka.posvec + tmp_speedvec,tmp_speedvec,1,0,0,tmp_speedvec * 0.04)     
                    enemyBulletGroup.add(bullet)
                if (self.spelltick + 10) % 15 == i:
                    tmp_speedvec = pygame.math.Vector2(0,-1).rotate(i * 24 + (self.spelltick / 5) % 360)
                    bullet = Bullet(1,(0,min(240 - self.spelltick % 240,self.spelltick % 240) * 2,240),20,20,baka.posvec + tmp_speedvec,tmp_speedvec,1,0,0,tmp_speedvec * 0.06)     
                    enemyBulletGroup.add(bullet)
        
        if self.spell == 9:
            if self.spelltick % 30 == 0:
                for i in range(20): # 白色奇数弹
                    tmpspeed_vec = (relative_direction(self,player_Character)*4).rotate(i * 18)
                    bullet = Bullet(1,(240,240,240),20,20,pygame.math.Vector2(self.posvec.x,self.posvec.y) + tmpspeed_vec,tmpspeed_vec,1,0,0,pygame.math.Vector2(0,0))
                    enemyBulletGroup.add(bullet)
            if self.spelltick % 30 == 15:
                for i in range(20): # 蓝色偶数弹
                    tmpspeed_vec = (relative_direction(self,player_Character)*4).rotate(i * 18 + 9)
                    bullet = Bullet(1,(0,120,240),20,20,pygame.math.Vector2(self.posvec.x,self.posvec.y) + tmpspeed_vec,tmpspeed_vec,1,0,0,pygame.math.Vector2(0,0))
                    enemyBulletGroup.add(bullet)
            if not self.spelltick % 180: # 创建变大弹幕
                self.stand = True
                bullet = Bullet(1,(0,0,0),10,10,pygame.math.Vector2(self.posvec.x,self.posvec.y) + pygame.math.Vector2(0,10),(0,0),1,0,0,pygame.math.Vector2(0,0))
                bullet.specialtag_1 = True
                enemyBulletGroup.add(bullet)
            if 0 < self.spelltick % 180 < 60: # 不断变大变炫彩
                tmp_tick = self.spelltick % 180
                for item in enemyBulletGroup:
                    if hasattr(item,"specialtag_1") and item.specialtag_1 == True:
                        enemyBulletGroup.remove(item)
                        bullet = Bullet(1,(min(12*tmp_tick,240),min(max(12*(tmp_tick-20),0),240),min(max(12*(tmp_tick-40),0),240)),10 + tmp_tick * 3,10 + tmp_tick * 3,pygame.math.Vector2(self.posvec.x,self.posvec.y) + pygame.math.Vector2(0,10 - tmp_tick),pygame.math.Vector2(0,0),1,0,0,pygame.math.Vector2(0,0))
                        bullet.specialtag_1 = True
                        enemyBulletGroup.add(bullet)
            if self.spelltick % 180 == 60: # 丢出去
                self.stand = False
                for item in enemyBulletGroup:
                    if hasattr(item,"specialtag_1") and item.specialtag_1 == True:
                        item.specialtag_1 = False
                        item.speedvec = relative_direction(self,player_Character)*5


def keydown(key):
    if key == pygame.K_UP:
        player_Character.upspeed = 1
    if key == pygame.K_DOWN:
        player_Character.downspeed = 1
    if key == pygame.K_LEFT:
        player_Character.leftspeed = 1
    if key == pygame.K_RIGHT:
        player_Character.rightspeed = 1
    if key == pygame.K_z:
        player_Character.shoot = True
    if key == pygame.K_x:
        if not player_Character.status == "bombing" and player_Character.Bomb > 0:
            player_Character.status = "usebomb"
    if key == pygame.K_LSHIFT:
        player_Character.setmode(mode=1)
    if key == pygame.K_ESCAPE:
        global done
        done = True
    
def keyup(key):
    if key == pygame.K_UP:
        player_Character.upspeed = 0
    if key == pygame.K_DOWN:
        player_Character.downspeed = 0
    if key == pygame.K_LEFT:
        player_Character.leftspeed = 0
    if key == pygame.K_RIGHT:
        player_Character.rightspeed = 0
    if key == pygame.K_z:
        player_Character.shoot = False
    if key == pygame.K_LSHIFT:
        player_Character.setmode(mode=0)

def relative_direction(sprite1:pygame.sprite.Sprite,sprite2:pygame.sprite.Sprite): # 返回从Sprite1指向Sprite2的单位向量 若为0向量则返回随机微小向量
    if (sprite2.rect.centerx - sprite1.rect.centerx) == 0 and (sprite2.rect.centery - sprite1.rect.centery) == 0:  
        return pygame.math.Vector2(random.uniform(-0.001,0.001),random.uniform(0.001,-0.001))
    return pygame.math.Vector2(sprite2.rect.centerx - sprite1.rect.centerx ,sprite2.rect.centery - sprite1.rect.centery).normalize()

def sprite_disappear(sprite:pygame.sprite.Sprite,disappeartime:int): # 令sprite在disappeartime里逐渐消失
    if not sprite in disappear_group:
        sprite.disappeartime = sprite.nowdisappeartime = disappeartime
        disappear_group.add(sprite)

def showspellscore():
    global showspellfailedtime
    if showspellscoredata["time"]:
        char_count = int((150 - showspellscoredata["time"]) / 6)
        screen.blit(font_Arial36.render("Get Spell Bonus!!",True, (255, 255, 255)),(210,250))
        screen.blit(font_Arial24.render(str(showspellscoredata["score"]).rjust(8,"0")[:char_count],True, (255, 0, 0)),(290,290))
        showspellscoredata["time"] -= 1
    if showspellfailedtime:
        screen.blit(font_Arial36.render("Bonus Failed...",True, (235, 235, 235)),(246,250))
        showspellfailedtime -= 1

def create_setting(): # 生成配置文件
    settings = {"powersave":True,"replay":False}
    with open("settings.json", "w") as file:
        file.write(json.dumps(settings))

try:
    with open('settings.json') as f:
        try:    
            settings = json.load(f,strict=False)
        except json.JSONDecodeError:
            raise FileNotFoundError
except FileNotFoundError:
    create_setting()
score = 0
showspellscoredata = {"score":0,"time":0}
showspellfailedtime = 0
screenX = 960
screenY = 720
gameX = 570
size = (screenX,screenY)
screen = pygame.display.set_mode(size)
chooseCharacter = "Marisa"
font_Arial20 = pygame.sysfont.SysFont('Arial',20)
font_Arial24 = pygame.sysfont.SysFont('Arial',24)
font_Arial36 = pygame.sysfont.SysFont('Arial',36)
font_Simsun20 = pygame.sysfont.SysFont('SimSun',20)
font_Simsun16 = pygame.sysfont.SysFont('SimSun',16)
if settings["replay"] == True:
    with open('rep.json') as f:
        load_event_list = json.load(f,strict=False)
    seed = load_event_list[0][0]
    type_replace_dict = {"0":768,"1":769}
    key_replace_dict = {"0":1073741906,"1":1073741905,"2":1073741904,"3":1073741903,"4":122,"5":120,"6":1073742049}
    for sublist in load_event_list[1:]:
        for item in sublist:
            type_value = str(item["type"])
            key_value = str(item["key"])
            if type_value in type_replace_dict:
                item["type"] = type_replace_dict[type_value]
            if key_value in key_replace_dict:
                item["key"] = key_replace_dict[key_value]
    '''
    replay_json = json.dumps(load_event_list)
    with open("rep_c.json", "w") as file:
        file.write(replay_json)
    '''
else:
    seed = random.randint(1000000000,9999999999) # 下面在为replay做准备 
    input_event_list = [[seed]]
random.seed(seed)
disappear_group = pygame.sprite.Group()
self_group = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
selfBulletGroup = pygame.sprite.Group()
enemyBulletGroup = pygame.sprite.Group()
bombgroup = pygame.sprite.Group()
if chooseCharacter == "Reimu":
    player_Character = playerCharacter(5,8,0.5,10,3,5)
    player_CharacterImage = playerCharacterImage(pygame.image.load("Picture/reimu.bmp").convert(),5,3)
    player_CharacterJadeRight = playerJade(pygame.image.load("Picture/reimu_option.bmp").convert(),30,28)
    player_CharacterJadeLeft = playerJade(pygame.image.load("Picture/reimu_option.bmp").convert(),-24,28)
    player_bullet_picture = pygame.image.load("Picture/reimu_needle.bmp").convert()
    player_bullet_picture.set_colorkey("BLACK")
    #这段也是Bing AI优化的
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    player_bomb_pictures = {}
    for color in colors:
        filename = "Picture/bigjade_" + color + ".bmp"
        picture = pygame.image.load(filename).convert()
        picture.set_colorkey("BLACK")
        player_bomb_pictures[color] = picture
    
if chooseCharacter == "Marisa":
    player_Character = playerCharacter(6,9,0.4,9,0,8)
    player_Character.bulletimage = pygame.image.load("Picture/grass.bmp")
    player_Character.bulletimage.convert()
    player_Character.bulletimage.set_colorkey((240,240,240))
    player_CharacterImage = playerCharacterImage(pygame.image.load("Picture/marisa.bmp").convert(),5,3)
    player_CharacterJadeRight = playerJade(pygame.image.load("Picture/marisa_option.bmp").convert(),30,28)
    player_CharacterJadeLeft = playerJade(pygame.image.load("Picture/marisa_option.bmp").convert(),-24,28)
    player_bullet_picture = pygame.image.load("Picture/marisa_missile.bmp").convert()
    player_bullet_picture.set_colorkey("BLACK")
    colors = ["red", "yellow", "green"]
    player_bomb_pictures = {}
    for color in colors:
        filename = "Picture/bigstar_" + color + ".bmp"
        picture = pygame.image.load(filename).convert()
        picture.set_colorkey((240,240,240))
        player_bomb_pictures[color] = picture

self_group.add(player_CharacterImage)
self_group.add(player_CharacterJadeRight)
self_group.add(player_CharacterJadeLeft)
self_group.add(player_Character)
UI = UIasset()
baka = Enemy(5000,5000,pygame.math.Vector2(355,100))
enemyGroup.add(baka)
clock = pygame.time.Clock()
done = False
tick = 0
while not done:
    print(player_CharacterImage.graze)
    clock.tick(60)
    tick += 1
    screen.fill((240, 240, 240))
    for item in disappear_group:
        if item.nowdisappeartime <= 0:
            item.kill()
            continue
        item.image.set_alpha(255 / item.disappeartime * item.nowdisappeartime)
        item.nowdisappeartime -= 1
    if not settings["replay"]:
        input_event_list.append([])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                keydown(event.key)
                input_event_list[tick].append({"t":tick,"type":event.type,"key":event.key})
            elif event.type == pygame.KEYUP:
                keyup(event.key)
                input_event_list[tick].append({"t":tick,"type":event.type,"key":event.key})
    else: # 播放录像
        item = load_event_list[1]
        if item[0]["t"] == tick:
            for event in item:
                for event in load_event_list[1]:
                    if event["type"] == pygame.QUIT:
                        done = True
                    elif event["type"] == pygame.KEYDOWN:
                        keydown(event["key"])
                    elif event["type"] == pygame.KEYUP:
                        keyup(event["key"])
            del load_event_list[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    tmp = pygame.time.get_ticks()
    player_Character.update()
    player_CharacterImage.update()
    player_CharacterJadeLeft.update()
    player_CharacterJadeRight.update()
    print("playerupdatetime:{0}".format(pygame.time.get_ticks()-tmp))
    enemyGroup.update()
    tmp = pygame.time.get_ticks()
    enemyBulletGroup.update()
    selfBulletGroup.update()
    bombgroup.update()
    print("bulletupdatetime:{0}".format(pygame.time.get_ticks()-tmp))
    if tick % 2 or not settings["powersave"]:
        tmp = pygame.time.get_ticks()
        UI.drawBefore()
        print("UIbefore:{0}".format(pygame.time.get_ticks()-tmp))
        tmp = pygame.time.get_ticks()
        self_group.draw(screen)
        enemyGroup.draw(screen)
        print("character:{0}".format(pygame.time.get_ticks()-tmp))
        tmp = pygame.time.get_ticks()
        selfBulletGroup.draw(screen)
        enemyBulletGroup.draw(screen)
        bombgroup.draw(screen)
        print("bullet:{0}".format(pygame.time.get_ticks()-tmp))
        tmp = pygame.time.get_ticks()
        UI.drawAfter()
        print("UIAfter:{0}".format(pygame.time.get_ticks()-tmp))
        pygame.display.flip()
done = True
if not settings["replay"]:
    input_event_list = [x for x in input_event_list if x != []] # 清除所有空项
    type_replace_dict = {"768":"0","769":"1"}
    key_replace_dict = {"1073741906":"0","1073741905":"1","1073741904":"2","1073741903":"3","122":"4","120":"5","1073742049":"6"}
    for sublist in input_event_list[1:]:
        for item in sublist:
            type_value = str(item["type"])
            key_value = str(item["key"])
            if type_value in type_replace_dict:
                item["type"] = type_replace_dict[type_value]
            if key_value in key_replace_dict:
                item["key"] = key_replace_dict[key_value]
    replay_json = json.dumps(input_event_list)
    with open("rep.json", "w") as file:
        file.write(replay_json)