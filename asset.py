from typing import Any
import pygame


class SEPlayer():
    MISS_CHANNEL = 33
    PLAYER_SPELL_CHANNEL = 34
    ENEMY_SPELL_CHANNEL = 35
    ENEMY_DESTORY_CHANNEL = 36
    SPELL_EXTEND_CHANNEL = 37
    VOLUME_TEST_CHANNEL = 37
    EXTEND_CHANNEL = 38
    def __init__(self,settings):
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
        self.soundasset["extend"] = pygame.mixer.Sound("SE/extend.wav")
        self.soundasset["defeat"] = pygame.mixer.Sound("SE/defeat.wav")
        self.setvolume(settings["sevol"])

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
    def __init__(self,font:pygame.font.Font,menulist,defaultcolor,choicecolor,disablecolor,posvec,iscirculute = False,defaultchoice = 0,linesep = 5):
        self.font = font
        self.menulist = menulist
        self.defaultcolor = defaultcolor
        self.choicecolor = choicecolor
        self.disablecolor = disablecolor
        self.choice = defaultchoice
        self.iscirculute = iscirculute
        self.posvec = posvec
        self.linesep = linesep
        self.optiongroup = pygame.sprite.Group()
        self.choiceablelist = []
        for i, struct in enumerate(self.menulist):
            self.optiongroup.add(self.MenuSprite(self,struct,i))
            if not struct.isdisabled:
                self.choiceablelist.append(i) # 维护一个可选择选项的索引
        pass
        self.exactchoice = self.choiceablelist[self.choice]
    def up(self):
        self.choice -= 1
        self.choice = max(0,self.choice) if not self.iscirculute else self.choice % len(self.choiceablelist)
        self.exactchoice = self.choiceablelist[self.choice]

    def down(self):
        self.choice += 1
        self.choice = min(len(self.choiceablelist) - 1,self.choice) if not self.iscirculute else self.choice % len(self.choiceablelist)
        self.exactchoice = self.choiceablelist[self.choice]
    
    def jumpto(self,id):
        self.exactchoice = id
        

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
            if self.id == self.owner.choice: # 默认选择
                self.color = self.owner.choicecolor
            if struct.isdisabled:
                self.color = self.owner.disablecolor
            self.image = self.owner.font.render(struct.text,True,self.color)
            self.rect = self.image.get_rect()
            self.rect.x,self.rect.y = self.owner.posvec[0], self.owner.posvec[1] + (self.image.get_height() + self.owner.linesep) * id

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

