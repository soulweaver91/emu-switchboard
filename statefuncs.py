__author__ = 'Soulweaver'

import subprocess


def noop_cb(env):
    pass


def open_calc_fn(env):
    print("Starting application...")
    env.runningProcess = subprocess.Popen('calc', stdin=None, stdout=None, stderr=None,
                                          close_fds=True)
    print("Application started.")


def previous_state(env):
    env.exit_state()
