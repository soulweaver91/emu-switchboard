#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Soulweaver'

import subprocess
import sys
from settings import config


def noop_cb(env):
    pass


def exit_program_fn(env):
    sys.exit()


def open_calc_fn(env):
    if sys.platform == 'win32':
        app = 'calc'
    else:
        app = config["platforms"][0]["commandline"]

    try:
        print("Launching" + app + "...")
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
