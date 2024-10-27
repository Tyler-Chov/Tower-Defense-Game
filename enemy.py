import pygame.draw


class Enemy:
    def __init__(self, e_type, health, speed, strength, path):
        self._type = e_type
        self._health = health
        self._max_health = health
        self._speed = speed
        self._strength = strength
        self._path = path
        self._position = self._path[0]
        self._path_index = 0
        self._status = True  # Means the enemy is alive
        self._resource_worth = health * 3

    def _move(self):
        if self._path_index < len(self._path) - 1:
            target_x, target_y = self._path[self._path_index]
            dir_x, dir_y = target_x - self._position[0], target_y - self._position[1]
            distance = (dir_x ** 2 + dir_y ** 2) ** 0.5
            if distance < self._speed:
                self._position = (target_x, target_y)
                self._path_index += 1  # Move to the next point
            else:
                self._position = (
                    self._position[0] + dir_x / distance * self._speed,
                    self._position[1] + dir_y / distance * self._speed,
                )

    def take_damage(self, damage):
        self._health = self._health - damage
        if self.get_enemy_health() <= 0:
            self.kill_enemy()

    def kill_enemy(self):
        self._status = False

    def reward_resources(self, base):
        base.add_money(self._resource_worth)

    def damage_base(self, base):
        base.remove_health(self.get_enemy_strength())
        self._status = False

    def is_alive(self):
        return self._status

    def get_enemy_type(self):
        return self._type

    def get_enemy_health(self):
        return self._health

    def get_enemy_speed(self):
        return self._speed

    def get_enemy_strength(self):
        return self._strength

    def render(self, window):
        pygame.draw.circle(window, (255, 0, 0),
                           (int(self._position[0]), int(self._position[1])), 10)
        self._draw_health_bar(window)

    def _draw_health_bar(self, window):
        health_ratio = self._health / self._max_health
        green = int(255 * health_ratio)
        red = 255 - green
        pygame.draw.rect(window, (red, green, 0), (self._position[0] - 15, self._position[1] - 20, 30 * health_ratio, 5))