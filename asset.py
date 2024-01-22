from typing import Any
import pygame


class SEPlayer():
    MISS_CHANNEL = 33
    PLAYER_SPELL_CHANNEL = 34
    ENEMY_SPELL_CHANNEL = 35
    ENEMY_DESTORY_CHANNEL = 36
    SPELL_EXTEND_CHANNEL = 37
    VOLUME_TEST_CHANNEL = 37
    def __init__(self):
        self.channel = 0
        self.soundasset = {}
        self.soundasset["damage"] = pygame.mixer.Sound("SE/damage.wav")
        self.soundasset["damageloud"] = pygame.mixer.Sound("SE/damageloud.wav")
        self.soundasset["destory"] = pygame.mixer.Sound("SE/destory.wav")
        self.soundasset["graze"] = pygame.mixer.Sound("SE/graze.wav")
        self.soundasset["item"] = pygame.mixer.Sound("SE/item.wav")
        self.soundasset["test"] = self.soundasset["miss"] = pygame.mixer.Sound("SE/miss.wav")
        self.soundasset["pause"] = pygame.mixer.Sound("SE/pause.wav")
        self.soundasset["timeout"] = pygame.mixer.Sound("SE/timeout.wav")
        self.soundasset["shoot"] = pygame.mixer.Sound("SE/shoot.wav")
        self.soundasset["bomb"] = pygame.mixer.Sound("SE/bomb.wav")
        self.soundasset["select"] = pygame.mixer.Sound("SE/select.wav")
        self.soundasset["confirm"] = pygame.mixer.Sound("SE/confirm.wav")
        self.soundasset["cancel"] = pygame.mixer.Sound("SE/cancel.wav")
        self.soundasset["invalid"] = pygame.mixer.Sound("SE/invalid.wav")
        self.soundasset["enemyst01"] = pygame.mixer.Sound("SE/enemyst01.wav")
        self.soundasset["enemyst02"] = pygame.mixer.Sound("SE/enemyst02.wav")
        self.soundasset["spellextend"] = pygame.mixer.Sound("SE/spellextend.wav")
        self.setvolume(0.5)

    def play(self, effect, channel=-1):
        sound = self.soundasset[effect]
        if channel == -1:
            self.channel += 1
            if self.channel > 31:
                self.channel = 0
            pygame.mixer.Channel(self.channel).play(sound)
            return
        pygame.mixer.Channel(channel).play(sound)

    def setvolume(self, volume):
        for sound in self.soundasset:
            self.soundasset[sound].set_volume(volume)


class PicLoader():
    def load(self, picname: str, width=0, height=0, hasalpha=False):
        if not hasalpha:
            pic = pygame.image.load(picname).convert()
            pic.set_colorkey("BLUE")
        else:
            pic = pygame.image.load(picname).convert_alpha()
        if not (width and height):
            return pic
        pic = pygame.transform.scale(pic, (width, height))
        pic.set_colorkey("BLUE")
        return pic

class MenuStruct():
    def __init__(self,text,isdisabled = False):
        self.text = text
        self.isdisabled = isdisabled

