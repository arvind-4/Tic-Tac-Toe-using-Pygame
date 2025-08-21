"""Tests for the constants module."""

from pathlib import Path

import pytest

import src.constants as constants


class TestGameDimensions:
    """Test game dimension constants."""

    def test_window_dimensions(self):
        """Test window dimension constants are positive integers."""
        assert constants.WINDOW_WIDTH == 400
        assert constants.WINDOW_HEIGHT == 400
        assert isinstance(constants.WINDOW_WIDTH, int)
        assert isinstance(constants.WINDOW_HEIGHT, int)
        assert constants.WINDOW_WIDTH > 0
        assert constants.WINDOW_HEIGHT > 0

    def test_status_bar_height(self):
        """Test status bar height is positive."""
        assert constants.STATUS_BAR_HEIGHT == 100
        assert isinstance(constants.STATUS_BAR_HEIGHT, int)
        assert constants.STATUS_BAR_HEIGHT > 0

    def test_total_height_calculation(self):
        """Test total height is correctly calculated."""
        expected_total = constants.WINDOW_HEIGHT + constants.STATUS_BAR_HEIGHT
        assert constants.TOTAL_HEIGHT == expected_total
        assert constants.TOTAL_HEIGHT == 500


class TestColors:
    """Test color constants."""

    def test_color_tuples_format(self):
        """Test all colors are RGB tuples with valid values."""
        colors = [
            constants.WHITE,
            constants.BLACK,
            constants.LINE_COLOR,
            constants.WINNING_LINE_COLOR,
            constants.DIAGONAL_LINE_COLOR,
        ]
        
        for color in colors:
            assert isinstance(color, tuple)
            assert len(color) == 3
            for component in color:
                assert isinstance(component, int)
                assert 0 <= component <= 255

    def test_specific_color_values(self):
        """Test specific color values are correct."""
        assert constants.WHITE == (255, 255, 255)
        assert constants.BLACK == (0, 0, 0)
        assert constants.LINE_COLOR == (10, 10, 10)
        assert constants.WINNING_LINE_COLOR == (250, 0, 0)
        assert constants.DIAGONAL_LINE_COLOR == (250, 70, 70)


class TestGameSettings:
    """Test game setting constants."""

    def test_fps_setting(self):
        """Test FPS is a positive integer."""
        assert constants.FPS == 30
        assert isinstance(constants.FPS, int)
        assert constants.FPS > 0

    def test_board_size(self):
        """Test board size is 3 for tic-tac-toe."""
        assert constants.BOARD_SIZE == 3
        assert isinstance(constants.BOARD_SIZE, int)
        assert constants.BOARD_SIZE > 0

    def test_line_widths(self):
        """Test line width constants are positive integers."""
        assert constants.LINE_WIDTH == 7
        assert constants.WINNING_LINE_WIDTH == 4
        assert isinstance(constants.LINE_WIDTH, int)
        assert isinstance(constants.WINNING_LINE_WIDTH, int)
        assert constants.LINE_WIDTH > 0
        assert constants.WINNING_LINE_WIDTH > 0


class TestImageSettings:
    """Test image-related constants."""

    def test_symbol_size(self):
        """Test symbol size is a valid tuple."""
        assert constants.SYMBOL_SIZE == (80, 80)
        assert isinstance(constants.SYMBOL_SIZE, tuple)
        assert len(constants.SYMBOL_SIZE) == 2
        assert all(isinstance(dim, int) and dim > 0 for dim in constants.SYMBOL_SIZE)


class TestImagePaths:
    """Test image path constants."""

    def test_root_dir_exists(self):
        """Test root directory path is valid."""
        assert isinstance(constants.ROOT_DIR, Path)
        assert constants.ROOT_DIR.exists()

    def test_images_dir_path(self):
        """Test images directory path is correctly constructed."""
        expected_images_dir = constants.ROOT_DIR / "images"
        assert constants.IMAGES_DIR == expected_images_dir
        assert isinstance(constants.IMAGES_DIR, Path)

    def test_image_file_paths(self):
        """Test individual image file paths are correctly constructed."""
        expected_welcome = constants.IMAGES_DIR / "welcome.png"
        expected_x = constants.IMAGES_DIR / "x.png"
        expected_o = constants.IMAGES_DIR / "o.png"
        
        assert constants.WELCOME_IMAGE == expected_welcome
        assert constants.X_IMAGE == expected_x
        assert constants.O_IMAGE == expected_o
        
        # Test they are Path objects
        assert isinstance(constants.WELCOME_IMAGE, Path)
        assert isinstance(constants.X_IMAGE, Path)
        assert isinstance(constants.O_IMAGE, Path)

    def test_image_files_exist(self):
        """Test that image files actually exist."""
        assert constants.WELCOME_IMAGE.exists(), f"Welcome image not found: {constants.WELCOME_IMAGE}"
        assert constants.X_IMAGE.exists(), f"X image not found: {constants.X_IMAGE}"
        assert constants.O_IMAGE.exists(), f"O image not found: {constants.O_IMAGE}"

    def test_image_files_are_png(self):
        """Test that image files have .png extension."""
        assert constants.WELCOME_IMAGE.suffix == ".png"
        assert constants.X_IMAGE.suffix == ".png"
        assert constants.O_IMAGE.suffix == ".png"


