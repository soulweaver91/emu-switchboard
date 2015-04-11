__author__ = 'Soulweaver'

import pygame
import pygame.freetype
import os


pygame.init()

main_font = pygame.freetype.Font(os.path.join('assets', 'AlegreyaSans-Bold.ttf'), size=40)
main_font_it = pygame.freetype.Font(os.path.join('assets', 'AlegreyaSans-BoldItalic.ttf'), size=40)
mono_font = pygame.freetype.Font(os.path.join('assets', 'DroidSansMono.ttf'), size=40)

c_white = (255, 255, 255)
c_black = (0, 0, 0)


def centered_pos(font, text, pos):
    return pos[0] - font.get_rect(text).width / 2, pos[1]
