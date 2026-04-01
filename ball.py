"""Ball class for the game."""

import pygame
import layout


class Ball:
    """Represents the ball in the game."""
    
    # Ball dimensions
    RADIUS = 90  # 6x larger than original
    COLOR = (240, 240, 200)  # Light cream color
    
    # Positions - use centralized layout constants
    POSITION_LEFT = layout.POSITION_LEFT
    POSITION_MIDDLE = layout.POSITION_MIDDLE
    POSITION_RIGHT = layout.POSITION_RIGHT
    VERTICAL_CENTER = layout.VERTICAL_CENTER
    
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
