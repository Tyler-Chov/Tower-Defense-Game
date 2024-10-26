import time
from enemy import Enemy


class Wave:
    def __init__(self, enemy_data: list, spawn_timer: int):
        self._enemy_data = enemy_data  # Enemy data of current wave
        self._spawn_timer = spawn_timer
        self._enemy_list = []  # Enemies that have been spawned
        self._enemy_number = 0

    def spawn_enemy(self):
        if self._enemy_number < len(self._enemy_data):
            this_enemy = self._enemy_data[self._enemy_number]
            self._enemy_list.append(this_enemy)
            self._enemy_number += 1
            return this_enemy
        return None

    def _is_wave_complete(self):
        return self._enemy_number >= len(self._enemy_data) and all(not enemy.is_alive() for enemy in self._enemy_list)
