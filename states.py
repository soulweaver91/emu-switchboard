#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Soulweaver'

import copy
import statefuncs
import os
from enum import Enum
from settings import config


class StateMenuStyle(Enum):
    main = 0,
    submenu = 1,
    filelist = 2


def make_state(options, callback, name="Unnamed state", kind=StateMenuStyle.submenu):
    return {
        'options': copy.copy(options),
        'callback': callback,
        'cursor_pos': 0,
        'name': name,
        'type': kind
    }


def open_calc():
    return make_state([], statefuncs.open_calc_fn)


def main():
    items = [(platform["name"], 'list_platform', pos) for pos, platform in enumerate(config["platforms"])]
    items += [
        ('Long list test', 'list_long_test'),
        ('App launch test', 'open_calc'),
        ('Quit', 'exit_program')
    ]

    return make_state(items, statefuncs.noop_cb, "Main Menu", StateMenuStyle.main)


def list_platform(platform):
    return make_state([
        ('No ' + config["platforms"][platform]["name"] + ' type files found', 'informative_option'),
        ('Recursive state test', 'list_platform', platform),
        ('Back', 'previous_state')
    ], statefuncs.noop_cb, config["platforms"][platform]["name"], StateMenuStyle.submenu)


def list_long_test():
    dir_data = os.listdir(os.path.expanduser(os.path.join('~', 'Downloads')))
    items = [(file, 'informative_option') for file in dir_data]
    items.append(('Back', 'previous_state'))

    return make_state(items, statefuncs.noop_cb, "Long list testing page", StateMenuStyle.filelist)


def informative_option():
    return make_state([], statefuncs.noop_cb)


def previous_state():
    return make_state([], statefuncs.previous_state)


def exit_program():
    return make_state([], statefuncs.exit_program_fn)
