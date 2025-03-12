#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as pg
from menu import MenuItem, Menu, fonts, UIElement, UIAnimationMove, UIAnimationAlpha


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


class ManualScene(Scene):
    def __init__(self, screen: pg.surface.Surface, created_by: Scene):
        super().__init__(screen)
        self.created_by = created_by
        self.assets = {
            'background': UIElement(pg.image.load("./Picture/mainbackground.png").convert(), (0, 0)),
            'logo': UIElement(pg.image.load('./Picture/title.png').convert_alpha(), (0, 0)),
        }
        item_list = [
            MenuItem(0, 'START', self.menu_action, True),
            MenuItem(1, 'PRACTICE\n START', self.menu_action, True),
            MenuItem(2, 'PLAYER DATA', self.menu_action, True),
            MenuItem(3, 'REPLAY', self.menu_action, True),
        ]
        self.menu = Menu(item_list, fonts['font_36'], (350, 250), None, loopable=False)
        self.manual_show = False
        self.animations = []

    def menu_action(self, action_id):
        if not self.manual_show:
            self.manual_show = True
            self.animations.append(UIAnimationMove(self.menu, 10, 0, False, target_pos=(50, 250)))

    def draw(self):
        self.assets['background'].draw(self.screen)
        self.menu.draw(self.screen)

    def update(self, events: list[pg.event.EventType]):
        self.update_inputs(events)

        # Clear animations that are done. Execute animations
        self.animations = [animation for animation in self.animations if animation.active]
        for animation in self.animations:
            animation.update()

        if not self.animations:
            if self.key_down(pg.K_x):
                if self.manual_show:
                    self.manual_show = False
                    self.animations.append(UIAnimationMove(self.menu, 10, 0, False, target_pos=(350, 250)))
                else:
                    self.goal = self.created_by

            self.menu.update(self.key_down)


        self.draw()
        self.tick += 1