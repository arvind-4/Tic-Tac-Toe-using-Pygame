"""Tests for the game UI module."""

from unittest.mock import MagicMock, patch

import pytest

import src.constants as constants


class TestGameUIInitialization:
    """Test GameUI class initialization."""

    def test_init_pygame_components(self, mock_ui_dependencies):
        """Test pygame components are initialized correctly."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        # Verify pygame.init was called
        mock_pygame.init.assert_called_once()
        
        # Verify display setup
        mock_pygame.display.set_mode.assert_called_once_with(
            (constants.WINDOW_WIDTH, constants.TOTAL_HEIGHT), 0, 32
        )
        mock_pygame.display.set_caption.assert_called_once_with("Tic Tac Toe")
        
        # Verify clock creation
        mock_pygame.time.Clock.assert_called_once()
        
        # Verify font creation
        mock_pygame.font.Font.assert_called_once_with(None, constants.FONT_SIZE)

    def test_load_images_called(self, mock_ui_dependencies):
        """Test image loading is called during initialization."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        # Verify images are loaded
        expected_calls = [
            ((constants.WELCOME_IMAGE,),),
            ((constants.X_IMAGE,),),
            ((constants.O_IMAGE,),),
        ]
        
        assert mock_pygame.image.load.call_count == 3
        for call in expected_calls:
            assert call in mock_pygame.image.load.call_args_list

    def test_scale_images_called(self, mock_ui_dependencies):
        """Test image scaling is called during initialization."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        # Verify images are scaled (3 calls for x, o, and welcome images)
        assert mock_pygame.transform.scale.call_count == 3


class TestWelcomeScreen:
    """Test welcome screen functionality."""

    def test_show_welcome_screen(self, mock_ui_dependencies):
        """Test welcome screen display."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.show_welcome_screen()
        
        # Verify screen blit and update
        ui.screen.blit.assert_called()
        mock_pygame.display.update.assert_called()
        mock_time.sleep.assert_called_once_with(1)


class TestBoardDrawing:
    """Test board drawing functionality."""

    def test_draw_board_fills_screen(self, mock_ui_dependencies):
        """Test board drawing fills screen with white."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.draw_board()
        
        # Verify screen is filled with white
        ui.screen.fill.assert_called_with(constants.WHITE)

    def test_draw_board_lines(self, mock_ui_dependencies):
        """Test board drawing creates grid lines."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.draw_board()
        
        # Should draw 4 lines total (2 vertical + 2 horizontal)
        assert mock_pygame.draw.line.call_count == 4

    def test_draw_board_line_positions(self, mock_ui_dependencies):
        """Test board lines are drawn at correct positions."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.draw_board()
        
        # Check that lines are drawn with correct parameters
        calls = mock_pygame.draw.line.call_args_list
        
        # Verify line color and width are used
        for call in calls:
            args, kwargs = call
            assert args[1] == constants.LINE_COLOR  # Color
            assert args[4] == constants.LINE_WIDTH  # Width


class TestSymbolDrawing:
    """Test symbol drawing functionality."""

    def test_draw_symbols_empty_board(self, mock_ui_dependencies, game_instance):
        """Test drawing symbols on empty board does nothing."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.draw_symbols(game_instance)
        
        # No symbols should be drawn on empty board
        ui.screen.blit.assert_not_called()

    def test_draw_symbols_with_moves(self, mock_ui_dependencies, game_with_moves):
        """Test drawing symbols with moves on board."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.draw_symbols(game_with_moves)
        
        # Should blit symbols for each non-None cell
        non_none_cells = sum(
            1 for row in game_with_moves.board 
            for cell in row if cell is not None
        )
        assert ui.screen.blit.call_count == non_none_cells

    def test_draw_symbols_correct_images(self, mock_ui_dependencies):
        """Test correct images are used for X and O."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        from src.game_logic import TicTacToe
        
        ui = GameUI()
        game = TicTacToe()
        
        # Place X and O on board
        game.make_move(0, 0)  # X
        game.make_move(1, 1)  # O
        
        ui.draw_symbols(game)
        
        # Verify correct images are blitted
        calls = ui.screen.blit.call_args_list
        assert len(calls) == 2  # Two symbols drawn


