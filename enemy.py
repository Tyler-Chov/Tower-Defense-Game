class Enemy:
    def __init__(self, health, speed, strength, path):
        self._health = health
        self._speed = speed
        self._strength = strength
        self._path = path
        self._position = self._path[0]
        self._path_index = 0
        self._status = True
        self._resource_worth = health * 3

    def _move(self):
        if self._path_index < len(self._path) - 1:
            _current_x, _current_y = self._position
            _next_x, _next_y = self._path[self._path_index + 1]
            # Calculate direction to the next point
            _direction_x = _next_x - _current_x
            _direction_y = _next_y - _current_y
            # Normalize direction and scale by speed
            _distance = (_direction_x ** 2 + _direction_y ** 2) ** 0.5
            if _distance != 0:
                _direction_x /= _distance
                _direction_y /= _distance
            # Move the enemy by speed units in the direction of the next point
            _new_x = _current_x + _direction_x * self._speed
            _new_y = _current_y + _direction_y * self._speed
            # Update position
            self._position = (_new_x, _new_y)
            # Check if the enemy has reached the next point
            if _distance <= self._speed:
                self._path_index += 1  # Move to the next point on the path
        else:
            # Reached the end of the path
            self.damage_base(self._strength)

    def take_damage(self, damage, player):
        self._health = self._health - damage
        if self._health <= 0:
            self.kill_enemy(player)

    def kill_enemy(self, base):
        self._status = False
        self.reward_resources(base)

    def reward_resources(self, base):
        base.add_money(self._resource_worth)

    def damage_base(self, base):
        base.remove_health(self._strength)
        self._status = False

    def is_alive(self):
        return self._status


path = ()  # placeholder for path, will be pulled from main class
_circle = Enemy(1, 2, 1, path)
_square = Enemy(3, 1, 2, path)
_triangle = Enemy(2, 4, 1, path)