class Menu():
    def __init__(self,font:pygame.font.Font,menulist,defaultcolor,choicecolor,disablecolor,posvec,iscirculute = False,defaultchoice = 0):
        self.font = font
        self.menulist = menulist
        self.defaultcolor = defaultcolor
        self.choicecolor = choicecolor
        self.disablecolor = disablecolor
        self.choice = defaultchoice
        self.exactchoice = defaultchoice
        self.iscirculute = iscirculute
        self.posvec = posvec
        self.optiongroup = pygame.sprite.Group()
        self.choiceablelist = []
        for i, struct in enumerate(self.menulist):
            self.optiongroup.add(self.MenuSprite(self,struct,i))
            if not struct.isdisabled:
                self.choiceablelist.append(i) # 维护一个可选择选项的索引
        pass

    def up(self):
        self.choice -= 1
        self.choice = max(0,self.choice) if not self.iscirculute else self.choice % len(self.choiceablelist)
        self.exactchoice = self.choiceablelist[self.choice]

    def down(self):
        self.choice += 1
        self.choice = min(len(self.choiceablelist) - 1,self.choice) if not self.iscirculute else self.choice % len(self.choiceablelist)
        self.exactchoice = self.choiceablelist[self.choice]
    
    def choose(self):
        return self.exactchoice
    
    def getelementbyid(self,id): # 东施效颦
        for element in self.optiongroup:
            if element.id == id:
                return element

    class MenuSprite(pygame.sprite.Sprite):
        def __init__(self,owner,struct:MenuStruct,id):
            super().__init__()
            self.id = id
            self.owner = owner
            self.struct = struct
            self.color = self.owner.defaultcolor
            if self.id == self.owner.exactchoice: # 默认选择
                self.color = self.owner.choicecolor
            if struct.isdisabled:
                self.color = self.owner.disablecolor
            self.image = self.owner.font.render(struct.text,True,self.color)
            self.rect = self.image.get_rect()
            self.rect.x,self.rect.y = self.owner.posvec[0], self.owner.posvec[1] + (self.image.get_height() + 5) * id

        def refresh(self): #强制重新渲染图片
            self.image = self.owner.font.render(self.struct.text,True,self.color)

        def settext(self,text):
            self.struct.text = text
            self.refresh()

        def update(self):
            if self.struct.isdisabled == True:
                return
            if self.id == self.owner.exactchoice: 
                if self.color != self.owner.choicecolor: # 说明是刚刚变动的
                    self.color = self.owner.choicecolor
                    self.image = self.owner.font.render(self.struct.text,True,self.color)
            else:
                if self.color != self.owner.defaultcolor: # 说明是刚刚变动的
                    self.color = self.owner.defaultcolor
                    self.image = self.owner.font.render(self.struct.text,True,self.color)
            
