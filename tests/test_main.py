"""Tests for the main module and game integration."""

import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

import src.constants as constants


class TestMainFunction:
    """Test main function and game initialization."""

    @patch('src.main.sys.exit')
    @patch('src.main.GameUI')
    @patch('src.main.TicTacToe')
    @patch('src.main.pygame.event.get')
    @patch('src.main.QUIT', 1)  # Mock the QUIT constant
    def test_main_initializes_components(self, mock_event_get, mock_tictactoe, mock_gameui, mock_exit):
        """Test main function initializes game components."""
        # Setup mocks
        mock_game = Mock()
        mock_ui = Mock()
        mock_tictactoe.return_value = mock_game
        mock_gameui.return_value = mock_ui

        # Mock pygame events to exit immediately
        mock_quit_event = Mock()
        mock_quit_event.type = 1  # QUIT event type
        mock_event_get.return_value = [mock_quit_event]

        from src.main import main
        main()

        # Verify components are created
        mock_tictactoe.assert_called_once()
        mock_gameui.assert_called_once()

        # Verify initial UI setup
        mock_ui.show_welcome_screen.assert_called_once()
        mock_ui.draw_board.assert_called_once()
        mock_ui.draw_status.assert_called_once_with(mock_game)
        mock_ui.update_display.assert_called()

    @patch('src.main.sys.exit')
    @patch('src.main.GameUI')
    @patch('src.main.TicTacToe')
    @patch('src.main.pygame.event.get')
    @patch('src.main.QUIT', 1)  # Mock the QUIT constant
    def test_main_game_loop_quit_event(self, mock_event_get, mock_tictactoe, mock_gameui, mock_exit):
        """Test main game loop handles quit event."""
        # Setup mocks
        mock_game = Mock()
        mock_ui = Mock()
        mock_tictactoe.return_value = mock_game
        mock_gameui.return_value = mock_ui

        # Mock quit event
        mock_quit_event = Mock()
        mock_quit_event.type = 1  # QUIT event type
        mock_event_get.return_value = [mock_quit_event]

        from src.main import main
        main()

        # Verify cleanup
        mock_ui.quit.assert_called_once()
        mock_exit.assert_called_once()

    @patch('src.main.handle_mouse_click')
    @patch('src.main.sys.exit')
    @patch('src.main.GameUI')
    @patch('src.main.TicTacToe')
    @patch('src.main.pygame.event.get')
    @patch('src.main.MOUSEBUTTONDOWN', 2)  # Mock the MOUSEBUTTONDOWN constant
    @patch('src.main.QUIT', 1)  # Mock the QUIT constant
    def test_main_game_loop_mouse_event(self, mock_event_get, mock_tictactoe, mock_gameui, mock_exit, mock_handle_click):
        """Test main game loop handles mouse events."""
        # Setup mocks
        mock_game = Mock()
        mock_ui = Mock()
        mock_tictactoe.return_value = mock_game
        mock_gameui.return_value = mock_ui

        # Mock mouse click event followed by quit event
        mock_mouse_event = Mock()
        mock_mouse_event.type = 2  # MOUSEBUTTONDOWN event type
        mock_mouse_event.pos = (100, 100)

        mock_quit_event = Mock()
        mock_quit_event.type = 1  # QUIT event type

        mock_event_get.side_effect = [
            [mock_mouse_event],  # First iteration: mouse click
            [mock_quit_event],   # Second iteration: quit
        ]

        from src.main import main
        main()

        # Verify mouse click was handled
        mock_handle_click.assert_called_once_with((100, 100), mock_game, mock_ui)

    @patch('src.main.sys.exit')
    @patch('src.main.GameUI')
    @patch('src.main.TicTacToe')
    @patch('src.main.pygame.event.get')
    @patch('src.main.QUIT', 1)  # Mock the QUIT constant
    def test_main_game_loop_tick_called(self, mock_event_get, mock_tictactoe, mock_gameui, mock_exit):
        """Test main game loop calls UI tick."""
        # Setup mocks
        mock_game = Mock()
        mock_ui = Mock()
        mock_tictactoe.return_value = mock_game
        mock_gameui.return_value = mock_ui

        # Mock quit event to exit after one iteration
        mock_quit_event = Mock()
        mock_quit_event.type = 1  # QUIT event type
        mock_event_get.return_value = [mock_quit_event]

        from src.main import main
        main()

        # Verify tick was called
        mock_ui.tick.assert_called()


