import random
import pygame


pygame.init()
screenX = 960
screenY = 720
gameX = 620
size = (screenX,screenY)
screen = pygame.display.set_mode(size)
font = pygame.sysfont.SysFont('Arial',24)
#text = font.render("Hello, World!", True, (240, 240, 240))
#screen.blit(text, (screenX/2 - text.get_width()/2, screenY/2 - text.get_height()/2))
class UIasset():
    def __init__(self):
        self.framework = pygame.image.load("Picture/framework.png")
        self.background = pygame.image.load("Picture/background.png")
        self.bomb = pygame.image.load("Picture/star_green.bmp")
        self.HP = pygame.image.load("Picture/star_red.bmp")
        self.framework.set_colorkey((255,255,255))
        self.bomb.set_colorkey((240,240,240))
        self.HP.set_colorkey((240,240,240))
    def drawBefore(self):
        screen.blit(self.background, (10, 10))
    def drawAfter(self):
        screen.blit(self.framework, (0, 0))

class playerCharacter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        pygame.draw.circle(self.image,'WHITE',(5,5),5)
        self.image.set_colorkey('BLACK')
        self.rect = self.image.get_rect()
        self.rect.x = 455
        self.rect.y = 600
        self.attackSpeed = 3
        self.attackCoolDown = 0
        self.leftspeed = 0
        self.rightspeed = 0
        self.upspeed = 0
        self.downspeed = 0
        self.slow = 1
        self.shoot = False
        self.HP = 5
        self.Bomb = 3
        self.invincibleTime = 0

    def update(self):
        self.rect.x += (self.rightspeed - self.leftspeed) * self.slow
        self.rect.y += (self.downspeed - self.upspeed) * self.slow
        self.rect.x=min(gameX - 20,self.rect.x)
        self.rect.x=max(10,self.rect.x)
        self.rect.y=min(screenY - 50,self.rect.y)
        self.rect.y=max(10,self.rect.y)
        list = pygame.sprite.spritecollide(self,enemyBulletGroup, True)
        if list:
            if not self.invincibleTime:
                self.invincibleTime = 120
                self.clearradius = 10
                self.diecenter = self.rect.center
                for item in list:
                    self.HP -= item.damage
                    break
        if self.invincibleTime > 0:
            self.invincibleTime -= 1
            if 0 < self.clearradius < 600:
                self.clearradius += 20
                for item in enemyBulletGroup:
                    if (item.rect.center[0]-self.rect.center[0])**2 + (item.rect.center[1]-self.rect.center[1])**2 < self.clearradius**2:
                        item.kill()
            else:
                self.clearradius = 0
        if self.shoot:
            if self.attackCoolDown - self.attackSpeed:
                self.attackCoolDown += 1
                return
            self.attackCoolDown = 0
            if self.slow == 0.5:
                self.attackSpeed = 3
                mybullet = Bullet(0,(255,0,0),10,30,player_CharacterJadeLeft.rect.x + 10,self.rect.y,0,-40,10,1,False)
                selfBulletGroup.add(mybullet)
                mybullet = Bullet(0,(255,0,0),10,30,player_CharacterJadeRight.rect.x + 10,self.rect.y,0,-40,10,1,False)
                selfBulletGroup.add(mybullet)
            if self.slow == 1:
                self.attackSpeed = 5
                mybullet = Bullet(2,(255,255,255),10,10,player_CharacterJadeLeft.rect.x + 10,self.rect.y,0,-20,6,1,True)
                selfBulletGroup.add(mybullet)
                mybullet = Bullet(2,(255,255,255),10,10,player_CharacterJadeRight.rect.x + 10,self.rect.y,0,-20,6,1,True)
                selfBulletGroup.add(mybullet)

