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
        self.bg_color = (255, 165, 0)  
        self.font = pygame.font.SysFont(None, 55)
        self.title_text = self.font.render('Tower Defense Game', True, (255, 255, 255))
        self.start_text = self.font.render('Click to Start', True, (255, 255, 255)) 

    def render(self):
        self.window.fill(self.bg_color)
        self.window.blit(self.title_text, (window_width // 2 - self.title_text.get_width() // 2, 200))
        self.window.blit(self.start_text, (window_width // 2 - self.start_text.get_width() // 2, 300))
        pygame.display.update()

    def check_for_click(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False


class MainGameScreen:
    def __init__(self, window):
        self.window = window
        self.background = pygame.image.load(os.path.join('game_assests', 'map_one.png'))
        self.background = pygame.transform.scale(self.background, (window_width, window_height))

    def render(self):
        self.window.blit(self.background, (0, 0))
        pygame.display.update()
    
    def check_for_click(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        return False


def main():
    start_screen = StartScreen(window)
    main_game_screen = MainGameScreen(window)
    game_state = 'start_screen'
    
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
