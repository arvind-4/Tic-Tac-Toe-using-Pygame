"""Pytest configuration and fixtures for Tic-Tac-Toe tests."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def mock_pygame():
    """Mock pygame module for UI tests."""
    pygame_mock = MagicMock()
    
    # Mock display
    pygame_mock.display.set_mode.return_value = MagicMock()
    pygame_mock.display.set_caption = MagicMock()
    pygame_mock.display.update = MagicMock()
    
    # Mock image loading
    mock_image = MagicMock()
    pygame_mock.image.load.return_value = mock_image
    pygame_mock.transform.scale.return_value = mock_image
    
    # Mock font
    mock_font = MagicMock()
    mock_text = MagicMock()
    mock_text.get_rect.return_value = MagicMock()
    mock_font.render.return_value = mock_text
    pygame_mock.font.Font.return_value = mock_font
    
    # Mock drawing functions
    pygame_mock.draw.line = MagicMock()
    
    # Mock clock
    mock_clock = MagicMock()
    pygame_mock.time.Clock.return_value = mock_clock
    
    # Mock events
    pygame_mock.event.get.return_value = []
    
    return pygame_mock


@pytest.fixture
def mock_time():
    """Mock time module for tests."""
    time_mock = MagicMock()
    time_mock.sleep = MagicMock()
    return time_mock


@pytest.fixture
def game_instance():
    """Create a fresh TicTacToe game instance."""
    from src.game_logic import TicTacToe
    return TicTacToe()


@pytest.fixture
def game_with_moves():
    """Create a TicTacToe game with some moves already made."""
    from src.game_logic import TicTacToe
    game = TicTacToe()
    # Make some moves: X at (0,0), O at (1,1), X at (0,1)
    game.make_move(0, 0)  # X
    game.make_move(1, 1)  # O
    game.make_move(0, 1)  # X
    return game


@pytest.fixture
def winning_game_x():
    """Create a game where X has won."""
    from src.game_logic import TicTacToe
    game = TicTacToe()
    # X wins with top row
    game.make_move(0, 0)  # X
    game.make_move(1, 0)  # O
    game.make_move(0, 1)  # X
    game.make_move(1, 1)  # O
    game.make_move(0, 2)  # X wins
    return game


@pytest.fixture
def winning_game_o():
    """Create a game where O has won."""
    from src.game_logic import TicTacToe
    game = TicTacToe()
    # O wins with left column
    game.make_move(0, 1)  # X
    game.make_move(0, 0)  # O
    game.make_move(1, 1)  # X
    game.make_move(1, 0)  # O
    game.make_move(0, 2)  # X
    game.make_move(2, 0)  # O wins
    return game


@pytest.fixture
def draw_game():
    """Create a game that ends in a draw."""
    from src.game_logic import TicTacToe
    game = TicTacToe()
    # Create a draw scenario
    moves = [
        (0, 0),  # X
        (0, 1),  # O
        (0, 2),  # X
        (1, 0),  # O
        (1, 2),  # X
        (1, 1),  # O
        (2, 0),  # X
        (2, 2),  # O
        (2, 1),  # X
    ]
    for row, col in moves:
        game.make_move(row, col)
    return game


@pytest.fixture
def mock_ui_dependencies(monkeypatch, mock_pygame, mock_time):
    """Mock all UI dependencies for GameUI tests."""
    monkeypatch.setattr("src.game_ui.pygame", mock_pygame)
    monkeypatch.setattr("src.game_ui.time", mock_time)
    return mock_pygame, mock_time


@pytest.fixture
def sample_board_states():
    """Provide various board states for testing."""
    return {
        "empty": [[None, None, None], [None, None, None], [None, None, None]],
        "partial": [["x", None, "o"], [None, "x", None], ["o", None, None]],
        "full_no_winner": [["x", "o", "x"], ["o", "x", "o"], ["o", "x", "o"]],
        "x_wins_row": [["x", "x", "x"], ["o", "o", None], [None, None, None]],
        "o_wins_col": [["o", "x", "x"], ["o", "x", None], ["o", None, None]],
        "x_wins_diagonal": [["x", "o", "o"], ["o", "x", None], [None, None, "x"]],
    }
