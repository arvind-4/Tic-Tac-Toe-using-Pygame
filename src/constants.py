"""Constants for the Tic-Tac-Toe game."""

from pathlib import Path

# Game dimensions
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
STATUS_BAR_HEIGHT = 100
TOTAL_HEIGHT = WINDOW_HEIGHT + STATUS_BAR_HEIGHT

# Colors (RGB tuples)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (10, 10, 10)
WINNING_LINE_COLOR = (250, 0, 0)
DIAGONAL_LINE_COLOR = (250, 70, 70)

# Game settings
FPS = 30
BOARD_SIZE = 3
LINE_WIDTH = 7
WINNING_LINE_WIDTH = 4

# Image settings
SYMBOL_SIZE = (80, 80)

# Image paths
ROOT_DIR = Path(__file__).parent.parent
IMAGES_DIR = ROOT_DIR / "images"
WELCOME_IMAGE = IMAGES_DIR / "welcome.png"
X_IMAGE = IMAGES_DIR / "x.png"
O_IMAGE = IMAGES_DIR / "o.png"

# Game symbols
PLAYER_X = "x"
PLAYER_O = "o"

# Font settings
FONT_SIZE = 30
STATUS_Y_POSITION = 450  # 500 - 50

# Grid calculations
CELL_WIDTH = WINDOW_WIDTH // BOARD_SIZE
CELL_HEIGHT = WINDOW_HEIGHT // BOARD_SIZE

# Positioning offsets
SYMBOL_OFFSET = 30

# Game states
GAME_ACTIVE = "active"
GAME_WON = "won"
GAME_DRAW = "draw"
