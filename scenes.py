#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as pg
from menu import MenuItem, Menu, fonts, UIElement, UIAnimationMove

def exit_game():
    # Post quit event. Quit is handled in the main loop instead
    pg.event.post(pg.event.Event(pg.QUIT))


class Scene:
    def __init__(self, screen: pg.surface.SurfaceType):
        self.screen = screen
        self.goal = None
        self.inputs = {'down': [], 'up': [], 'pressed': type[pg.key.ScancodeWrapper]}
        self.tick = 0

    def get_input(self, events: list[pg.event.EventType]):
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
        self.get_input(events)
        self.draw()
        self.tick = self.tick + 1


class BannerScene(Scene):
    def __init__(self, screen: pg.surface.SurfaceType):
        super().__init__(screen)
        self.animation_tick = 0
        self.assets = {'banner': pg.image.load("./Picture/banner.png").convert()}

    def jump_to_title(self):
        if self.animation_tick >= 180:
            self.goal = TitleScene(self.screen)

    def draw(self):
        self.assets['banner'].set_alpha(min(255, self.animation_tick * 4))
        self.screen.fill('black')
        self.screen.blit(self.assets['banner'], (0, 0))

    def update(self, events: list[pg.event.EventType]):
        self.jump_to_title()
        self.get_input(events)
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
        self.item_list = [
            MenuItem(0, 'START', self.jump_to_scene, True),
            MenuItem(1, 'PRACTICE START', self.jump_to_scene, False),
            MenuItem(2, 'PLAYER DATA', self.jump_to_scene, True),
            MenuItem(3, 'REPLAY', self.jump_to_scene, True),
            MenuItem(4, 'MANUAL', self.jump_to_scene, True),
            MenuItem(5, 'OPTION', self.jump_to_scene, True),
            MenuItem(6, 'MUSIC ROOM', self.jump_to_scene, False),
            MenuItem(7, 'EXIT', exit_game, True),
        ]
        self.menu = Menu(self.item_list, fonts['font_24'], (50, 400), None, loopable=True)
        self.animations = [
            UIAnimationMove(self.assets['logo'], 60, 60, False, (100, 200), (300,250)),
            UIAnimationMove(self.menu, 60, 60, False, (500, 200), (600,250))
        ]

    def jump_to_scene(self):
        if self.menu.selected_item != 0:
            return
        self.goal = BannerScene(self.screen)

    def draw(self):
        self.assets['background'].draw(self.screen)
        self.assets['logo'].draw(self.screen)
        self.menu.draw(self.screen)

    def update(self, events: list[pg.event.EventType]):
        self.get_input(events)
        self.menu.update(self.key_down)

        # Clear animations that are done
        self.animations = [animation for animation in self.animations if animation.active]
        for animation in self.animations:
            animation.update()

        self.draw()
        self.tick += 1