import pytest
from projectile import Projectile, Explosion
from enemy import Enemy
import pygame

pygame.init()

@pytest.fixture
def mock_enemy():
    """Creates a mock enemy for testing."""
    return Enemy("circle", [(0, 0), (100, 100)], "easy")

@pytest.fixture
def projectile_image():
    """Loads a mock projectile image for testing."""
    return pygame.Surface((10, 10))  

@pytest.fixture
def mock_projectile(mock_enemy, projectile_image):
    """Creates a mock projectile for testing."""
    return Projectile(
        position=(0, 0),
        target=mock_enemy,
        speed=10,
        damage=20,
        size=32,
        image_path=projectile_image,  
    )

@pytest.fixture
def mock_explosion():
    """Creates a mock explosion for testing."""
    return Explosion(position=(50, 50), max_radius=100, duration=15)

def test_projectile_move(mock_projectile, mock_enemy):
    """Tests if the projectile moves toward the enemy."""
    initial_position = mock_projectile._position[:]
    mock_enemy._position = (50, 50)
    mock_projectile.move()
    assert mock_projectile._position != initial_position

def test_projectile_hits_target(mock_projectile, mock_enemy):
    """Tests if the projectile deactivates and damages the enemy on hit."""
    mock_projectile._position = list(mock_enemy._position)  
    mock_projectile.move()
    assert mock_enemy.get_enemy_health() < mock_enemy._max_health
    assert not mock_projectile.is_active()

def test_apply_splash_damage(mock_projectile, mock_enemy):
    """Tests if splash damage is applied to enemies within radius."""
    enemies = [mock_enemy, Enemy("triangle", [(40, 40), (100, 100)], "easy")]
    explosions = []
    mock_projectile._AoE_radius = 100
    mock_projectile.apply_splash_damage(enemies, explosions)
    assert len(explosions) == 1
    for enemy in enemies:
        assert enemy.get_enemy_health() < enemy._max_health

def test_explosion_update(mock_explosion):
    """Tests if the explosion deactivates after its duration."""
    for i in range(mock_explosion._duration):
        mock_explosion.update()
    assert not mock_explosion.is_active()

def test_explosion_render(mock_explosion):
    """Tests if the explosion renders correctly (surface integrity check)."""
    pygame.init()
    window = pygame.Surface((200, 200), pygame.SRCALPHA)
    mock_explosion.render(window)
    assert mock_explosion.is_active()
    pygame.quit()

if __name__ == "__main__":
    pytest.main()