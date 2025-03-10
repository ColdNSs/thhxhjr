#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as pg
from menu import *

def exit_game():
    pg.quit()
    exit()


class Scene:
    def __init__(self, screen: pg.surface.SurfaceType, created_by=None):
        self.screen = screen
        self.created_by = created_by
        self.goal = None
        self.inputs = {'down': [], 'up': [], 'pressed': type[pg.key.ScancodeWrapper]}
        self.tick = 0

    def get_input(self, events: list[pg.event.EventType]):
        # Get changed inputs
        down_inputs = []
        up_inputs = []
        for event in events:
            if event.type == pg.KEYDOWN:
                down_inputs.append(event.key)
            if event.type == pg.KEYUP:
                up_inputs.append(event.key)

        # Get pressed inputs
        pressed_inputs = pg.key.get_pressed()

        self.inputs['down'] = down_inputs
        self.inputs['up'] = up_inputs
        self.inputs['pressed'] = pressed_inputs

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
    def __init__(self, screen: pg.surface.SurfaceType, created_by=None):
        super().__init__(screen, created_by)
        self.animation_tick = 0
        self.assets = {'banner': pg.image.load("./Picture/banner.png").convert()}

    def jump_to_title(self):
        if self.animation_tick >= 180:
            self.goal = TitleScene(self.screen, self)

    def draw(self):
        self.assets['banner'].set_alpha(min(255, self.animation_tick * 4))
        self.screen.fill('black')
        self.screen.blit(self.assets['banner'], (0, 0))

    def update(self, events: list[pg.event.EventType]):
        self.jump_to_title()
        self.get_input(events)
        if self.key_pressed(pg.K_LCTRL):
            self.animation_tick += 1
        self.draw()
        self.tick += 1
        self.animation_tick += 1


class TitleScene(Scene):
    def __init__(self, screen: pg.surface.SurfaceType, created_by=None):
        super().__init__(screen, created_by)
        self.assets = {'background': pg.image.load("./Picture/mainbackground.png").convert(),
                       'logo': pg.image.load('./Picture/title.png').convert_alpha(),
                       }
        self.selected_item = 0
        self.background_offset = (0, 0)
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
        self.menu = Menu(self.item_list, font_24, (50, 400), None, is_circulate=True)

    def jump_to_scene(self):
        pass

    def draw(self):
        self.screen.blit(self.assets['background'], self.background_offset)
        self.screen.blit(self.assets['logo'], (0, 0))
        self.menu.draw(self.screen)

    def update(self, events: list[pg.event.EventType]):
        self.get_input(events)
        self.menu.update(self)
        self.draw()
        self.tick = self.tick + 1