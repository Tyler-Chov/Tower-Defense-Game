import pygame
import os
from abc import ABC
from projectile import Projectile
"""
Tower Class for Defense Tower Game

This file defines a Tower class used in a tower defense game. Each Tower object has attributes 
such as damage, attack range, and cooldown, and methods for attacking enemies, upgrading, 
and displaying itself on the screen.

Attributes:
    - name (str): Name of the tower.
    - damage (int): Damage dealt per attack.
    - shot_cooldown (int): Time (in frames) between attacks.
    - price (int): Cost to build the tower.
    - attack_range (int): Attack range for hitting enemies.
    - attack_pattern (int): Defines the tower's specific attack style.
    - position (tuple): Position of the tower on the screen.
    - upgrade_level (int): Current level of the tower.
    - enemies_defeated (int): Count of enemies defeated by this tower.
"""


class Tower(ABC):
    def __init__(self, name: str, damage: int, shot_cooldown: int, price: int, attack_range: int, attack_pattern: int):
        """Initializes the Tower with its primary attributes."""
        self._name = name
        self._damage = damage
        self._shot_cooldown = shot_cooldown * 60
        self._price = price
        self._sell_price = int(price * 0.25)
        self._attack_range = attack_range
        self._attack_pattern = attack_pattern
        self._position = None
        self._upgrade_level = 1
        self._upgrade_cost = int(price + (price * 0.5))
        self._enemies_defeated = 0
        self._cooldown_counter = 0
        self._image = pygame.image.load(os.path.join('game_assests', "tower.png"))
        self.size = 28
        self.projectile_image = pygame.image.load(os.path.join('game_assests', "projectile.png"))
        self._flipped_image = pygame.transform.flip(self._image, True, False)
        self._is_facing_left = False


    def render(self, window):
        """Draws the tower image on the game window at its position."""
        if self._position:
            adjusted_x = self._position[0] - (self.size * 3) // 2
            adjusted_y = self._position[1] - (self.size * 3) // 2
            current_image = self._flipped_image if self._is_facing_left else self._image
            tower_surface = pygame.transform.scale(current_image, (self.size * 3, self.size * 3))
            window.blit(tower_surface, (adjusted_x, adjusted_y))

    def _render_range(self, window):
        """Displays a circle around the tower to indicate its attack range."""
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
        """Sets the tower's position on the game map."""
        self._position = position

    def get_name(self):
        """Returns the name of the tower."""
        return self._name

    def set_name(self, name):
        """Sets the name of the tower, raising an error if the name is empty."""
        if name == "":
            raise ValueError("Not a Valid Name")
        else:
            self._name = name

    def get_damage(self):
        """Returns the current damage of the tower."""
        return self._damage

    def set_damage(self, damage):
        """Sets the tower's damage, ensuring it is positive."""
        if damage > 0:
            self._damage = damage
        else:
            raise ValueError("Damage must be greater than 0.")

    def get_range(self):
        """Returns the tower's attack range."""
        return self._attack_range

    def set_attack_range(self, attack_range):
        """Sets the tower's attack range, ensuring it is positive."""
        if attack_range > 0:
            self._attack_range = attack_range
        else:
            raise ValueError("Range must be greater than 0.")

    def get_price(self):
        """Returns the initial cost of the tower."""
        return self._price

    def get_sell_price(self):
        """Returns the sell price of the tower."""
        return self._sell_price

    def get_upgrade_cost(self):
        """Returns the cost to upgrade the tower to the next level."""
        return self._upgrade_cost

    def get_enemies_defeated(self):
        """Returns the count of enemies defeated by this tower."""
        return self._enemies_defeated

    def upgrade_tower(self):
        """Upgrades the tower's attributes, increasing damage, range, and upgrade cost."""
        self._upgrade_level += 1
        self._damage += int(self._damage * 0.5)
        self._attack_range += 1
        self._upgrade_cost = int(self._price * (1 + 0.5 * self._upgrade_level))

    def sell_tower(self):
        """Displays a message indicating the tower has been sold."""
        print(f"{self._name} tower sold for {self._sell_price} credits.")

    def attack(self, enemies, projectiles_list):
        """Attacks the first enemy within range if the tower is not on cooldown."""
        if self._cooldown_counter > 0:
            self._cooldown_counter -= 1
            return
        for enemy in enemies:
            if self._in_range(enemy):
                self._is_facing_left = enemy._position[0] < self._position[0]

                projectile = Projectile(
                    position=self._position,
                    target=enemy,
                    speed=10,  
                    damage=self._damage,
                    size = 32,
                    image_path=self.projectile_image
                )
                projectiles_list.append(projectile)
                self._cooldown_counter = self._shot_cooldown
                break

    def _in_range(self, enemy):
        """Calculates if the enemy is within the tower's attack range."""
        ex, ey = enemy._position
        tx, ty = self._position
        distance = ((tx - ex) ** 2 + (ty - ey) ** 2) ** 0.5
        return distance <= self._attack_range

    def get_stats(self):
        """Returns a dictionary of the tower's statistics."""
        return {
            "Name": self._name,
            "Damage": self._damage,
            "Range": self._attack_range,
            "Cooldown": self._shot_cooldown,
            "Enemies Defeated": self._enemies_defeated,
            "Sell Tower": self._sell_price,
            "Upgrade Cost": self._upgrade_cost
        }


