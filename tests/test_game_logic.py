"""Tests for the game logic module."""

import pytest

from src.game_logic import TicTacToe
import src.constants as constants


class TestTicTacToeInitialization:
    """Test TicTacToe class initialization."""

    def test_initial_state(self, game_instance):
        """Test game initializes with correct default state."""
        assert game_instance.current_player == constants.PLAYER_X
        assert game_instance.winner is None
        assert game_instance.game_state == constants.GAME_ACTIVE

    def test_initial_board(self, game_instance):
        """Test board initializes as empty 3x3 grid."""
        expected_board = [[None, None, None], [None, None, None], [None, None, None]]
        assert game_instance.board == expected_board
        assert len(game_instance.board) == constants.BOARD_SIZE
        assert all(len(row) == constants.BOARD_SIZE for row in game_instance.board)


class TestGameReset:
    """Test game reset functionality."""

    def test_reset_after_moves(self, game_with_moves):
        """Test reset clears board and resets state."""
        # Verify game has moves
        assert any(cell is not None for row in game_with_moves.board for cell in row)
        
        game_with_moves.reset_game()
        
        # Verify reset state
        assert game_with_moves.current_player == constants.PLAYER_X
        assert game_with_moves.winner is None
        assert game_with_moves.game_state == constants.GAME_ACTIVE
        assert all(cell is None for row in game_with_moves.board for cell in row)

    def test_reset_after_win(self, winning_game_x):
        """Test reset after game is won."""
        # Verify game is won
        assert winning_game_x.game_state == constants.GAME_WON
        assert winning_game_x.winner == constants.PLAYER_X
        
        winning_game_x.reset_game()
        
        # Verify reset state
        assert winning_game_x.current_player == constants.PLAYER_X
        assert winning_game_x.winner is None
        assert winning_game_x.game_state == constants.GAME_ACTIVE

    def test_reset_after_draw(self, draw_game):
        """Test reset after game is drawn."""
        # Verify game is drawn
        assert draw_game.game_state == constants.GAME_DRAW
        
        draw_game.reset_game()
        
        # Verify reset state
        assert draw_game.current_player == constants.PLAYER_X
        assert draw_game.winner is None
        assert draw_game.game_state == constants.GAME_ACTIVE


class TestMakeMove:
    """Test make_move functionality."""

    def test_valid_first_move(self, game_instance):
        """Test making a valid first move."""
        result = game_instance.make_move(0, 0)
        
        assert result is True
        assert game_instance.board[0][0] == constants.PLAYER_X
        assert game_instance.current_player == constants.PLAYER_O

    def test_valid_second_move(self, game_instance):
        """Test making valid consecutive moves."""
        game_instance.make_move(0, 0)  # X
        result = game_instance.make_move(1, 1)  # O
        
        assert result is True
        assert game_instance.board[1][1] == constants.PLAYER_O
        assert game_instance.current_player == constants.PLAYER_X

    def test_invalid_move_occupied_cell(self, game_instance):
        """Test move to already occupied cell fails."""
        game_instance.make_move(0, 0)  # X
        result = game_instance.make_move(0, 0)  # Try to place O in same spot
        
        assert result is False
        assert game_instance.board[0][0] == constants.PLAYER_X  # Unchanged
        assert game_instance.current_player == constants.PLAYER_O  # Unchanged

    def test_invalid_move_out_of_bounds(self, game_instance):
        """Test moves outside board boundaries fail."""
        invalid_positions = [(-1, 0), (0, -1), (3, 0), (0, 3), (-1, -1), (3, 3)]
        
        for row, col in invalid_positions:
            result = game_instance.make_move(row, col)
            assert result is False
            assert game_instance.current_player == constants.PLAYER_X  # Unchanged

    def test_move_after_game_won(self, winning_game_x):
        """Test moves are rejected after game is won."""
        result = winning_game_x.make_move(1, 2)
        
        assert result is False
        assert winning_game_x.game_state == constants.GAME_WON

    def test_move_after_game_drawn(self, draw_game):
        """Test moves are rejected after game is drawn."""
        # Try to make a move (shouldn't be possible as board is full)
        result = draw_game.make_move(0, 0)
        
        assert result is False
        assert draw_game.game_state == constants.GAME_DRAW


