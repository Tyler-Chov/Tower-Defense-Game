class Tower:
    def __init__(self, name: str, damage: int, shot_cooldown: int, price: int, attack_range: int, attack_pattern: int):
        self._name = name
        self._damage = damage
        self._shot_cooldown = shot_cooldown
        self._price = price
        self._sell_price = price * 0.25
        self._attack_range = attack_range
        self._attack_pattern = attack_pattern
        self._position = None
        self._upgrade_level = 1
        self._upgrade_cost = price + (price * 0.5)
        self._enemies_defeated = 0

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

    def get_attack_range(self):
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

    def place_tower(self, position: int):
        self._position = position

    def upgrade_tower(self):
        self._upgrade_level += 1
        self._damage += int(self._damage * 0.5)
        self._attack_range += 1
        self._upgrade_cost = int(self._price * (1 + 0.5 * self._upgrade_level))

    def sell_tower(self):
        print(f"{self._name} tower sold for {self._sell_price} credits.")

    def attack_enemy(self, enemy):
        if self._shot_cooldown == 0:
            if self._attack_pattern == 1:
                pass
            elif self._attack_pattern == 2:
                pass
            self._shot_cooldown = 3
            self._enemies_defeated += 1
        else:
            self._shot_cooldown -= 1

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
