import pygame
import os

class Tower:
    def __init__(self, name: str, damage: int, shot_cooldown: int, price: int, attack_range: int, attack_pattern: int):
        self._name = name
        self._damage = damage

        self._shot_cooldown = shot_cooldown * 60
        self._price = price
        self._sell_price = price * 0.25
        self._attack_range = attack_range
        self._attack_pattern = attack_pattern
        self._position = None
        self._upgrade_level = 1
        self._upgrade_cost = price + (price * 0.5)
        self._enemies_defeated = 0
        self._cooldown_counter = 0
        self._image = pygame.image.load(os.path.join('game_assests', "tower.png"))
        self.size = 28


    def render(self, window):
        if self._position:
            adjusted_x = self._position[0] - (self.size * 3) // 2
            adjusted_y = self._position[1] - (self.size * 3) // 2
            tower_surface = pygame.transform.scale(self._image, (self.size * 3, self.size * 3))
            window.blit(tower_surface, (adjusted_x, adjusted_y))


    def _render_range(self, window):
        range_surface = pygame.Surface((self._attack_range * 2, self._attack_range * 2), pygame.SRCALPHA)
        range_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(
            range_surface,
            (128, 128, 128, 100),
            (self._attack_range, self._attack_range),
            self._attack_range
        )

        adjusted_x = self._position[0] - self._attack_range
        adjusted_y = self._position[1] - self._attack_range
        window.blit(range_surface, (adjusted_x, adjusted_y))


    def place(self, position):
        self._position = position


    def get_name(self):
            return self._name


    def set_name(self, name):
        if name == "":
            raise ValueError("Not a Valid Name")
        else:
            self._name = name


    def get_damage(self):
        return self._damage
    

    def set_damage(self, damage):
        if damage > 0:
            self._damage = damage
        else:
            raise ValueError("Damage must be greater than 0.")
        

    def get_range(self):
        return self._attack_range
    

    def set_attack_range(self, attack_range):
        if attack_range > 0:
            self._attack_range = attack_range
        else:
            raise ValueError("Range must be greater than 0.")
        

    def get_price(self):
        return self._price
    

    def get_sell_price(self):
        return self._sell_price
    

    def get_upgrade_cost(self):
        return self._upgrade_cost
    

    def get_enemies_defeated(self):
        return self._enemies_defeated
    

    def upgrade_tower(self):
        self._upgrade_level += 1
        self._damage += int(self._damage * 0.5)
        self._attack_range += 1
        self._upgrade_cost = int(self._price * (1 + 0.5 * self._upgrade_level))


    def sell_tower(self):
        print(f"{self._name} tower sold for {self._sell_price} credits.")


    def attack(self, enemies):
        if self._cooldown_counter > 0:
            self._cooldown_counter -= 1
            return # tower is still on cooldown.

        for enemy in enemies:
            if self._in_range(enemy):
                enemy.take_damage(self._damage)
                self._cooldown_counter = self._shot_cooldown  
                self._enemies_defeated += 1  
                break 

    
    def _in_range(self, enemy): #calculates if tower is in range
        ex, ey = enemy._position
        tx, ty = self._position
        distance = ((tx - ex) ** 2 + (ty - ey) ** 2) ** 0.5
        return distance <= self._attack_range 
    
    
    def get_stats(self):
        return {
            "Name": self._name,
            "Damage": self._damage,
            "Range": self._attack_range,
            "Cooldown": self._shot_cooldown,
            "Enemies Defeated": self._enemies_defeated,
            "Sell Tower": self._sell_price,
            "Upgrade Cost": self._upgrade_cost
        }
    

tower = Tower("Archer Tower", 50, 3, 100, 5, 1)
print(tower.get_stats())