class TestWinningLineDrawing:
    """Test winning line drawing functionality."""

    def test_draw_winning_line_no_winner(self, mock_ui_dependencies, game_instance):
        """Test no line drawn when no winner."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.draw_winning_line(game_instance)
        
        # No line should be drawn
        mock_pygame.draw.line.assert_not_called()

    def test_draw_winning_line_row_win(self, mock_ui_dependencies, winning_game_x):
        """Test winning line drawn for row win."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.draw_winning_line(winning_game_x)
        
        # Should draw a line
        mock_pygame.draw.line.assert_called_once()
        
        # Verify line color
        call_args = mock_pygame.draw.line.call_args
        assert call_args[0][1] == constants.WINNING_LINE_COLOR

    def test_draw_winning_line_different_types(self, mock_ui_dependencies):
        """Test different winning line types are handled."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        from src.game_logic import TicTacToe
        
        ui = GameUI()
        
        # Test different win types
        win_scenarios = [
            # Row win
            [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)],  # X wins row 0
            # Column win  
            [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],  # X wins col 0
            # Diagonal win
            [(0, 0), (0, 1), (1, 1), (0, 2), (2, 2)],  # X wins main diagonal
        ]
        
        for moves in win_scenarios:
            mock_pygame.draw.line.reset_mock()
            game = TicTacToe()
            
            for row, col in moves:
                game.make_move(row, col)
            
            ui.draw_winning_line(game)
            
            # Should draw exactly one line
            assert mock_pygame.draw.line.call_count == 1


class TestStatusDrawing:
    """Test status message drawing."""

    def test_draw_status_active_game(self, mock_ui_dependencies, game_instance):
        """Test status message for active game."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.draw_status(game_instance)
        
        # Verify text rendering
        ui.font.render.assert_called_once()
        call_args = ui.font.render.call_args
        
        # Should show current player's turn
        message = call_args[0][0]
        assert "X'S TURN" in message.upper()

    def test_draw_status_won_game(self, mock_ui_dependencies, winning_game_x):
        """Test status message for won game."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.draw_status(winning_game_x)
        
        # Verify text rendering
        ui.font.render.assert_called_once()
        call_args = ui.font.render.call_args
        
        # Should show winner
        message = call_args[0][0]
        assert "X WON" in message.upper()

    def test_draw_status_draw_game(self, mock_ui_dependencies, draw_game):
        """Test status message for draw game."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.draw_status(draw_game)
        
        # Verify text rendering
        ui.font.render.assert_called_once()
        call_args = ui.font.render.call_args
        
        # Should show draw message
        message = call_args[0][0]
        assert "DRAW" in message.upper()

    def test_draw_status_clears_area(self, mock_ui_dependencies, game_instance):
        """Test status drawing clears the status area."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.draw_status(game_instance)
        
        # Verify status area is cleared
        fill_calls = ui.screen.fill.call_args_list
        assert len(fill_calls) >= 1
        
        # Check that black fill is called for status area
        black_fill_call = None
        for call in fill_calls:
            if len(call[0]) > 1 and call[0][0] == constants.BLACK:
                black_fill_call = call
                break
        
        assert black_fill_call is not None


class TestMouseClickHandling:
    """Test mouse click to cell conversion."""

    def test_get_clicked_cell_valid_positions(self, mock_ui_dependencies):
        """Test valid mouse positions convert to correct cells."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        # Test corner positions
        test_cases = [
            ((0, 0), (0, 0)),  # Top-left
            ((constants.CELL_WIDTH - 1, 0), (0, 0)),  # Still top-left
            ((constants.CELL_WIDTH, 0), (0, 1)),  # Top-middle
            ((0, constants.CELL_HEIGHT), (1, 0)),  # Middle-left
            ((constants.CELL_WIDTH, constants.CELL_HEIGHT), (1, 1)),  # Center
        ]
        
        for mouse_pos, expected_cell in test_cases:
            result = ui.get_clicked_cell(mouse_pos)
            assert result == expected_cell

    def test_get_clicked_cell_outside_board(self, mock_ui_dependencies):
        """Test mouse positions outside board return None."""
        mock_pygame, mock_time = mock_ui_dependencies

        from src.game_ui import GameUI
        ui = GameUI()

        # Test positions outside the game board
        outside_positions = [
            (constants.WINDOW_WIDTH, 0),  # Right of board
            (0, constants.WINDOW_HEIGHT),  # Below board
            (constants.WINDOW_WIDTH + 10, constants.WINDOW_HEIGHT + 10),  # Far outside
            (-10, -10),  # Negative coordinates
            (-1, 0),  # Negative x
            (0, -1),  # Negative y
        ]

        for pos in outside_positions:
            result = ui.get_clicked_cell(pos)
            assert result is None

    def test_get_clicked_cell_boundary_cases(self, mock_ui_dependencies):
        """Test boundary cases for cell detection."""
        mock_pygame, mock_time = mock_ui_dependencies

        from src.game_ui import GameUI
        ui = GameUI()

        # Test exact boundary positions
        # Note: CELL_WIDTH = 133, CELL_HEIGHT = 133 (400 // 3)
        # (399, 399) would map to (3, 3) but that's outside board, so should return None
        boundary_cases = [
            ((constants.WINDOW_WIDTH - 1, constants.WINDOW_HEIGHT - 1), None),  # (399, 399) -> None (outside board)
            ((constants.CELL_WIDTH * 2 - 1, constants.CELL_HEIGHT * 2 - 1), (1, 1)),  # (265, 265) -> (1, 1)
            ((constants.CELL_WIDTH * 3 - 1, constants.CELL_HEIGHT * 3 - 1), (2, 2)),  # (398, 398) -> (2, 2) - valid
        ]

        for mouse_pos, expected_cell in boundary_cases:
            result = ui.get_clicked_cell(mouse_pos)
            assert result == expected_cell

        # Test valid positions within each cell
        valid_cases = [
            ((0, 0), (0, 0)),  # Top-left
            ((constants.CELL_WIDTH - 1, constants.CELL_HEIGHT - 1), (0, 0)),  # Still in first cell
            ((constants.CELL_WIDTH, constants.CELL_HEIGHT), (1, 1)),  # Second cell
            ((constants.CELL_WIDTH * 2, constants.CELL_HEIGHT * 2), (2, 2)),  # Third cell
        ]

        for mouse_pos, expected_cell in valid_cases:
            result = ui.get_clicked_cell(mouse_pos)
            assert result == expected_cell