class GameUI():
    picLoader = PicLoader()

    def __init__(self, settings):
        self.bulletitem = self.picLoader.load("Picture/bulletitem.bmp")
        self.enemy_hp_bar = self.picLoader.load("Picture/hp_bar.bmp")
        self.framework = self.picLoader.load("Picture/framework.png")
        self.background = self.picLoader.load("Picture/background.png")
        self.bomb = self.picLoader.load("Picture/star_green.bmp",25,25)
        self.HP = self.picLoader.load("Picture/star_red.bmp",25,25)
        self.time_panel = self.picLoader.load("Picture/time_panel.bmp")
        self.lifetext = self.picLoader.load("Picture/lifetext.png",hasalpha=True)
        self.spelltext = self.picLoader.load("Picture/spelltext.png",hasalpha=True)
        self.hiscoretext = self.picLoader.load("Picture/hiscore.png",hasalpha=True)
        self.scoretext = self.picLoader.load("Picture/score.png",hasalpha=True)
        self.grazetext = self.picLoader.load("Picture/graze.png",hasalpha=True)
        self.bonustext = self.picLoader.load("Picture/spellbonus.png",hasalpha=True)
        self.bonusfailedtext = self.picLoader.load("Picture/bounsfailed.png",hasalpha=True)
        self.tempbar = self.picLoader.load("Picture/tempbar.bmp")
        self.test = self.picLoader.load("Picture/test.png")
        self.ice = self.picLoader.load("Picture/ice.bmp",16,16)
        self.mainmenureimu = self.picLoader.load("Picture/reimu.png",hasalpha=True)
        self.mainmenumarisa = self.picLoader.load("Picture/marisa.png",hasalpha=True)
        self.reimu = self.picLoader.load("Picture/reimu.png",360,540,True)
        self.marisa = self.picLoader.load("Picture/marisa.png",360,540,True)
        self.cirno = self.picLoader.load("Picture/cirno.png",360,540,True)
        self.marisadesc = self.picLoader.load("Picture/marisadesc.png",hasalpha=True)
        self.reimudesc = self.picLoader.load("Picture/reimudesc.png",hasalpha=True)
        self.mainbackground = self.picLoader.load("Picture/mainbackground.png")
        self.font_36 = pygame.font.Font("fonts/fonts.ttf", 36)
        self.font_28 = pygame.font.Font("fonts/fonts.ttf", 28)
        self.font_24 = pygame.font.Font("fonts/fonts.ttf", 24)
        self.font_20 = pygame.font.Font("fonts/fonts.ttf", 20)
        self.font_16 = pygame.font.Font("fonts/fonts.ttf", 16)
        self.font_12 = pygame.font.Font("fonts/fonts.ttf", 12)
        self.settings = settings
        self.fpsTimer = 0
        self.fpslist = []
        self.versiontext = self.font_16.render(
                "DEV 240120 早期开发版本", True, "WHITE")
        self.framework.blit(self.scoretext,(642,130)) # 将文字绘制到背景
        self.framework.blit(self.lifetext,(620,170))
        self.framework.blit(self.spelltext,(620,210))
        self.framework.blit(self.grazetext,(642,250))
        self.framework.blit(self.versiontext, (0, 700))
    

    def drawBefore(self, screen):
        screen.blit(self.background, (30, 20))

    def drawAfter(self, screen, baka, player_Character, se, clock, score):
        # 游戏UI背景
        screen.blit(self.framework, (0, 0))
        # 帧率显示
        if not self.fpsTimer:
            nowfps = clock.get_fps()
            if nowfps > 57:
                fpscolor = (255, 255, 255)
            else:
                fpscolor = (255, 0, 0)
            self.fpstext = self.font_20.render(str("{0:.2f}".format(
                nowfps/2 if self.settings["powersave"] else nowfps)), True, fpscolor)
            self.fpslist.append(nowfps/2 if self.settings["powersave"] else nowfps)
            self.fpsTimer = 60
        screen.blit(self.fpstext, (900, 680))
        self.fpsTimer -= 1
        # 敌机血量显示
        screen.blit(pygame.transform.scale(self.enemy_hp_bar, (max(
            500*baka.HP/baka.spelldata[baka.spell].hp, 0), 20)), (90, 35))
        screen.blit(self.time_panel, (50, 22))
        # 敌机剩余符卡显示
        spellcount = 0
        for spell in baka.spelldata[baka.spell:len(baka.spelldata)]:
            if spell.isspell:
                spellcount += 1
                screen.blit(self.ice, (80+16*spellcount, 60))
        # 分数显示
        screen.blit(self.font_24.render("{0:0>10}".format(
            score), True, (240, 240, 240)), (740, 130))
        # 残机显示
        for i in range(player_Character.HP):
            screen.blit(self.HP, (740+i*25, 172))
        # 符卡显示
        for i in range(player_Character.Bomb):
            screen.blit(self.bomb, (740+i*25, 212))
        # 擦弹数量显示
        screen.blit(self.font_24.render("{0}".format(
            player_Character.graze), True, (240, 240, 240)), (740, 250))
        # 敌人位置显示
        screen.blit(self.font_16.render(
            "| ENEMY |", True, (255, 0, 0)), (baka.rect.x, 700))
        # 剩余时间显示
        self.lefttime = int(
            (baka.spelldata[baka.spell].time - baka.spelltick) / 6)
        lefttimestr = str(self.lefttime)
        if self.lefttime > 99:
            for i,c in enumerate(lefttimestr):
                if i == 2:
                    screen.blit(self.font_20.render(".",True,"BLACK"),(79,31))
                    screen.blit(self.font_16.render(c,True,"BLACK"),(83,36))
                    return
                screen.blit(self.font_20.render(c,True,"BLACK"),(55+12*i,31))
            return
        elif self.lefttime > 9:
            if lefttimestr[1] == "0": # 非等宽字体，只能单个绘制
                se.play("timeout")
            screen.blit(self.font_20.render("0", True, "RED"), (55, 31))
            screen.blit(self.font_20.render(lefttimestr[0], True, "RED"), (67, 31))
            screen.blit((self.font_20.render(".", True, "RED")), (79, 31))
            screen.blit(self.font_16.render(lefttimestr[1], True, "RED"), (83, 36))
            return
        else:
            screen.blit(self.font_20.render("0", True, "RED"), (55, 31))
            screen.blit(self.font_20.render("0", True, "RED"), (67, 31))
            screen.blit((self.font_20.render(".", True, "RED")), (79, 31))
            screen.blit(self.font_16.render(lefttimestr[0], True, "RED"), (83, 36))