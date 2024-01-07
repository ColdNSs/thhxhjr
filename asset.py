import pygame


class SEPlayer():
    MISS_CHANNEL = 33
    PLAYER_SPELL_CHANNEL = 34
    ENEMY_SPELL_CHANNEL = 35
    ENEMY_DESTORY_CHANNEL = 35

    def __init__(self):
        self.channel = 0
        self.soundasset = {}
        self.soundasset["damage"] = pygame.mixer.Sound("SE/damage.wav")
        self.soundasset["damageloud"] = pygame.mixer.Sound("SE/damageloud.wav")
        self.soundasset["destory"] = pygame.mixer.Sound("SE/destory.wav")
        self.soundasset["graze"] = pygame.mixer.Sound("SE/graze.wav")
        self.soundasset["item"] = pygame.mixer.Sound("SE/item.wav")
        self.soundasset["miss"] = pygame.mixer.Sound("SE/miss.wav")
        self.soundasset["pause"] = pygame.mixer.Sound("SE/pause.wav")
        self.soundasset["timeout"] = pygame.mixer.Sound("SE/timeout.wav")
        self.soundasset["shoot"] = pygame.mixer.Sound("SE/shoot.wav")
        self.soundasset["bomb"] = pygame.mixer.Sound("SE/bomb.wav")
        self.soundasset["enemyst01"] = pygame.mixer.Sound("SE/enemyst01.wav")
        self.soundasset["enemyst02"] = pygame.mixer.Sound("SE/enemyst02.wav")
        self.setvolume(0.2)

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


class UIDrawer():
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
        self.ice = self.picLoader.load("Picture/ice.bmp",16,16)
        self.font_24 = pygame.font.Font("fonts/fonts.ttf", 24)
        self.font_20 = pygame.font.Font("fonts/fonts.ttf", 20)
        self.font_16 = pygame.font.Font("fonts/fonts.ttf", 16)
        self.settings = settings
        self.fpsTimer = 0
        self.framework.blit(self.scoretext,(642,130)) # 将文字绘制到背景
        self.framework.blit(self.lifetext,(620,170))
        self.framework.blit(self.spelltext,(620,210))
        self.framework.blit(self.grazetext,(642,250))
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
            self.versiontext = self.font_16.render(
                "DEV 240107 早期开发版本", True, "WHITE")
            self.fpsTimer = 60
        screen.blit(self.fpstext, (900, 680))
        screen.blit(self.versiontext, (0, 700))
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
        screen.blit(self.font_20.render("0", True, "RED"), (55, 31))
        screen.blit(self.font_20.render("0", True, "RED"), (67, 31))
        screen.blit((self.font_20.render(".", True, "RED")), (79, 31))
        screen.blit(self.font_16.render(lefttimestr[0], True, "RED"), (83, 36))