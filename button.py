import pygame

"""
Python file for button objects

Button.py is creates a button object out of an image, position, and the images scale.
All of the features aren't fully implemented as plan, main.py currently handles the button logic
while the Button class creates the rectangle and its dimensions, and draws the image on screen.

Typical usage example:

    pause_button = Button(100, 200, pause_button.pdf, .5)
    pause_button.draw
"""

class Button():
    """button objects
    
    Attributes:
        width: an int representing the original images width
        height: an int representing the original images height
        image: an image file that is passed through the constructor
        rect: a rect object for the image
        rect.topleft: an int representing the top left coordinate for the image
        clicked: a boolean representing whether the button has been clicked
        """

    
    def __init__(self, x, y, image, scale):
        """initializes an instance based on the image, it's position and scale
        
        Args:
            x: defines x coordinate for instance
            y: defines y coordinate for instance
            image: the image file for instance
            scale: scale for the new image relative to the original
            """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        """draws the button and returns true if it is clicked
        
        Args:
            surface: the screen/surface that the button will be drawn on (window).
             
        Returns:
            Action - a boolean that is true when the button is clicked
        """
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # Check if mouse is clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.cliciked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action