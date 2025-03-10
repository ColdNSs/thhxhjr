#!/usr/bin/python
# -*- coding: utf-8 -*-
# New start for reborn cause I'm not building new stuff on that shit - ColdNSs 2025/03/09

import pygame as pg
from scenes import *

RESOLUTION = (960, 720)

game_version = "r0.0.2"
pg.init()
pg.mixer.set_num_channels(40)
screen = pg.display.set_mode(RESOLUTION)
pg.display.set_caption(
    '东方槐夏寒晶R ~ Cold Lake In Scorching Gensokyo: Reborn   Ver. ' + game_version)
pg.display.set_icon(pg.image.load("Picture/colicon.png").convert_alpha())
clock = pg.time.Clock()

banner = BannerScene(screen)
current_scene = banner

while True:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    # Background
    screen.fill('green')

    # Scene
    goal = current_scene.get_goal()
    if goal:
        current_scene = goal
    current_scene.update(events)

    # Update
    pg.display.update()
    clock.tick(60)