import random
import pygame

pygame.init()
screenX = 960
screenY = 720
gameX = 570
size = (screenX,screenY)
screen = pygame.display.set_mode(size)
chooseCharacter = "Reimu"
font_Arial20 = pygame.sysfont.SysFont('Arial',20)
font_Simsun20 = pygame.sysfont.SysFont('SimSun',20)
font_Simsun16 = pygame.sysfont.SysFont('SimSun',16)
        
class UIasset():
    def __init__(self):
        self.framework = pygame.image.load("Picture/framework.png").convert()
        self.background = pygame.image.load("Picture/background.png").convert()
        self.bomb = pygame.image.load("Picture/star_green.bmp").convert()
        self.HP = pygame.image.load("Picture/star_red.bmp").convert()
        self.framework.set_colorkey((255,255,255))
        self.bomb.set_colorkey((240,240,240))
        self.HP.set_colorkey((240,240,240))
        self.fpsTimer = 0
    def drawBefore(self):
        screen.blit(self.background, (30, 20))
    def drawAfter(self):
        #游戏UI背景
        screen.blit(self.framework, (0, 0))
        #帧率显示
        if not self.fpsTimer:
            self.fpstext = font_Arial20.render(str("{0:.2f}".format(clock.get_fps()/2 if powersave_mode else clock.get_fps())), True, (255, 255, 255))
            self.fpsTimer = 60
        screen.blit(self.fpstext, (900, 680))
        self.fpsTimer -= 1
        #敌机血量显示
        pygame.draw.rect(screen, 'RED', (40, 30, 570*baka.HP/baka.maxHP, 10), 0)
        #残机显示
        screen.blit(font_Simsun20.render("剩余人数：",True, (240, 240, 240)),(630,170))
        for i in range(player_Character.HP):
            screen.blit(UI.HP, (730+i*25, 170))
        #符卡显示
        screen.blit(font_Simsun20.render("剩余符卡：",True, (240, 240, 240)),(630,200))
        for i in range(player_Character.Bomb):
            screen.blit(UI.bomb, (730+i*25, 200))
        #擦弹数量显示
        font = pygame.sysfont.SysFont('SimSun',20)
        screen.blit(font_Simsun20.render("擦弹数：{0}".format(player_CharacterImage.graze),True, (240, 240, 240)),(630,230))
        #敌人位置显示
        font = pygame.sysfont.SysFont('SimSun',16)
        screen.blit(font_Simsun16.render("| ENEMY |",True, (255, 0, 0)),(baka.rect.x,700))


