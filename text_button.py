import pygame
from pygame.locals import *

pygame.init()

font = pygame.font.SysFont(None , 26)

#define colours
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 180, 0)
grey = 100, 100, 100

#define global variable
clicked = False
counter = 0

class Button():
        
    #colours for button and text
    
    hover_col = (0, 225, 0)
    click_col = (0, 150, 0)
    text_col = white
    width = 100
    height = 50
    def __init__(self, x, y, width, height, text, color, surface):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.button_col = self.add_transparency(color)
        self.surface = surface
        self.hover_col = self.darken(color)
        self.hover_col = self.add_transparency(self.hover_col)
        self.click_col = self.hover_col

    def darken(self, color):
        """returns a color 25 values darker than one that is given"""
        if color == black:
            return grey
        new_color = []
        for i in range (3):
            new_color.append(color[i])
            if color[i] >= 50:
                new_color[i] = color[i] - 25
        return new_color

    def add_transparency(self, color):
        """returns a color with fourth value"""
        new_color = []
        for i in range (3):
            new_color.append(color[i])
        new_color.append(50)
        return new_color
                
    def draw_button(self):

        global clicked
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #create pygame Rect object for the button
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # button_rect.set_alpha(90)
        
        #check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:  # left click true
                clicked = True
                pygame.draw.rect(self.surface, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:  # left click false
                clicked = False
                action = True
            else:
                pygame.draw.rect(self.surface, self.hover_col, button_rect)

        else:
            pygame.draw.rect(self.surface, self.button_col, button_rect)
            
        
        #add shading to button
        pygame.draw.line(self.surface, white, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(self.surface, white, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(self.surface, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(self.surface, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        #add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.surface.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action
