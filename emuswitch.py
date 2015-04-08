__author__ = 'Soulweaver'

import sys, math
import pygame
from menuevent import MenuEvent, MenuEventType


class EmuSwitch:
    def __init__(self):
        print('Starting up emu-switchboard...')

        # Initialize pygame and joystick support
        pygame.init()
        pygame.joystick.init()
        pygame.display.set_caption("EmuSwitchboard")

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
        self.screen = pygame.display.set_mode((1280, 720))

        self.UIObjects = set()
        self.config = {
            # temporary fixed config for a specific controller model
            'joyButtons': {
                'down': 14,
                'up': 12,
                'left': 15,
                'right': 13,
                'accept': 2,
                'cancel': 1,
                'information': 9
            },
            'joyAxis': {
                'upDown': 1,
                'leftRight': 0
            },
            'gameKillSwitches': {
                'joystick': [4, 5, 6, 7, 10, 11],
                'keyboard': [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_k]
            },
            'axisThreshold': 0.3
        }

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
            else:
                p_event = None
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w, pygame.K_KP8]:
                        p_event = MenuEventType.up
                    elif event.key in [pygame.K_DOWN, pygame.K_s, pygame.K_KP2]:
                        p_event = MenuEventType.down
                    elif event.key in [pygame.K_LEFT, pygame.K_a, pygame.K_KP4]:
                        p_event = MenuEventType.left
                    elif event.key in [pygame.K_RIGHT, pygame.K_d, pygame.K_KP6]:
                        p_event = MenuEventType.right
                    elif event.key in [pygame.K_SPACE, pygame.K_KP_ENTER, pygame.K_RETURN]:
                        p_event = MenuEventType.accept
                    elif event.key in [pygame.K_BACKSPACE, pygame.K_ESCAPE]:
                        p_event = MenuEventType.cancel

                elif event.type == pygame.JOYBUTTONDOWN:
                    if event.button == self.config['joyButtons']['up']:
                        p_event = MenuEventType.up
                    elif event.button == self.config['joyButtons']['down']:
                        p_event = MenuEventType.down
                    elif event.button == self.config['joyButtons']['left']:
                        p_event = MenuEventType.left
                    elif event.button == self.config['joyButtons']['right']:
                        p_event = MenuEventType.right
                    elif event.button == self.config['joyButtons']['accept']:
                        p_event = MenuEventType.accept
                    elif event.button == self.config['joyButtons']['cancel']:
                        p_event = MenuEventType.cancel
                    elif event.button == self.config['joyButtons']['information']:
                        p_event = MenuEventType.information

                elif event.type == pygame.JOYAXISMOTION and math.fabs(event.value) > self.config['axisThreshold']:
                    if event.axis == self.config['joyAxis']['upDown']:
                        if event.value < 0:
                            p_event = MenuEventType.up
                        else:
                            p_event = MenuEventType.down
                    if event.axis == self.config['joyAxis']['leftRight']:
                        if event.value < 0:
                            p_event = MenuEventType.left
                        else:
                            p_event = MenuEventType.right

                if p_event is not None:
                    p_event = MenuEvent(p_event, False)
                    for obj in self.UIObjects:
                        obj.input(p_event)
                    print(p_event.kind, p_event.repeat)

        # Check for game kill switches
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            if all([pygame.joystick.Joystick(i).get_button(button)
                    for button in self.config['gameKillSwitches']['joystick']]):
                print("Kill switch on joystick", i)

        pressed_keys = pygame.key.get_pressed()
        if all([pressed_keys[key] for key in self.config['gameKillSwitches']['keyboard']]):
            print("Kill switch on keyboard")

    def tick_process(self):
        for obj in self.UIObjects:
            obj.process()

    def tick_draw(self):
        # Paint the window black
        self.screen.fill((0, 0, 0))

        for obj in self.UIObjects:
            obj.draw(self.screen)

        pygame.display.flip()

# Initialize the application
if __name__ == "__main__":
    MainWindow = EmuSwitch()
    MainWindow.start()
