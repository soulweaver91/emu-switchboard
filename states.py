#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Soulweaver'

import copy
import os
import sys
import glob
import subprocess
import shlex
import re
from settings import config


# Python 3.3 feature
shlex_quote_find_unsafe = re.compile(r'[^\w@%+=:,./-]', re.ASCII).search


def shlex_quote(s):
    """Return a shell-escaped version of the string *s*."""
    if not s:
        return "''"
    if shlex_quote_find_unsafe(s) is None:
        return s

    # use single quotes, and put single quotes into double quotes
    # the string $'b is then quoted as '$'"'"'b'
    return "'" + s.replace("'", "'\"'\"'") + "'"


class StateMenuStyle:
    main = 0
    submenu = 1
    filelist = 2
    error = 3
    warning = 4
    information = 5


def find_exe_recursive(rdir):
    exes = []
    for folder, subs, files in os.walk(rdir):
        for file in files:
            if (os.path.splitext(file))[1].lower() == '.exe':
                exes.append(os.path.join(folder, file))

    return exes


def make_state(options, name="Unnamed state", kind=StateMenuStyle.submenu, data={}):
    # As the basis of the object, use the data object. Core variables will always be written over
    # the ones provided in the data object, by the update method.
    template = data.copy()
    template.update({
        'options': copy.copy(options),
        'cursor_pos': 0,
        'name': name,
        'type': kind
    })

    return template


def launch_console_game(env, platform, path):
    if sys.platform == 'win32':
        app = config["platforms"][platform]["commandline"].format('"' + path + '"')
        print("Launching " + app + "...")
    else:
        app = shlex.split(config["platforms"][platform]["commandline"].format(shlex_quote(path)))
        print("Launching " + ' '.join(app) + "...")

    return start_processes(env, app)


def launch_dos(env, path):
    if sys.platform == 'win32':
        app = config["dosboxCmd"].format('"' + path + '"')
        print("Launching " + app + "...")
    else:
        app = shlex.split(config["dosboxCmd"].format(shlex_quote(path)))
        print("Launching " + ' '.join(app) + "...")

    return start_processes(env, app)


def start_processes(env, cmd):
    try:
        env.runningProcess = subprocess.Popen(cmd, stdin=None, stdout=None, stderr=None, close_fds=True)
    except (OSError, IOError):
        print("Failed to launch the application.")
        return display_error(env, 'Launching the game failed!')
    except:
        raise
    else:
        print("Application started.")
        if env.ffmpegAvailable and config["streamingServiceDomain"] != "" and config["streamingKey"] != "":
            if sys.platform == 'win32':
                command = "{0} -f dshow -i video=\"screen-capture-recorder\":audio=\"Stereo Mix (VIA High Definition\""\
                          " -s 1280x720 -r 30 -c:v libx264 -preset fast -pix_fmt yuv420p -c:a libmp3lame -threads 0" \
                          " -f flv \"rtmp://{1}/app/{2}\"".format(config["ffmpegLocation"],
                                                                  config["streamingServiceDomain"],
                                                                  config["streamingKey"])
            else:
                command = "{0} -f x11grab -s 720x480 -r 10 -i :0.0" \
                          " -c:v libx264 -preset ultrafast -pix_fmt yuv420p -b:v 500k -minrate 500k -maxrate 500k" \
                          " -bufsize 500k" \
                          " -f flv \"rtmp://{1}/app/{2}\"".format(config["ffmpegLocation"],
                                                                  config["streamingServiceDomain"],
                                                                  config["streamingKey"])
                command = shlex.split(command)
            env.ffmpegInstance = subprocess.Popen(command, stdin=None, stdout=None, stderr=None, close_fds=True)

    return make_state([])


def main():
    items = [(platform["name"], 'list_platform', pos) for pos, platform in enumerate(config["platforms"])]
    items += [
        ('DOS games', 'list_dos'),
        ('Quit', 'exit_program')
    ]

    return make_state(items, "Main Menu", StateMenuStyle.main)


def list_platform(env, platform):
    files = sum([glob.glob(os.path.join(config["gamesDir"], selector))
                for selector in config["platforms"][platform]["selector"].split(';')], [])

    if len(files) > 0:
        items = [(os.path.basename(name), 'launch_console_game', platform, os.path.abspath(name)) for name in files]
        items += [('Back', 'previous_state')]
        return make_state(items, config["platforms"][platform]["name"], StateMenuStyle.filelist)
    else:
        return display_info(env, 'No ' + config["platforms"][platform]["name"]
                            + ' games were found in the game directory.')


def list_dos(env):
    files = find_exe_recursive(os.path.join(config["dosboxDir"]))

    if len(files) > 0:
        items = [(os.path.basename(name) + ' in ' + os.path.relpath(os.path.split(name)[0], config["dosboxDir"]),
                  'launch_dos', os.path.abspath(name)) for name in files]
        items += [('Back', 'previous_state')]
        return make_state(items, 'DOS games', StateMenuStyle.filelist)
    else:
        return display_info(env, 'No DOS games were found in the game directory.')


def informative_option(env):
    # do nothing
    return make_state([])


def previous_state(env):
    env.exit_state()
    return make_state([])


def exit_program(env):
    sys.exit()


def display_error(env, message):
    return make_state([
        ('OK', 'previous_state')
    ], "Error", StateMenuStyle.error, {
        "message": message
    })


def display_warning(env, message):
    return make_state([
        ('OK', 'previous_state')
    ], "Warning", StateMenuStyle.warning, {
        "message": message
    })


def display_info(env, message):
    return make_state([
        ('OK', 'previous_state')
    ], "Information", StateMenuStyle.information, {
        "message": message
    })
