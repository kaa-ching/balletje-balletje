"""Ball class for the game."""

import pygame


class Ball:
    """Represents the ball in the game."""
    
    # Ball dimensions
    RADIUS = 90  # 6x larger than original
    COLOR = (240, 240, 200)  # Light cream color
    
    # Positions (relative to play area)
    PLAY_AREA_LEFT = 100
    PLAY_AREA_WIDTH = 1920 - 200  # Minus borders
    PLAY_AREA_TOP = 100
    PLAY_AREA_HEIGHT = 1080 - 100 - 150  # Minus top and bottom borders/message bar
    
    POSITION_LEFT = PLAY_AREA_LEFT + PLAY_AREA_WIDTH // 6
    POSITION_MIDDLE = PLAY_AREA_LEFT + PLAY_AREA_WIDTH // 2
    POSITION_RIGHT = PLAY_AREA_LEFT + (PLAY_AREA_WIDTH * 5) // 6
    
    VERTICAL_CENTER = PLAY_AREA_TOP + PLAY_AREA_HEIGHT // 2
    
    def __init__(self, position: str = "left"):
        """Initialize the ball at a given position.
        
        Args:
            position: "left", "middle", or "right"
        """
        self.position = position
        
        # Set x position based on position string
        if position == "left":
            self.x = self.POSITION_LEFT
        elif position == "middle":
            self.x = self.POSITION_MIDDLE
        else:  # right
            self.x = self.POSITION_RIGHT
        
        self.y = self.VERTICAL_CENTER
    
    def draw(self, surface: pygame.Surface):
        """Draw the ball to the surface."""
        pygame.draw.circle(surface, self.COLOR, (int(self.x), int(self.y)), self.RADIUS)
        # Add a slight border for definition
        pygame.draw.circle(surface, (200, 200, 150), (int(self.x), int(self.y)), self.RADIUS, 2)
