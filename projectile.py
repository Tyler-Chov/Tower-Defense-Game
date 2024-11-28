import pygame
import os


class Projectile:
    def __init__(self, position, target, speed, damage, image_path="game_assests/projectile.png", AoE_radius = 0, ):
        self._position = list(position)
        self._target = target
        self._speed = speed
        self._damage = damage
        self._active = True
        self._image = image_path
        self._AoE_radius = AoE_radius
        self._size = 32

    def move(self):
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
            self._target.take_damage(self._damage)
        else:  
            self._position[0] += dir_x / distance * self._speed
            self._position[1] += dir_y / distance * self._speed

    def apply_splash_damage(self, enemies):
        if self._AoE_radius > 0:
            px, py = self._position
            for enemy in enemies:
                ex, ey = enemy._position
                distance = ((px - ex) ** 2 + (py - ey) ** 2) ** 0.5
                if distance < self._AoE_radius and enemy.is_alive():
                    enemy.take_damage(int(self._damage * 0.5))

    def render(self, window):
        scaled_image = pygame.transform.scale(self._image, (self._size, self._size))
        window.blit(scaled_image, (self._position[0] - self._size // 2, self._position[1] - self._size // 2))

    def is_active(self):
        return self._active