class TestGameSymbols:
    """Test game symbol constants."""

    def test_player_symbols(self):
        """Test player symbols are correct strings."""
        assert constants.PLAYER_X == "x"
        assert constants.PLAYER_O == "o"
        assert isinstance(constants.PLAYER_X, str)
        assert isinstance(constants.PLAYER_O, str)
        assert constants.PLAYER_X != constants.PLAYER_O


class TestFontSettings:
    """Test font-related constants."""

    def test_font_size(self):
        """Test font size is a positive integer."""
        assert constants.FONT_SIZE == 30
        assert isinstance(constants.FONT_SIZE, int)
        assert constants.FONT_SIZE > 0

    def test_status_y_position(self):
        """Test status Y position is correctly calculated."""
        assert constants.STATUS_Y_POSITION == 450
        assert isinstance(constants.STATUS_Y_POSITION, int)
        assert constants.STATUS_Y_POSITION > 0


class TestGridCalculations:
    """Test grid calculation constants."""

    def test_cell_dimensions(self):
        """Test cell dimensions are correctly calculated."""
        expected_cell_width = constants.WINDOW_WIDTH // constants.BOARD_SIZE
        expected_cell_height = constants.WINDOW_HEIGHT // constants.BOARD_SIZE
        
        assert constants.CELL_WIDTH == expected_cell_width
        assert constants.CELL_HEIGHT == expected_cell_height
        assert constants.CELL_WIDTH == 133  # 400 // 3
        assert constants.CELL_HEIGHT == 133  # 400 // 3

    def test_symbol_offset(self):
        """Test symbol offset is a positive integer."""
        assert constants.SYMBOL_OFFSET == 30
        assert isinstance(constants.SYMBOL_OFFSET, int)
        assert constants.SYMBOL_OFFSET > 0


class TestGameStates:
    """Test game state constants."""

    def test_game_state_values(self):
        """Test game state constants are correct strings."""
        assert constants.GAME_ACTIVE == "active"
        assert constants.GAME_WON == "won"
        assert constants.GAME_DRAW == "draw"
        
        # Test they are strings
        assert isinstance(constants.GAME_ACTIVE, str)
        assert isinstance(constants.GAME_WON, str)
        assert isinstance(constants.GAME_DRAW, str)
        
        # Test they are unique
        states = {constants.GAME_ACTIVE, constants.GAME_WON, constants.GAME_DRAW}
        assert len(states) == 3


class TestConstantsIntegrity:
    """Test overall constants integrity and relationships."""

    def test_window_dimensions_divisible_by_board_size(self):
        """Test window dimensions work well with board size."""
        # While not strictly required, it's good if dimensions are divisible
        # by board size for clean grid layout
        width_remainder = constants.WINDOW_WIDTH % constants.BOARD_SIZE
        height_remainder = constants.WINDOW_HEIGHT % constants.BOARD_SIZE
        
        # Document the remainders (they should be small)
        assert width_remainder < constants.BOARD_SIZE
        assert height_remainder < constants.BOARD_SIZE

    def test_symbol_size_fits_in_cell(self):
        """Test symbol size fits within cell dimensions."""
        symbol_width, symbol_height = constants.SYMBOL_SIZE
        
        # Symbols should fit in cells with some margin
        assert symbol_width < constants.CELL_WIDTH
        assert symbol_height < constants.CELL_HEIGHT

    def test_symbol_offset_reasonable(self):
        """Test symbol offset leaves reasonable space."""
        symbol_width, symbol_height = constants.SYMBOL_SIZE
        
        # Check that symbol + offset fits in cell
        assert constants.SYMBOL_OFFSET + symbol_width <= constants.CELL_WIDTH
        assert constants.SYMBOL_OFFSET + symbol_height <= constants.CELL_HEIGHT

    def test_status_position_below_game_area(self):
        """Test status position is below the game board."""
        assert constants.STATUS_Y_POSITION > constants.WINDOW_HEIGHT
        assert constants.STATUS_Y_POSITION < constants.TOTAL_HEIGHT
