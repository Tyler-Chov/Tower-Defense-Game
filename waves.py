class Wave:
    """The class used for generating waves"""
    def __init__(self, enemy_data: list, spawn_timer: int):
        self._enemy_data = enemy_data
        """Enemy data of current wave"""
        self._spawn_timer = spawn_timer
        """Time between the spawning of enemies"""
        self._enemy_list = []
        """Enemies that have been spawned"""
        self._enemy_number = 0
        """Tracks which enemy is going to be spawned next"""

    def spawn_enemy(self):
        """Function that spawns enemies"""
        if self._enemy_number < len(self._enemy_data):
            """Checks if there are still more enemies to spawn"""
            this_enemy = self._enemy_data[self._enemy_number]
            self._enemy_list.append(this_enemy)
            """Spawns the next enemy"""
            self._enemy_number += 1
            """Prepares the next enemy to be spawned"""
            return this_enemy
        return None
        """If there are no enemies to spawn, return None"""

    def _is_wave_complete(self):
        """Checks if the wave is complete"""
        return self._enemy_number >= len(self._enemy_data) and all(
            not enemy.is_alive() for enemy in self._enemy_list)
