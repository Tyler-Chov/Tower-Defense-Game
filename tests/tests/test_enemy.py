import pytest
import pygame
from enemy import Enemy

@pytest.fixture(scope="module")
def setup_pygame():
    pygame.init()

@pytest.fixture
def path():
    return [(0, 0), (100, 100), (200, 200)]

@pytest.fixture
def window():
    return pygame.display.set_mode((800, 600))

def test_enemy_initialization_easy(setup_pygame, path):
    """Tests if the enemy initializes correctly on easy difficulty."""
    enemy = Enemy('circle', path, 'easy')
    assert enemy.get_enemy_type() == 'circle'
    assert enemy.get_enemy_health() == 50
    assert enemy.get_enemy_speed() == 1
    assert enemy.get_enemy_strength() == 1

def test_enemy_initialization_medium(setup_pygame, path):
    """Tests if the enemy initializes correctly on medium difficulty."""
    enemy = Enemy('triangle', path, 'medium')
    assert enemy.get_enemy_type() == 'triangle'
    assert enemy.get_enemy_health() == 75
    assert enemy.get_enemy_speed() == 7.5
    assert enemy.get_enemy_strength() == 1

def test_enemy_initialization_hard(setup_pygame, path):
    """Tests if the enemy initializes correctly on hard difficulty."""
    enemy = Enemy('rectangle', path, 'hard')
    assert enemy.get_enemy_type() == 'rectangle'
    assert enemy.get_enemy_health() == 400
    assert enemy.get_enemy_speed() == 1
    assert enemy.get_enemy_strength() == 5

def test_enemy_move(setup_pygame, path):
    """Tests if the enemy moves along the path."""
    enemy = Enemy('circle', path, 'easy')
    initial_position = enemy._position
    enemy._move()
    enemy._move()
    assert enemy._position != initial_position

def test_enemy_damage(setup_pygame, path):
    """Tests if the enemy takes damage and dies."""
    enemy = Enemy('circle', path, 'easy')
    enemy.take_damage(25)
    assert enemy.get_enemy_health() == 25
    enemy.take_damage(25)
    assert not enemy.is_alive()

def test_enemy_kill(setup_pygame, path):
    """Tests if the enemy is killed."""
    enemy = Enemy('circle', path, 'easy')
    enemy.kill_enemy()
    assert not enemy.is_alive()

def test_enemy_damage_base(setup_pygame, path):
    """Tests if the enemy causes damage to the health stat."""
    class MockBase:
        def __init__(self):
            self.health = 100

        def remove_health(self, amount):
            self.health -= amount

    base = MockBase()
    enemy = Enemy('ghost', path, 'easy')
    enemy.damage_base(base)
    assert base.health == 80
    assert not enemy.is_alive()

if __name__ == "__main__":
    pytest.main()