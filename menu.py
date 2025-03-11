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
fonts = {
    'font_36': font_36,
    'font_28': font_28,
    'font_24': font_24,
    'font_20': font_20,
    'font_16': font_16,
    'font_12': font_12,
    'font_mono_24': font_mono_24,
    'font_mono_20': font_mono_20,
}


class UIElement(pg.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class UIAnimation:
    def __init__(self, element: UIElement, duration: int, delay=0, linear=True):
        if duration < 1:
            duration = 1
        self.element = element
        self.duration = duration
        self.delay = delay
        self.linear = linear
        self.animation_tick = 0
        self.active = True

    def start(self):
        pass

    def complete(self):
        pass

    def animate_progress(self, progress):
        pass

    def update(self):
        if not self.active:
            return

        if self.delay > 0:
            self.delay -= 1
            return

        if self.animation_tick >= self.duration:
            # Animation complete. Element stays at the target state
            self.complete()
            self.active = False
        elif self.animation_tick == 0:
            # Animation start. Element changed to the start state
            self.start()
        else:
            progress = self.animation_tick / self.duration # Linear
            eased_progress = 1 - (1 - progress) ** 2  # Quadratic easing out
            if self.linear:
                self.animate_progress(progress)
            else:
                self.animate_progress(eased_progress)

        self.animation_tick += 1


class UIAnimationMove(UIAnimation):
    def __init__(self, element: UIElement, duration: int, delay=0, linear=True, start_pos=None, target_pos=None):
        if start_pos is None:
            start_pos = element.rect.topleft
        if target_pos is None:
            target_pos = element.rect.topleft

        super().__init__(element, duration, delay, linear)
        self.start_pos = start_pos
        self.target_pos = target_pos

    def start(self):
        self.element.rect.topleft = self.start_pos

    def complete(self):
        self.element.rect.topleft = self.target_pos

    def animate_progress(self, progress):
        new_x = self.start_pos[0] + (self.target_pos[0] - self.start_pos[0]) * progress
        new_y = self.start_pos[1] + (self.target_pos[1] - self.start_pos[1]) * progress
        self.element.rect.topleft = (new_x, new_y)


class MenuItem(UIElement):
    def __init__(self, assigned_id: int, caption: str, action, valid=True):
        # Instantiate UIElement with placeholder. Call Menu.update_items() to update image, rect, x and y
        super().__init__(pg.surface.Surface((16, 16)), (0, 0))
        self.id = assigned_id
        self.caption = caption
        self.action = action
        self.valid = valid
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


# TODO: Make Menu a UIElement. A surface with items blitted on it will be its image
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

        self.update_items()

    def draw(self, screen: pg.surface.SurfaceType):
        for item in self.item_list:
            item.draw(screen)

    def down(self):
        # Continue searching in one direction until a valid one is found
        for i in range(1, len(self.item_list)):
            goal_item = self.selected_item + i

            # Loop logic when out of index
            if goal_item > len(self.item_list) - 1:
                if not self.loopable:
                    return
                goal_item = goal_item - len(self.item_list)

            # Set selected when a valid one is found
            if self.item_list[goal_item].valid:
                self.selected_item = goal_item
                return

    def up(self):
        # Similar to down(). See above
        for i in range(1, len(self.item_list)):
            goal_item = self.selected_item - i

            if goal_item < 0:
                if not self.loopable:
                    return
                goal_item = goal_item + len(self.item_list)

            if self.item_list[goal_item].valid:
                self.selected_item = goal_item
                return

    def update_items(self):
        for item in self.item_list:
            item.update(self.font, self.pos, self.color, self.line_space, self.selected_item)

    def update(self, key_down):
        if key_down(pg.K_z):
            self.item_list[self.selected_item].action()
        elif key_down(pg.K_DOWN):
            self.down()
            self.update_items()
        elif key_down(pg.K_UP):
            self.up()
            self.update_items()

