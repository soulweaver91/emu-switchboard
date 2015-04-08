__author__ = 'Soulweaver'

import sys
import pygame


class EmuSwitch:
    def __init__(self):
        print('Starting up emu-switchboard...')

        # Initialize pygame and joystick support
        pygame.init()
        pygame.joystick.init()
        pygame.display.set_caption("EmuSwitchboard")

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
        self.config = ""

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
                # TODO: Preprocess events
                for obj in self.UIObjects:
                    obj.input()
                print(event)

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
