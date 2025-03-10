#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as pg


class Scene:
    def __init__(self, screen: pg.surface.SurfaceType, created_by=None):
        self.screen = screen
        self.created_by = created_by
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

    def draw(self):
        self.assets['banner'].set_alpha(min(255, self.animation_tick * 4))
        self.screen.fill('black')
        self.screen.blit(self.assets['banner'], (0, 0))

    def update(self, events: list[pg.event.EventType]):
        self.get_input(events)
        if self.key_pressed(pg.K_LCTRL):
            self.animation_tick += 1
        self.draw()
        self.tick += 1
        self.animation_tick += 1


class TitleScene(Scene):
    def __init__(self, screen: pg.surface.SurfaceType, created_by=None):
        super().__init__(screen, created_by)
        self.assets = {'background': pg.image.load("./Picture/background.png").convert(),
                       }
        self.selected_item = 0

    def draw(self):
        pass

    def update(self, events: list[pg.event.EventType]):
        self.get_input(events)
        self.draw()
        self.tick = self.tick + 1