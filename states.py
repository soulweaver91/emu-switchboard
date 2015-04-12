__author__ = 'Soulweaver'

import copy
import statefuncs


def make_state(options, callback, name="Unnamed state"):
    return {
        'options': copy.copy(options),
        'callback': callback,
        'cursor_pos': 0,
        'name': name
    }


def open_calc():
    return make_state([], statefuncs.open_calc_fn)


def main():
    return make_state([
        ('NES', 'list_platform', 'nes'),
        ('SNES', 'list_platform', 'snes'),
        ('Test function', 'open_calc'),
        ('Quit', 'exit_program')
    ], statefuncs.noop_cb, "Main Menu")


def list_platform(platform):
    print(platform)

    return make_state([
        ('No ' + platform + ' type files found', 'informative_option'),
        ('Recursive state test', 'list_platform', platform),
        ('Back', 'previous_state')
    ], statefuncs.noop_cb, platform + " games")


def informative_option():
    return make_state([], statefuncs.noop_cb)


def previous_state():
    return make_state([], statefuncs.previous_state)


def exit_program():
    return make_state([], statefuncs.exit_program_fn)
