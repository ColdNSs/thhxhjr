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


class UIDrawer():
    def __init__(self, settings):
        self.bulletitem = pygame.image.load("Picture/bulletitem.bmp").convert()
        self.enemy_hp_bar = pygame.image.load("Picture/hp_bar.bmp").convert()
        self.framework = pygame.image.load("Picture/framework.png").convert()
        self.background = pygame.image.load("Picture/background.png").convert()
        self.bomb = pygame.image.load("Picture/star_green.bmp").convert()
        self.HP = pygame.image.load("Picture/star_red.bmp").convert()
        self.time_panel = pygame.image.load("Picture/time_panel.bmp").convert()
        self.framework.set_colorkey((255, 255, 255))
        self.bomb.set_colorkey((240, 240, 240))
        self.HP.set_colorkey((240, 240, 240))
        self.time_panel.set_colorkey("BLACK")
        self.font_Arial20 = pygame.sysfont.SysFont('Arial', 20)
        self.font_Arial24 = pygame.sysfont.SysFont('Arial', 24)
        self.font_Arial36 = pygame.sysfont.SysFont('Arial', 36)
        self.font_Simsun20 = pygame.sysfont.SysFont('SimSun', 20)
        self.font_Simsun16 = pygame.sysfont.SysFont('SimSun', 16)
        self.settings = settings
        self.fpsTimer = 0
        self.showspellfailedtime = 0
        self.showspellscoredata = {"score": 0, "time": 0}

    def drawBefore(self, screen):
        screen.blit(self.background, (30, 20))

    def showspellscore(self, screen):
        if self.showspellscoredata["time"]:
            char_count = int((150 - self.showspellscoredata["time"]) / 6)
            screen.blit(self.font_Arial36.render("Get Spell Bonus!!",
                        True, (255, 255, 255)), (210, 250))
            screen.blit(self.font_Arial24.render(str(self.showspellscoredata["score"]).rjust(
                8, "0")[:char_count], True, (255, 0, 0)), (290, 290))
            self.showspellscoredata["time"] -= 1
        if self.showspellfailedtime:
            screen.blit(self.font_Arial36.render("Bonus Failed...",
                        True, (235, 235, 235)), (246, 250))
            self.showspellfailedtime -= 1

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
            self.fpstext = self.font_Arial20.render(str("{0:.2f}".format(
                nowfps/2 if self.settings["powersave"] else nowfps)), True, fpscolor)
            self.versiontext = self.font_Simsun16.render(
                "DEV 231226 早期开发版本", True, "WHITE")
            self.fpsTimer = 60
        screen.blit(self.fpstext, (900, 680))
        screen.blit(self.versiontext, (0, 700))
        self.fpsTimer -= 1
        # 敌机血量显示
        screen.blit(pygame.transform.scale(self.enemy_hp_bar, (max(
            500*baka.HP/baka.HPlist[baka.spell - 1], 0), 20)), (90, 35))
        screen.blit(self.time_panel, (50, 22))
        # 分数显示
        screen.blit(self.font_Simsun20.render("   Score：{0:0>10}".format(
            score), True, (240, 240, 240)), (630, 140))
        # 残机显示
        screen.blit(self.font_Simsun20.render(
            "剩余人数：", True, (240, 240, 240)), (630, 170))
        for i in range(player_Character.HP):
            screen.blit(self.HP, (730+i*25, 170))
        # 符卡显示
        screen.blit(self.font_Simsun20.render(
            "剩余符卡：", True, (240, 240, 240)), (630, 200))
        for i in range(player_Character.Bomb):
            screen.blit(self.bomb, (730+i*25, 200))
        # 擦弹数量显示
        screen.blit(self.font_Simsun20.render("擦弹数：{0}".format(
            player_Character.graze), True, (240, 240, 240)), (630, 230))
        # 敌人位置显示
        screen.blit(self.font_Simsun16.render(
            "| ENEMY |", True, (255, 0, 0)), (baka.rect.x, 700))
        # 剩余时间显示
        self.lefttime = int(
            (baka.spellTimeLimitList[baka.spell - 1] - baka.spelltick) / 6)
        if self.lefttime > 99:
            screen.blit(self.font_Arial24.render(
                str(int(self.lefttime / 10)), True, "BLACK"), (55, 31))
            screen.blit((self.font_Arial24.render(
                ".", True, "BLACK")), (79, 31))
            screen.blit(self.font_Arial20.render(
                str(int(self.lefttime - int(self.lefttime / 10) * 10)), True, "BLACK"), (83, 35))
        else:
            if self.lefttime % 10 == 9:
                se.play("timeout")
            screen.blit(self.font_Arial24.render(
                "0"+str(int(self.lefttime / 10)), True, "RED"), (55, 31))
            screen.blit((self.font_Arial24.render(".", True, "RED")), (79, 31))
            screen.blit(self.font_Arial20.render(
                str(int(self.lefttime - int(self.lefttime / 10) * 10)), True, "RED"), (83, 35))
        self.showspellscore(screen)
