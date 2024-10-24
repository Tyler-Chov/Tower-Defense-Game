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
        self.wave_text = self.font.render(f'Wave: {self.wave}', True, (255, 255, 255))
        pause_img = pygame.image.load(os.path.join('game_assests', 'Play-Pause.png')).convert_alpha() # not working because file isn't suppourted
        self.pause_button = button.Button(710, 510, pause_img, 0.15 )

        self.pause = True

 
        self.grid_active = False
        self.grid_size = 14
        self.map_path = ((0, 274), (116, 274), (116, 124), (258, 124), (258, 322), (444, 322), (444, 226), (700, 226))
        
        #Debugging Variables
        self.debug = False
        self.cursor_text = self.font.render('', True, (255, 255, 255)) 


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
        player_stats

        if self.pause_button.draw(window): # checks if the pause button is clicked
            print("button hit")
            if self.pause == True:
                self.pause = False
            elif self.pause == False:
                self.pause = True
            print(self.pause)
       
        self.pause_button.draw(window)

        tower_boxes = [
        Rectangle(705, 100, 90, 90, (100, 100, 100)),
        Rectangle(705, 200, 90, 90, (100, 100, 100)),
        Rectangle(705, 300, 90, 90, (100, 100, 100)),
        Rectangle(705, 400, 90, 90, (100, 100, 100))
        ]

        for box in tower_boxes:
            box.draw()
        
        if self.grid_active:
            self.draw_grid()
        
        self.window.blit(self.health_text, (705, 10))
        self.window.blit(self.money_text, (705, 40))
        self.window.blit(self.wave_text, (705, 70))
        
        if self.debug:
            self.update_cursor_position()
            self.draw_enemy_path()


        pygame.display.update()
    
    def draw_grid(self):
        grid_color = (0, 0, 0)
        grid_width = window_width - 100
        grid_height = window_height - 100
        for x in range(0, grid_width, self.grid_size):
            pygame.draw.line(self.window, grid_color, (x, 0), (x, grid_height))
        for y in range(0, grid_height, self.grid_size):
            pygame.draw.line(self.window, grid_color, (0, y), (grid_width, y))

    def check_for_click(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                tower_boxes = [
                    pygame.Rect(705, 100, 90, 90),
                    pygame.Rect(705, 200, 90, 90),
                    pygame.Rect(705, 300, 90, 90),
                    pygame.Rect(705, 400, 90, 90)
                ]
                for box in tower_boxes:
                    if box.collidepoint(mouse_pos):
                        self.grid_active = not self.grid_active 
                        return
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.debug = True
                    return

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
    
    # Debugging Functions
    def update_cursor_position(self):
        """Update and render the cursor position."""
        mouse_pos = pygame.mouse.get_pos()  
        self.cursor_text = self.font.render(f'Cursor: {mouse_pos}', True, (255, 255, 255))
        self.window.blit(self.cursor_text, (10, 10)) 
    
    def draw_enemy_path(self):
        path_color = (255, 0, 0)
        path_width = 3

        for i in range(len(self.map_path) - 1):
            start_pos = self.map_path[i]
            end_pos = self.map_path[i + 1]
            pygame.draw.line(self.window, path_color, start_pos, end_pos, path_width)


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
            main_game_screen.check_for_click()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
