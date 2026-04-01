"""Base state class for the game."""

import pygame
import layout


class BaseGameState:
    """Base class for all game states."""
    
    # Layout constants - imported from centralized layout module
    SCREEN_WIDTH = layout.SCREEN_WIDTH
    SCREEN_HEIGHT = layout.SCREEN_HEIGHT
    BORDER_SIZE = layout.BORDER_SIZE
    MESSAGE_BAR_HEIGHT = layout.MESSAGE_BAR_HEIGHT
    
    def __init__(self, game):
        """Initialize the game state.
        
        Args:
            game: Reference to the main Game instance
        """
        self.game = game
    
    def on_key_down(self, key: int):
        """Handle key press events. Override in subclasses."""
        pass
    
    def update(self, dt: float):
        """Update the game state. Override in subclasses."""
        pass
    
    def draw(self, surface: pygame.Surface):
        """Draw the game state. Override in subclasses."""
        pass
    
    def _draw_border(self, surface: pygame.Surface):
        """Draw the border around the play area."""
        # Top border
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, self.SCREEN_WIDTH, self.BORDER_SIZE))
        # Bottom border (above message bar)
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (0, self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT - self.BORDER_SIZE, self.SCREEN_WIDTH, self.BORDER_SIZE)
        )
        # Left border
        pygame.draw.rect(surface, (0, 0, 0), (0, self.BORDER_SIZE, self.BORDER_SIZE, self.SCREEN_HEIGHT - self.BORDER_SIZE - self.MESSAGE_BAR_HEIGHT))
        # Right border
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (self.SCREEN_WIDTH - self.BORDER_SIZE, self.BORDER_SIZE, self.BORDER_SIZE, self.SCREEN_HEIGHT - self.BORDER_SIZE - self.MESSAGE_BAR_HEIGHT)
        )
    
    def _draw_message_bar(self, surface: pygame.Surface, message: str):
        """Draw the message bar at the bottom.
        
        Args:
            surface: The pygame surface to draw on
            message: The message text to display
        """
        # Draw message bar background
        message_bar_rect = pygame.Rect(
            0,
            self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT,
            self.SCREEN_WIDTH,
            self.MESSAGE_BAR_HEIGHT
        )
        pygame.draw.rect(surface, (40, 40, 60), message_bar_rect)
        pygame.draw.rect(surface, (100, 100, 150), message_bar_rect, 3)
        
        # Draw message text
        font = pygame.font.Font(None, 72)
        text = font.render(message, True, (200, 200, 255))
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT // 2))
        surface.blit(text, text_rect)