class playerCharacter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.set_colorkey('BLACK')
        self.rect = self.image.get_rect()
        self.posvec = pygame.math.Vector2(455,600)
        self.rect.x = 455
        self.rect.y = 600
        self.attackSpeed = 3
        self.attackCoolDown = 0 
        self.speedvec = pygame.math.Vector2(0,0)
        self.speed = 8
        self.slow = 1
        self.speedMultiplier = 0.5
        self.shoot = False
        self.HP = 5
        self.Bomb = 3
        self.leftspeed = 0
        self.rightspeed = 0
        self.upspeed = 0
        self.downspeed = 0
        self.invincibleTime = 0
        self.QTETime = 0
        self.status = "alive"
        self.mode = 0
    def setmode(self,mode):
        if mode == 1:
            player_Character.slow = self.speedMultiplier
            pygame.draw.circle(player_Character.image,'WHITE',(5,5),5)
            pygame.draw.circle(player_Character.image,'RED',(5,5),5,1)   
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
        self.speedvec.x = self.rightspeed - self.leftspeed
        self.speedvec.y = self.upspeed - self.downspeed
        if self.speedvec.length():
            self.speedvec.scale_to_length(self.speed * self.slow)
            self.posvec += self.speedvec 
            self.posvec.x = min(gameX + 20,self.posvec.x)
            self.posvec.x = max(40,self.posvec.x)
            self.posvec.y = min(screenY - 50,self.posvec.y)
            self.posvec.y = max(50,self.posvec.y)
            self.rect.x ,
            '''
        if self.bombTrigger and not self.isBombing:
            self.isBombing , self.bombTrigger = self.bombTrigger , self.isBombing
            pygame.draw.circle(player_Character.image,'WHITE',(5,5),5)
            pygame.draw.circle(player_Character.image,'RED',(5,5),5,1)   
            self.Bomb -= 1
            self.dying = False
            #todo
        '''
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
            if self.QTETime:
                self.QTETime = 0
            self.status = "bombing"
            self.bombingTime = 120
        if self.status == "bombing":
            self.missCheck()
            self.bombingCheck()
        if self.shoot:
            if self.attackCoolDown - self.attackSpeed:
                self.attackCoolDown += 1
                return
            self.attackCoolDown = 0
            if self.slow == 0.5:
                self.attackSpeed = 3            
                mybullet = Bullet(0,(255,0,0),10,30,pygame.math.Vector2(player_CharacterJadeLeft.rect.x + 10,player_CharacterJadeLeft.rect.y + 10),pygame.math.Vector2(0,-40),10,1,False)
                selfBulletGroup.add(mybullet)
                mybullet = Bullet(0,(255,0,0),10,30,pygame.math.Vector2(player_CharacterJadeRight.rect.x + 10,player_CharacterJadeLeft.rect.y + 10),pygame.math.Vector2(0,-40),10,1,False)
                selfBulletGroup.add(mybullet)
            if self.slow == 1:
                self.attackSpeed = 5
                mybullet = Bullet(2,(255,255,255),10,10,pygame.math.Vector2(player_CharacterJadeLeft.rect.x + 10,player_CharacterJadeLeft.rect.y + 10),pygame.math.Vector2(0,-20),6,1,True)
                selfBulletGroup.add(mybullet)
                mybullet = Bullet(2,(255,255,255),10,10,pygame.math.Vector2(player_CharacterJadeRight.rect.x + 10,player_CharacterJadeLeft.rect.y + 10),pygame.math.Vector2(0,-20),6,1,True)
                selfBulletGroup.add(mybullet)
    
    def bombingCheck(self):
        self.bombingTime -= 1
        if not self.bombingTime:
            self.status = "alive"
    
    def QTECheck(self):
        self.QTETime -= 1
        if self.Bomb == 0:
            self.QTETime = 0
        if not self.QTETime:
            self.status = "invincible"
            self.invincibleTime = 120
            self.HP -= 1
            self.clearradius = 10
            self.diecenter = self.rect.center
            self.Bomb = max(2,self.Bomb)
            pygame.draw.circle(player_Character.image,'WHITE',(5,5),5)
            pygame.draw.circle(player_Character.image,'RED',(5,5),5,1)
            self.setmode(mode=self.mode)

    def invincibleCheck(self):
        self.invincibleTime -= 1
        if 0 < self.clearradius < 600:
            self.clearradius += 25
            for item in enemyBulletGroup:
                if (item.rect.center[0]-self.rect.center[0])**2 + (item.rect.center[1]-self.rect.center[1])**2 < self.clearradius**2:
                    item.kill()
        else:
            self.clearradius = 0
        if not self.invincibleTime:
            self.status = "alive"

    def missCheck(self):
        self.iscoll = False
        for item in enemyBulletGroup:
            if pygame.sprite.collide_circle_ratio(0.6)(item,player_Character):
                self.iscoll = item
                break
        if self.iscoll:
            item.kill()
            if self.status == "alive":
                self.QTETime = 10 
                self.status = "dying"
                pygame.draw.circle(player_Character.image,'RED',(5,5),5)

