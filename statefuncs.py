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
    env.runningProcess = subprocess.Popen('calc', stdin=None, stdout=None, stderr=None,
                                          close_fds=True)
    print("Application started.")


def previous_state(env):
    env.exit_state()
