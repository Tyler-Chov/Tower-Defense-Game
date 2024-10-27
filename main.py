import pygame, sys, os, button
from tower import Tower
from enemy import Enemy
from waves import Wave

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

        pause_img = pygame.image.load(os.path.join('game_assests', 'Play-Pause.png')).convert_alpha() # not working because file isn't suppourted
        self.pause_button = button.Button(710, 510, pause_img, 0.15 )
        self.pause = True

        #Map Variables
        self.map_path = ((0, 274), (116, 274), (116, 124), (258, 124), (258, 322), (444, 322),
                         (444, 226), (700, 226), (800, 226))
        self.collision_rects = [
            pygame.Rect(min(0, 140), min(248, 300), max(0, 140) - min(0, 140), max(248, 300) - min(248, 300)),
            pygame.Rect(min(140, 96), min(300, 100), max(140, 96) - min(140, 96), max(300, 100) - min(300, 100)),
            pygame.Rect(min(96, 278), min(100, 146), max(96, 278) - min(96, 278), max(146, 100) - min(100, 146)),
            pygame.Rect(min(278, 230), min(146, 348), max(278, 230) - min(278, 230), max(348, 146) - min(146, 348)),
            pygame.Rect(min(230, 470), min(348, 299), max(470, 230) - min(230, 470), max(348, 299) - min(299, 348)),
            pygame.Rect(min(470, 418), min(299, 200), max(470, 418) - min(470, 418), max(299, 200) - min(200, 299)),
            pygame.Rect(min(418, 700), min(200, 250), max(700, 418) - min(418, 700), max(250, 200) - min(200, 250)),
        ]

        #Tower Variables
        self.grid_active = False
        self.grid_size = 14 #Will remove later, some things still depend on this.
        self.tower_size = 3
        self.selected_tower = None
        self.placed_towers = []

        # Wave and Enemy
        self.wave = 1
        self._waves = []  # list of waves
        self._time_since_previous_spawn = 0
        self._enemy_list = []
        self._current_wave = 0
        self.wave_text = self.font.render(f'Wave: {self.wave}', True, (255, 255, 255))

        #progressive game difficulty for waves, may need different formula
        for wave_number in range(1, 60):  
            enemy_count = 3 * wave_number 
            enemy_hp = 10 + (5 * wave_number) 
            wave_data = [
                Enemy('circle', enemy_hp, 1, 1, self.map_path) for i in range(enemy_count)
            ]
            self._waves.append(Wave(wave_data, 60)) 

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
        self.pause_button.draw(window) # checks if the pause button is clicked
        if self.pause == False:
            pass # call waves/enemies
       
        tower_boxes = [
        Rectangle(705, 100, 90, 90, (100, 100, 100)),
        Rectangle(705, 200, 90, 90, (100, 100, 100)),
        Rectangle(705, 300, 90, 90, (100, 100, 100)),
        Rectangle(705, 400, 90, 90, (100, 100, 100))
        ]
        tower_image = pygame.image.load(os.path.join("game_assests", "tower.png"))
        tower_image = pygame.transform.scale(tower_image, (90, 90))
        for box in tower_boxes:
            box.draw()
        self.window.blit(tower_image, (705, 95))
        
        if self.grid_active:
            self.render_tower_preview()

        if self.selected_tower:
            self.draw_radius(self.selected_tower._position, self.selected_tower.get_range(), (128, 128, 128, 100))
            #Logic for upgrades and tower selection info should go here

        self.tower1_price = self.font.render(f'$200', True, (255, 255, 255))
        self.window.blit(self.health_text, (705, 10))
        self.window.blit(self.money_text, (705, 40))
        self.window.blit(self.wave_text, (705, 70))
        self.window.blit(self.tower1_price, (731, 167))
        
        for tower in self.placed_towers:
            tower.render(self.window)

        if self.debug:
            self.update_cursor_position()
            self.draw_enemy_path()
            self.render_tower_preview()
            self.render_collision_rects()
            '''
            for tower in self.placed_towers:
                print(tower._position) 
            '''

        self.update_waves()
        for enemy in self._enemy_list:
            if enemy.is_alive():
                enemy._move()
                enemy.render(self.window)
                if enemy._path_index >= len(enemy._path) - 1:
                    enemy.damage_base(self)
                    self.remove_health(enemy._strength)
                    self.remove_money(enemy._resource_worth)
                enemy.render(self.window)
        self.update_attacks()
        pygame.display.update()

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
                if self.grid_active:
                    self.place_tower(mouse_pos)
                    return
                
                #selecting towers.
                tower_clicked = False
                for tower in self.placed_towers:
                    tower_size = int(self.grid_size * self.tower_size * 0.8)
                    tower_rect = pygame.rect.Rect(
                        tower._position[0] - tower_size // 2,
                        tower._position[1] - tower_size // 2,
                        tower_size, tower_size
                    )
                    if tower_rect.collidepoint(mouse_pos):
                        self.selected_tower = tower
                        tower_clicked = True
                        break
                if not tower_clicked:
                    self.selected_tower = None

                #Pause button functionality                    
                pause_button = pygame.Rect(710, 510, 75, 75)
                if pause_button.collidepoint(mouse_pos):
                    if self.pause == True:
                        self.pause = False
                    elif self.pause == False:
                        self.pause = True

            #Debug toggle button.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.debug == True:
                        self.debug = False
                    else: 
                        self.debug = True
                    return
    
    
    def draw_radius(self, center, radius, color):
        range_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        range_surface.fill((0, 0, 0, 0))  
        pygame.draw.circle(
            range_surface, color, (radius, radius), radius
        )
        top_left = (center[0] - radius, center[1] - radius)
        self.window.blit(range_surface, top_left)


    def render_tower_preview(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        temp_tower = Tower("Archer Tower", 50, 3, 100, 80, 1)
        if self.check_collision(mouse_x, mouse_y):
            color = (255, 0, 0, 100)
        else:
            color = (128, 128, 128, 100) 
        self.draw_radius((mouse_x, mouse_y), temp_tower.get_range(), color)
        tower_surface = pygame.transform.scale(
            temp_tower._image, (temp_tower.size * 3, temp_tower.size * 3)
        )
        self.window.blit(
            tower_surface,
            (mouse_x - tower_surface.get_width() // 2, mouse_y - tower_surface.get_height() // 2)
        )


    def place_tower(self, mouse_pos):
        if not self.check_collision(mouse_pos[0], mouse_pos[1]):
            if self.money < 200:
                return
            new_tower = Tower("Archer Tower", 20, 2, 1, 80, 1)
            #need to expand on this to allow for different towers
            new_tower.place(mouse_pos)
            self.placed_towers.append(new_tower)
            self.grid_active = False 
            self.selected_tower = False
            self.remove_money(200)
        else:
            print("Cannot place the tower here. Collision detected.")


    def check_collision(self, x, y):
        preview_size = self.grid_size * self.tower_size 

        preview_rect = pygame.Rect(
            x - preview_size // 2, y - preview_size // 2, preview_size, preview_size
        )

        for tower in self.placed_towers: #checking to see if colliding with any placed towers.
            tower_size = int(self.grid_size * self.tower_size * 0.8)
            tower_rect = pygame.Rect(
                tower._position[0] - tower_size // 2,
                tower._position[1] - tower_size // 2,
                tower_size, tower_size
            )
            if preview_rect.colliderect(tower_rect):
                return True 
        
        for rect in self.collision_rects: #checking to see if collide with map path.
            if preview_rect.colliderect(rect):
                return True
        bottom_bar = pygame.Rect(0, window_height - 100, window_width, 100)
        side_bar = pygame.Rect(window_width - 100, 0, 100, window_height)

        if preview_rect.colliderect(bottom_bar) or preview_rect.colliderect(side_bar):
            return True
        return False

    
    def update_attacks(self):
        for tower in self.placed_towers:
            tower.attack(self._enemy_list)
        for enemy in self._enemy_list:
            if not enemy.is_alive():
                self.add_money(enemy._resource_worth)
                self._enemy_list.remove(enemy)


    def update_waves(self):
        if self._current_wave < len(self._waves):
            current_wave = self._waves[self._current_wave]
            if current_wave._is_wave_complete():
                self._current_wave += 1
                if self._current_wave < len(self._waves):
                    self.wave += 1
                    self.wave_text = self.font.render(f"Wave: {self.wave}", True, (255, 255, 255))
                return

            self._time_since_previous_spawn += 1
            if self._time_since_previous_spawn >= current_wave._spawn_timer:
                if current_wave.spawn_enemy():
                    new_enemy = current_wave._enemy_list[-1]
                    self._enemy_list.append(new_enemy)
                self._time_since_previous_spawn = 0

            #self._enemy_list = [e for e in self._enemy_list if e.is_alive()]


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

    def render_collision_rects(self):
        """Render the collision rectangles for debugging."""
        for rect in self.collision_rects:
            pygame.draw.rect(self.window, (255, 0, 0), rect, 2)  

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
