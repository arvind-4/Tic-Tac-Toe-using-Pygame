"""Game logic for Tic-Tac-Toe."""

from constants import BOARD_SIZE, GAME_ACTIVE, GAME_DRAW, GAME_WON, PLAYER_O, PLAYER_X


class TicTacToe:
    """Tic-Tac-Toe game logic handler."""

    def __init__(self) -> None:
        """Initialize a new game."""
        self.board: list[list[str | None]] = [
            [None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)
        ]
        self.current_player = PLAYER_X
        self.winner: str | None = None
        self.game_state = GAME_ACTIVE

    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = PLAYER_X
        self.winner = None
        self.game_state = GAME_ACTIVE

    def make_move(self, row: int, col: int) -> bool:
        """Make a move at the specified position.

        Args:
            row: Row index (0-2)
            col: Column index (0-2)

        Returns:
            True if move was successful, False otherwise

        """
        if (
            self.game_state != GAME_ACTIVE
            or not self._is_valid_position(row, col)
            or self.board[row][col] is not None
        ):
            return False

        self.board[row][col] = self.current_player
        self._check_game_state()

        if self.game_state == GAME_ACTIVE:
            self._switch_player()

        return True

    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if the position is valid."""
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def _switch_player(self) -> None:
        """Switch to the other player."""
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

    def _check_game_state(self) -> None:
        """Check if the game has ended (win or draw)."""
        # Check for winner
        winner = self._check_winner()
        if winner:
            self.winner = winner
            self.game_state = GAME_WON
            return

        # Check for draw
        if self._is_board_full():
            self.game_state = GAME_DRAW

    def _check_winner(self) -> str | None:
        """Check if there's a winner.

        Returns:
            The winning player symbol or None if no winner

        """
        # Check rows
        for row in range(BOARD_SIZE):
            if (
                self.board[row][0] == self.board[row][1] == self.board[row][2]
                and self.board[row][0] is not None
            ):
                return self.board[row][0]

        # Check columns
        for col in range(BOARD_SIZE):
            if (
                self.board[0][col] == self.board[1][col] == self.board[2][col]
                and self.board[0][col] is not None
            ):
                return self.board[0][col]

        # Check diagonals
        if (
            self.board[0][0] == self.board[1][1] == self.board[2][2]
            and self.board[0][0] is not None
        ):
            return self.board[0][0]

        if (
            self.board[0][2] == self.board[1][1] == self.board[2][0]
            and self.board[0][2] is not None
        ):
            return self.board[0][2]

        return None

    def _is_board_full(self) -> bool:
        """Check if the board is full."""
        return all(
            self.board[row][col] is not None
            for row in range(BOARD_SIZE)
            for col in range(BOARD_SIZE)
        )

    def get_winning_line(self) -> tuple[str, int] | None:
        """Get the winning line information.

        Returns:
            Tuple of (line_type, index) where line_type is 'row', 'col',
            'diagonal_main', or 'diagonal_anti', and index is the line number

        """
        if self.winner is None:
            return None

        # Check rows
        for row in range(BOARD_SIZE):
            if (
                self.board[row][0] == self.board[row][1] == self.board[row][2]
                and self.board[row][0] == self.winner
            ):
                return ("row", row)

        # Check columns
        for col in range(BOARD_SIZE):
            if (
                self.board[0][col] == self.board[1][col] == self.board[2][col]
                and self.board[0][col] == self.winner
            ):
                return ("col", col)

        # Check main diagonal (top-left to bottom-right)
        if (
            self.board[0][0] == self.board[1][1] == self.board[2][2]
            and self.board[0][0] == self.winner
        ):
            return ("diagonal_main", 0)

        # Check anti-diagonal (top-right to bottom-left)
        if (
            self.board[0][2] == self.board[1][1] == self.board[2][0]
            and self.board[0][2] == self.winner
        ):
            return ("diagonal_anti", 0)

        return None
