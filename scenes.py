#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as pg
from menu import TextItem, Text, MenuItem, Menu, fonts, UIElement, UIAnimationMove, UIAnimationAlpha


class Scene:
    def __init__(self, screen: pg.surface.SurfaceType):
        self.screen = screen
        self.goal = None
        self.inputs = {'down': [], 'up': [], 'pressed': type[pg.key.ScancodeWrapper]}
        self.tick = 0

    def update_inputs(self, events: list[pg.event.EventType]):
        # GET DOWN inputs and up inputs
        self.inputs['down'] = [event.key for event in events if event.type == pg.KEYDOWN]
        self.inputs['up'] = [event.key for event in events if event.type == pg.KEYUP]

        # Get pressed inputs
        self.inputs['pressed'] = pg.key.get_pressed()

    def key_down(self, key: int):
        if key in self.inputs['down']:
            return True
        return False

    def key_up(self, key: int):
        if key in self.inputs['up']:
            return True
        return False

    def key_pressed(self, key: int):
        if self.inputs['pressed'][key]:
            return True
        return False

    def get_goal(self):
        goal = self.goal
        self.goal = None
        return goal

    def draw(self):
        pass

    def update(self, events: list[pg.event.EventType]):
        self.update_inputs(events)
        self.draw()
        self.tick = self.tick + 1


class BannerScene(Scene):
    def __init__(self, screen: pg.surface.SurfaceType):
        super().__init__(screen)
        self.animation_tick = 0
        self.assets = {'banner': UIElement(pg.image.load("./Picture/banner.png").convert(), (0, 0))}

    def jump_to_title(self):
        if self.animation_tick >= 180:
            self.goal = TitleScene(self.screen)

    def draw(self):
        self.assets['banner'].image.set_alpha(min(255, self.animation_tick * 4))
        self.screen.fill('black')
        self.assets['banner'].draw(self.screen)

    def update(self, events: list[pg.event.EventType]):
        self.jump_to_title()
        self.update_inputs(events)
        if self.key_pressed(pg.K_LCTRL):
            self.animation_tick += 2
        self.draw()
        self.animation_tick += 1
        self.tick += 1


class TitleScene(Scene):
    def __init__(self, screen: pg.surface.SurfaceType):
        super().__init__(screen)
        self.assets = {
            'background': UIElement(pg.image.load("./Picture/mainbackground.png").convert(), (0, 0)),
            'logo': UIElement(pg.image.load('./Picture/title.png').convert_alpha(), (0, 0)),
                       }
        item_list = [
            MenuItem(0, 'START', self.menu_action, True),
            MenuItem(1, 'PRACTICE START', self.menu_action, False),
            MenuItem(2, 'PLAYER DATA', self.menu_action, True),
            MenuItem(3, 'REPLAY', self.menu_action, True),
            MenuItem(4, 'MANUAL', self.menu_action, True),
            MenuItem(5, 'OPTION', self.menu_action, True),
            MenuItem(6, 'MUSIC ROOM', self.menu_action, False),
            MenuItem(7, 'EXIT', self.menu_action, True),
        ]
        self.menu = Menu(item_list, fonts['font_24'], (50, 400), None, loopable=True)
        self.animations = [
            UIAnimationMove(self.assets['logo'], 60, 0, False, (200, 100), (350,175)),
            UIAnimationAlpha(self.assets['logo'], 60, 0, False, start_alpha=40),
            # UIAnimationMove(self.menu, 60, 60, True, (500, 200), (600,250))
        ]

    def menu_action(self, action_id: int):
        if action_id == 7:
            # Post quit event. Quit is handled in the main loop instead
            pg.event.post(pg.event.Event(pg.QUIT))
        elif action_id == 4:
            self.goal = ManualScene(self.screen, self)
        else:
            self.goal = BannerScene(self.screen)

    def draw(self):
        self.assets['background'].draw(self.screen)
        self.assets['logo'].draw(self.screen)
        self.menu.draw(self.screen)

    def update(self, events: list[pg.event.EventType]):
        self.update_inputs(events)

        # Clear animations that are done. Execute animations
        self.animations = [animation for animation in self.animations if animation.active]
        for animation in self.animations:
            animation.update()

        self.menu.update(self.key_down)

        self.draw()
        self.tick += 1