class playerCharacterImage(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.image = image
        self.originimage = image
        self.image.set_colorkey((240,240,240))
        self.x = x
        self.y = y
    def update(self):
        self.rect = self.image.get_rect()
        width,height = self.image.get_size()
        self.rect.x , self.rect.y = (-width / 2 + player_Character.rect.x + self.x,-height / 2 + player_Character.rect.y + self.y)

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
    def __init__(self,shape,color,width,height,x,y,xspeed,yspeed,damage,belong,track):
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
        self.rect.x = x
        self.rect.y = y
        self.nextx = x + xspeed
        self.nexty = y + yspeed
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.inputxspeed = xspeed
        self.inputyspeed = yspeed
        self.damage = damage
        self.belong = belong
        self.track = track
        self.width = width
        self.height = height
    def update(self):
        self.nextx += self.xspeed
        self.nexty += self.yspeed
        self.rect.x = self.nextx
        self.rect.y = self.nexty
        if self.track:
            directdistance = ((self.rect.x - Baka.rect.x)**2 + (self.rect.y - Baka.rect.y)**2)**0.5
            self.xspeed = (self.rect.x - Baka.rect.x - Baka.width / 2) * -((self.inputxspeed**2)+(self.inputyspeed**2))**0.5 / directdistance
            self.yspeed = (self.rect.y - Baka.rect.y - Baka.height / 2) * -((self.inputxspeed**2)+(self.inputyspeed**2))**0.5 / directdistance
            '''
            directdistance = Int(Sqr((playershapes(I).Left - baka.Left) ^ 2 + (playershapes(I).Top - baka.Top) ^ 2))
            playerdanmakus(I).xspeed = -(playershapes(I).Left - baka.Left - baka.Width / 2) * 100 / directdistance
            playerdanmakus(I).yspeed = -(playershapes(I).Top - baka.Top - baka.Height / 2) * 100 / directdistance
            '''
        if self.rect.x - self.width > gameX or self.rect.x < 0 or self.rect.y > screenY or self.rect.y + self.height < 0:
            self.kill()
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self,maxHP,HP,x,y):
        super().__init__()
        self.image = pygame.image.load("Picture/cirno.bmp")
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
            self.xspeed = 0#random.randint(-3,3)
            self.yspeed = 0#random.randint(-3,3)
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
            bullet = Bullet(1,((random.randint(0,240)),(random.randint(0,240)),(random.randint(0,240))),20,20,self.rect.x-10+random.randint(0,45),self.rect.y-10+random.randint(0,45),-2+random.randint(0,40)*0.1,-1+random.randint(0,60)*0.1,1,0,0)
            if not (abs(bullet.yspeed) < 1 and abs(bullet.xspeed) < 1):
                break
        enemyBulletGroup.add(bullet)
def keydown(key):
    if key == pygame.K_LEFT:
        player_Character.leftspeed = 8
    if key == pygame.K_RIGHT:
        player_Character.rightspeed = 8
    if key == pygame.K_UP:
        player_Character.upspeed = 8
    if key == pygame.K_DOWN:
        player_Character.downspeed = 8
    if key == pygame.K_z:
        player_Character.shoot = True
    if key == pygame.K_LSHIFT:
        player_Character.slow = 0.5

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
        player_Character.slow = 1

def DrawUI():
    pygame.draw.rect(screen, 'RED', (20, 20, 590*Baka.HP/Baka.maxHP, 10), 0)
    for i in range(player_Character.HP):
        screen.blit(UI.HP, (660+i*30, 200))

selfGroup = pygame.sprite.Group()
enemyGroup = pygame.sprite.Group()
selfBulletGroup = pygame.sprite.Group()
enemyBulletGroup = pygame.sprite.Group()
player_Character = playerCharacter()
player_CharacterImage = playerCharacterImage(pygame.image.load("Picture/reimu.bmp"),5,3)
player_CharacterJadeRight = playerJade(pygame.image.load("Picture/jade.bmp"),18,-23)
player_CharacterJadeLeft = playerJade(pygame.image.load("Picture/jade.bmp"),-15,-23)
selfGroup.add(player_CharacterImage)
selfGroup.add(player_CharacterJadeRight)
selfGroup.add(player_CharacterJadeLeft)
selfGroup.add(player_Character)
UI = UIasset()
Baka = Enemy(5000,5000,455,100)
enemyGroup.add(Baka)
clock = pygame.time.Clock()
done = False

while not done:
    print(Baka.HP)
    clock.tick(60)
    screen.fill((240, 240, 240))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            keydown(event.key)
        elif event.type == pygame.KEYUP:
            keyup(event.key)
    UI.drawBefore()
    player_Character.update()
    player_CharacterImage.update()
    player_CharacterJadeLeft.update()
    player_CharacterJadeRight.update()
    enemyGroup.update()
    enemyBulletGroup.update()
    selfBulletGroup.update()
    selfGroup.draw(screen)
    enemyGroup.draw(screen)
    selfBulletGroup.draw(screen)
    enemyBulletGroup.draw(screen)
    UI.drawAfter()
    #screen.blit(text, (screenX/2 - text.get_width()/2, screenY/2 - text.get_height()/2))
    DrawUI()
    # 更新窗口
    pygame.display.update()
    # 控制游戏帧率
done = True