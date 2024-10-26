import time
from enemy import Enemy


class Wave:
    def __init__(self, enemy_data: list, spawn_timer: int):
        self._enemy_data = enemy_data  # Enemy data of current wave
        self._spawn_timer = spawn_timer
        self._enemy_list = []  # Enemies that have been spawned
        self._enemy_number = 0


    def spawn_enemy(self):
        if self._enemy_number < len(self._enemy_list):
            this_enemy = self._enemy_data[self._enemy_number]
            enemy = Enemy(**this_enemy)
            self._enemy_list.append(enemy)
            self._enemy_number += 1
            return enemy
        return None

    def _is_wave_complete(self):
        return self._enemy_number >= len(self._enemy_data) and all(not enemy.is_alive() for enemy in self._enemy_list)


class Wave_Loop:
    def __init__(self, player):
        self._player = player
        self._waves = [] #list of waves
        self._current_wave = 0
        self._time_since_previous_spawn = 0

    def add_wave(self, wave):
        self._waves.append(wave)

    def spawn_wave(self):
        if self._current_wave < len(self._waves):
            wave = self._waves[self._current_wave]
            if not wave._is_wave_complete():
                if self._time_since_previous_spawn >= wave._spawn_timer:
                    wave.spawn_enemy()
                    self._time_since_previous_spawn = 0
            else:
                print(f"Wave {self._current_wave + 1} completed")
                self._current_wave += 1

    def update(self, d_time):
        self._time_since_previous_spawn += d_time
        if self._current_wave < len(self._waves):
            self.spawn_wave()
        current_wave = self._waves[self._current_wave] if self._current_wave < len(self._waves) else None
        if current_wave:
            for enemy in current_wave._enemy_list:
                if enemy.is_alive():
                    enemy._move()
                    if enemy._path_index >= (len(enemy._path) - 1) and enemy.is_alive():
                        enemy.damage_base(self._player)
                        print(f"Player base health: {self._player.health}")
                    if enemy._health <= 0:
                        enemy.kill_enemy(self._player)

    def get_wave_index(self):
        return self._current_wave

    def get_waves(self):
        return self._waves


