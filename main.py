import pygame, sys, os, button, pygame_widgets
from tower import Tower
from enemy import Enemy
from waves import Wave
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import text_button

FPS = 60
fpsClock = pygame.time.Clock()
window_width = 800
window_height = 600
global sound_volume 
global bgm_volume
sound_volume = 1
bgm_volume = 1
pygame.display.set_caption('Tower Defense Game')
pygame.init()
window = pygame.display.set_mode((window_width, window_height))


class StartScreen:
    """
    A class to represent the start screen of the Tower Defense Game.
    Attributes:
    
    Attributes:
    window: The window surface where the start screen will be rendered.
    background: The background image of the start screen.
    font: The font used for rendering text on the start screen.
    title_text: The rendered text surface for the game title.
    start_text: The rendered text surface for the start button.
    start_button_rect: The rectangle area of the start button.
   
    Methods:
    render(): Renders the start screen with the background, title, and start button.
    check_for_click(): Checks for mouse click events and returns True if the start button is clicked.
    """
    def __init__(self, window):
        """
        Initializes the main game window and loads the start screen assets.
        Args:
            window: The window surface where the start screen will be rendered.
        """
        self.window = window
        self.background = pygame.image.load(os.path.join('game_assests', 'start_screen_background.jpg'))
        self.background = pygame.transform.scale(self.background, (window_width, window_height))
        self.font = pygame.font.SysFont(None, 55)
        self.title_text = self.font.render('Tower Defense Game', True, (255, 255, 255))
        self.start_text = self.font.render('Click to Start', True, (255, 255, 255))

    def render(self):
        """
        Renders the start screen with the background, title, and start button.
        """
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
        """
        Checks for mouse click events and returns True if the start button is clicked.

        Returns:
            bool: True if the start button is clicked, False otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.start_button_rect.collidepoint(mouse_pos):
                    return True
        return False


class Stage_Select_Screen:
    def __init__(self, window):
        self.window = window
        self.background = pygame.image.load(os.path.join('game_assests', 'Stage_Select.png'))
        self.background = pygame.transform.scale(self.background, (window_width, window_height))
        self.font = pygame.font.SysFont(None, 55)
        self.stage_selection = None
        self.difficulty_selection = None
        self.hovered_stage = None
        self.hovered_difficulty = None
        self.start_button_hovered = False
        self.stage1_button_rect = pygame.Rect(147, 125, 236, 110)
        self.stage2_button_rect = pygame.Rect(147, 245, 236, 110)
        self.stage3_button_rect = pygame.Rect(147, 365, 236, 110)
        self.easy_button_rect = pygame.Rect(403, 398, 76, 34)
        self.medium_button_rect = pygame.Rect(491, 398, 77, 34)
        self.hard_button_rect = pygame.Rect(579, 398, 77, 34)
        self.start_button_rect = pygame.Rect(402, 441, 254, 37)

        self.click_sound = pygame.mixer.Sound(os.path.join('game_assests/sounds', 'click.mp3'))
        self.music = pygame.mixer.music.load(os.path.join('game_assests/sounds', 'stage_selection_music.mp3'))
    def render(self):
        self.window.blit(self.background, (0, 0))
        if self.hovered_stage == "stage1" or self.stage_selection == "stage1":
            self._draw_overlay(self.stage1_button_rect)
        if self.hovered_stage == "stage2" or self.stage_selection == "stage2":
            self._draw_overlay(self.stage2_button_rect)
        if self.hovered_stage == "stage3" or self.stage_selection == "stage3":
            self._draw_overlay(self.stage3_button_rect)
        if self.hovered_difficulty == "easy" or self.difficulty_selection == "easy":
            self._draw_overlay(self.easy_button_rect)
        if self.hovered_difficulty == "medium" or self.difficulty_selection == "medium":
            self._draw_overlay(self.medium_button_rect)
        if self.hovered_difficulty == "hard" or self.difficulty_selection == "hard":
            self._draw_overlay(self.hard_button_rect)
        if self.start_button_hovered:
            self._draw_overlay(self.start_button_rect)
        pygame.display.update()

    def check_for_click(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_stage = None
            self.hovered_difficulty = None
            self.start_button_hovered = False

            if self.stage1_button_rect.collidepoint(mouse_pos):
                self.hovered_stage = "stage1"
            if self.stage2_button_rect.collidepoint(mouse_pos):
                self.hovered_stage = "stage2"
            if self.stage3_button_rect.collidepoint(mouse_pos):
                self.hovered_stage = "stage3"

            if self.easy_button_rect.collidepoint(mouse_pos):
                self.hovered_difficulty = "easy"
            if self.medium_button_rect.collidepoint(mouse_pos):
                self.hovered_difficulty = "medium"
            if self.hard_button_rect.collidepoint(mouse_pos):
                self.hovered_difficulty = "hard"

            if self.start_button_rect.collidepoint(mouse_pos):
                self.start_button_hovered = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click_sound.set_volume(sound_volume)
                pygame.mixer.Sound.play(self.click_sound)
                if self.hovered_stage:
                    self.stage_selection = self.hovered_stage
                if self.hovered_difficulty:
                    self.difficulty_selection = self.hovered_difficulty
                if self.start_button_hovered:
                    return True  

    def _draw_overlay(self, rect):
        overlay = pygame.Surface((rect.width, rect.height))
        overlay.set_alpha(90)
        overlay.fill((0, 0, 0))
        self.window.blit(overlay, (rect.x, rect.y))

    def return_selection(self):
        return {
            "stage": self.stage_selection,
            "difficulty": self.difficulty_selection
        }
    
    def reset_selection(self):
        self.stage_selection = None
        self.difficulty_selection = None


class MainGameScreen:
    """The game screen which shows the map and handles the generation of enemies, towers, and player stats."""
    def __init__(self, window, map, difficulty):
        self.window = window
        """The window for the game."""
        """Scales the image in self.background appropriately and then saves it back to self.background."""
        self.font = pygame.font.SysFont(None, 22)
        """Sets the font style to be used."""
        self.health = 0
        """Holds the amount of health the player has remaining."""
        self.health_text = self.font.render(f'Health: {self.health}', True, (255, 255, 255))
        """Renders the health text so the player knows how much health they have remaining."""
        self.money = 0
        """Holds the amount of money the player has"""
        self.money_text = self.font.render(f'Money: {self.money}', True, (255, 255, 255))
        """Renders the money text so the player knows how much money they have remaining."""

        # Wave Pause button
        wave_pause_img = pygame.image.load(os.path.join('game_assests', 'Play-Pause.png')).convert_alpha()
        """The image of the pause button."""
        self.wave_pause_button = button.Button(710, 510, wave_pause_img, 0.15)
        """Makes the pause button a button to be clicked, using the image stored in pause_img."""

        self.game_pause_img = pygame.image.load(os.path.join('game_assests', 'pause.png'))
        self.game_pause_img = pygame.transform.scale(self.game_pause_img, (30, 30))
        self.wave_pause = False
        self.pause = False
        """Sets pause to True when initially ran."""
        self.map = map
        self.return_to_stage_select = False

        # Map Variables
        if self.map == 1:
            self.background = pygame.image.load(os.path.join('game_assests', 'map_one.png'))
            """Loads the image."""
            self.background = pygame.transform.scale(self.background, (window_width - 100, window_height - 100))
            self.map_path = ((0, 274), (116, 274), (116, 124), (258, 124), (258, 322), (444, 322),
                            (444, 226), (700, 226), (800, 226))
            """Sets the path for enemies to traverse."""
            self.collision_rects = [
                pygame.Rect(min(0, 140), min(248, 300), max(0, 140) - min(0, 140), max(248, 300) - min(248, 300)),
                pygame.Rect(min(140, 96), min(300, 100), max(140, 96) - min(140, 96), max(300, 100) - min(300, 100)),
                pygame.Rect(min(96, 278), min(100, 146), max(96, 278) - min(96, 278), max(146, 100) - min(100, 146)),
                pygame.Rect(min(278, 230), min(146, 348), max(278, 230) - min(278, 230), max(348, 146) - min(146, 348)),
                pygame.Rect(min(230, 470), min(348, 299), max(470, 230) - min(230, 470), max(348, 299) - min(299, 348)),
                pygame.Rect(min(470, 418), min(299, 200), max(470, 418) - min(470, 418), max(299, 200) - min(200, 299)),
                pygame.Rect(min(418, 700), min(200, 250), max(700, 418) - min(418, 700), max(250, 200) - min(200, 250)),
            ]
            """Sets up some collision spots, where the towers cannot be placed. (ie. the enemy path)"""
        elif map == 2:
            pass

        # Tower Variables
        self.grid_active = False
        """Used to show the grid"""
        self.grid_size = 14  # Will remove later, some things still depend on this.
        """Determines the grid size."""
        self.tower_size = 3
        """Determines the tower size"""
        self.selected_tower = None
        """Determines which tower the player has selected."""
        self.placed_towers = []
        """A list to hold all the towers that have been placed."""

        # Wave and Enemy
        self.difficulty = difficulty
        self.wave = 1
        """Stores which wave number is currently displayed to the player"""
        self._waves = []  # list of waves
        self._time_since_previous_spawn = 0
        self._enemy_list = []
        self._current_wave = 0
        self.wave_text = self.font.render(f'Wave: {self.wave}', True, (255, 255, 255))
        """Renders the current wave number."""

        for wave_number in range(1, 60):
            """Loop for generating waves, changes are planned to further improve."""
            enemy_count = 3 * wave_number
            """Determines amount of enemies to be spawned, dependent on wave number."""
            enemy_hp = 10 + (5 * wave_number)
            """Increases health of the enemies, dependent on wave number."""
            speed = 1 + (0.2 * wave_number)
            """Increases speed of the enemies, dependent on wave number."""
            wave_data = [
                Enemy('circle', enemy_hp, speed, 1, self.map_path) for i in range(enemy_count)
            ]
            """Generate wave data, to be added to self._waves"""
            self._waves.append(Wave(wave_data, 60))

            # Debugging Variables
        self.debug = False
        """Used to help debug."""
        self.cursor_text = self.font.render('', True, (255, 255, 255))
        """Displays the text for the cursor."""

    def render(self):
        """Used to render the game and enemies."""
        self.window.blit(self.background, (0, 0))
        """Sets window"""

        class Rectangle:
            """Creates rectangles for the UI."""
            def __init__(self, x, y, width, height, color):
                self.x = x
                """The x position of the rectangle."""
                self.y = y
                """The y position of the rectangle."""
                self.width = width
                """The width of the rectangle."""
                self.height = height
                """The height of the rectangle."""
                self.color = color
                """The color of the rectangle."""
                self.rect = pygame.Rect(x, y, width, height)
                """The pygame.Rect object for collision detection."""

            def draw(self):
                """Draws the rectangle."""
                pygame.draw.rect(window, self.color, self.rect)

            def is_hovered(self, mouse_pos):
                """Checks if the mouse is hovering over the rectangle."""
                return self.rect.collidepoint(mouse_pos)

        # create menus, tower slots, and tower image
        side_bar = Rectangle((window_width - 100), 0, 100, window_height, (150, 150, 150))
        """Menu on the right side, shows player stats and towers that can be used."""
        bottom_bar = Rectangle(0, (window_height - 100), window_width, 100, (150, 150, 150))
        """Menu on the bottom, currently hold nothing."""

        box_unselected_color = (100, 100, 100)
        tower_boxes = [
            Rectangle(705, 100, 90, 90, box_unselected_color),
            Rectangle(705, 200, 90, 90, box_unselected_color),
            Rectangle(705, 300, 90, 90, box_unselected_color),
            Rectangle(705, 400, 90, 90, box_unselected_color)
        ]
        """Makes the rectangles for the tower boxes."""

        health_box = Rectangle(5, 505, 680, 90, (100, 100, 100))
        health_bar = Rectangle(10, 510, (670 * (self.health / 100)), 80, (0, 190, 0))
        """Makes the rectangles for the health bar/box"""
       
        upgrade_boxes = [
            Rectangle(5, 505, 340, 90, (100, 100, 100)),
            Rectangle(355, 505, 340, 90, (100, 100, 100)),
        ]
        """Makes the rectangles for the upgrade boxes."""

        upgrade_damage_button = text_button.Button(230, 540, 'Upgrade', window)
        upgrade_cooldown_button = text_button.Button(580, 540, 'Upgrade', window)
        upgrade_buttons = [
            Rectangle(200, 525, 130, 50, (0, 180, 0)),
            Rectangle(550, 525, 130, 50, (0, 180, 0)),
        ]

        tower_image = pygame.image.load(os.path.join("game_assests", "tower.png"))
        """Loads tower image."""
        tower_image = pygame.transform.scale(tower_image, (90, 90))
        """Scales tower image."""

        if self.grid_active:
            """Checks if grid is currently active, then renders a preview of the tower selected."""
            self.render_tower_preview()
        
        bottom_bar.draw()
        
        if self.selected_tower:
            """Renders the attack radius of the selected tower."""
            self.draw_radius(self.selected_tower._position, self.selected_tower.get_range(), (128, 128, 128, 100))
            # Logic for upgrades and tower selection info should go here
            for box in upgrade_boxes:
                box.draw()
            if upgrade_damage_button.draw_button():
                if self.money >= 50:
                    self.selected_tower._damage *= 1.5
                    self.remove_money(50)
                
            if upgrade_cooldown_button.draw_button():
                if self.money >= 50:
                    self.selected_tower._shot_cooldown *= .75
                    self.remove_money(50)
            self.attack_damage_text = self.font.render(f"Attack Damage: {self.selected_tower._damage}", True, (255, 255, 255))
            self.attack_cooldown_text = self.font.render(f"Attack Cooldown: {self.selected_tower._shot_cooldown}", True, (255, 255, 255))
            self.window.blit(self.attack_damage_text, (10, 510))
            self.window.blit(self.attack_cooldown_text, (370, 510))
            
        else:
            health_box.draw()
            health_bar.draw()
        self.tower1_price = self.font.render(f'$200', True, (255, 255, 255))
        """Renders the price of tower1."""

        for tower in self.placed_towers:
            """Renders each placed tower."""
            tower.render(self.window)
        
        for enemy in self._enemy_list:
            enemy.render(self.window)

        if self.debug:
            """When debug is true, updates the game and renders various aspects."""
            self.update_cursor_position()
            self.draw_enemy_path()
            self.render_tower_preview()
            self.render_collision_rects()
            '''
            for tower in self.placed_towers:
                print(tower._position) 
            '''
        if not self.wave_pause:
            
            self.update_waves()
            for enemy in self._enemy_list:
                """For each active enemy, the enemy will move along the set path towards the player base."""
                if enemy.is_alive():
                    enemy._move()
                    if enemy._path_index >= len(enemy._path) - 1:
                        enemy.damage_base(self)
                        self.remove_health(enemy._strength)
                        self.remove_money(enemy._resource_worth)
            self.update_attacks()

        # Display menu and UI
        side_bar.draw()
        mouse_pos = pygame.mouse.get_pos()
        for box in tower_boxes:
            if box.is_hovered(mouse_pos):
                box.color = (70, 70, 70)
            else:
                box.color = box_unselected_color
        for box in tower_boxes:
            """Draws each box in the tower_boxes list."""
            box.draw()
        # for box in upgrade_boxes:
            # """Draws each box in the upgrade_boxes list."""
            # box.draw()
            
        self.window.blit(tower_image, (705, 95))
        self.window.blit(self.health_text, (705, 10))
        self.window.blit(self.money_text, (705, 40))
        self.window.blit(self.wave_text, (705, 70))
        self.window.blit(self.tower1_price, (731, 167))
        self.wave_pause_button.draw(window)
        self.window.blit(self.game_pause_img, (10, 10))
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

                # selecting towers.
                tower_clicked = False
                bottom_bar = pygame.rect.Rect(0, (window_height - 100), window_width, 100)
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
                if not tower_clicked and not bottom_bar.collidepoint(mouse_pos):
                    self.selected_tower = None

                # Wave Pause button functionality
                wave_pause_button = pygame.Rect(710, 510, 75, 75)
                if wave_pause_button.collidepoint(mouse_pos):
                    if self.wave_pause == True:
                        self.wave_pause = False
                    elif self.wave_pause == False:
                        self.wave_pause = True
                    return
                 
                # Game Pause button functionality
                game_pause_button = pygame.Rect(10, 10, 30, 30)
                if game_pause_button.collidepoint(mouse_pos):
                    self.pause = True
                    self.wave_pause = True
                    result = self.pause_screen()
                    if result == "resume":
                        self.wave_pause = False
                        self.pause = False

                        return
                    elif result == "stage_select":
                        self.return_to_stage_select = True
                        return "stage_select"
                    return

                
                # upgrade button functionality here

            # Debug toggle button.
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
            # need to expand on this to allow for different towers
            new_tower.place(mouse_pos)
            self.placed_towers.append(new_tower)
            self.grid_active = False
            self.selected_tower = False
            self.remove_money(200)
        else:
            #print("Cannot place the tower here. Collision detected.")
            pass
    def check_collision(self, x, y):
        preview_size = self.grid_size * self.tower_size

        preview_rect = pygame.Rect(
            x - preview_size // 2, y - preview_size // 2, preview_size, preview_size
        )

        for tower in self.placed_towers:  # checking to see if colliding with any placed towers.
            tower_size = int(self.grid_size * self.tower_size * 0.8)
            tower_rect = pygame.Rect(
                tower._position[0] - tower_size // 2,
                tower._position[1] - tower_size // 2,
                tower_size, tower_size
            )
            if preview_rect.colliderect(tower_rect):
                return True

        for rect in self.collision_rects:  # checking to see if collide with map path.
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
        """Checks if the current wave is complete, moves on to the next wave prepared once it is."""
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
                    """Records the next enemy to be spawned."""
                    self._enemy_list.append(new_enemy)
                self._time_since_previous_spawn = 0

    def setting_screen(self):
        global sound_volume, bgm_volume

        overlay = pygame.Surface((window_width, window_height))
        overlay.fill((120, 120, 120, 100))
        self.window.blit(overlay, (0, 0))

        font = pygame.font.SysFont(None, 40)
        label_font = pygame.font.SysFont(None, 30)
        setting_text = pygame.font.SysFont(None, 60)

        bgm_slider = Slider(self.window, window_width // 2 - 100, window_height // 2 - 50, 200, 20, min=0, max=10, step=1)
        bgm_slider.setValue(int(bgm_volume * 10))
        sfx_slider = Slider(self.window, window_width // 2 - 100, window_height // 2 + 50, 200, 20, min=0, max=10, step=1)
        sfx_slider.setValue(int(sound_volume * 10))

        bgm_label = label_font.render("BGM", True, (255, 255, 255))
        bgm_label_rect = bgm_label.get_rect(center=(window_width // 2, window_height // 2 - 80))
        sfx_label = label_font.render("SFX", True, (255, 255, 255))
        sfx_label_rect = sfx_label.get_rect(center=(window_width // 2, window_height // 2 + 20))
        back_button_rect = pygame.Rect(window_width // 2 - 100, window_height - 100, 200, 50)
        back_text = font.render("Back", True, (255, 255, 255))
        setting_text = setting_text.render("Settings", True, (255, 255, 255))
        setting_text_rect = setting_text.get_rect(center=(window_width // 2, 120))

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if back_button_rect.collidepoint(mouse_pos):
                        running = False
    
            pygame_widgets.update(events)
            bgm_value = bgm_slider.getValue() / 10.0 
            sfx_value = sfx_slider.getValue() / 10.0  
            bgm_volume = bgm_value
            sound_volume = sfx_value
            pygame.mixer.music.set_volume(bgm_volume) 
            self.window.fill((30, 30, 30))
            self.window.blit(overlay, (0, 0))
            pygame.draw.rect(self.window, (100, 100, 100), back_button_rect)
            self.window.blit(back_text, (back_button_rect.centerx - back_text.get_width() // 2, back_button_rect.centery - back_text.get_height() // 2))
            self.window.blit(bgm_label, bgm_label_rect)
            self.window.blit(sfx_label, sfx_label_rect)
            self.window.blit(setting_text, setting_text_rect)
            bgm_slider.draw()
            sfx_slider.draw()
            pygame.display.flip()

    def pause_screen(self):
        paused = True
        game_snapshot = self.window.copy() 
        overlay = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  
        font = pygame.font.SysFont(None, 30)
        pause_font = pygame.font.SysFont(None, 80)
        pause_text = pause_font.render("Paused", True, (255, 255, 255))

        button_width, button_height = 200, 50
        resume_button_rect = pygame.Rect(window_width // 2 - button_width // 2, 220, button_width, button_height)
        stage_select_button_rect = pygame.Rect(window_width // 2 - button_width // 2, 290, button_width, button_height)
        setting_button_rect = pygame.Rect(window_width // 2 - button_width // 2, 360, button_width, button_height)
        quit_button_rect = pygame.Rect(window_width // 2 - button_width // 2, 430, button_width, button_height)

        resume_text = font.render("Resume", True, (255, 255, 255))
        stage_select_text = font.render("Stage Select", True, (255, 255, 255))
        setting_text = font.render("Settings", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        while paused:
            self.window.blit(game_snapshot, (0, 0))
            self.window.blit(overlay, (0, 0))
            self.window.blit(pause_text, (window_width // 2 - pause_text.get_width() // 2, 100))
            cursor_pos = pygame.mouse.get_pos()
            for button_rect, text, color in [
                (resume_button_rect, resume_text, (100, 100, 100) if resume_button_rect.collidepoint(cursor_pos) else (150, 150, 150)),
                (stage_select_button_rect, stage_select_text, (100, 100, 100) if stage_select_button_rect.collidepoint(cursor_pos) else (150, 150, 150)),
                (setting_button_rect, setting_text, (100, 100, 100) if setting_button_rect.collidepoint(cursor_pos) else (150, 150, 150)),
                (quit_button_rect, quit_text, (100, 100, 100) if quit_button_rect.collidepoint(cursor_pos) else (150, 150, 150)),
            ]:
                pygame.draw.rect(self.window, color, button_rect)
                self.window.blit(text, (button_rect.centerx - text.get_width() // 2, button_rect.centery - text.get_height() // 2))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if resume_button_rect.collidepoint(mouse_pos):
                        paused = False  
                    elif stage_select_button_rect.collidepoint(mouse_pos):
                        return "stage_select"
                    elif setting_button_rect.collidepoint(mouse_pos):
                        self.setting_screen() 
                    elif quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = False 
        self.pause = False
        self.wave_pause = False

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
    stage_select = Stage_Select_Screen(window)
    game_state = 'start_screen'
    main_game_screen = None  

    while True:
        if game_state == 'start_screen':
            start_screen.render()
            if start_screen.check_for_click():
                game_state = 'stage_select'

        elif game_state == 'stage_select':
            stage_select.render()
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(os.path.join('game_assests/sounds', 'stage_selection_music.mp3'))
                pygame.mixer.music.play(-1)
            if stage_select.check_for_click():
                selection = stage_select.return_selection()
                if selection["stage"] and selection["difficulty"]:
                    stage_select.reset_selection()
                    map = int(selection["stage"][-1])  
                    difficulty = selection["difficulty"]
                    game_state = 'main_game'
                    main_game_screen = MainGameScreen(window, map, difficulty)
                    main_game_screen.set_health(100)
                    main_game_screen.set_money(500)
                    pygame.mixer.music.stop()

        elif game_state == 'main_game':
            if main_game_screen is not None:
                main_game_screen.render()
                main_game_screen.check_for_click()

                if main_game_screen.return_to_stage_select:
                    game_state = 'stage_select'
                    main_game_screen = None  

                elif main_game_screen.pause:
                    result = main_game_screen.pause_screen()
                    if result == "resume":
                        main_game_screen.pause = False
                    elif result == "stage_select":
                        game_state = 'stage_select'
                        stage_select.selected_stage = None
                        stage_select.selected_difficulty = None 
                        main_game_screen = None  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()