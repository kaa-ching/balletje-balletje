"""Ball visible state for the game."""

import pygame
import random
from backdrop import Backdrop
from ball import Ball


class BallVisible:
    """The ball visible state of the game."""
    
    # Layout constants (from game.py)
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    BORDER_SIZE = 100
    MESSAGE_BAR_HEIGHT = 150
    
    def __init__(self, game):
        """Initialize the ball visible state.
        
        Args:
            game: Reference to the main Game instance
        """
        self.game = game
        self.backdrop = Backdrop(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # Create ball at random position
        random_position = random.choice(["left", "middle", "right"])
        self.ball = Ball(random_position)
        print(f"Ball created at position: {random_position} ({self.ball.x}, {self.ball.y})")
    
    def on_key_down(self, key: int):
        """Handle key press events.
        
        Args:
            key: The pygame key code
        """
        if key == pygame.K_SPACE:
            # Return to start screen
            from game import GameState
            self.game.change_state(GameState.START_SCREEN)
    
    def update(self, dt: float):
        """Update the ball visible state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update backdrop (moving down)
        self.backdrop.update(dt, direction="down")
    
    def draw(self, surface: pygame.Surface):
        """Draw the ball visible state.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Draw backdrop
        self.backdrop.draw(surface)
        
        # Draw border
        self._draw_border(surface)
        
        # Draw ball
        self.ball.draw(surface)
        
        # Draw message bar
        self._draw_message_bar(surface)
    
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
    
    def _draw_message_bar(self, surface: pygame.Surface):
        """Draw the message bar at the bottom."""
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
        message = "Press SPACE to continue"
        text = font.render(message, True, (200, 200, 255))
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT // 2))
        surface.blit(text, text_rect)
