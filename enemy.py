import pygame.draw, os
"""pygame.draw used to more easily render enemies"""


class Enemy:
    """Class that handles the creation of enemies"""
    def __init__(self, e_type,  path):
        self._type = e_type
        """The type of enemy, to be used at a later date for different kinds of enemies"""
        if e_type == 'circle':
            self._speed = 1
            self._strength = 1
            self._health = 50
            self._max_health = self._health
            self._image = pygame.image.load(os.path.join("game_assests", "circle_ENEMY.png"))

        if e_type == 'triangle':
            self._speed = 5
            self._strength = 1
            self._health = 50
            self._max_health = self._health
            self._image = pygame.image.load(os.path.join("game_assests", "Triangle Enemy.png"))

        if e_type == 'rectangle':
            self._speed = 0.5
            self._strength = 5
            self._health = 200
            self._max_health = self._health
            self._image = pygame.image.load(os.path.join("game_assests", "Rectangle_Enemy.png"))

        if e_type == 'ghost':
            self._speed = 1
            self._strength = 20
            self._health = 1000
            self._max_health = self._health
            self._image = pygame.image.load(os.path.join("game_assests", "Ghost-Enemy.png"))

        self._path = path
        """The path the enemy is supposed to follow"""
        self._position = self._path[0]
        """Initially set at the starting point on the path"""
        self._path_index = 0
        self._status = True
        """Means the enemy is alive"""
        self._resource_worth = self._health

    def _move(self):
        """Function to move the enemy"""
        if self._path_index < len(self._path) - 1:
            """Checks to see if the enemy has anywhere else to go."""
            target_x, target_y = self._path[self._path_index]
            """Finds the target x and y"""
            dir_x, dir_y = target_x - self._position[0], target_y - self._position[1]
            """Sets the direction to go"""
            distance = (dir_x ** 2 + dir_y ** 2) ** 0.5
            """Helps adjust distance and move based on speed stat"""
            if distance < self._speed:
                self._position = (target_x, target_y)
                self._path_index += 1
                """Move to the next point"""
            else:
                self._position = (
                    self._position[0] + dir_x / distance * self._speed,
                    self._position[1] + dir_y / distance * self._speed,
                )

    def take_damage(self, damage):
        """Takes damage and calls kill_enemy if health hits zero"""
        self._health = self._health - damage
        if self.get_enemy_health() <= 0:
            self.kill_enemy()

    def kill_enemy(self):
        """Kills the enemy and calls reward_resources"""
        self._status = False

    def reward_resources(self, base):
        """Gives player resources based on how much the enemy is worth"""
        base.add_money(self._resource_worth)

    def damage_base(self, base):
        """Damages the base and removes the enemy"""
        base.remove_health(self.get_enemy_strength())
        self._status = False

    def is_alive(self):
        """Returns the enemy status"""
        return self._status

    def get_enemy_type(self):
        """Returns the enemy type"""
        return self._type

    def get_enemy_health(self):
        """Returns the enemy's health"""
        return self._health

    def get_enemy_speed(self):
        """Returns the enemy's speed"""
        return self._speed

    def get_enemy_strength(self):
        """Returns the enemy's strength"""
        return self._strength

    def render(self, window):
        """Renders the enemy, currently as a circle. Plan to render as different shapes based on enemy type"""
        x, y = int(self._position[0]), int(self._position[1])
        window.blit(self._image, (x - self._image.get_width() // 2, y - self._image.get_height() // 2))
        self._draw_health_bar(window)

    def _draw_health_bar(self, window):
        """Creates a visual for the player to know the status of the enemy's health"""
        health_ratio = self._health / self._max_health
        """Finds ratio of health"""
        green = int(255 * health_ratio)
        red = 255 - green
        pygame.draw.rect(window, (red, green, 0),
                         (self._position[0] - 15, self._position[1] - 20, 30 * health_ratio, 5))