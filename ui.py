#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as pg
import json

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

def no_action(action_id=None):
    return


class UIElement(pg.sprite.Sprite):
    def __init__(self, image=None, pos=None):
        if image is None:
            image = pg.surface.Surface((16, 16))
        if pos is None:
            pos = (0, 0)
        super().__init__()
        self.image = image
        self.shadow = self.image
        self.rect = self.image.get_rect()
        self.pos = pos

    def draw(self, screen: pg.surface.SurfaceType):
        # Use pos as the real rect coordinates, since rect.x and rect.y might be reset when rect is updated
        self.rect.topleft = self.pos
        screen.blit(self.image, self.rect)

    def draw_shadow(self, screen: pg.surface.SurfaceType, shadow_offset: int):
        x, y = self.pos
        self.rect.topleft = (x + shadow_offset, y + shadow_offset)
        screen.blit(self.shadow, self.rect)


class UIAnimation:
    def __init__(self, element: UIElement, duration: int, delay=0, linear=True):
        duration = max(duration, 1)
        delay = max(delay, 0)
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
            eased_progress = 1 - (1 - progress) ** 2  # None-linear
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
        self.element.pos = self.start_pos

    def complete(self):
        self.element.pos = self.target_pos

    def animate_progress(self, progress):
        new_x = self.start_pos[0] + (self.target_pos[0] - self.start_pos[0]) * progress
        new_y = self.start_pos[1] + (self.target_pos[1] - self.start_pos[1]) * progress
        self.element.pos = (new_x, new_y)


class UIAnimationAlpha(UIAnimation):
    def __init__(self, element: UIElement, duration: int, delay=0, linear=True, start_alpha=None, target_alpha=None):
        if start_alpha is None:
            start_alpha = element.image.get_alpha()
        elif start_alpha < 0:
            start_alpha = 0
        elif start_alpha > 255:
            start_alpha = 255

        if target_alpha is None:
            target_alpha = element.image.get_alpha()
        elif target_alpha < 0:
            target_alpha = 0
        elif target_alpha > 255:
            target_alpha = 255

        super().__init__(element, duration, delay, linear)
        self.start_alpha = start_alpha
        self.target_alpha = target_alpha

    def start(self):
        self.element.image.set_alpha(self.start_alpha)

    def complete(self):
        self.element.image.set_alpha(self.target_alpha)

    def animate_progress(self, progress):
        new_alpha = self.start_alpha + (self.target_alpha - self.start_alpha) * progress
        self.element.image.set_alpha(new_alpha)


class TextItem(UIElement):
    def __init__(self, caption, color=None):
        super().__init__()
        self.caption = caption
        self.color = color

    def update(self, font: pg.font.FontType, color: str, line_space: int, max_bottom: int, pos=(0, 0)):
        if self.color:
            color = self.color

        # pos here is relative to Text surface, not screen
        x, y = pos
        self.image = font.render(self.caption, True, color)
        self.shadow = font.render(self.caption, True, 'black')
        self.rect = self.image.get_rect()
        self.pos = (x, y + max_bottom + line_space)