class playerCharacterImage(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.originimage = image
        self.image.set_colorkey((240,240,240))
        self.x = x
        self.y = y
        self.graze = 0
    def update(self):
        self.rect = self.image.get_rect()
        #width,height = self.image.get_size()
        self.rect.center = player_Character.rect.center
        #list = pygame.sprite.spritecollide(self,enemyBulletGroup,False)
        for item in enemyBulletGroup:
            if pygame.sprite.collide_circle_ratio(1.5)(item,player_Character) and not item.alreadyGraze:
                self.graze += 1
                item.alreadyGraze = True

class playerJade(playerCharacterImage):
    def __init__(self,image,x,y):
        super(playerJade,self).__init__(image,x,y)
        self.angle = 0
    def update(self):
        self.rect = self.image.get_rect()
        width,height = self.image.get_size()
        self.rect.x , self.rect.y = (-width / 2 + player_Character.rect.x + self.x,-height / 2 + player_Character.rect.y + self.y)
        self.image = pygame.transform.rotate(self.originimage,self.angle+1)
        self.rect = self.image.get_rect(center = self.rect.center)
        self.angle += 1
        if self.angle > 360:
            self.angle = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self,shape,color,width,height,posvec:pygame.math.Vector2,speedvec:pygame.math.Vector2,damage,belong,track):
        super().__init__()
        self.image = pygame.Surface([width, height])
        if shape == 2:
            pygame.draw.circle(self.image,color,(width/2,height/2),width/2)
            self.image.set_colorkey('BLACK')
        if shape == 1:
            pygame.draw.circle(self.image,color,(width/2,height/2),width/2)
            pygame.draw.circle(self.image,(color[0]+14,color[1]+14,color[2]+14),(width/2,height/2),width/3)
            pygame.draw.circle(self.image,'WHITE',(width/2,height/2),width/2-2,1)
            self.image.set_colorkey('BLACK')
        elif shape == 0:
            self.image.fill(color)
        self.rect = self.image.get_rect()
        self.posvec = posvec
        self.speedvec = speedvec
        self.inputspeedvec = speedvec
        self.rect.x , self.rect.y = posvec
        self.damage = damage
        self.belong = belong
        self.track = track
        self.width = width
        self.height = height
        self.alreadyGraze = False

    def update(self):
        self.posvec += self.speedvec
        self.rect.x , self.rect.y = self.posvec
        if self.track:
            directdistance = ((self.rect.x - baka.rect.x)**2 + (self.rect.y - baka.rect.y)**2)**0.5
            self.speedvec = baka.posvec
            self.xspeed = (self.rect.x - baka.rect.x - baka.width / 2) * -((self.inputxspeed**2)+(self.inputyspeed**2))**0.5 / directdistance
            self.yspeed = (self.rect.y - baka.rect.y - baka.height / 2) * -((self.inputxspeed**2)+(self.inputyspeed**2))**0.5 / directdistance
            '''
            directdistance = Int(Sqr((playershapes(I).Left - baka.Left) ^ 2 + (playershapes(I).Top - baka.Top) ^ 2))
            playerdanmakus(I).xspeed = -(playershapes(I).Left - baka.Left - baka.Width / 2) * 100 / directdistance
            playerdanmakus(I).yspeed = -(playershapes(I).Top - baka.Top - baka.Height / 2) * 100 / directdistance
            '''
        if self.rect.x - self.width > gameX + 50 or self.rect.x < -50 or self.rect.y > screenY + 50 or self.rect.y + self.height < -50:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,maxHP,HP,x,y):
        super().__init__()
        self.image = pygame.image.load("Picture/cirno.bmp").convert()
        self.image.set_colorkey((240,240,240))
        self.rect = self.image.get_rect()
        self.HP = HP
        self.maxHP = maxHP
        self.rect.x = x
        self.rect.y = y
        self.xspeed = 0
        self.yspeed = 0
        self.width = 59
        self.height = 74
        self.moveCoolDown = random.randint(120,600)
        self.moveCoolDownCount = 0
        self.shootCoolDown = 2
        self.shootCoolDownCount = 0
    def update(self):
        self.moveCoolDownCount += 1
        self.shootCoolDownCount += 1
        if self.moveCoolDown == self.moveCoolDownCount:
            self.moveCoolDown = random.randint(120,600)
            self.moveCoolDownCount = 0
            self.xspeed = random.randint(-3,3)
            self.yspeed = random.randint(-3,3)
        if self.shootCoolDown == self.shootCoolDownCount:
            self.shoot()
            self.shootCoolDownCount = 0
        list = pygame.sprite.spritecollide(self,selfBulletGroup,True)
        for item in list:
            self.HP -= item.damage
        if self.HP == 0:
            self.kill()
        self.rect.x += self.xspeed
        self.rect.y += self.yspeed
        self.rect.x=min(gameX - 50,self.rect.x)
        self.rect.x=max(0,self.rect.x)
        self.rect.y=min(screenY - 50,self.rect.y)
        self.rect.y=max(0,self.rect.y)

    def shoot(self):
        while True:
            bullet = Bullet(1,((random.randint(0,240)),(random.randint(0,240)),(random.randint(0,240))),20,20,pygame.math.Vector2(self.rect.x-10+random.randint(0,45),self.rect.y-10+random.randint(0,45)),pygame.math.Vector2(-2+random.randint(0,40)*0.1,-1+random.randint(0,60)*0.1),1,0,0)
            if not (bullet.speedvec.length() < 1):
                break
        enemyBulletGroup.add(bullet)
