#!/usr/bin/python
# -*- coding: utf-8 -*-
# New start for reborn cause I'm not building new stuff on that shit - ColdNSs 2025/03/09

import pygame as pg

gameVersion = "r0.0.1c"
pg.init()
pg.mixer.set_num_channels(40)
window = pg.display.set_mode((960, 720))
pg.display.set_caption(
    '东方槐夏寒晶R ~ Cold Lake In Scorching Gensokyo: Reborn   Ver. ' + gameVersion)
icon = pg.image.load("Picture/colicon.png").convert_alpha()
pg.display.set_icon(icon)
clock = pg.time.Clock()

