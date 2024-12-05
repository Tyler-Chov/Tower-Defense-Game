import pytest
from waves import Wave
from enemy import Enemy

@pytest.fixture
def mock_enemies():
    """Creates a list of mock enemies for testing."""
    return [Enemy("circle", [(0, 0), (100, 100)], "easy"),
            Enemy("triangle", [(0, 0), (100, 100)], "easy")]

@pytest.fixture
def wave(mock_enemies):
    """Creates a mock wave for testing."""
    return Wave(mock_enemies, spawn_timer=5)

def test_wave_spawn_enemy(wave):
    """Tests if enemies spawn correctly."""
    enemy = wave.spawn_enemy()
    assert enemy is not None
    assert wave._enemy_number == 1

def test_wave_spawn_all_enemies(wave):
    """Tests if all enemies spawn correctly."""
    for i in range(len(wave._enemy_data)):
        wave.spawn_enemy()
    assert wave._enemy_number == len(wave._enemy_data)
    assert wave.spawn_enemy() is None 

def test_is_wave_complete(wave):
    """Tests if the wave is complete when all enemies are spawned and dead."""
    for i in range(len(wave._enemy_data)):
        wave.spawn_enemy()

    for enemy in wave._enemy_data:
        enemy.kill_enemy()
    assert wave._is_wave_complete() is True

def test_wave_not_complete(wave):
    """Tests if the wave is not complete when enemies are still alive."""
    wave.spawn_enemy()
    assert wave._is_wave_complete() is False