class TestHandleMouseClick:
    """Test mouse click handling function."""

    def test_handle_mouse_click_invalid_cell(self):
        """Test handling click outside valid game area."""
        from src.main import handle_mouse_click
        
        mock_game = Mock()
        mock_ui = Mock()
        mock_ui.get_clicked_cell.return_value = None
        
        handle_mouse_click((500, 500), mock_game, mock_ui)
        
        # Should not attempt to make a move
        mock_game.make_move.assert_not_called()

    def test_handle_mouse_click_valid_cell_successful_move(self):
        """Test handling valid click that results in successful move."""
        from src.main import handle_mouse_click
        
        mock_game = Mock()
        mock_game.make_move.return_value = True
        mock_game.game_state = constants.GAME_ACTIVE
        
        mock_ui = Mock()
        mock_ui.get_clicked_cell.return_value = (1, 1)
        
        handle_mouse_click((150, 150), mock_game, mock_ui)
        
        # Verify move was attempted
        mock_game.make_move.assert_called_once_with(1, 1)
        
        # Verify UI was updated
        mock_ui.draw_board.assert_called_once()
        mock_ui.draw_symbols.assert_called_once_with(mock_game)
        mock_ui.draw_status.assert_called_once_with(mock_game)
        mock_ui.update_display.assert_called()

    def test_handle_mouse_click_valid_cell_failed_move(self):
        """Test handling valid click that results in failed move."""
        from src.main import handle_mouse_click
        
        mock_game = Mock()
        mock_game.make_move.return_value = False
        
        mock_ui = Mock()
        mock_ui.get_clicked_cell.return_value = (1, 1)
        
        handle_mouse_click((150, 150), mock_game, mock_ui)
        
        # Verify move was attempted
        mock_game.make_move.assert_called_once_with(1, 1)
        
        # Verify UI was not updated (since move failed)
        mock_ui.draw_board.assert_not_called()
        mock_ui.draw_symbols.assert_not_called()

    @patch('src.main.time.sleep')
    def test_handle_mouse_click_winning_move(self, mock_sleep):
        """Test handling click that results in winning move."""
        from src.main import handle_mouse_click
        
        mock_game = Mock()
        mock_game.make_move.return_value = True
        mock_game.game_state = constants.GAME_WON
        
        mock_ui = Mock()
        mock_ui.get_clicked_cell.return_value = (0, 2)
        
        handle_mouse_click((250, 50), mock_game, mock_ui)
        
        # Verify winning line is drawn
        mock_ui.draw_winning_line.assert_called_once_with(mock_game)
        
        # Verify game reset sequence
        mock_sleep.assert_called_once_with(3)
        mock_game.reset_game.assert_called_once()
        
        # Verify UI is redrawn after reset
        assert mock_ui.draw_board.call_count == 2  # Once for move, once for reset
        assert mock_ui.draw_status.call_count == 2  # Once for move, once for reset

    @patch('src.main.time.sleep')
    def test_handle_mouse_click_draw_move(self, mock_sleep):
        """Test handling click that results in draw."""
        from src.main import handle_mouse_click
        
        mock_game = Mock()
        mock_game.make_move.return_value = True
        mock_game.game_state = constants.GAME_DRAW
        
        mock_ui = Mock()
        mock_ui.get_clicked_cell.return_value = (2, 1)
        
        handle_mouse_click((150, 250), mock_game, mock_ui)
        
        # Verify no winning line is drawn for draw
        mock_ui.draw_winning_line.assert_not_called()
        
        # Verify game reset sequence
        mock_sleep.assert_called_once_with(3)
        mock_game.reset_game.assert_called_once()

    def test_handle_mouse_click_active_game_no_reset(self):
        """Test handling click in active game doesn't trigger reset."""
        from src.main import handle_mouse_click
        
        mock_game = Mock()
        mock_game.make_move.return_value = True
        mock_game.game_state = constants.GAME_ACTIVE
        
        mock_ui = Mock()
        mock_ui.get_clicked_cell.return_value = (1, 0)
        
        with patch('src.main.time.sleep') as mock_sleep:
            handle_mouse_click((50, 150), mock_game, mock_ui)
        
        # Verify no reset occurs
        mock_sleep.assert_not_called()
        mock_game.reset_game.assert_not_called()


