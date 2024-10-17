import pygame, sys, os

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
        self.font = pygame.font.SysFont(None, 30)
        self.health = 0 
        self.health_text = self.font.render(f'Health: {self.health}', True, (255, 255, 255))
        self.money = 0 
        self.money_text = self.font.render(f'Money: {self.money}', True, (255, 255, 255))

    def render(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.health_text, (10, 10))
        self.window.blit(self.money_text, (10, 50))

        bottom_rect_width = window_width
        bottom_rect_height = 100
        bottom_rect_x = window_width - bottom_rect_width
        bottom_rect_y = window_height - bottom_rect_height
        pygame.draw.rect(self.window, (200, 200, 200), (bottom_rect_x, bottom_rect_y, bottom_rect_width, bottom_rect_height))

    
        Side_rect_width = 100
        Side_rect_height = window_height
        Side_rect_x = window_width - Side_rect_width
        Side_rect_y = window_height
        pygame.draw.rect(self.window, (200, 200, 200), (Side_rect_x, Side_rect_y, Side_rect_width, Side_rect_height))

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