class normal_tower(Tower):
    def __init__(self):
        """Initializes the Normal Tower with specific attributes."""
        super().__init__(name="Normal Tower", damage=30, shot_cooldown=4, price=200, attack_range=75, attack_pattern=1)
        self._upgrade_level = 1
        self._upgrade_cost = self._price + (self._price * 0.25)
        self._image = pygame.image.load(os.path.join('game_assests', "Basic_Tower.png"))
        self.projectile_image = pygame.image.load(os.path.join('game_assests', "projectile.png"))
        self._flipped_image = pygame.transform.flip(self._image, True, False)
    
class Archer_Tower(Tower):
    def __init__(self):
        """Initializes the Archer Tower with specific attributes."""
        super().__init__(name="Archer Tower", damage=20, shot_cooldown=2, price=150, attack_range=60, attack_pattern=1)
        self._upgrade_level = 1
        self._upgrade_cost = self._price + (self._price * 0.25)
        self._image = pygame.image.load(os.path.join('game_assests', "Archer_Tower.png"))
        self._flipped_image = pygame.transform.flip(self._image, True, False)

    def attack(self, enemies, projectiles_list):
        """Specific implementation for archer_tower's attack logic."""
        if self._cooldown_counter > 0:
            self._cooldown_counter -= 1
            return

        for enemy in enemies:
            if self._in_range(enemy):
                self._is_facing_left = enemy._position[0] < self._position[0]
                projectile = Projectile(
                    position=self._position,
                    target=enemy,
                    speed=10,  
                    damage=self._damage,
                    size = 30,
                    image_path=self.projectile_image
                )
                projectiles_list.append(projectile)
                self._cooldown_counter = self._shot_cooldown
                break

    def upgrade_tower(self):
        """Upgrades the tower's attributes based on the level, elimination requirements, and upgrade cost."""
        if self._upgrade_level == 1 and self._enemies_defeated >= 15:
            if self._upgrade_cost <= self._price:
                print("Level 2 Upgrade Options:")
                print("1. +1 Damage")
                print("2. +1 Range")
                choice = input("Choose your upgrade (1 or 2): ")

                if choice == "1":
                    self._damage += 1
                    print("Archer Tower upgraded: +1 damage")
                elif choice == "2":
                    self._attack_range += 1
                    print("Archer Tower upgraded: +1 range")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                self._upgrade_cost = self._price + (self._price * 0.5)

        elif self._upgrade_level == 2 and self._enemies_defeated >= 30:
            if self._upgrade_cost <= self._price:
                print("Level 3 Upgrade Options:")
                print("1. +2 Damage")
                print("2. +1 Range")
                choice = input("Choose your upgrade (1 or 2): ")

                if choice == "1":
                    self._damage += 2
                    print("Archer Tower upgraded: +2 damage")
                elif choice == "2":
                    self._attack_range += 1
                    print("Archer Tower upgraded: +1 range")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                self._upgrade_cost = self._price + (self._price * 0.75)

        elif self._upgrade_level == 3 and self._enemies_defeated >= 50:
            if self._upgrade_cost <= self._price:
                print("Level 4 Upgrade Options:")
                print("1. +3 Damage")
                print("2. +2 Range")
                print("3. -1 Cooldown")
                choice = input("Choose your upgrade (1, 2, or 3): ")

                if choice == "1":
                    self._damage += 3
                    print("Archer Tower upgraded: +3 damage")
                elif choice == "2":
                    self._attack_range += 2
                    print("Archer Tower upgraded: +2 range")
                elif choice == "3":
                    self._shot_cooldown = max(1, self._shot_cooldown - 1)
                    print("Archer Tower upgraded: -1 cooldown")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                self._upgrade_cost = self._price + self._price

        elif self._upgrade_level == 4 and self._enemies_defeated >= 80:
            if self._upgrade_cost <= self._price:
                print("Level 5 Upgrade Options:")
                print("1. +4 Damage")
                print("2. +3 Range")
                print("3. -3 Cooldown")
                choice = input("Choose your upgrade (1, 2, or 3): ")

                if choice == "1":
                    self._damage += 4
                    print("Archer Tower upgraded: +4 damage")
                elif choice == "2":
                    self._attack_range += 3
                    print("Archer Tower upgraded: +3 range")
                elif choice == "3":
                    self._shot_cooldown = max(1, self._shot_cooldown - 3)
                    print("Archer Tower upgraded: -3 cooldown")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                print("Archer Tower reached Max Level!")
        else:
            print("Requirements not met, insufficient funds, or maximum level reached.")


