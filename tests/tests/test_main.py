import pytest
import pygame
from main import StartScreen, Stage_Select_Screen, MainGameScreen

@pytest.fixture
def window():
    pygame.init()
    return pygame.display.set_mode((800, 600))

def test_start_screen_initialization(window):
    """Tests if the start screen initializes correctly."""
    start_screen = StartScreen(window)
    assert start_screen.window == window
    assert start_screen.background is not None
    assert start_screen.font is not None
    assert start_screen.start_button_rect == pygame.Rect(310, 444, 180, 46)

def test_stage_select_initialization(window):
    """Tests if the stage select screen initializes correctly."""
    stage_select = Stage_Select_Screen(window)
    assert stage_select.window == window
    assert stage_select.background is not None
    assert stage_select.font is not None
    assert stage_select.stage_selection == "stage1"
    assert stage_select.difficulty_selection is None

def test_main_game_screen_initialization(window):
    """Tests if the main game screen initializes correctly."""
    main_game_screen = MainGameScreen(window, 1, "easy")
    assert main_game_screen.window == window
    assert main_game_screen.map == 1
    assert main_game_screen.difficulty == "easy"
    assert main_game_screen.health == 0
    assert main_game_screen.money == 0

def test_main_game_screen_place_tower(window):
    """Tests if a tower can be placed"""
    main_game_screen = MainGameScreen(window, 1, "easy")
    main_game_screen.selected_tower_type = 0
    main_game_screen.money = 400
    main_game_screen.place_tower((400, 200))
    assert len(main_game_screen.placed_towers) == 1

def test_main_game_screen_remove_health(window):
    """Tests if health can be removed"""
    main_game_screen = MainGameScreen(window, 1, "easy")
    main_game_screen.set_health(100)
    main_game_screen.remove_health(10)
    assert main_game_screen.health == 90

def test_main_game_screen_add_money(window):
    """Tests if money can be added"""
    main_game_screen = MainGameScreen(window, 1, "easy")
    main_game_screen.add_money(100)
    assert main_game_screen.money == 100

def test_main_game_screen_remove_money(window):
    """Tests if money can be removed"""
    main_game_screen = MainGameScreen(window, 1, "easy")
    main_game_screen.set_money(100)
    main_game_screen.remove_money(50)
    assert main_game_screen.money == 50

if __name__ == "__main__":
    pytest.main()
    