"""Layout and configuration constants for the game."""

from cup import Cup

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Border dimensions
BORDER_SIZE = 100
MESSAGE_BAR_HEIGHT = 150

# Play area calculated dimensions
PLAY_AREA_LEFT = BORDER_SIZE
PLAY_AREA_TOP = BORDER_SIZE
PLAY_AREA_WIDTH = SCREEN_WIDTH - 2 * BORDER_SIZE
PLAY_AREA_HEIGHT = SCREEN_HEIGHT - 2 * BORDER_SIZE - MESSAGE_BAR_HEIGHT

# Vertical positions
PLAY_AREA_BOTTOM = PLAY_AREA_TOP + PLAY_AREA_HEIGHT
VERTICAL_CENTER = PLAY_AREA_TOP + PLAY_AREA_HEIGHT // 2

# Horizontal positions for ball and cups (3 columns)
POSITION_LEFT = PLAY_AREA_LEFT + PLAY_AREA_WIDTH // 6
POSITION_MIDDLE = PLAY_AREA_LEFT + PLAY_AREA_WIDTH // 2
POSITION_RIGHT = PLAY_AREA_LEFT + (PLAY_AREA_WIDTH * 5) // 6


# Cup position helpers
def get_cup_center_y():
    """Get the vertical center position for cups (accounting for cup height)."""
    return VERTICAL_CENTER - Cup.HEIGHT // 2


def get_cup_up_position():
    """Get the up position for cups (one cup height above center)."""
    center_y = get_cup_center_y()
    return center_y - Cup.HEIGHT


def get_cup_down_position():
    """Get the down position for cups (one cup height below center)."""
    center_y = get_cup_center_y()
    return center_y + Cup.HEIGHT
