#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Soulweaver'

import pygame


config = {
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
    'platforms': [
        {
            'name': 'Nintendo Entertainment System',
            'commandline': '/usr/bin/mednafen {0]',
            'selector': '*.nes'
        },
        {
            'name': 'Super Nintendo Entertainment System',
            'commandline': '/usr/bin/mednafen {0]',
            'selector': '*.sfc'
        },
        {
            'name': 'Nintendo Game Boy',
            'commandline': '/usr/bin/mednafen {0]',
            'selector': '*.gb'
        },
        {
            'name': 'Nintendo Game Boy Color',
            'commandline': '/usr/bin/mednafen {0]',
            'selector': '*.gbc'
        },
        {
            'name': 'Nintendo Game Boy Advance',
            'commandline': '/usr/bin/mednafen {0]',
            'selector': '*.gba;*.agb'
        },
        {
            'name': 'Sony PlayStation',
            'commandline': '/usr/bin/pcsx',
            'selector': '*.psx.iso'
        }
    ]
}