class TestPlayerSwitching:
    """Test player switching logic."""

    def test_alternating_players(self, game_instance):
        """Test players alternate correctly."""
        assert game_instance.current_player == constants.PLAYER_X
        
        game_instance.make_move(0, 0)
        assert game_instance.current_player == constants.PLAYER_O
        
        game_instance.make_move(1, 1)
        assert game_instance.current_player == constants.PLAYER_X
        
        game_instance.make_move(0, 1)
        assert game_instance.current_player == constants.PLAYER_O

    def test_no_switch_on_invalid_move(self, game_instance):
        """Test player doesn't switch on invalid move."""
        game_instance.make_move(0, 0)  # X
        current_player = game_instance.current_player  # Should be O
        
        game_instance.make_move(0, 0)  # Invalid move
        assert game_instance.current_player == current_player  # Unchanged

    def test_no_switch_on_winning_move(self, game_instance):
        """Test player doesn't switch when making winning move."""
        # Set up a winning scenario for X
        game_instance.make_move(0, 0)  # X
        game_instance.make_move(1, 0)  # O
        game_instance.make_move(0, 1)  # X
        game_instance.make_move(1, 1)  # O
        
        # X makes winning move
        game_instance.make_move(0, 2)  # X wins
        
        assert game_instance.current_player == constants.PLAYER_X  # No switch
        assert game_instance.game_state == constants.GAME_WON


class TestWinDetection:
    """Test win detection logic."""

    def test_row_wins(self, game_instance):
        """Test detection of row wins."""
        # Test each row
        for row in range(3):
            game_instance.reset_game()
            
            # X wins the row
            for col in range(3):
                game_instance.make_move(row, col)  # X
                if col < 2:  # Don't place O after winning move
                    game_instance.make_move((row + 1) % 3, col)  # O
            
            assert game_instance.game_state == constants.GAME_WON
            assert game_instance.winner == constants.PLAYER_X

    def test_column_wins(self, game_instance):
        """Test detection of column wins."""
        # Test each column
        for col in range(3):
            game_instance.reset_game()
            
            # X wins the column
            for row in range(3):
                game_instance.make_move(row, col)  # X
                if row < 2:  # Don't place O after winning move
                    game_instance.make_move(row, (col + 1) % 3)  # O
            
            assert game_instance.game_state == constants.GAME_WON
            assert game_instance.winner == constants.PLAYER_X

    def test_main_diagonal_win(self, game_instance):
        """Test detection of main diagonal win."""
        # X wins main diagonal (0,0), (1,1), (2,2)
        game_instance.make_move(0, 0)  # X
        game_instance.make_move(0, 1)  # O
        game_instance.make_move(1, 1)  # X
        game_instance.make_move(0, 2)  # O
        game_instance.make_move(2, 2)  # X wins
        
        assert game_instance.game_state == constants.GAME_WON
        assert game_instance.winner == constants.PLAYER_X

    def test_anti_diagonal_win(self, game_instance):
        """Test detection of anti-diagonal win."""
        # X wins anti-diagonal (0,2), (1,1), (2,0)
        game_instance.make_move(0, 2)  # X
        game_instance.make_move(0, 1)  # O
        game_instance.make_move(1, 1)  # X
        game_instance.make_move(0, 0)  # O
        game_instance.make_move(2, 0)  # X wins
        
        assert game_instance.game_state == constants.GAME_WON
        assert game_instance.winner == constants.PLAYER_X

    def test_o_player_wins(self, game_instance):
        """Test O player can also win."""
        # O wins first column
        game_instance.make_move(0, 1)  # X
        game_instance.make_move(0, 0)  # O
        game_instance.make_move(1, 1)  # X
        game_instance.make_move(1, 0)  # O
        game_instance.make_move(0, 2)  # X
        game_instance.make_move(2, 0)  # O wins
        
        assert game_instance.game_state == constants.GAME_WON
        assert game_instance.winner == constants.PLAYER_O