class cannon_tower(Tower):
    def __init__(self):
        """Initializes the Cannon Tower with specific attributes."""
        super().__init__(name="Cannon Tower", damage=40, shot_cooldown=7, price=300, attack_range=70, attack_pattern=1)
        self._upgrade_level = 1
        self._upgrade_cost = self._price + (self._price * 0.25)
        self._image = pygame.image.load(os.path.join('game_assests', "cannon_tower.png"))
        self.projectile_image = pygame.image.load(os.path.join('game_assests', "projectile.png"))
        self._flipped_image = pygame.transform.flip(self._image, True, False)

    def attack(self, enemies, projectiles_list):
        """Specific implementation for archer_tower's attack logic."""
        if self._cooldown_counter > 0:
            self._cooldown_counter -= 1
            return

        for enemy in enemies:
            if self._in_range(enemy):
                self._is_facing_left = enemy._position[0] < self._position[0]
                projectile = Projectile(
                    position=self._position,
                    target=enemy,
                    speed=7, 
                    damage=self._damage,
                    size = 60,
                    image_path=self.projectile_image,
                    AoE_radius= 70
                )
                projectiles_list.append(projectile)
                self._cooldown_counter = self._shot_cooldown
                break

    def upgrade_tower(self):
        """Upgrades the tower's attributes based on the level, elimination requirements, and upgrade cost."""
        if self._upgrade_level == 1 and self._enemies_defeated >= 30:
            if self._upgrade_cost <= self._price:
                print("Level 2 Upgrade Options:")
                print("1. +1 Damage")
                print("2. +1 Range")
                choice = input("Choose your upgrade (1 or 2): ")

                if choice == "1":
                    self._damage += 1
                    print("Cannon Tower upgraded: +1 damage")
                elif choice == "2":
                    self._attack_range += 1
                    print("Cannon Tower upgraded: +1 range")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                self._upgrade_cost = self._price + (self._price * 0.5)

        elif self._upgrade_level == 2 and self._enemies_defeated >= 55:
            if self._upgrade_cost <= self._price:
                print("Level 3 Upgrade Options:")
                print("1. +1 Damage")
                print("2. +2 Range")
                choice = input("Choose your upgrade (1 or 2): ")

                if choice == "1":
                    self._damage += 1
                    print("Cannon Tower upgraded: +2 damage")
                elif choice == "2":
                    self._attack_range += 2
                    print("Cannon Tower upgraded: +1 range")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                self._upgrade_cost = self._price + (self._price * 0.75)

        elif self._upgrade_level == 3 and self._enemies_defeated >= 50:
            if self._upgrade_cost <= self._price:
                print("Level 4 Upgrade Options:")
                print("1. +2 Damage")
                print("2. +3 Range")
                print("3. -1 Cooldown")
                choice = input("Choose your upgrade (1, 2, or 3): ")

                if choice == "1":
                    self._damage += 2
                    print("Cannon Tower upgraded: +3 damage")
                elif choice == "2":
                    self._attack_range += 3
                    print("Cannon Tower upgraded: +2 range")
                elif choice == "3":
                    self._shot_cooldown = max(1, self._shot_cooldown - 1)
                    print("Cannon Tower upgraded: -1 cooldown")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                self._upgrade_cost = self._price + self._price

        elif self._upgrade_level == 4 and self._enemies_defeated >= 80:
            if self._upgrade_cost <= self._price:
                print("Level 5 Upgrade Options:")
                print("1. +4 Damage")
                print("2. +3 Range")
                print("3. -2 Cooldown")
                choice = input("Choose your upgrade (1, 2, or 3): ")

                if choice == "1":
                    self._damage += 4
                    print("Cannon Tower upgraded: +4 damage")
                elif choice == "2":
                    self._attack_range += 3
                    print("Cannon Tower upgraded: +3 range")
                elif choice == "3":
                    self._shot_cooldown = max(1, self._shot_cooldown - 2)
                    print("Cannon Tower upgraded: -3 cooldown")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                print("Cannon Tower reached Max Level!")
        else:
            print("Requirements not met, insufficient funds, or maximum level reached.")


