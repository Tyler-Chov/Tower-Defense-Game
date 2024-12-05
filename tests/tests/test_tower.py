import pytest
from tower import Tower, normal_tower as NormalTower, Archer_Tower, cannon_tower as CannonTower, slingshot_tower as SlingshotTower
import pygame

pygame.init()

@pytest.fixture(scope="module", autouse=True)
def init_pygame_mixer():
    pygame.mixer.init()

@pytest.fixture
def tower():
    return Tower("Test Tower", 10, 1, 100, 50, 1)

@pytest.fixture
def normal_tower_fixture():
    return NormalTower()

@pytest.fixture
def archer_tower_fixture():
    return Archer_Tower()

@pytest.fixture
def cannon_tower_fixture():
    return CannonTower()

@pytest.fixture
def slingshot_tower_fixture():
    return SlingshotTower()

def test_initial_attributes(tower):
    """Tests if the tower initializes correctly."""
    assert tower.get_name() == "Test Tower"
    assert tower.get_damage() == 10
    assert tower.get_price() == 100
    assert tower.get_sell_price() == 25
    assert tower.get_range() == 50
    assert tower.get_enemies_defeated() == 0

def test_set_name(tower):
    """Tests if the tower name can be set."""
    tower.set_name("New Name")
    assert tower.get_name() == "New Name"
    with pytest.raises(ValueError):
        tower.set_name("")

def test_set_damage(tower):
    """Tests if the tower damage can be set."""
    tower.set_damage(20)
    assert tower.get_damage() == 20
    with pytest.raises(ValueError):
        tower.set_damage(0)

def test_set_attack_range(tower):
    """Tests if the tower attack range can be set."""
    tower.set_attack_range(60)
    assert tower.get_range() == 60
    with pytest.raises(ValueError):
        tower.set_attack_range(0)

def test_upgrade_tower(tower):
    """Tests if the tower can be upgraded."""
    initial_damage = tower.get_damage()
    initial_range = tower.get_range()
    tower.upgrade_tower()
    assert tower.get_damage() == initial_damage + int(initial_damage * 0.5)
    assert tower.get_range() == initial_range + 1

def test_sell_tower(tower):
    """Tests if the tower can be sold."""
    assert tower.get_sell_price() == 25

def test_normal_tower_initial_attributes(normal_tower_fixture):
    """Tests if the normal tower initializes correctly."""
    assert normal_tower_fixture.get_name() == "Normal Tower"
    assert normal_tower_fixture.get_damage() == 30
    assert normal_tower_fixture.get_price() == 200
    assert normal_tower_fixture.get_sell_price() == 50
    assert normal_tower_fixture.get_range() == 75

def test_archer_tower_initial_attributes(archer_tower_fixture):
    """Tests if the archer tower initializes correctly."""
    assert archer_tower_fixture.get_name() == "Archer Tower"
    assert archer_tower_fixture.get_damage() == 20
    assert archer_tower_fixture.get_price() == 150
    assert archer_tower_fixture.get_sell_price() == 37
    assert archer_tower_fixture.get_range() == 75

def test_cannon_tower_initial_attributes(cannon_tower_fixture):
    """Tests if the cannon tower initializes correctly."""
    assert cannon_tower_fixture.get_name() == "Cannon Tower"
    assert cannon_tower_fixture.get_damage() == 40
    assert cannon_tower_fixture.get_price() == 300
    assert cannon_tower_fixture.get_sell_price() == 75
    assert cannon_tower_fixture.get_range() == 70

def test_slingshot_tower_initial_attributes(slingshot_tower_fixture):
    """Tests if the slingshot tower initializes correctly."""
    assert slingshot_tower_fixture.get_name() == "Slingshot Tower"
    assert slingshot_tower_fixture.get_damage() == 80
    assert slingshot_tower_fixture.get_price() == 400
    assert slingshot_tower_fixture.get_sell_price() == 100
    assert slingshot_tower_fixture.get_range() == 150

def test_tower_attack(tower):
    """Tests if the tower attacks enemies."""
    class MockEnemy:
        def __init__(self, position):
            self._position = position

    enemies = [MockEnemy((40, 40)), MockEnemy((100, 100))]
    projectiles_list = []
    tower.place((50, 50))
    tower.attack(enemies, projectiles_list)
    assert len(projectiles_list) == 1

def test_tower_upgrade_cost(tower):
    """Tests if the tower upgrade cost is calculated correctly."""
    initial_upgrade_cost = tower.get_upgrade_cost()
    tower.upgrade_tower()
    assert tower.get_upgrade_cost() == int(tower.get_price() * (1 + 0.5 * tower._upgrade_level))

if __name__ == "__main__":
    pytest.main()
