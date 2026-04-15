"""Base state class for the game."""

import pygame
import layout
from backdrop import Backdrop


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
        self.backdrop = Backdrop(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
    
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
        """Draw the field frame when a margin is configured."""
        if self.BORDER_SIZE <= 0:
            return

        # Top frame
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, self.SCREEN_WIDTH, self.BORDER_SIZE))
        # Bottom frame (above message bar)
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (0, self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT - self.BORDER_SIZE, self.SCREEN_WIDTH, self.BORDER_SIZE)
        )
        # Left frame
        pygame.draw.rect(surface, (0, 0, 0), (0, self.BORDER_SIZE, self.BORDER_SIZE, self.SCREEN_HEIGHT - self.BORDER_SIZE - self.MESSAGE_BAR_HEIGHT))
        # Right frame
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
    
    def _all_cups_stopped(self, cups: list) -> bool:
        """Check if all cups have finished moving.
        
        Args:
            cups: List of Cup objects to check
            
        Returns:
            True if all cups are stopped, False otherwise
        """
        return all(not cup.moving for cup in cups)
    
    def _find_cup_with_ball(self, cups: list) -> int:
        """Find the index of the cup that contains the ball.
        
        Args:
            cups: List of Cup objects
            
        Returns:
            Index of the cup with the ball, or None if not found
        """
        for i, cup in enumerate(cups):
            if cup.has_ball:
                return i
        return None
    
    def _draw_base(self, surface: pygame.Surface, message: str = None):
        """Draw the base elements (backdrop, field frame, message bar).
        Convenience method for states without custom content layering.
        
        Args:
            surface: The pygame surface to draw on
            message: Optional message to display (None or empty string for blank bar)
        """
        self._draw_state(surface, message)
    
    def _draw_base_background(self, surface: pygame.Surface):
        """Draw just the backdrop and field frame (without message bar).
        Useful for states that need custom content layering between frame and message.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Draw backdrop
        self.backdrop.draw(surface)
        
        # Draw field frame
        self._draw_border(surface)
    
    def _draw_state(self, surface: pygame.Surface, message: str = None, content_callback=None):
        """Draw a complete state with custom content between backdrop and message bar.
        This is the main drawing helper for all states.
        
        Args:
            surface: The pygame surface to draw on
            message: Message to display in the message bar (None or empty string for blank bar)
            content_callback: Optional function(surface) to call for drawing custom content
                            (called between backdrop/frame and message bar)
        """
        # Draw backdrop and field frame
        self._draw_base_background(surface)
        
        # Draw custom content if provided
        if content_callback:
            content_callback(surface)
        
        # Draw message bar (always visible, even if empty)
        self._draw_message_bar(surface, message or "")