class TestGameIntegration:
    """Test integration between game components."""

    @patch('src.main.time.sleep')
    def test_complete_game_flow_x_wins(self, mock_sleep):
        """Test complete game flow where X wins."""
        from src.main import handle_mouse_click
        from src.game_logic import TicTacToe
        import src.constants as constants

        # Use real game logic with mocked UI
        game = TicTacToe()
        mock_ui = Mock()

        # Mock UI responses for winning sequence
        click_sequence = [
            ((50, 50), (0, 0)),    # X at (0,0)
            ((50, 150), (1, 0)),   # O at (1,0)
            ((150, 50), (0, 1)),   # X at (0,1)
            ((150, 150), (1, 1)),  # O at (1,1)
            ((250, 50), (0, 2)),   # X at (0,2) - wins!
        ]

        for i, (mouse_pos, cell_pos) in enumerate(click_sequence):
            mock_ui.get_clicked_cell.return_value = cell_pos
            mock_ui.reset_mock()

            if i == 4:  # The winning move
                # Check state before the winning move
                assert game.game_state == constants.GAME_ACTIVE

                handle_mouse_click(mouse_pos, game, mock_ui)

                # After the winning move, the game should have been won and then reset
                # So we check that the UI methods were called correctly
                mock_ui.draw_winning_line.assert_called_once()
                mock_sleep.assert_called_once_with(3)

                # Game should be reset to active state
                assert game.game_state == constants.GAME_ACTIVE
                assert game.winner is None
            else:
                handle_mouse_click(mouse_pos, game, mock_ui)
                # Verify UI updates for non-winning moves
                assert game.game_state == constants.GAME_ACTIVE

    @patch('src.main.time.sleep')
    def test_complete_game_flow_draw(self, mock_sleep):
        """Test complete game flow that ends in draw."""
        from src.main import handle_mouse_click
        from src.game_logic import TicTacToe
        import src.constants as constants

        # Use real game logic with mocked UI
        game = TicTacToe()
        mock_ui = Mock()

        # Sequence that leads to draw
        draw_sequence = [
            ((50, 50), (0, 0)),      # X
            ((150, 50), (0, 1)),     # O
            ((250, 50), (0, 2)),     # X
            ((50, 150), (1, 0)),     # O
            ((250, 150), (1, 2)),    # X
            ((150, 150), (1, 1)),    # O
            ((50, 250), (2, 0)),     # X
            ((250, 250), (2, 2)),    # O
            ((150, 250), (2, 1)),    # X - draw!
        ]

        for i, (mouse_pos, cell_pos) in enumerate(draw_sequence):
            mock_ui.get_clicked_cell.return_value = cell_pos
            mock_ui.reset_mock()

            if i == 8:  # The final move that causes draw
                # Check state before the final move
                assert game.game_state == constants.GAME_ACTIVE

                handle_mouse_click(mouse_pos, game, mock_ui)

                # After the draw move, the game should have been drawn and then reset
                mock_sleep.assert_called_once_with(3)

                # Game should be reset to active state
                assert game.game_state == constants.GAME_ACTIVE
                assert game.winner is None
            else:
                handle_mouse_click(mouse_pos, game, mock_ui)
                # Verify UI updates for non-final moves
                assert game.game_state == constants.GAME_ACTIVE

    def test_invalid_moves_ignored(self):
        """Test that invalid moves are properly ignored."""
        from src.main import handle_mouse_click
        from src.game_logic import TicTacToe
        
        game = TicTacToe()
        mock_ui = Mock()
        
        # Make a valid move first
        mock_ui.get_clicked_cell.return_value = (0, 0)
        handle_mouse_click((50, 50), game, mock_ui)
        
        assert game.board[0][0] == constants.PLAYER_X
        assert game.current_player == constants.PLAYER_O
        
        # Try to make move in same position
        mock_ui.reset_mock()
        mock_ui.get_clicked_cell.return_value = (0, 0)
        handle_mouse_click((50, 50), game, mock_ui)
        
        # Game state should be unchanged
        assert game.board[0][0] == constants.PLAYER_X
        assert game.current_player == constants.PLAYER_O  # Still O's turn
        
        # UI should not be updated for invalid move
        mock_ui.draw_board.assert_not_called()

    def test_clicks_outside_board_ignored(self):
        """Test that clicks outside the board are ignored."""
        from src.main import handle_mouse_click
        from src.game_logic import TicTacToe
        
        game = TicTacToe()
        mock_ui = Mock()
        
        # Click outside board
        mock_ui.get_clicked_cell.return_value = None
        handle_mouse_click((500, 500), game, mock_ui)
        
        # Game state should be unchanged
        assert game.current_player == constants.PLAYER_X
        assert all(cell is None for row in game.board for cell in row)
        
        # UI should not be updated
        mock_ui.draw_board.assert_not_called()


class TestMainModuleImports:
    """Test main module imports and dependencies."""

    def test_required_imports_available(self):
        """Test that all required modules can be imported."""
        try:
            import src.main as main
            from src.main import main as main_func, handle_mouse_click
            
            # Verify functions exist
            assert callable(main_func)
            assert callable(handle_mouse_click)
            
        except ImportError as e:
            pytest.fail(f"Failed to import main module: {e}")

    def test_constants_imported_correctly(self):
        """Test that constants are imported correctly."""
        import src.main as main

        # Verify constants are accessible through the main module's imports
        # The main module imports GAME_WON and GAME_DRAW from constants
        assert hasattr(main, 'GAME_WON')
        assert hasattr(main, 'GAME_DRAW')
        assert main.GAME_WON == "won"
        assert main.GAME_DRAW == "draw"

    def test_pygame_imports_available(self):
        """Test that pygame imports are available."""
        import src.main as main
        
        # Verify pygame components are imported
        assert hasattr(main, 'pygame')
        assert hasattr(main, 'MOUSEBUTTONDOWN')
        assert hasattr(main, 'QUIT')
