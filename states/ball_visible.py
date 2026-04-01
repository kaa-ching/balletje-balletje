"""Ball visible state for the game."""

import pygame
import random
from ball import Ball
from states.base_state import BaseGameState
import layout


class BallVisible(BaseGameState):
    """The ball visible state of the game."""
    
    def __init__(self, game):
        """Initialize the ball visible state.
        
        Args:
            game: Reference to the main Game instance
        """
        super().__init__(game)
        
        # Create ball at random position
        random_position = random.choice(["left", "middle", "right"])
        self.ball = Ball(random_position)
    
    def on_key_down(self, key: int):
        """Handle key press events.
        
        Args:
            key: The pygame key code
        """
        if key == pygame.K_SPACE:
            # Save ball position and pass ball object to cups moving state
            self.game.ball_position = self.ball.position
            self.game.ball_object = self.ball
            from game import GameState
            self.game.change_state(GameState.CUPS_MOVING)
    
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
        # Draw base elements (backdrop, border, message bar)
        self._draw_base(surface, "Press SPACE to continue")
        
        # Draw ball
        self.ball.draw(surface)
