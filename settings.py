#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Soulweaver'

import pygame
import json

config = {}


def save_config(obj=config):
    with open('config.json', 'w') as outfile:
        json.dump(obj, outfile, indent=2)


def load_config():
    try:
        with open('config.json', 'r') as infile:
            loaded = json.load(infile)
    except:
        loaded = {
            # temporary fixed config for a specific controller model
            'joyButtons': {
                'down': 14,
                'up': 12,
                'left': 15,
                'right': 13,
                'accept': 2,
                'cancel': 1,
                'information': 9
            },
            'joyAxis': {
                'upDown': 1,
                'leftRight': 0
            },
            'gameKillSwitches': {
                'joystick': [4, 5, 6, 7, 10, 11],
                'keyboard': [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_k]
            },
            'axisThreshold': 0.95,
            'gamesDir': '~/Games',
            'platforms': [
                {
                    'name': 'Nintendo Entertainment System',
                    'commandline': '/usr/pi/Emulators/fceux {0}',
                    'selector': '*.nes'
                },
                {
                    'name': 'Super Nintendo Entertainment System',
                    'commandline': '/usr/pi/Emulators/foo',
                    'selector': '*.sfc'
                },
                {
                    'name': 'Nintendo Game Boy',
                    'commandline': '/usr/pi/Emulators/foo',
                    'selector': '*.gb'
                },
                {
                    'name': 'Nintendo Game Boy Color',
                    'commandline': '/usr/pi/Emulators/foo',
                    'selector': '*.gbc'
                },
                {
                    'name': 'Nintendo Game Boy Advance',
                    'commandline': '/usr/pi/Emulators/foo',
                    'selector': '*.gba;*.agb'
                },
                {
                    'name': 'Sony PlayStation',
                    'commandline': '/usr/pi/Emulators/foo',
                    'selector': '*.psx.iso'
                },
                {
                    'name': 'Sega Mega Drive',
                    'commandline': '/usr/pi/Emulators/foo',
                    'selector': '*.md'
                }
            ]
        }
        save_config(loaded)

    return loaded

config = load_config()