class TestDrawDetection:
    """Test draw detection logic."""

    def test_draw_game(self, draw_game):
        """Test draw is detected when board is full with no winner."""
        assert draw_game.game_state == constants.GAME_DRAW
        assert draw_game.winner is None

    def test_no_draw_with_winner(self, winning_game_x):
        """Test draw is not detected when there's a winner."""
        assert winning_game_x.game_state == constants.GAME_WON
        assert winning_game_x.game_state != constants.GAME_DRAW

    def test_no_draw_with_empty_spaces(self, game_with_moves):
        """Test draw is not detected when board has empty spaces."""
        assert game_with_moves.game_state == constants.GAME_ACTIVE
        assert game_with_moves.game_state != constants.GAME_DRAW


class TestWinningLineDetection:
    """Test winning line detection."""

    def test_winning_line_row(self, game_instance):
        """Test winning line detection for row wins."""
        # X wins row 0
        game_instance.make_move(0, 0)  # X
        game_instance.make_move(1, 0)  # O
        game_instance.make_move(0, 1)  # X
        game_instance.make_move(1, 1)  # O
        game_instance.make_move(0, 2)  # X wins
        
        winning_line = game_instance.get_winning_line()
        assert winning_line == ("row", 0)

    def test_winning_line_column(self, game_instance):
        """Test winning line detection for column wins."""
        # O wins column 1
        game_instance.make_move(0, 0)  # X
        game_instance.make_move(0, 1)  # O
        game_instance.make_move(1, 0)  # X
        game_instance.make_move(1, 1)  # O
        game_instance.make_move(0, 2)  # X
        game_instance.make_move(2, 1)  # O wins
        
        winning_line = game_instance.get_winning_line()
        assert winning_line == ("col", 1)

    def test_winning_line_main_diagonal(self, game_instance):
        """Test winning line detection for main diagonal."""
        # X wins main diagonal
        game_instance.make_move(0, 0)  # X
        game_instance.make_move(0, 1)  # O
        game_instance.make_move(1, 1)  # X
        game_instance.make_move(0, 2)  # O
        game_instance.make_move(2, 2)  # X wins
        
        winning_line = game_instance.get_winning_line()
        assert winning_line == ("diagonal_main", 0)

    def test_winning_line_anti_diagonal(self, game_instance):
        """Test winning line detection for anti-diagonal."""
        # X wins anti-diagonal
        game_instance.make_move(0, 2)  # X
        game_instance.make_move(0, 1)  # O
        game_instance.make_move(1, 1)  # X
        game_instance.make_move(0, 0)  # O
        game_instance.make_move(2, 0)  # X wins
        
        winning_line = game_instance.get_winning_line()
        assert winning_line == ("diagonal_anti", 0)

    def test_no_winning_line_active_game(self, game_with_moves):
        """Test no winning line for active game."""
        winning_line = game_with_moves.get_winning_line()
        assert winning_line is None

    def test_no_winning_line_draw_game(self, draw_game):
        """Test no winning line for draw game."""
        winning_line = draw_game.get_winning_line()
        assert winning_line is None


class TestPrivateMethods:
    """Test private helper methods."""

    def test_is_valid_position(self, game_instance):
        """Test position validation."""
        # Valid positions
        valid_positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        for row, col in valid_positions:
            assert game_instance._is_valid_position(row, col) is True
        
        # Invalid positions
        invalid_positions = [(-1, 0), (0, -1), (3, 0), (0, 3), (-1, -1), (3, 3), (10, 10)]
        for row, col in invalid_positions:
            assert game_instance._is_valid_position(row, col) is False

    def test_is_board_full(self, game_instance):
        """Test board full detection."""
        # Empty board
        assert game_instance._is_board_full() is False
        
        # Partially filled board
        game_instance.make_move(0, 0)
        assert game_instance._is_board_full() is False
        
        # Full board
        for row in range(3):
            for col in range(3):
                if game_instance.board[row][col] is None:
                    game_instance.board[row][col] = constants.PLAYER_X
        
        assert game_instance._is_board_full() is True

    def test_check_winner_no_winner(self, game_with_moves):
        """Test winner check returns None when no winner."""
        winner = game_with_moves._check_winner()
        assert winner is None

    def test_check_winner_with_winner(self, winning_game_x):
        """Test winner check returns correct winner."""
        winner = winning_game_x._check_winner()
        assert winner == constants.PLAYER_X
