#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as pg

pg.font.init()
font_36 = pg.font.Font("fonts/fonts.ttf", 36)
font_28 = pg.font.Font("fonts/fonts.ttf", 28)
font_24 = pg.font.Font("fonts/fonts.ttf", 24)
font_20 = pg.font.Font("fonts/fonts.ttf", 20)
font_16 = pg.font.Font("fonts/fonts.ttf", 16)
font_12 = pg.font.Font("fonts/fonts.ttf", 12)
font_mono_20 = pg.font.Font("fonts/fonts_mono.ttf", 20)
font_mono_24 = pg.font.Font("fonts/fonts_mono.ttf", 24)


class MenuItem(pg.sprite.Sprite):
    def __init__(self, assigned_id: int, caption: str, action, valid=True):
        super().__init__()
        self.id = assigned_id
        self.caption = caption
        self.action = action
        self.valid = valid
        self.image = None
        self.rect = None
        self.color = 'white'

    def draw(self, screen: pg.surface.SurfaceType):
        screen.blit(self.image, self.rect)

    def update(self, font: pg.font.FontType, pos: tuple, color: dict, line_space: int, selected_item: int):
        if selected_item == self.id:
            self.color = color['selected']
        elif self.valid:
            self.color = color['valid']
        else:
            self.color = color['invalid']

        self.image = font.render(self.caption, True, self.color)
        self.rect = self.image.get_rect()
        x, y = pos
        self.rect.topleft = (x, y + (self.image.get_height() + line_space) * self.id)


class Menu:
    def __init__(
            self,
            item_list: list[MenuItem],
            font: pg.font.FontType,
            pos: tuple,
            color=None,
            line_space=5,
            default_item=0,
            loopable=False,
    ):
        if color is None:
            color = {'selected': 'red', 'valid': 'white', 'invalid': 'grey'}
        self.item_list = item_list
        self.font = font
        self.pos = pos
        self.color = color
        self.line_space = line_space
        self.selected_item = default_item
        self.loopable = loopable

    def draw(self, screen: pg.surface.SurfaceType):
        for item in self.item_list:
            item.draw(screen)

    def down(self):
        for i in range(1, len(self.item_list)):
            goal_id = self.selected_item + i
            if goal_id > len(self.item_list) - 1:
                if not self.loopable:
                    return
                goal_id = goal_id - len(self.item_list)
            if self.item_list[goal_id].valid:
                self.selected_item = goal_id
                return

    def up(self):
        for i in range(1, len(self.item_list)):
            goal_id = self.selected_item - i
            if goal_id < 0:
                if not self.loopable:
                    return
                goal_id = goal_id + len(self.item_list)
            if self.item_list[goal_id].valid:
                self.selected_item = goal_id
                return

    def update(self, scene):
        if scene.key_down(pg.K_z):
            self.item_list[self.selected_item].action()
        elif scene.key_down(pg.K_DOWN):
            self.down()
        elif scene.key_down(pg.K_UP):
            self.up()

        for item in self.item_list:
            item.update(self.font, self.pos, self.color, self.line_space, self.selected_item)
