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

#define global variable
clicked = False
counter = 0

class Button():
        
    #colours for button and text
    button_col = green
    hover_col = (0, 225, 0)
    click_col = (0, 150, 0)
    text_col = white
    width = 100
    height = 50
    def __init__(self, x, y, text, surface):
        self.x = x
        self.y = y
        self.text = text

        self.surface = surface

    def draw_button(self):

        global clicked
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #create pygame Rect object for the button
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        #check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(self.surface, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
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
