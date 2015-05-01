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


def make_state(options, name="Unnamed state", kind=StateMenuStyle.submenu):
    return {
        'options': copy.copy(options),
        'cursor_pos': 0,
        'name': name,
        'type': kind
    }


def launch_game(env, platform, path):
    try:
        if sys.platform == 'win32':
            app = config["platforms"][platform]["commandline"].format('"' + path + '"')
            print("Launching " + app + "...")
        else:
            app = shlex.split(config["platforms"][platform]["commandline"].format(shlex_quote(path)))
            print("Launching " + ' '.join(app) + "...")

        env.runningProcess = subprocess.Popen(app, stdin=None, stdout=None, stderr=None, close_fds=True)
    except (OSError, IOError):
        print("Failed to launch the application.")
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
                command = "{0} -f x11grab -s 720x480 -r 10 -i :0.0 -f alsa -ac 2 -i default" \
                          " -c:v libx264 -preset ultrafast -pix_fmt yuv420p -b:v 200k -minrate 200k -maxrate 200k" \
                          " -bufsize 100k -c:a libmp3lame -threads 0 -c:a libmp3lame -ab 96k -ar 44100 -threads 0 " \
                          " -f flv \"rtmp://{1}/app/{2}\"".format(config["ffmpegLocation"],
                                                                  config["streamingServiceDomain"],
                                                                  config["streamingKey"])
                command = shlex.split(command)
            env.ffmpegInstance = subprocess.Popen(command, stdin=None, stdout=None, stderr=None, close_fds=True)

    return make_state([])


def main():
    items = [(platform["name"], 'list_platform', pos) for pos, platform in enumerate(config["platforms"])]
    items += [('Quit', 'exit_program')]

    return make_state(items, "Main Menu", StateMenuStyle.main)


def list_platform(env, platform):
    files = sum([glob.glob(os.path.join(config["gamesDir"], selector))
                for selector in config["platforms"][platform]["selector"].split(';')], [])

    items = [(os.path.basename(name), 'launch_game', platform, os.path.abspath(name)) for name in files]
    items += [('Back', 'previous_state')]
    return make_state(items, config["platforms"][platform]["name"], StateMenuStyle.filelist)


def informative_option(env):
    # do nothing
    return make_state([])


def previous_state(env):
    env.exit_state()
    return make_state([])


def exit_program(env):
    sys.exit()
