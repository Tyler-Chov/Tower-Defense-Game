class Enemy:
    def __init__(self, health, speed, strength, path):
        self.health = health
        self.speed = speed
        self.strength = strength
        self.path = path
        self.position = self.path[0]
        self.path_index = 0
        self.status = True
        self.resource_worth = strength * 3

    def move(self):
        if self.path_index < len(self.path) - 1:
            current_x, current_y = self.position
            next_x, next_y = self.path[self.path_index + 1]
            # Calculate direction to the next point
            direction_x = next_x - current_x
            direction_y = next_y - current_y
            # Normalize direction and scale by speed
            distance = (direction_x ** 2 + direction_y ** 2) ** 0.5
            if distance != 0:
                direction_x /= distance
                direction_y /= distance
            # Move the enemy by speed units in the direction of the next point
            new_x = current_x + direction_x * self.speed
            new_y = current_y + direction_y * self.speed
            # Update position
            self.position = (new_x, new_y)
            # Check if the enemy has reached the next point
            if distance <= self.speed:
                self.path_index += 1  # Move to the next point on the path
        else:
            # Reached the end of the path
            self.damage_base(self.strength)

    def take_damage(self, damage, player):
        self.health = self.health - damage
        if self.health <= 0:
            self.kill_enemy(player)

    def kill_enemy(self, player):
        self.status = False
        self.reward_resources(player)

    def reward_resources(self, player):
        player.resources = player.resources + self.resource_worth

    def damage_base(self, base):
        base.health = base.health - self.strength
        self.status = False
        base.check_base()

    def is_alive(self):
        return self.status

