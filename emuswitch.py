#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'Soulweaver'

import os
import sys
import math
import pygame

import fonts
from menuevent import MenuEvent, MenuEventType
import states
from settings import config


class EmuSwitch:
    def __init__(self):
        print('Starting up emu-switchboard...')

        # Initialize pygame and joystick support
        pygame.init()
        pygame.joystick.init()
        pygame.display.set_caption("Emulator Switchboard")

        # Set repeat mode for keys
        # Wait 0.5 seconds, then send events every 0.1 seconds
        pygame.key.set_repeat(500, 100)

        # Set up all joysticks that were found
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print('WARNING: No joysticks detected!')
        else:
            print('Found', joystick_count, 'joysticks.')
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()

                print('Initialized joystick', joystick.get_name(), '-',
                      joystick.get_numbuttons(), 'buttons,',
                      joystick.get_numaxes(), 'axes,',
                      joystick.get_numhats(), 'hats')

        # Set up a clock object
        self.clock = pygame.time.Clock()
        
        # Set the window options
        self.screen = pygame.display.set_mode((720, 450))

        # Set up the state stack
        self.states = []
        self.enter_state(states.main())

        self.enter_state(states.display_error(self, "Test error"))
        self.enter_state(states.display_error(self, "one\n\ntwo\n\nthree"))
        self.enter_state(states.display_warning(self, "Test warning"))
        self.enter_state(states.display_info(self, "Testing menu messages."))

        self.UIObjects = set()

        # Holds the launched game
        self.runningProcess = None

        # Check for the availability of FFmpeg
        self.ffmpegAvailable = os.path.exists(config["ffmpegLocation"]) and os.access(config["ffmpegLocation"], os.X_OK)
        self.ffmpegInstance = None

        self.backdrop = pygame.image.load(os.path.join('assets', 'backdrop.png'))
        self.warning_bg = pygame.image.load(os.path.join('assets', 'warningbox.png'))
        self.error_bg = pygame.image.load(os.path.join('assets', 'errorbox.png'))
        self.info_bg = pygame.image.load(os.path.join('assets', 'infobox.png'))

    def start(self):
        while True:
            self.tick()

            # Limit FPS to 30
            self.clock.tick(30)

    def tick(self):
        self.tick_input()
        self.tick_process()
        self.tick_draw()
            
    def tick_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif self.runningProcess is not None:
                pass
            else:
                p_event = None
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w, pygame.K_KP8]:
                        p_event = MenuEventType["up"]
                    elif event.key in [pygame.K_DOWN, pygame.K_s, pygame.K_KP2]:
                        p_event = MenuEventType["down"]
                    elif event.key in [pygame.K_LEFT, pygame.K_a, pygame.K_KP4]:
                        p_event = MenuEventType["left"]
                    elif event.key in [pygame.K_RIGHT, pygame.K_d, pygame.K_KP6]:
                        p_event = MenuEventType["right"]
                    elif event.key in [pygame.K_SPACE, pygame.K_KP_ENTER, pygame.K_RETURN]:
                        p_event = MenuEventType["accept"]
                    elif event.key in [pygame.K_BACKSPACE, pygame.K_ESCAPE]:
                        p_event = MenuEventType["cancel"]

                elif event.type == pygame.JOYBUTTONDOWN:
                    for action, button in config['joyButtons'].items():
                        if event.button == button:
                            p_event = MenuEventType[action]
                            break

                elif event.type == pygame.JOYAXISMOTION and math.fabs(event.value) > config['axisThreshold']:
                    if event.axis == config['joyAxis']['upDown']:
                        if event.value < 0:
                            p_event = MenuEventType["up"]
                        else:
                            p_event = MenuEventType["down"]
                    if event.axis == config['joyAxis']['leftRight']:
                        if event.value < 0:
                            p_event = MenuEventType["left"]
                        else:
                            p_event = MenuEventType["right"]

                if p_event is not None:
                    p_event = MenuEvent(p_event, False)
                    for obj in self.UIObjects:
                        obj.input(p_event)
                    print(p_event.kind, p_event.repeat)

                    if p_event.kind == MenuEventType["accept"]:
                        self.select_option()
                    elif p_event.kind == MenuEventType["cancel"]:
                        if len(self.states) > 1:
                            self.exit_state()
                        else:
                            self.states[0]['cursor_pos'] = len(self.states[0]['options']) - 1
                    elif p_event.kind == MenuEventType["up"]:
                        self.prev_option()
                    elif p_event.kind == MenuEventType["down"]:
                        self.next_option()
                    elif p_event.kind == MenuEventType["left"] and self.states[-1]["type"] == states.StateMenuStyle.filelist:
                        self.prev_page()
                    elif p_event.kind == MenuEventType["right"] and self.states[-1]["type"] == states.StateMenuStyle.filelist:
                        self.next_page()
                    elif p_event.kind == MenuEventType["information"]:
                        print(repr(self.states))

        if self.runningProcess is not None:
            # Check for game kill switches
            kill = False

            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                if all([pygame.joystick.Joystick(i).get_button(button)
                        for button in config['gameKillSwitches']['joystick']]):
                    kill = True

            pressed_keys = pygame.key.get_pressed()
            if all([pressed_keys[key] for key in config['gameKillSwitches']['keyboard']]):
                kill = True

            if kill:
                print("Kill switch recognized, killing the application...")
                self.runningProcess.terminate()
                self.runningProcess.wait()
                self.runningProcess = None

    def tick_process(self):
        for obj in self.UIObjects:
            obj.process()

        if self.runningProcess is not None:
            if self.runningProcess.poll() is not None:
                self.runningProcess = None
                self.ffmpegInstance.terminate()
                self.ffmpegInstance.wait()

    def tick_draw(self):
        # Paint the backdrop
        if self.runningProcess is not None:
            self.screen.fill(fonts.c_black)
            fonts.main_font.render_to(self.screen, fonts.centered_pos(fonts.main_font, "Game in progress...",
                                                                      (360, 200), 50),
                                      "Game in progress...", fonts.c_white, size=50)
        else:
            self.screen.blit(self.backdrop, self.backdrop.get_rect())
            fonts.main_font.render_to(self.screen, (10, 10), "Emulator Switchboard (Test build)", fonts.c_white)
            fonts.main_font.render_to(self.screen, (10, 28), ' '.join(["» " + state['name'] for state in self.states]),
                                      fonts.c_white, size=15)

            if self.states[-1]["type"] == states.StateMenuStyle.error:
                self.screen.blit(self.error_bg, pygame.Rect(0, 50, 720, 400))
                title_col = fonts.c_red
            elif self.states[-1]["type"] == states.StateMenuStyle.warning:
                self.screen.blit(self.warning_bg, pygame.Rect(0, 50, 720, 400))
                title_col = fonts.c_yellow
            elif self.states[-1]["type"] == states.StateMenuStyle.information:
                self.screen.blit(self.info_bg, pygame.Rect(0, 50, 720, 400))
                title_col = fonts.c_white

            if self.states[-1]["type"] == states.StateMenuStyle.filelist:
                min_pos = min(max(self.states[-1]['cursor_pos'] - 11, 0), len(self.states[-1]["options"]) - 23)
                min_offset = max(0, min_pos) - self.states[-1]['cursor_pos'] + 11
                for idx, option in enumerate(self.states[-1]["options"][min_pos:min_pos+23]):
                    if idx == 11 - min_offset:
                        self.screen.fill(fonts.c_white, pygame.Rect(0, 60 + idx * 15, 720, 15))
                        fonts.mono_font.render_to(self.screen, (10, 60 + idx * 15), option[0], fonts.c_black, size=15)
                    else:
                        fonts.mono_font.render_to(self.screen, (10, 60 + idx * 15), option[0], fonts.c_white, size=15)
            elif self.states[-1]["type"] in [states.StateMenuStyle.error,
                                             states.StateMenuStyle.warning,
                                             states.StateMenuStyle.information]:
                fonts.main_font.render_to(self.screen,
                                          fonts.centered_pos(fonts.main_font, self.states[-1]["name"], (360, 75), 30),
                                          self.states[-1]["name"], title_col, size=30)

                for i, line in enumerate(self.states[-1]["message"].split('\n')):
                    fonts.main_font.render_to(self.screen, (20, 130 + 20 * i), line, fonts.c_black)

                for idx, option in enumerate(self.states[-1]["options"]):
                    color = fonts.c_ltgray
                    if self.states[-1]['cursor_pos'] == idx:
                        color = fonts.c_white
                    fonts.main_font.render_to(self.screen, fonts.centered_pos(fonts.main_font, option[0],
                                                                              (360, 360 + idx * 20), 20),
                                              option[0], color, size=20)
            else:
                for idx, option in enumerate(self.states[-1]["options"]):
                    color = fonts.c_ltgray
                    if self.states[-1]['cursor_pos'] == idx:
                        color = fonts.c_white
                    fonts.main_font.render_to(self.screen, fonts.centered_pos(fonts.main_font, option[0],
                                                                              (360, 60 + idx * 20), 20),
                                              option[0], color, size=20)

            for obj in self.UIObjects:
                obj.draw(self.screen)

        pygame.display.flip()

    def enter_state(self, state):
        if len(state['options']) > 0:
            self.states.append(state)

    def exit_state(self):
        self.states.pop()

    def next_option(self):
        self.states[-1]['cursor_pos'] = (self.states[-1]['cursor_pos'] + 1) % len(self.states[-1]['options'])

    def prev_option(self):
        self.states[-1]['cursor_pos'] = (self.states[-1]['cursor_pos'] - 1) % len(self.states[-1]['options'])

    def next_page(self):
        if self.states[-1]['cursor_pos'] == len(self.states[-1]['options']) - 1:
            self.next_option()
        else:
            self.states[-1]['cursor_pos'] = min(self.states[-1]['cursor_pos'] + 18, len(self.states[-1]['options']) - 1)

    def prev_page(self):
        if self.states[-1]['cursor_pos'] == 0:
            self.prev_option()
        else:
            self.states[-1]['cursor_pos'] = max(self.states[-1]['cursor_pos'] - 18, 0)

    def select_option(self):
        try:
            # Select from the current state, from the position the cursor is currently, the second item of the tuple,
            # which names a function in the imported states, and then call that function with the items in the same
            # tuple starting from the third one
            selected_option = self.states[-1]['options'][self.states[-1]['cursor_pos']]
            received_state = getattr(states, selected_option[1])(self, *selected_option[2:])
        except AttributeError:
            print('ERROR: Invalid target state, trying to cope by ignoring it...')
        except:
            raise
        else:
            self.enter_state(received_state)

# Initialize the application
if __name__ == "__main__":
    MainWindow = EmuSwitch()
    MainWindow.start()
