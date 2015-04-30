#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Soulweaver'

import copy
import os
import sys
import glob
import subprocess
from settings import config


class StateMenuStyle:
    main = 0
    submenu = 1
    filelist = 2


def make_state(options, name="Unnamed state", kind=StateMenuStyle.submenu):
    return {
        'options': copy.copy(options),
        'cursor_pos': 0,
        'name': name,
        'type': kind
    }


def open_calc(env):

    if sys.platform == 'win32':
        app = 'calc'
    else:
        app = config["platforms"][0]["commandline"]

    try:
        print("Launching " + app + "...")
        env.runningProcess = subprocess.Popen(app, stdin=None, stdout=None, stderr=None,
                                              close_fds=True)
    except FileNotFoundError:
        print("Failed to launch the application.")
    except:
        raise
    else:
        print("Application started.")

    return make_state([])


def launch_game(env, platform, path):
    try:
        app = config["platforms"][platform]["commandline"].format(path)
        print("Launching " + app + "...")
        env.runningProcess = subprocess.Popen(app, stdin=None, stdout=None, stderr=None,
                                              close_fds=True)
    except FileNotFoundError:
        print("Failed to launch the application.")
    except:
        raise
    else:
        print("Application started.")

    return make_state([])


def main():
    items = [(platform["name"], 'list_platform', pos) for pos, platform in enumerate(config["platforms"])]
    items += [
        ('Long list test', 'list_long_test'),
        ('App launch test', 'open_calc'),
        ('Quit', 'exit_program')
    ]

    return make_state(items, "Main Menu", StateMenuStyle.main)


def list_platform(env, platform):
    files = sum([glob.glob(os.path.join(config["gamesDir"], selector))
                for selector in config["platforms"][platform]["selector"].split(';')], [])

    items = [(os.path.basename(name), 'launch_game', platform, os.path.abspath(name)) for name in files]
    items += [('Recursive state test', 'list_platform', platform),
              ('Back', 'previous_state')]
    return make_state(items, config["platforms"][platform]["name"], StateMenuStyle.filelist)


def list_long_test(env):
    mode = StateMenuStyle.filelist
    try:
        dir_data = os.listdir(config["gamesDir"])
    except FileNotFoundError:
        items = [('Error: could not open directory', 'informative_option')]
        mode = StateMenuStyle.submenu
    except:
        raise
    else:
        items = [(file, 'informative_option') for file in dir_data]

    items.append(('Back', 'previous_state'))
    return make_state(items, "Long list testing page", mode)


def informative_option(env):
    # do nothing
    return make_state([])


def previous_state(env):
    env.exit_state()
    return make_state([])


def exit_program(env):
    sys.exit()
