import pygame, sys, os, button

FPS = 60
fpsClock = pygame.time.Clock()
window_width = 800
window_height = 600

pygame.display.set_caption('Tower Defense Game')
pygame.init()
window = pygame.display.set_mode((window_width, window_height))

class StartScreen:
    def __init__(self, window):
        self.window = window
        self.background = pygame.image.load(os.path.join('game_assests', 'start_screen_background.jpg'))
        self.background = pygame.transform.scale(self.background, (window_width, window_height))
        self.font = pygame.font.SysFont(None, 55)
        self.title_text = self.font.render('Tower Defense Game', True, (255, 255, 255))
        self.start_text = self.font.render('Click to Start', True, (255, 255, 255)) 

    def render(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.title_text, (window_width // 2 - self.title_text.get_width() // 2, 100))
        start_text_rect = self.start_text.get_rect(center=(window_width // 2, 400))
        rect_x = start_text_rect.x - 10
        rect_y = start_text_rect.y - 10
        rect_width = start_text_rect.width + 20
        rect_height = start_text_rect.height + 20

        pygame.draw.rect(self.window, (39, 145, 39), (rect_x, rect_y, rect_width, rect_height))
        self.window.blit(self.start_text, start_text_rect.topleft)
        pygame.display.update()
        self.start_button_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    def check_for_click(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_button_rect.collidepoint(mouse_pos):
                    return True
        return False



class MainGameScreen:
    def __init__(self, window):
        self.window = window
        self.background = pygame.image.load(os.path.join('game_assests', 'map_one.png'))
        self.background = pygame.transform.scale(self.background, (window_width - 100, window_height - 100))
        self.font = pygame.font.SysFont(None, 24)
        self.health = 0 
        self.health_text = self.font.render(f'Health: {self.health}', True, (255, 255, 255))
        self.money = 0 
        self.money_text = self.font.render(f'Money: {self.money}', True, (255, 255, 255))
        self.wave = 0 
        self.wave_text = self.font.render(f'wave: {self.wave}', True, (255, 255, 255))
        pause_img = pygame.image.load(os.path.join('game_assests', 'Play-Pause.png')).convert_alpha() # not working because file isn't suppourted
        self.pause_button = button.Button(710, 510, pause_img, 0.15 )


    def render(self):
        self.window.blit(self.background, (0, 0))

        class Rectangle():
            def __init__(self, x, y, width, height, color):
                self.x = x 
                self.y = y
                self.width = width
                self.height = height
                self.color = color

            def draw(self):
                pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

        # create and draw menus
        bottom_bar = Rectangle(0, (window_height - 100), window_width, 100, (150,150,150))
        side_bar = Rectangle((window_width - 100), 0, 100, window_height, (150,150,150))
        bottom_bar.draw()
        side_bar.draw()

        top_box = Rectangle(700, 495, 100, 5, (100,100,100))
        side_box = Rectangle(695, 500, 5, 100, (100,100,100))
        top_box.draw()
        side_box.draw()
        self.pause_button.draw(window)
        
        self.window.blit(self.health_text, (705, 10))
        self.window.blit(self.money_text, (705, 40))
        self.window.blit(self.wave_text, (705, 70))


        """
        # potential code for pause button hitbox
        top_pause_box_width = 50
        top_pause_box_height = 5
        top_pause_box_x = 725
        top_pause_box_y = 525
        pygame.draw.rect(self.window, (0, 0, 0), (top_pause_box_x, top_pause_box_y, top_pause_box_width, top_pause_box_height))

        side_pause_box_width = 5
        side_pause_box_height = 50
        side_pause_box_x = 7
        side_pause_box_y = 500
        pygame.draw.rect(self.window, (0, 0, 0), (side_pause_box_x, side_pause_box_y, side_pause_box_width, side_pause_box_height))
        """

        pygame.display.update()
    
    def check_for_click(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        return False

    def remove_health(self, health):
        self.health -= health
        self.health_text = self.font.render(f'Health: {self.health}', True, (255, 255, 255))
        if self.health <= 0:
            self.game_over()

    def add_money(self, money):
        self.money += money
        self.money_text = self.font.render(f'Money: {self.money}', True, (255, 255, 255))

    def remove_money(self, money):
        self.money -= money
        self.money_text = self.font.render(f'Money: {self.money}', True, (255, 255, 255))

    def set_health(self, health):
        self.health = health
        self.health_text = self.font.render(f'Health: {self.health}', True, (255, 255, 255))

    def set_money(self, money):
        self.money = money
        self.money_text = self.font.render(f'Money: {self.money}', True, (255, 255, 255))
    
        
def main():
    start_screen = StartScreen(window)
    main_game_screen = MainGameScreen(window)
    game_state = 'start_screen'
    main_game_screen.set_health(100)
    main_game_screen.set_money(500)
    while True:
        if game_state == 'start_screen':
            start_screen.render()
            if start_screen.check_for_click():
                game_state = 'main_game'
                
        elif game_state == 'main_game':
            main_game_screen.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
