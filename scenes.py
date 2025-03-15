#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame as pg
from ui import TextItem, Text, MenuItem, Menu, fonts, UIElement, UIAnimationMove, UIAnimationAlpha, Localization, no_action

localization = Localization('zh_CN')


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
        self.menu = None
        self.create_ui()
        self.animations = [
            UIAnimationMove(self.assets['logo'], 60, 0, False, (200, 100), (350,175)),
            UIAnimationAlpha(self.assets['logo'], 60, 0, False, start_alpha=40),
            # UIAnimationMove(self.menu, 60, 60, True, (500, 200), (600,250))
        ]

    def create_ui(self):
        item_list = [
            MenuItem(0, localization.get('title.menu.strings.start'), self.menu_action, True),
            MenuItem(1, localization.get('title.menu.strings.practice_start'), self.menu_action, False),
            MenuItem(2, localization.get('title.menu.strings.player_data'), self.menu_action, True),
            MenuItem(3, localization.get('title.menu.strings.replay'), self.menu_action, True),
            MenuItem(4, localization.get('title.menu.strings.manual'), self.menu_action, True),
            MenuItem(5, localization.get('title.menu.strings.option'), self.menu_action, True),
            MenuItem(6, localization.get('title.menu.strings.music_room'), self.menu_action, False),
            MenuItem(7, localization.get('title.menu.strings.exit'), self.menu_action, True),
        ]
        font = fonts[localization.get('title.menu.font')]
        pos = (localization.get('title.menu.pos.x'), localization.get('title.menu.pos.y'))
        self.menu = Menu(item_list, font, pos, loopable=True)

    def get_goal(self):
        goal = self.goal
        if goal:
            for animation in self.animations:
                # This will flag the animation done at the next update
                animation.delay = 0
                animation.animation_tick = animation.duration
            self.goal = None
        return goal

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
            'logo': UIElement(pg.image.load('./Picture/title.png').convert_alpha(), (0, 0))
        }
        self.assets['background'].image.set_alpha(128)
        self.menu = None
        self.texts = []
        self.create_ui()
        for text in self.texts:
            text.image.set_alpha(0)
        self.text_show = False
        self.animations = []

    def create_ui(self):
        item_list = [TextItem(localization.get('manual.title.strings.title'))]
        font = fonts[localization.get('manual.title.font')]
        pos = (localization.get('manual.title.pos.x'), localization.get('manual.title.pos.y'))
        self.assets['title'] = Text(item_list, font, pos, shadow_offset=2)

        item_list = [TextItem(localization.get('manual.subtitle.strings.subtitle'))]
        font = fonts[localization.get('manual.subtitle.font')]
        pos = (localization.get('manual.subtitle.pos.x'), localization.get('manual.subtitle.pos.y'))
        self.assets['subtitle'] = Text(item_list, font, pos, 'grey', shadow_offset=2)

        item_list = [
            MenuItem(0, localization.get('manual.menu.strings.introduction'), no_action, True),
            MenuItem(1, localization.get('manual.menu.strings.controls'), no_action, True),
            MenuItem(2, localization.get('manual.menu.strings.hud'), no_action, True),
            MenuItem(3, localization.get('manual.menu.strings.freeze'), no_action, True),
        ]
        font = fonts[localization.get('manual.menu.font')]
        pos = (localization.get('manual.menu.pos.x'), localization.get('manual.menu.pos.y'))
        self.menu = Menu(item_list, font, pos, self.scroll_down, self.scroll_up, loopable=False)

        item_list = [
            TextItem(localization.get('manual.introduction.strings.item_0')),
            TextItem(localization.get('manual.introduction.strings.item_1')),
            TextItem(localization.get('manual.introduction.strings.item_2')),
            TextItem(localization.get('manual.introduction.strings.item_3')),
            TextItem(localization.get('manual.introduction.strings.item_4')),
            TextItem(localization.get('manual.introduction.strings.item_5')),
            TextItem(localization.get('manual.introduction.strings.item_6')),
            TextItem(localization.get('manual.introduction.strings.item_7')),
            TextItem(localization.get('manual.introduction.strings.item_8')),
        ]
        font = fonts[localization.get('manual.introduction.font')]
        pos = (localization.get('manual.introduction.pos.x'), localization.get('manual.introduction.pos.y'))
        introduction = Text(item_list, font, pos, 'white')

        item_list = [
            TextItem(localization.get('manual.controls.strings.item_0')),
            TextItem(localization.get('manual.controls.strings.item_1')),
            TextItem(localization.get('manual.controls.strings.item_2')),
            TextItem(localization.get('manual.controls.strings.item_3')),
            TextItem(localization.get('manual.controls.strings.item_4')),
            TextItem(localization.get('manual.controls.strings.item_5'), 'red'),
        ]
        font = fonts[localization.get('manual.controls.font')]
        pos = (localization.get('manual.controls.pos.x'), localization.get('manual.controls.pos.y'))
        controls = Text(item_list, font, pos, 'white')

        item_list = [
            TextItem(localization.get('manual.hud.strings.item_0')),
            TextItem(localization.get('manual.hud.strings.item_1'), 'red'),
            TextItem(localization.get('manual.hud.strings.item_2'), 'green'),
            TextItem(localization.get('manual.hud.strings.item_3')),
            TextItem(localization.get('manual.hud.strings.item_4')),
            TextItem(localization.get('manual.hud.strings.item_5')),
            TextItem(localization.get('manual.hud.strings.item_6')),
        ]
        font = fonts[localization.get('manual.hud.font')]
        pos = (localization.get('manual.hud.pos.x'), localization.get('manual.hud.pos.y'))
        hud = Text(item_list, font, pos, 'white')

        item_list = [
            TextItem(localization.get('manual.freeze.strings.item_0')),
            TextItem(localization.get('manual.freeze.strings.item_1')),
            TextItem(localization.get('manual.freeze.strings.item_2')),
            TextItem(localization.get('manual.freeze.strings.item_3')),
            TextItem(localization.get('manual.freeze.strings.item_4')),
            TextItem(localization.get('manual.freeze.strings.item_5')),
            TextItem(localization.get('manual.freeze.strings.item_6')),
            TextItem(localization.get('manual.freeze.strings.item_7')),
            TextItem(localization.get('manual.freeze.strings.item_8')),
            TextItem(localization.get('manual.freeze.strings.item_9')),
            TextItem(localization.get('manual.freeze.strings.item_10')),
            TextItem(localization.get('manual.freeze.strings.item_11')),
            TextItem(localization.get('manual.freeze.strings.item_12'), 'green'),
            TextItem(localization.get('manual.freeze.strings.item_13'), 'red'),
            TextItem(localization.get('manual.freeze.strings.item_14')),
        ]
        font = fonts[localization.get('manual.freeze.font')]
        pos = (localization.get('manual.freeze.pos.x'), localization.get('manual.freeze.pos.y'))
        freeze = Text(item_list, font, pos, 'white')

        self.texts = [introduction, controls, hud, freeze]

    def draw(self):
        self.screen.fill('black')
        self.assets['background'].draw(self.screen)
        for text in self.texts:
            text.draw(self.screen)

        self.menu.draw(self.screen)
        self.assets['subtitle'].draw(self.screen)
        self.assets['title'].draw(self.screen)

    def scroll_down(self, action_id):
        if not self.text_show:
            return
        # Make sure the menu is NOT loopable, or this will create an out-of-index error
        self.animations.append(UIAnimationAlpha(self.texts[self.menu.selected_index - 1], 6, 0, False, target_alpha=0))
        self.animations.append(UIAnimationAlpha(self.texts[self.menu.selected_index], 6, 0, False, target_alpha=255))

    def scroll_up(self, action_id):
        if not self.text_show:
            return
        self.animations.append(UIAnimationAlpha(self.texts[self.menu.selected_index + 1], 6, 0, False, target_alpha=0))
        self.animations.append(UIAnimationAlpha(self.texts[self.menu.selected_index], 6, 0, False, target_alpha=255))

    def set_show(self, show: bool):
        if show == self.text_show:
            return
        menu_x = localization.get('manual.menu.pos.x')
        menu_y = localization.get('manual.menu.pos.y')
        menu_text_show_x = localization.get('manual.menu.pos_text_show.x')
        menu_text_show_y = localization.get('manual.menu.pos_text_show.y')
        selected = self.texts[self.menu.selected_index]
        if show:
            self.animations.append(UIAnimationMove(self.menu, 6, 0, False, target_pos=(menu_text_show_x, menu_text_show_y)))
            self.animations.append(UIAnimationAlpha(selected, 6, 0, False, target_alpha=255))
        if not show:
            self.animations.append(UIAnimationMove(self.menu, 6, 0, False, target_pos=(menu_x, menu_y)))
            self.animations.append(UIAnimationAlpha(selected, 6, 0, False, target_alpha=0))

        self.text_show = show

    def update(self, events: list[pg.event.EventType]):
        self.update_inputs(events)

        # Clear animations that are done. Execute animations
        self.animations = [animation for animation in self.animations if animation.active]
        for animation in self.animations:
            animation.update()

        if not self.animations:
            if self.key_down(pg.K_z):
                    self.set_show(True)
            elif self.key_down(pg.K_x):
                    if not self.text_show:
                        self.goal = self.created_by
                    self.set_show(False)
            elif self.key_down(pg.K_r):
                localization.reload()
                self.create_ui()
                for text in self.texts:
                    text.image.set_alpha(0)
                self.text_show = False
                self.animations = []

            self.menu.update(self.key_down)

        self.draw()
        self.tick += 1