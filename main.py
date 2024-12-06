import pygame
import sys
import os
import pygame_widgets
import random
from tower import Archer_Tower, cannon_tower, slingshot_tower, normal_tower
from enemy import Enemy
from waves import Wave
from projectile import Projectile
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

# Define colours
bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 180, 0)
grey = (100, 100, 100)


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
    render(): Renders the start screen with the background, title, and
    start button.
    check_for_click(): Checks for mouse click events and returns True if the
    start button is clicked.
    """
    def __init__(self, window):
        """
        Initializes the main game window and loads the start screen assets.
        Args:
            window: The window surface where the start screen will be rendered.
        """
        self.window = window
        self.background = pygame.image.load(os.path.join('game_assests',
                                                         'Start_Screen.png'))
        self.background = pygame.transform.scale(self.background,
                                                 (window_width, window_height))
        self.font = pygame.font.SysFont(None, 55)
        self.start_button_rect = pygame.Rect(310, 444, 180, 46)

    def render(self):
        """
        Renders the start screen with the background, title, and start button.
        """
        self.window.blit(self.background, (0, 0))
        pygame.display.update()

    def check_for_click(self):
        """
        Checks for mouse click events and returns True if the start button
        is clicked.

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
        self.background = pygame.image.load(os.path.join('game_assests',
                                                         'Stage_Select1.png'))
        self.background = pygame.transform.scale(self.background,
                                                 (window_width, window_height))
        self.font = pygame.font.SysFont(None, 55)
        self.stage_selection = "stage1"
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

        self.click_sound = pygame.mixer.Sound(
            os.path.join('game_assests/sounds', 'click.mp3'))
        self.music = pygame.mixer.music.load(
            os.path.join('game_assests/sounds', 'stage_selection_music.mp3'))

    def render(self):
        if self.stage_selection == "stage1":
            self.background = pygame.image.load(
                os.path.join('game_assests', 'Stage_Select1.png'))
            self.background = pygame.transform.scale(
                self.background, (window_width, window_height))
        elif self.stage_selection == "stage2":
            self.background = pygame.image.load(
                os.path.join('game_assests', 'Stage_Select2.png'))
            self.background = pygame.transform.scale(
                self.background, (window_width, window_height))
        elif self.stage_selection == "stage3":
            self.background = pygame.image.load(
                os.path.join('game_assests', 'Stage_Select3.png'))
            self.background = pygame.transform.scale(
                self.background, (window_width, window_height))

        self.window.blit(self.background, (0, 0))
        if (self.hovered_stage == "stage1"
                or self.stage_selection == "stage1"):
            self._draw_overlay(self.stage1_button_rect)
        if (self.hovered_stage == "stage2"
                or self.stage_selection == "stage2"):
            self._draw_overlay(self.stage2_button_rect)
        if (self.hovered_stage == "stage3"
                or self.stage_selection == "stage3"):
            self._draw_overlay(self.stage3_button_rect)
        if (self.hovered_difficulty == "easy"
                or self.difficulty_selection == "easy"):
            self._draw_overlay(self.easy_button_rect)
        if (self.hovered_difficulty == "medium"
                or self.difficulty_selection == "medium"):
            self._draw_overlay(self.medium_button_rect)
        if (self.hovered_difficulty == "hard"
                or self.difficulty_selection == "hard"):
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
        overlay.set_alpha(150)
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
    """The game screen which shows the map and handles the generation of
    enemies, towers, and player stats."""
    def __init__(self, window, map, difficulty):
        self.window = window
        """The window for the game."""
        """Scales the image in self.background appropriately and
        then saves it back to self.background."""
        self.font = pygame.font.Font(os.path.join(
            'game_assests', 'EXEPixelPerfect.ttf'), 22)
        """Sets the font style to be used."""
        self.health = 0
        """Holds the amount of health the player has remaining."""
        self.health_text = self.font.render(
            f'Health: {self.health}', True, (255, 255, 255))
        """Renders the health text so the player knows how much
        health they have remaining."""
        self.money = 0
        """Holds the amount of money the player has"""
        self.money_text = self.font.render(
            f'Money: {int(self.money)}', True, (255, 255, 255))
        """Renders the money text so the player knows how much money
        they have remaining."""

        # Wave Pause button
        wave_pause_img = pygame.image.load(
            os.path.join('game_assests', 'Play-Pause.png')).convert_alpha()
        """The image of the pause button."""

        self.game_pause_img = pygame.image.load(os.path.join('game_assests',
                                                             'pause.png'))
        self.game_pause_img = pygame.transform.scale(
            self.game_pause_img, (30, 30))
        self.wave_pause = True
        self.pause = False
        """Sets pause to True when initially ran."""
        self.map = map
        self.return_to_stage_select = False
        self.projectiles = []
        self.explosions = []
        self.background_color = grey
        self.music = None
        # Map Variables
        if self.map == 1:
            self.background = pygame.image.load(os.path.join('game_assests',
                                                             'map_one.png'))
            """Loads the image."""
            self.music = pygame.mixer.music.load(os.path.join(
                'game_assests/sounds', 'Stage_One_Song.mp3'))
            self.background = pygame.transform.scale(
                self.background, (window_width - 100, window_height - 100))
            self.map_path = ((0, 274), (128, 274), (128, 118), (296, 118),
                             (296, 328), (522, 328), (522, 222), (700, 222),
                             (800, 222))
            """Sets the path for enemies to traverse."""
            self.collision_rects = [(0, 254, 128, 40), (108, 124, 40, 150),
                                    (128, 104, 166, 40), (274, 124, 40, 204),
                                    (294, 308, 228, 40), (502, 226, 40, 102),
                                    (522, 206, 178, 40), (700, 206, 100, 40)]
            """Sets up some collision spots, where the towers cannot be placed.
            ie. the enemy path)"""

            self.background_color = (146, 114, 86)
            self.box_color = (166, 134, 106)
            self.selected_box_color = (126, 94, 66)
            """sets up the colors for the menu"""

        elif map == 2:
            self.background = pygame.image.load(
                os.path.join('game_assests', 'map_two.png'))
            self.music = pygame.mixer.music.load(
                os.path.join('game_assests/sounds', 'Stage_Two_Song.mp3'))
            self.background = pygame.transform.scale(
                self.background, (window_width - 100, window_height - 100))
            self.map_path = ((84, 0), (84, 184), (360, 184), (360, 346),
                             (84, 346), (84, 454), (530, 454), (530, 134),
                             (750, 134), (800, 134))
            self.collision_rects = [(64, 0, 40, 184), (84, 164, 276, 40),
                                    (340, 184, 40, 162), (84, 326, 276, 40),
                                    (64, 346, 40, 108), (84, 434, 446, 40),
                                    (510, 134, 40, 320), (530, 114, 220, 40),
                                    (750, 114, 50, 40)]
            self.background_color = (122, 155, 199)
            self.box_color = (142, 175, 219)
            self.selected_box_color = (102, 135, 179)

        elif map == 3:
            self.music = pygame.mixer.music.load(
                os.path.join('game_assests/sounds', 'Stage_Three_Song.mp3'))
            self.background = pygame.image.load(
                os.path.join('game_assests', 'map_three.png'))
            self.background = pygame.transform.scale(
                self.background, (window_width - 100, window_height - 100))
            self.map_path = ((0, 398), (364, 398), (364, 134), (88, 134),
                             (88, 242), (530, 242), (530, 396), (644, 396),
                             (644, 184), (750, 184), (800, 184))
            self.collision_rects = [(0, 378, 364, 40), (344, 134, 40, 264),
                                    (88, 114, 276, 40), (68, 134, 40, 108),
                                    (80, 220, 470, 40), (510, 244, 40, 152),
                                    (530, 376, 114, 40), (644, 164, 106, 40),
                                    (750, 164, 50, 40)]

            self.background_color = (156, 114, 86)
            self.box_color = (176, 134, 106)
            self.selected_box_color = (136, 94, 66)
            """sets up the colors for the menu"""

        self.wave_pause_button = text_button.Button(
            712, 510, 75, 75, "Pause", self.box_color, window)
        self.wave_play_button = text_button.Button(
            712, 510, 75, 75, "Play", self.box_color, window)
        """Makes the pause button a button to be clicked, using the image
        stored in pause_img."""

        # Tower Variables
        self.grid_active = False
        """Used to show the grid"""
        self.grid_size = 14
        """Determines the grid size."""
        self.tower_size = 3
        """Determines the tower size"""
        self.selected_tower = None
        self.selected_tower_type = None
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
        self.wave_text = self.font.render(
            f'Wave: {self.wave}', True, (255, 255, 255))
        """Renders the current wave number."""

        for wave_number in range(1, 60):
            """Loop for generating waves, changes are planned to further
            improve."""
            enemy_count = 3 * wave_number
            if wave_number <= 10:
                types_of_enemy = [{'type': 'circle', 'weight': 1,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'triangle', 'weight': 0,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'rectangle', 'weight': 0,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'ghost', 'weight': 0,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty}]
            elif wave_number <= 20:
                types_of_enemy = [{'type': 'circle', 'weight': 0.9,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'triangle', 'weight': 0.1,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'rectangle', 'weight': 0,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'ghost', 'weight': 0,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty}]
            elif wave_number < 30:
                types_of_enemy = [{'type': 'circle', 'weight': 0.6,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'triangle', 'weight': 0.1,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'rectangle', 'weight': 0.3,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'ghost', 'weight': 0,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty}]
            elif wave_number == 30:
                types_of_enemy = [{'type': 'circle', 'weight': 0,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'triangle', 'weight': 0,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'rectangle', 'weight': 1,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'ghost', 'weight': 0,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty}]
            elif wave_number < 60:
                types_of_enemy = [{'type': 'circle', 'weight': 0.4,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'triangle', 'weight': 0.2,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'rectangle', 'weight': 0.4,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'ghost', 'weight': 0,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty}]
            elif wave_number == 60:
                types_of_enemy = [{'type': 'circle', 'weight': 0.3,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'triangle', 'weight': 0.2,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'rectangle', 'weight': 0.4,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty},
                                  {'type': 'ghost', 'weight': 0.1,
                                   'path': self.map_path,
                                   'difficulty': self.difficulty}]
            """Determines amount of enemies to be spawned, dependent on
            wave number."""
            wave_data = []
            for enemy_type in types_of_enemy:
                count = int(enemy_count * enemy_type["weight"])
                for _ in range(count):
                    wave_data.append(
                        Enemy(enemy_type["type"], enemy_type["path"],
                              enemy_type["difficulty"])
                    )
            random.shuffle(wave_data)
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
        side_bar = Rectangle(
            (window_width - 100), 0, 100, window_height, self.background_color)
        """Menu on the right side, shows player stats and towers that can
        be used."""
        bottom_bar = Rectangle(
            0, (window_height - 100), window_width, 100, self.background_color)
        """Menu on the bottom, currently hold nothing."""

        box_unselected_color = self.box_color

        tower_boxes = [
            Rectangle(705, 100, 90, 90, box_unselected_color),
            Rectangle(705, 200, 90, 90, box_unselected_color),
            Rectangle(705, 300, 90, 90, box_unselected_color),
            Rectangle(705, 400, 90, 90, box_unselected_color)
        ]
        """Makes the rectangles for the tower boxes."""

        health_box = Rectangle(5, 505, 680, 90, self.background_color)
        """Makes the rectangles for the health bar/box"""

        upgrade_boxes = [
            Rectangle(5, 505, 190, 90, self.box_color),
            Rectangle(200, 505, 195, 90, self.box_color),
            Rectangle(400, 505, 195, 90, self.box_color),
            Rectangle(600, 505, 100, 90, self.box_color)
        ]
        """Makes the rectangles for the upgrade butons."""

        normal_tower_image = pygame.image.load(
            os.path.join("game_assests", "Basic_Tower.png"))
        """Loads tower image."""
        normal_towertower_image = pygame.transform.scale(
            normal_tower_image, (90, 90))
        """Scales tower image."""
        Archer_Tower_image = pygame.image.load(
            os.path.join("game_assests", "Archer_Tower.png"))
        Archer_Tower_image = pygame.transform.scale(
            Archer_Tower_image, (90, 90))

        slingshot_tower_image = pygame.image.load(
            os.path.join("game_assests", "Slingshot_Tower.png"))
        slingshot_tower_image = pygame.transform.scale(
            slingshot_tower_image, (90, 90))

        cannon_tower_image = pygame.image.load(
            os.path.join("game_assests", "Cannon_Tower.png"))
        cannon_tower_image = pygame.transform.scale(
            cannon_tower_image, (90, 90))

        if self.grid_active:
            """Checks if grid is currently active, then renders a preview of
            the tower selected."""
            self.render_tower_preview()

        bottom_bar.draw()

        if self.selected_tower:
            """Renders the attack radius and upgrade options of the
              selected tower."""
            self.draw_radius(self.selected_tower._position,
                             self.selected_tower.get_range(),
                             (128, 128, 128, 100))
            for box in upgrade_boxes:
                box.draw()

            upgrade_damage_button = text_button.Button(
                210, 540, 180, 50,
                (f"Upgrade for: ${int(self.selected_tower._upgrade_cost)}"),
                green, window)
            upgrade_cooldown_button = text_button.Button(
                410, 540, 180, 50,
                (f"Upgrade for: ${int(self.selected_tower._upgrade_cost)}"),
                green, window)
            sell_button = text_button.Button(
                605, 540, 90, 50, (f"Sell"), red, window)
            """creates the buttons for the tower"""

            image = self.selected_tower._image
            width = image.get_width()
            height = image.get_height()
            scale = 1.5
            self.image = pygame.transform.scale(
                image, (int(width * scale), int(height * scale) - 15))
            """creates an image to display in the menu to show the selected
            tower"""

            self.name_text = self.font.render(
                f"{self.selected_tower._name}", True, (255, 255, 255))
            self.enemys_defeated_text = self.font.render(
                f"Enemies Defeated: {self.selected_tower._enemies_defeated}",
                True, (255, 255, 255))
            self.sell_price_text = self.font.render(
                f"Sell Price: {self.selected_tower._sell_price}", True,
                (255, 255, 255))
            self.attack_damage_text = self.font.render(
                f"Attack Damage: {self.selected_tower._damage}", True,
                (255, 255, 255))
            self.attack_cooldown_text = self.font.render(
                f"Attack Cooldown: {self.selected_tower._shot_cooldown}", True,
                (255, 255, 255))
            self.window.blit(self.attack_damage_text, (210, 510))
            self.window.blit(self.attack_cooldown_text, (410, 510))
            self.window.blit(self.name_text, (10, 510))
            self.window.blit(self.image, (10, 520))
            self.window.blit(self.enemys_defeated_text, (10, 580))
            self.window.blit(self.sell_price_text, (605, 510))
            """creates and display text regarding the towers stats, upgrades,
            and sell prices."""

            if upgrade_damage_button.draw_button():
                if self.money >= self.selected_tower._upgrade_cost:
                    self.selected_tower._damage = int(
                        self.selected_tower._damage + 5)
                    self.remove_money(self.selected_tower._upgrade_cost)
            """upgrades damage and updates variables when button is pressed"""

            if upgrade_cooldown_button.draw_button():
                if self.money >= (int(self.selected_tower._upgrade_cost)):
                    self.selected_tower._shot_cooldown = int(
                        self.selected_tower._shot_cooldown * .75)
                    self.remove_money(int(self.selected_tower._upgrade_cost))
            """upgrades cooldown and updates variables when button is
            pressed"""

            if sell_button.draw_button():
                self.add_money(self.selected_tower._sell_price)
                self.selected_tower.sell_tower
                # TODO - add logic for removing towers
                self.placed_towers.remove(self.selected_tower)
                self.selected_tower._position = (900, 900)
                self.selected_tower = None
            """sells tower and updates variables when pressed"""

        else:
            health_box.draw()
            """draws an empty gray box when no tower is selected"""

        self.tower1_price = self.font.render(f'$200', True, (255, 255, 255))
        self.archer_price = self.font.render(f'$150', True, (255, 255, 255))
        self.slingshot_price = self.font.render(f'$500', True, (255, 255, 255))
        self.cannon_price = self.font.render(f'$300', True, (255, 255, 255))
        """Renders the price of the towers."""

        for tower in self.placed_towers:
            """Renders each placed tower."""
            tower.render(self.window)

        for enemy in self._enemy_list:
            enemy.render(self.window)

        if self.debug:
            """When debug is true, updates the game and renders various
            aspects."""
            self.update_cursor_position()
            self.draw_enemy_path()
            self.render_collision_rects()
            '''
            for tower in self.placed_towers:
                print(tower._position)
            '''
        if not self.wave_pause:

            self.update_waves()
            for enemy in self._enemy_list:
                """For each active enemy, the enemy will move along the set
                path towards the player base."""
                if enemy.is_alive():
                    enemy._move()
                    if enemy._path_index >= len(enemy._path) - 1:
                        enemy.damage_base(self)
                        self.remove_health(enemy._strength)
                        self.remove_money(enemy._resource_worth)
            self.update_attacks()

        for projectile in self.projectiles[:]:
            if projectile.is_active():
                projectile.move()
                projectile.render(self.window)
            else:
                projectile.apply_splash_damage(self._enemy_list,
                                               self.explosions)
                self.projectiles.remove(projectile)

        for explosion in self.explosions[:]:
            if explosion.is_active():
                explosion.update()
                explosion.render(self.window)
            else:
                self.explosions.remove(explosion)

        # Display menu and UI
        side_bar.draw()
        mouse_pos = pygame.mouse.get_pos()
        for box in tower_boxes:
            if box.is_hovered(mouse_pos):
                box.color = self.selected_box_color
            else:
                box.color = box_unselected_color
        for box in tower_boxes:
            """Draws each box in the tower_boxes list."""
            box.draw()

        self.window.blit(normal_tower_image, (717, 105))
        self.window.blit(Archer_Tower_image, (705, 195))
        self.window.blit(slingshot_tower_image, (705, 295))
        self.window.blit(cannon_tower_image, (710, 395))
        self.window.blit(self.health_text, (705, 10))
        self.window.blit(self.money_text, (705, 40))
        self.window.blit(self.wave_text, (705, 70))
        self.window.blit(self.tower1_price, (734, 167))
        self.window.blit(self.archer_price, (734, 267))
        self.window.blit(self.cannon_price, (734, 467))
        self.window.blit(self.slingshot_price, (734, 367))
        if self.wave_pause is False:
            self.wave_pause_button.draw_button()
        else:
            self.wave_play_button.draw_button()
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
                for i, box in enumerate(tower_boxes):
                    if box.collidepoint(mouse_pos):
                        self.grid_active = not self.grid_active
                        self.selected_tower_type = i
                        return
                if self.grid_active:
                    self.place_tower(mouse_pos)
                    return

                # selecting towers.
                tower_clicked = False
                bottom_bar = pygame.rect.Rect(0, (window_height - 100),
                                              window_width, 100)
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
                    if not bottom_bar.collidepoint(mouse_pos):
                        self.selected_tower = None

                # Wave Pause button functionality
                wave_pause_button = pygame.Rect(710, 510, 75, 75)
                if wave_pause_button.collidepoint(mouse_pos):
                    if self.wave_pause is True:
                        self.wave_pause = False
                    elif self.wave_pause is False:
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

            # Debug toggle button.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.debug is True:
                        self.debug = False
                    else:
                        self.debug = True
                    return

                if event.key == pygame.K_o:
                    self.add_money(1000)
                    return

    def draw_radius(self, center, radius, color):
        range_surface = pygame.Surface((radius * 2, radius * 2),
                                       pygame.SRCALPHA)
        range_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(
            range_surface, color, (radius, radius), radius
        )
        top_left = (center[0] - radius, center[1] - radius)
        self.window.blit(range_surface, top_left)

    def render_tower_preview(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.selected_tower_type == 0:
            temp_tower = normal_tower()
        elif self.selected_tower_type == 1:
            temp_tower = Archer_Tower()
        elif self.selected_tower_type == 2:
            temp_tower = slingshot_tower()
        elif self.selected_tower_type == 3:
            temp_tower = cannon_tower()
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
            (mouse_x - tower_surface.get_width() // 2, mouse_y -
             tower_surface.get_height() // 2)
        )

    def place_tower(self, mouse_pos):
        if not self.check_collision(mouse_pos[0], mouse_pos[1]):
            if self.selected_tower_type == 0:
                new_tower = normal_tower()
            elif self.selected_tower_type == 1:
                new_tower = Archer_Tower()
            elif self.selected_tower_type == 2:
                new_tower = slingshot_tower()
            elif self.selected_tower_type == 3:
                new_tower = cannon_tower()
            new_tower.update_volume(sound_volume)

            if self.money >= new_tower.get_price():
                new_tower.place(mouse_pos)
                self.placed_towers.append(new_tower)
                self.grid_active = False
                self.remove_money(new_tower.get_price())
            else:
                self.grid_active = False
                self.selected_tower = False
                return
        else:
            pass

        """def remove_tower(self):
            self.paced_towers.remove(tower)
            self.tower._position = None"""

    def check_collision(self, x, y):
        preview_size = self.grid_size * self.tower_size

        preview_rect = pygame.Rect(
            x - preview_size // 2, y - preview_size // 2, preview_size,
            preview_size
        )

        for tower in self.placed_towers:
            tower_size = int(self.grid_size * self.tower_size * 0.8)
            tower_rect = pygame.Rect(
                tower._position[0] - tower_size // 2,
                tower._position[1] - tower_size // 2,
                tower_size, tower_size
            )
            if preview_rect.colliderect(tower_rect):
                return True

        for rect in self.collision_rects:
            if preview_rect.colliderect(rect):
                return True
        bottom_bar = pygame.Rect(0, window_height - 100, window_width, 100)
        side_bar = pygame.Rect(window_width - 100, 0, 100, window_height)

        if (preview_rect.colliderect(bottom_bar) or preview_rect.colliderect(
                side_bar)):
            return True
        return False

    def update_attacks(self):
        for tower in self.placed_towers:
            tower.attack(self._enemy_list, self.projectiles)
        for enemy in self._enemy_list:
            if not enemy.is_alive():
                self.add_money(enemy._resource_worth)
                self._enemy_list.remove(enemy)

    def update_waves(self):
        """Checks if the current wave is complete, moves on to the next wave
        prepared once it is."""
        if self._current_wave < len(self._waves):
            current_wave = self._waves[self._current_wave]
            if current_wave._is_wave_complete():
                self._current_wave += 1
                if self._current_wave < len(self._waves):
                    self.wave += 1
                    self.wave_text = self.font.render(f"Wave: {self.wave}",
                                                      True, (255, 255, 255))
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

        font = pygame.font.Font(
            os.path.join('game_assests', 'EXEPixelPerfect.ttf'), 40)
        label_font = pygame.font.Font(
            os.path.join('game_assests', 'EXEPixelPerfect.ttf'), 30)
        setting_text = pygame.font.Font(
            os.path.join('game_assests', 'EXEPixelPerfect.ttf'), 60)

        bgm_slider = Slider(self.window, window_width // 2 - 100, window_height
                            // 2 - 50, 200, 20, min=0, max=10, step=1)
        bgm_slider.setValue(int(bgm_volume * 10))
        sfx_slider = Slider(self.window, window_width // 2 - 100, window_height
                            // 2 + 50, 200, 20, min=0, max=10, step=1)
        sfx_slider.setValue(int(sound_volume * 10))

        bgm_label = label_font.render("BGM", True, (255, 255, 255))
        bgm_label_rect = bgm_label.get_rect(center=(window_width // 2,
                                                    window_height // 2 - 80))
        sfx_label = label_font.render("SFX", True, (255, 255, 255))
        sfx_label_rect = sfx_label.get_rect(center=(window_width // 2,
                                                    window_height // 2 + 20))
        back_button_rect = pygame.Rect(window_width // 2 - 100,
                                       window_height - 100, 200, 50)
        back_text = font.render("Back", True, (255, 255, 255))
        setting_text = setting_text.render("Settings", True, (255, 255, 255))
        setting_text_rect = setting_text.get_rect(
            center=(window_width // 2, 120))

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if back_button_rect.collidepoint(mouse_pos):
                            running = False

            pygame_widgets.update(events)
            bgm_value = bgm_slider.getValue() / 10.0
            sfx_value = sfx_slider.getValue() / 10.0
            bgm_volume = bgm_value
            sound_volume = sfx_value
            pygame.mixer.music.set_volume(bgm_volume)

            # Update the volume of all towers
            for tower in self.placed_towers:
                tower.update_volume(sound_volume)

            self.window.fill((30, 30, 30))
            self.window.blit(overlay, (0, 0))
            pygame.draw.rect(self.window, (100, 100, 100), back_button_rect)
            self.window.blit(back_text, (back_button_rect.centerx - back_text.
                                         get_width() // 2,
                                         back_button_rect.centery -
                                         back_text.get_height() // 2))
            self.window.blit(bgm_label, bgm_label_rect)
            self.window.blit(sfx_label, sfx_label_rect)
            self.window.blit(setting_text, setting_text_rect)
            bgm_slider.draw()
            sfx_slider.draw()
            pygame.display.flip()

    def pause_screen(self):
        paused = True
        game_snapshot = self.window.copy()
        overlay = pygame.Surface((window_width, window_height),
                                 pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        font = pygame.font.Font(os.path.join('game_assests',
                                             'EXEPixelPerfect.ttf'), 35)
        pause_font = pygame.font.Font(os.path.join('game_assests',
                                                   'EXEPixelPerfect.ttf'), 80)
        pause_text = pause_font.render("Paused", True, (255, 255, 255))

        button_width, button_height = 200, 50
        resume_button_rect = pygame.Rect(window_width // 2 - button_width // 2,
                                         220, button_width, button_height)
        stage_select_button_rect = pygame.Rect(window_width // 2 - button_width
                                               // 2, 290, button_width,
                                               button_height)
        setting_button_rect = pygame.Rect(window_width // 2 - button_width
                                          // 2, 360, button_width,
                                          button_height)
        quit_button_rect = pygame.Rect(window_width // 2 - button_width // 2,
                                       430, button_width, button_height)

        resume_text = font.render("Resume", True, (255, 255, 255))
        stage_select_text = font.render("Stage Select", True, (255, 255, 255))
        setting_text = font.render("Settings", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        while paused:
            self.window.blit(game_snapshot, (0, 0))
            self.window.blit(overlay, (0, 0))
            self.window.blit(pause_text, (window_width // 2 -
                                          pause_text.get_width() // 2, 100))
            cursor_pos = pygame.mouse.get_pos()
            for button_rect, text, color in [
                (resume_button_rect, resume_text, (100, 100, 100) if
                 resume_button_rect.collidepoint(cursor_pos)
                 else (150, 150, 150)),
                (stage_select_button_rect, stage_select_text, (100, 100, 100)
                 if stage_select_button_rect.collidepoint(cursor_pos)
                 else (150, 150, 150)),
                (setting_button_rect, setting_text, (100, 100, 100)
                 if setting_button_rect.collidepoint(cursor_pos)
                 else (150, 150, 150)),
                (quit_button_rect, quit_text, (100, 100, 100)
                 if quit_button_rect.collidepoint(cursor_pos)
                 else (150, 150, 150)),
            ]:
                pygame.draw.rect(self.window, color, button_rect)
                self.window.blit(text, (button_rect.centerx - text.get_width()
                                        // 2, button_rect.centery -
                                        text.get_height() // 2))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif (event.type == pygame.MOUSEBUTTONDOWN
                      and event.button == 1):
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

        self.pause = False
        self.wave_pause = False

    def remove_health(self, health):
        self.health -= health
        self.health_text = self.font.render(f'Health: {self.health}',
                                            True, (255, 255, 255))
        if self.health <= 0:
            self.game_over()

    def add_money(self, money):
        self.money += int(money)
        self.money_text = self.font.render(f'Money: {self.money}',
                                           True, (255, 255, 255))

    def remove_money(self, money):
        self.money -= int(money)
        self.money_text = self.font.render(f'Money: {self.money}',
                                           True, (255, 255, 255))

    def set_health(self, health):
        self.health = health
        self.health_text = self.font.render(f'Health: {self.health}',
                                            True, (255, 255, 255))

    def set_money(self, money):
        self.money = money
        self.money_text = self.font.render(f'Money: {self.money}',
                                           True, (255, 255, 255))

    def update_cursor_position(self):
        """Update and render the cursor position."""
        mouse_pos = pygame.mouse.get_pos()
        self.cursor_text = self.font.render(f'Cursor: {mouse_pos}',
                                            True, (255, 255, 255))

        self.window.blit(self.cursor_text, (10, 10))

    def draw_enemy_path(self):
        path_color = (255, 0, 0)
        path_width = 3

        for i in range(len(self.map_path) - 1):
            start_pos = self.map_path[i]
            end_pos = self.map_path[i + 1]
            pygame.draw.line(self.window, path_color, start_pos,
                             end_pos, path_width)

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
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(
                    os.path.join('game_assests/sounds',
                                 'stage_selection_music.mp3'))
                pygame.mixer.music.play(-1)
        elif game_state == 'stage_select':
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(
                    os.path.join('game_assests/sounds',
                                 'stage_selection_music.mp3'))
                pygame.mixer.music.play(-1)
            stage_select.render()
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
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)
                main_game_screen.render()
                main_game_screen.check_for_click()

                if main_game_screen.return_to_stage_select:
                    game_state = 'stage_select'
                    main_game_screen = None
                    pygame.mixer.music.stop()

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