def keydown(key):
    if key == pygame.K_LEFT:
        player_Character.moveleft = 1
    if key == pygame.K_RIGHT:
        player_Character.rightspeed = 1
    if key == pygame.K_UP:
        player_Character.upspeed = 1
    if key == pygame.K_DOWN:
        player_Character.downspeed = 1
    if key == pygame.K_z:
        player_Character.shoot = True
    if key == pygame.K_LSHIFT:
        player_Character.setmode(mode=1)
    if key == pygame.K_x and not player_Character.status == "bombing" and player_Character.Bomb > 0:
        player_Character.status = "usebomb"
def keyup(key):
    if key == pygame.K_LEFT:
        player_Character.leftspeed = 0
    if key == pygame.K_RIGHT:
        player_Character.rightspeed = 0
    if key == pygame.K_UP:
        player_Character.upspeed = 0
    if key == pygame.K_DOWN:
        player_Character.downspeed = 0
    if key == pygame.K_z:
        player_Character.shoot = False
    if key == pygame.K_LSHIFT:
        player_Character.setmode(mode=0)

self_group = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
selfBulletGroup = pygame.sprite.Group()
enemyBulletGroup = pygame.sprite.Group()
player_Character = playerCharacter()
if chooseCharacter == "Reimu":
    player_CharacterImage = playerCharacterImage(pygame.image.load("Picture/reimu.bmp").convert(),5,3)
    player_CharacterJadeRight = playerJade(pygame.image.load("Picture/reimu_option.bmp").convert(),30,28)
    player_CharacterJadeLeft = playerJade(pygame.image.load("Picture/reimu_option.bmp").convert(),-24,28)
if chooseCharacter == "Marisa":
    pass
self_group.add(player_CharacterImage)
self_group.add(player_CharacterJadeRight)
self_group.add(player_CharacterJadeLeft)
self_group.add(player_Character)
UI = UIasset()
baka = Enemy(5000,5000,455,100)
enemyGroup.add(baka)
clock = pygame.time.Clock()
done = False
tick = 0
powersave_mode = False
while not done:
    print(player_CharacterImage.graze)
    clock.tick(60)
    tick += 1
    screen.fill((240, 240, 240))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            keydown(event.key)
        elif event.type == pygame.KEYUP:
            keyup(event.key)
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
    print("bulletupdatetime:{0}".format(pygame.time.get_ticks()-tmp))
    if tick % 2 or not powersave_mode:
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
        print("bullet:{0}".format(pygame.time.get_ticks()-tmp))
        tmp = pygame.time.get_ticks()
        UI.drawAfter()
        print("UIAfter:{0}".format(pygame.time.get_ticks()-tmp))
    #screen.blit(text, (screenX/2 - text.get_width()/2, screenY/2 - text.get_height()/2))
    # 更新窗口
        pygame.display.flip()
    # 控制游戏帧率
done = True