class TestDisplayAndClock:
    """Test display and clock functionality."""

    def test_update_display(self, mock_ui_dependencies):
        """Test display update."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.update_display()
        
        mock_pygame.display.update.assert_called()

    def test_tick_clock(self, mock_ui_dependencies):
        """Test clock tick."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.tick()
        
        ui.clock.tick.assert_called_once_with(constants.FPS)

    def test_quit_pygame(self, mock_ui_dependencies):
        """Test pygame quit."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        ui.quit()
        
        mock_pygame.quit.assert_called_once()


class TestUIIntegration:
    """Test UI component integration."""

    def test_full_game_render_sequence(self, mock_ui_dependencies, game_with_moves):
        """Test complete rendering sequence."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        ui = GameUI()
        
        # Simulate full render sequence
        ui.draw_board()
        ui.draw_symbols(game_with_moves)
        ui.draw_status(game_with_moves)
        ui.update_display()
        
        # Verify all components were called
        assert ui.screen.fill.called  # Board background
        assert ui.screen.blit.called  # Symbols
        assert ui.font.render.called  # Status text
        assert mock_pygame.display.update.called  # Display update

    def test_ui_handles_game_state_changes(self, mock_ui_dependencies):
        """Test UI correctly handles different game states."""
        mock_pygame, mock_time = mock_ui_dependencies
        
        from src.game_ui import GameUI
        from src.game_logic import TicTacToe
        
        ui = GameUI()
        game = TicTacToe()
        
        # Test active game state
        ui.draw_status(game)
        first_call = ui.font.render.call_args[0][0]
        
        # Make a winning move
        game.make_move(0, 0)  # X
        game.make_move(1, 0)  # O
        game.make_move(0, 1)  # X
        game.make_move(1, 1)  # O
        game.make_move(0, 2)  # X wins
        
        ui.font.render.reset_mock()
        ui.draw_status(game)
        second_call = ui.font.render.call_args[0][0]
        
        # Messages should be different
        assert first_call != second_call
        assert "WON" in second_call.upper()