class ManualContent():
    class Struct():
        def __init__(self,text,color="WHITE"):
            self.text = text
            self.color = color
    
    textlist = [[
            Struct("1.游戏的简要介绍:"),
            Struct("这是一款东方同人弹幕射击游戏，目标是操纵主角打倒敌人。"),
            Struct(""),
            Struct("背景故事:"),
            Struct("红魔馆旁的雾之湖，似乎受到了某种奇怪异变的影响。"),
            Struct("即使在初夏阳光的照耀下散去雾气的湖面，也散发着不自然的冷气。"),
            Struct("以雾之湖为基地，由自然力量具象出的冰之小妖精琪露诺，"),
            Struct("也因为这异变的影响变得更加的强大和躁动了起来。"),
            Struct("而灵梦和魔理沙，也已在前往雾之湖一探究竟的路上。")
            # 纯属瞎编 没有后续
        ],[
            Struct("2.操作方法:"),
            Struct("自机移动:↑ ↓ ← →"),
            Struct("确定/射击:Z"),
            Struct("取消/释放符卡:X"),
            Struct("特殊按键:C（后述）"),
            Struct("需要注意的是:在存储录像输入机签时使用ESC取消，ENTER确认。","RED")
        ],[
            Struct("3.游戏界面:"),
            Struct("剩余人数:剩余可以MISS的次数，当所有星星消失后再次MISS游戏结束","RED"),
            Struct("剩余符卡:可以使用BOMB的次数","GREEN"),
            Struct("GRAZE:擦弹数，通过擦弹可以得到分数和增加温度槽（后述）"),
            Struct("SCORE/HISCORE:当前得分和历史最高得分"),
            Struct("温度槽:右下角的指示器,用于指示当前温度")
        ],[
            Struct("4.小心低温！:"),
            Struct("雾之湖正出奇的寒冷，而妖精身上也时刻散发着非比寻常的寒气",(32,64,255)),
            Struct("体温时刻在降低，作为人类的灵梦和魔理沙并不能长时间的身处这种环境下战斗。"),
            Struct("好在借助河童的科技装置，主角们可以通过各种方式提升自己的体温。"),
            Struct("说明:右下角的温度槽指示着自机的当前温度，同时分别具有红蓝两个标记。"),
            Struct("当温度高于红色标记时,擦弹将会有额外得分，"),
            Struct("当温度溢出后，获得的温度将转化为分数，并增加生命恢复槽，生命恢复槽满则残机+1；"),
            Struct("反之，当温度低于蓝色标记时，副机将无法进行射击，且视野逐渐变暗"),
            Struct("当温度归零后，自机将无法使用BOMB。"),
            Struct("可以随时通过使用河童的供暖装置（按下C键），将目前持有的一个BOMB转化成温度"),
            Struct("以下事件会影响温度:"),
            Struct("+ 擦弹、获取分数道具、收取符卡、造成伤害","GREEN"),
            Struct("- 随时间自然减少、MISS","RED"),
            Struct("切记管理好自己的体温，避免陷入苦战的恶性循环！")
        ]]

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
        self.bonustext = self.picLoader.load("Picture/spellbonus.png",hasalpha=True)
        self.bonusfailedtext = self.picLoader.load("Picture/bounsfailed.png",hasalpha=True)
        self.tempbar = self.picLoader.load("Picture/tempbar.bmp")
        self.fontasset = self.picLoader.load("Picture/fontasset.png",hasalpha=True)
        self.ice = self.picLoader.load("Picture/ice.bmp",16,16)
        self.mainmenureimu = self.picLoader.load("Picture/reimu.png",hasalpha=True)
        self.mainmenumarisa = self.picLoader.load("Picture/marisa.png",hasalpha=True)
        self.reimu = self.picLoader.load("Picture/reimu.png",360,540,True)
        self.marisa = self.picLoader.load("Picture/marisa.png",360,540,True)
        self.cirno = self.picLoader.load("Picture/cirno.png",360,540,True)
        self.marisadesc = self.picLoader.load("Picture/marisadesc.png",hasalpha=True)
        self.reimudesc = self.picLoader.load("Picture/reimudesc.png",hasalpha=True)
        self.mainbackground = self.picLoader.load("Picture/mainbackground.png")
        self.enemypos = self.picLoader.load("Picture/enemypos.png",hasalpha=True)
        self.liferecbox = self.picLoader.load("Picture/liferecbox.png")
        self.liferecbar = self.picLoader.load("Picture/liferecbar.png")
        self.whitestar = self.picLoader.load("Picture/bigstar_white.bmp")
        self.gameclear = self.picLoader.load("Picture/gameclear.png",hasalpha=True)
        self.font_36 = pygame.font.Font("fonts/fonts.ttf", 36)
        self.font_28 = pygame.font.Font("fonts/fonts.ttf", 28)
        self.font_24 = pygame.font.Font("fonts/fonts.ttf", 24)
        self.font_20 = pygame.font.Font("fonts/fonts.ttf", 20)
        self.font_16 = pygame.font.Font("fonts/fonts.ttf", 16)
        self.font_12 = pygame.font.Font("fonts/fonts.ttf", 12)
        self.font_mono_20 = pygame.font.Font("fonts/fonts_mono.ttf", 20)
        self.font_mono_24 = pygame.font.Font("fonts/fonts_mono.ttf", 24)
        self.settings = settings
        self.fpsTimer = 0
        self.fpslist = []
        self.framework.blit(self.fontasset,(620,95))
        self.framework.blit(self.liferecbox,(742,290))

    def updatesettings(self,settings):
        self.settings = settings
        
    def drawBefore(self, screen):
        screen.blit(self.background, (30, 20))

    def drawAfter(self, screen, baka, player_Character, se, clock, score,hiscore):
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
            nowfps = min(60,nowfps) # 防止超过60的帧率影响处理落率的计算
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
        # 分数和最高分显示 非等宽坏文明
        hiscoretext = "{0:0>10}".format(max(score,hiscore))
        scoretext = "{0:0>10}".format(score)
        for i in range(10):
            if hiscoretext[i] == "1":
                screen.blit(self.font_24.render(hiscoretext[i], True, (240, 240, 240)), (740+16*i+7, 90))
            else:
                screen.blit(self.font_24.render(hiscoretext[i], True, (240, 240, 240)), (740+16*i, 90))
            if scoretext[i] == "1":
                screen.blit(self.font_24.render(scoretext[i], True, (240, 240, 240)), (740+16*i+7, 130))
            else:
                screen.blit(self.font_24.render(scoretext[i], True, (240, 240, 240)), (740+16*i, 130))
        # 残机显示
        for i in range(player_Character.HP):
            screen.blit(self.HP, (740+i*25, 172))
        # 符卡显示
        for i in range(player_Character.Bomb):
            screen.blit(self.bomb, (740+i*25, 212))
        # 擦弹数量显示
        screen.blit(self.font_24.render("{0}".format(
            player_Character.graze), True, (240, 240, 240)), (740, 250))
        # 生命恢复槽显示
        screen.blit(pygame.transform.scale(self.liferecbar, (
            123*player_Character.liferecprog/player_Character.liferectotal, 28)), (743, 291))
        # 敌人位置显示
        screen.blit(self.enemypos, (baka.rect.x, 696))
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