#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Soulweaver'

import subprocess
import sys


def noop_cb(env):
    pass


def exit_program_fn(env):
    sys.exit()


def open_calc_fn(env):
    print("Starting application...")
    if sys.platform == 'win32':
        app = 'calc'
    else:
        app = 'snes9x-rpi'

    try:
        env.runningProcess = subprocess.Popen(app, stdin=None, stdout=None, stderr=None,
                                              close_fds=True)
    except FileNotFoundError:
        print("Failed to launch the application.")
    except:
        raise
    else:
        print("Application started.")


def previous_state(env):
    env.exit_state()