class Text(UIElement):
    def __init__(
            self,
            items: list[TextItem],
            font: pg.font.FontType,
            pos: tuple,
            color='white',
            line_space=5,
            shadow_offset=1
    ):
        super().__init__()
        self.items = items
        self.font = font
        self.pos = pos
        self.color = color
        self.line_space = line_space
        self.shadow_offset = shadow_offset

        self.update_items()

    def update_items(self):
        # Update color and relative pos of each item and blit all items on menu surface
        if not self.items:
            return

        max_right = 1
        max_bottom = 0

        for item in self.items:
            item.update(self.font, self.color, self.line_space, max_bottom)
            item.rect.topleft = item.pos

            # Find the largest width
            if item.rect.right > max_right:
                max_right = item.rect.right

            # Use the bottom of the last item as height
            max_bottom = item.rect.bottom

        max_right += self.shadow_offset
        max_bottom += self.shadow_offset

        max_bottom = max(max_bottom, 1)

        self.image = pg.surface.Surface((max_right, max_bottom), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()

        if self.shadow_offset:
            for item in self.items:
                item.draw_shadow(self.image, self.shadow_offset)
        for item in self.items:
            item.draw(self.image)

    def update(self):
        return


class MenuItem(UIElement):
    def __init__(self, action_id: int, caption: str, action_handler=no_action, valid=True):
        # Instantiate UIElement. Call Menu.update_items() to update image, rect, x and y
        super().__init__()
        self.action_id = action_id
        self.caption = caption
        self.action_handler = action_handler
        self.valid = valid
        self.color = 'white'

    def update(self, font: pg.font.FontType, color: dict, line_space: int, max_bottom: int, selected_item, pos=(0, 0)):
        if self is selected_item:
            self.color = color['selected']
        elif self.valid:
            self.color = color['valid']
        else:
            self.color = color['invalid']

        # pos here is relative to Menu surface, not screen
        x, y = pos
        self.image = font.render(self.caption, True, self.color)
        self.shadow = font.render(self.caption, True, 'black')
        self.rect = self.image.get_rect()
        self.pos = (x, y + max_bottom + line_space)


class Menu(UIElement):
    def __init__(
            self,
            items: list[MenuItem],
            font: pg.font.FontType,
            pos: tuple,
            down_action=no_action,
            up_action=no_action,
            color=None,
            line_space=5,
            default_item=0,
            loopable=False,
            shadow_offset = 1
    ):
        if color is None:
            color = {'selected': 'red', 'valid': 'white', 'invalid': 'grey'}
        super().__init__()
        self.items = items
        self.font = font
        self.pos = pos
        self.down_action = down_action
        self.up_action = up_action
        self.color = color
        self.line_space = line_space
        self.selected_index = default_item
        self.loopable = loopable
        self.shadow_offset = shadow_offset

        self.update_items()

    def down(self):
        # Continue searching in one direction until a valid one is found
        for i in range(1, len(self.items)):
            goal_item = self.selected_index + i

            # Loop logic when out of index
            if goal_item > len(self.items) - 1:
                if not self.loopable:
                    return
                goal_item = goal_item - len(self.items)

            # Set selected when a valid one is found
            if self.items[goal_item].valid:
                self.selected_index = goal_item
                self.down_action(self.items[self.selected_index].action_id)
                return

    def up(self):
        # Similar to down(). See above
        for i in range(1, len(self.items)):
            goal_item = self.selected_index - i

            if goal_item < 0:
                if not self.loopable:
                    return
                goal_item = goal_item + len(self.items)

            if self.items[goal_item].valid:
                self.selected_index = goal_item
                self.up_action(self.items[self.selected_index].action_id)
                return

    def update_items(self):
        # Update color and relative pos of each item and blit all items on menu surface
        if not self.items:
            return

        max_right = 1
        max_bottom = 0

        for item in self.items:
            item.update(self.font, self.color, self.line_space, max_bottom, self.items[self.selected_index])
            item.rect.topleft = item.pos

            # Find the largest width
            if item.rect.right > max_right:
                max_right = item.rect.right

            # Use the bottom of the last item as height
            max_bottom = item.rect.bottom

        max_right += self.shadow_offset
        max_bottom += self.shadow_offset

        max_bottom = max(max_bottom, 1)

        self.image = pg.surface.Surface((max_right, max_bottom), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()

        if self.shadow_offset:
            for item in self.items:
                item.draw_shadow(self.image, self.shadow_offset)
        for item in self.items:
            item.draw(self.image)

    def update(self, key_down):
        if key_down(pg.K_z):
            item = self.items[self.selected_index]
            item.action_handler(item.action_id)
        elif key_down(pg.K_DOWN):
            self.down()
            self.update_items()
        elif key_down(pg.K_UP):
            self.up()
            self.update_items()


class Localization:
    def __init__(self, language: str):
        self.language = language
        self.localization = None
        self.reload()

    def set_language(self, language: str):
        self.language = language

    def reload(self):
        with open(f"localization/{self.language}.json") as f:
            self.localization =  json.load(f)

    def get(self, scene_box_attr_item: str):
        """Example usage: localization.get('title.menu.strings.manual')"""
        keys = scene_box_attr_item.split('.')
        if len(keys) >=4:
            return self.localization.get(keys[0], "").get(keys[1], "").get(keys[2], "").get(keys[3], "")
        return self.localization.get(keys[0], "").get(keys[1], "").get(keys[2], "")
