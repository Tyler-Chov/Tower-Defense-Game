import pygame
from pygame.locals import *
import os

pygame.init()

font = pygame.font.Font(
    os.path.join('game_assests', 'EXEPixelPerfect.ttf'), 26)
"""The font used for the button"""

# define colours
_bg = (204, 102, 0)
_red = (255, 0, 0)
_black = (0, 0, 0)
_white = (255, 255, 255)
_green = (0, 180, 0)
_grey = 100, 100, 100

# define global variable
clicked = False
"""The status of the button click"""
_counter = 0


class Button():
    # colours for button and text
    hover_col = (0, 225, 0)
    """The color of the button when hovered over"""
    click_col = (0, 150, 0)
    """The color of the button when clicked"""
    text_col = _white
    """The color of the text on the button"""
    width = 100
    """The width of the button"""
    height = 50
    """The height of the button"""

    def __init__(self, x, y, width, height, text, color, surface):
        self.x = x
        """The x position of the button"""
        self.y = y
        """The y position of the button"""
        self.width = width
        """The width of the button"""
        self.height = height
        """The height of the button"""
        self.text = text
        """The text on the button"""
        self.button_col = self.add_transparency(color)
        """The color of the button"""
        self.surface = surface
        """The surface the button is drawn on"""
        self.hover_col = self.darken(color)
        self.hover_col = self.add_transparency(self.hover_col)
        self.click_col = self.hover_col

    def darken(self, color):
        """returns a color 25 values darker than one that is given"""
        if color == _black:
            return _grey
        new_color = []
        for i in range(3):
            new_color.append(color[i])
            if color[i] >= 50:
                new_color[i] = color[i] - 25
        return new_color

    def add_transparency(self, color):
        """returns a color with fourth value"""
        new_color = []
        for i in range(3):
            new_color.append(color[i])
        new_color.append(50)
        return new_color

    def draw_button(self):
        """draws the button on the surface"""
        global clicked
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # create pygame Rect object for the button
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # button_rect.set_alpha(90)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:  # left click true
                clicked = True
                pygame.draw.rect(self.surface, self.click_col, button_rect)
            # left click false
            elif pygame.mouse.get_pressed()[0] == 0 and clicked is True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(self.surface, self.hover_col, button_rect)

        else:
            pygame.draw.rect(self.surface, self.button_col, button_rect)

        # add shading to button
        pygame.draw.line(self.surface, _white, (self.x, self.y),
                         (self.x + self.width, self.y), 2)
        pygame.draw.line(self.surface, _white, (self.x, self.y),
                         (self.x, self.y + self.height), 2)
        pygame.draw.line(self.surface, _black, (self.x, self.y + self.height),
                         (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(self.surface, _black, (self.x + self.width, self.y),
                         (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.surface.blit(text_img, (self.x + int(
            self.width / 2) - int(text_len / 2) + 2, self.y + 25))
        return action