# TODO: Move this whole ass text block to somewhere else; adding localization support
class ManualScene(Scene):
    def __init__(self, screen: pg.surface.Surface, created_by: Scene):
        super().__init__(screen)
        self.created_by = created_by
        self.assets = {
            'background': UIElement(pg.image.load("./Picture/mainbackground.png").convert(), (0, 0)),
            'logo': UIElement(pg.image.load('./Picture/title.png').convert_alpha(), (0, 0)),
        }
        item_list = [
            MenuItem(0, '简要介绍', self.no_action, True),
            MenuItem(1, '操作方法', self.no_action, True),
            MenuItem(2, '游戏界面', self.no_action, True),
            MenuItem(3, '小心低温！', self.no_action, True),
        ]
        self.menu = Menu(item_list, fonts['font_36'], (350, 250), None, loopable=False)
        item_list = [
            TextItem("1.游戏的简要介绍:"),
            TextItem("这是一款东方同人弹幕射击游戏，目标是操纵主角打倒敌人。"),
            TextItem(""),
            TextItem("背景故事:"),
            TextItem("红魔馆旁的雾之湖，似乎受到了某种奇怪异变的影响。"),
            TextItem("即使在初夏阳光的照耀下散去雾气的湖面，也散发着不自然的冷气。"),
            TextItem("以雾之湖为基地，由自然力量具象出的冰之小妖精琪露诺，"),
            TextItem("也因为这异变的影响变得更加的强大和躁动了起来。"),
            TextItem("而灵梦和魔理沙，也已在前往雾之湖一探究竟的路上。")
            # 纯属瞎编 没有后续
            # 俺觉得编得蛮不错 - ColdNSs
        ]
        self.text_1 = Text(item_list, fonts['font_24'], (250, 200), 'white')
        self.text_2 = Text(item_list, fonts['font_24'], (250, 200 + 720), 'white')
        self.text_3 = Text(item_list, fonts['font_24'], (250, 200 + 720 * 2), 'white')
        self.text_4 = Text(item_list, fonts['font_24'], (250, 200 + 720 * 3), 'white')
        self.text_1.image.set_alpha(0)
        self.text_2.image.set_alpha(0)
        self.text_3.image.set_alpha(0)
        self.text_4.image.set_alpha(0)
        self.manual_show = False
        self.animations = []

    def no_action(self, action_id):
        return

    def draw(self):
        self.assets['background'].draw(self.screen)
        self.text_1.draw(self.screen)
        self.text_2.draw(self.screen)
        self.text_3.draw(self.screen)
        self.text_4.draw(self.screen)

        self.menu.draw(self.screen)

    def update(self, events: list[pg.event.EventType]):
        self.update_inputs(events)

        # Clear animations that are done. Execute animations
        self.animations = [animation for animation in self.animations if animation.active]
        for animation in self.animations:
            animation.update()

        if not self.animations:
            if self.key_down(pg.K_z):
                if not self.manual_show:
                    self.manual_show = True
                    self.animations.append(UIAnimationMove(self.menu, 6, 0, False, target_pos=(50, 250)))
                    self.animations.append(UIAnimationAlpha(self.text_1, 6, 0, False, target_alpha=255))
                    self.animations.append(UIAnimationAlpha(self.text_2, 6, 0, False, target_alpha=255))
                    self.animations.append(UIAnimationAlpha(self.text_3, 6, 0, False, target_alpha=255))
                    self.animations.append(UIAnimationAlpha(self.text_4, 6, 0, False, target_alpha=255))
            elif self.key_down(pg.K_x):
                if self.manual_show:
                    self.manual_show = False
                    self.animations.append(UIAnimationMove(self.menu, 6, 0, False, target_pos=(350, 250)))
                    self.animations.append(UIAnimationAlpha(self.text_1, 6, 0, False, target_alpha=0))
                    self.animations.append(UIAnimationAlpha(self.text_2, 6, 0, False, target_alpha=0))
                    self.animations.append(UIAnimationAlpha(self.text_3, 6, 0, False, target_alpha=0))
                    self.animations.append(UIAnimationAlpha(self.text_4, 6, 0, False, target_alpha=0))
                else:
                    self.goal = self.created_by

            self.menu.update(self.key_down)

            text_top = 200 - 720 * self.menu.selected_index
            if self.text_1.pos[1] != text_top:
                self.animations.append(UIAnimationMove(self.text_1, 10, 0, False, target_pos=(250, text_top)))
                self.animations.append(UIAnimationMove(self.text_2, 10, 0, False, target_pos=(250, text_top + 720)))
                self.animations.append(UIAnimationMove(self.text_3, 10, 0, False, target_pos=(250, text_top + 720 * 2)))
                self.animations.append(UIAnimationMove(self.text_4, 10, 0, False, target_pos=(250, text_top + 720 * 3)))

        self.draw()
        self.tick += 1