class slingshot_tower(Tower):
    def __init__(self):
        """Initializes the Slingshot Tower with specific attributes."""
        super().__init__(name="Slingshot Tower", damage=80, shot_cooldown=8, price=500, attack_range=150, attack_pattern=1)
        self._upgrade_level = 1
        self._upgrade_cost = self._price + (self._price * 0.25)
        self._image = pygame.image.load(os.path.join('game_assests', "slingshot_tower.png"))
        self._flipped_image = pygame.transform.flip(self._image, True, False)
        self.projectile_image = pygame.image.load(os.path.join('game_assests', "projectile.png"))

    def attack(self, enemies, projectiles_list):
        """Specific implementation for slingshot_tower's attack logic."""
        if self._cooldown_counter > 0:
            self._cooldown_counter -= 1
            return

        for enemy in enemies:
            if self._in_range(enemy):
                self._is_facing_left = enemy._position[0] < self._position[0]
                projectile = Projectile(
                    position=self._position,
                    target=enemy,
                    speed=10,  
                    damage=self._damage,
                    size = 32,
                    image_path=self.projectile_image
                )
                projectiles_list.append(projectile)
                self._cooldown_counter = self._shot_cooldown
                break

    def upgrade_tower(self):
        """Upgrades the tower's attributes based on the level, elimination requirements, and upgrade cost."""
        if self._upgrade_level == 1 and self._enemies_defeated >= 20:
            if self._upgrade_cost <= self._price:
                print("Level 2 Upgrade Options:")
                print("1. +1 Damage")
                print("2. +1 Range")
                choice = input("Choose your upgrade (1 or 2): ")

                if choice == "1":
                    self._damage += 1
                    print("Slingshot Tower upgraded: +1 damage")
                elif choice == "2":
                    self._attack_range += 1
                    print("Slingshot Tower upgraded: +1 range")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                self._upgrade_cost = self._price + (self._price * 0.5)

        elif self._upgrade_level == 2 and self._enemies_defeated >= 55:
            if self._upgrade_cost <= self._price:
                print("Level 3 Upgrade Options:")
                print("1. +2 Damage")
                print("2. +1 Range")
                choice = input("Choose your upgrade (1 or 2): ")

                if choice == "1":
                    self._damage += 2
                    print("Slingshot Tower upgraded: +2 damage")
                elif choice == "2":
                    self._attack_range += 3
                    print("Slingshot Tower upgraded: +1 range")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                self._upgrade_cost = self._price + (self._price * 0.75)

        elif self._upgrade_level == 3 and self._enemies_defeated >= 50:
            if self._upgrade_cost <= self._price:
                print("Level 4 Upgrade Options:")
                print("1. +3 Damage")
                print("2. +2 Range")
                print("3. -1 Cooldown")
                choice = input("Choose your upgrade (1, 2, or 3): ")

                if choice == "1":
                    self._damage += 3
                    print("Slingshot Tower upgraded: +3 damage")
                elif choice == "2":
                    self._attack_range += 2
                    print("Slingshot Tower upgraded: +2 range")
                elif choice == "3":
                    self._shot_cooldown = max(1, self._shot_cooldown - 1)
                    print("Slingshot Tower upgraded: -1 cooldown")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                self._upgrade_cost = self._price + self._price

        elif self._upgrade_level == 4 and self._enemies_defeated >= 80:
            if self._upgrade_cost <= self._price:
                print("Level 5 Upgrade Options:")
                print("1. +4 Damage")
                print("2. +3 Range")
                print("3. -2 Cooldown")
                choice = input("Choose your upgrade (1, 2, or 3): ")

                if choice == "1":
                    self._damage += 4
                    print("Slingshot Tower upgraded: +4 damage")
                elif choice == "2":
                    self._attack_range += 3
                    print("Slingshot Tower upgraded: +3 range")
                elif choice == "3":
                    self._shot_cooldown = max(1, self._shot_cooldown - 2)
                    print("Slingshot Tower upgraded: -3 cooldown")
                else:
                    print("Invalid choice. No upgrade applied.")
                    return

                self._upgrade_level += 1
                print("Slingshot Tower reached Max Level!")
        else:
            print("Requirements not met, insufficient funds, or maximum level reached.")


