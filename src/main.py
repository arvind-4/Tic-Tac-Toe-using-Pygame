"""Main entry point for the Tic-Tac-Toe game."""

import sys
import time

import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT

from constants import GAME_DRAW, GAME_WON
from game_logic import TicTacToe
from game_ui import GameUI


def main() -> None:
    """Entry point for the game."""
    # Initialize game components
    game = TicTacToe()
    ui = GameUI()

    # Show welcome screen and initial board
    ui.show_welcome_screen()
    ui.draw_board()
    ui.draw_status(game)
    ui.update_display()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos, game, ui)

        ui.tick()

    ui.quit()
    sys.exit()


def handle_mouse_click(mouse_pos: tuple[int, int], game: TicTacToe, ui: GameUI) -> None:
    """Handle mouse click events."""
    # Get the clicked cell
    cell = ui.get_clicked_cell(mouse_pos)
    if cell is None:
        return

    row, col = cell

    # Try to make a move
    if game.make_move(row, col):
        # Redraw the game
        ui.draw_board()
        ui.draw_symbols(game)

        # Draw winning line if game is won
        if game.game_state == GAME_WON:
            ui.draw_winning_line(game)

        ui.draw_status(game)
        ui.update_display()

        # Reset game after win or draw
        if game.game_state in (GAME_WON, GAME_DRAW):
            time.sleep(3)
            game.reset_game()
            ui.draw_board()
            ui.draw_status(game)
            ui.update_display()


if __name__ == "__main__":
    main()
