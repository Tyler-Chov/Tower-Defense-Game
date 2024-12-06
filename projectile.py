import pygame
import os
import math


class Projectile:
    """Class that handles the creation of projectiles"""
    def __init__(self, position, target, speed, damage, size,
                 image_path="game_assests/projectile.png", AoE_radius=0,
                 tower=None):
        """Initializes the projectile with the given parameters

        Args:
            position (tuple): The position of the projectile
            target (Enemy): The target enemy
            speed (int): The speed of the projectile
            damage (int): The damage the projectile deals
            size (int): The size of the projectile
            image_path (str, optional): The path to the image of the
                projectile. Defaults to "game_assests/projectile.png".
        """
        self._position = list(position)
        self._target = target
        self._speed = speed
        self._damage = damage
        self._active = True
        self._original_image = image_path
        self._current_image = self._original_image
        self._scaled_image = pygame.transform.scale(self._original_image,
                                                    (size, size))
        self._AoE_radius = AoE_radius
        self._size = size
        self._explosions = []
        self._tower = tower

    def move(self):
        """Moves the projectile towards the target enemy. If the projectile
        reaches the target, it deals damage to the enemy and deactivates"""

        if not self._target.is_alive():
            self._active = False
            return

        tx, ty = self._target._position
        px, py = self._position
        dir_x, dir_y = tx - px, ty - py
        distance = (dir_x ** 2 + dir_y ** 2) ** 0.5

        if distance < self._speed:
            self._position = [tx, ty]
            self._active = False
            was_alive = self._target.is_alive()
            self._target.take_damage(self._damage)
            if was_alive and not self._target.is_alive():
                self._tower._enemies_defeated += 1
        else:
            self._position[0] += dir_x / distance * self._speed
            self._position[1] += dir_y / distance * self._speed

        angle = math.degrees(math.atan2(-dir_y, dir_x))
        self._current_image = pygame.transform.rotate(self._scaled_image,
                                                      int(angle))

    def apply_splash_damage(self, enemies, explosions_list):
        """Applies splash damage to enemies within the area of effect radius

        Args:
            enemies (list): A list of enemies
            explosions_list (list): A list of explosions
        """
        if self._AoE_radius > 0:
            px, py = self._position
            for enemy in enemies:
                ex, ey = enemy._position
                distance = ((px - ex) ** 2 + (py - ey) ** 2) ** 0.5
                if distance < self._AoE_radius and enemy.is_alive():
                    enemy.take_damage(int(self._damage * 0.5))
            explosion = Explosion((px, py), self._AoE_radius, duration=15)
            explosions_list.append(explosion)

    def render(self, window):
        """Renders the projectile on the game screen.

        Args:
            window (pygame.Surface): The game window
        """
        rotated_rect = self._current_image.get_rect(center=(self._position[0],
                                                            self._position[1]))
        window.blit(self._current_image, rotated_rect.topleft)

    def is_active(self):
        """Returns the status of the projectile

        Returns:
            bool: True if the projectile is active, False otherwise
        """
        return self._active


class Explosion:
    """Class that handles the creation of explosions, explosions are
    purely cosmetic."""
    def __init__(self, position, max_radius, duration):
        """Initializes the explosion with the given parameters

        Args:
            position (tuple): The position of the explosion
            max_radius (int): The maximum radius of the explosion
            duration (int): The duration of the explosion
        """
        self._position = position
        self._max_radius = max_radius
        self._duration = duration
        self._current_frame = 0
        self._active = True

    def update(self):
        """Updates the explosion, deactivates it if the duration is reached"""
        self._current_frame += 1
        if self._current_frame >= self._duration:
            self._active = False

    def render(self, window):
        """Renders the explosion on the game screen.

        Args:
            window (pygame.Surface): The game window
        """
        if self._active:
            current_radius = self._max_radius * (self._current_frame /
                                                 self._duration)
            alpha = int(255 * (1 - self._current_frame / self._duration))
            surface = pygame.Surface((self._max_radius * 2,
                                      self._max_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                surface,
                (255, 100, 0, alpha),
                (self._max_radius, self._max_radius),
                int(current_radius)
            )
            window.blit(
                surface,
                (self._position[0] - self._max_radius, self._position[1] -
                 self._max_radius)
            )

    def is_active(self):
        """Returns the status of the explosion

        Returns:
            bool: True if the explosion is active, False otherwise
        """
        return self._active
