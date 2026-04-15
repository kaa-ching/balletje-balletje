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
        
        # Store ball position and object for next state
        self.game.ball_position = self.ball.position
        self.game.ball_object = self.ball
        
        self.wait_time = 0
        self.min_display_time = 1.5  # Show ball for at least 1.5 seconds
    
    def on_key_down(self, key: int):
        """Handle key press events.
        
        Args:
            key: The pygame key code
        """
        pass  # No input needed - auto-transitions to cups moving
    
    def update(self, dt: float):
        """Update the ball visible state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update backdrop (moving down)
        self.backdrop.update(dt, direction="down")
        
        # Update ball animation
        self.ball.update(dt)
        
        # Auto-transition after minimum display time
        self.wait_time += dt
        if self.wait_time > self.min_display_time:
            from game import GameState
            self.game.change_state(GameState.CUPS_MOVING)
    
    def draw(self, surface: pygame.Surface):
        """Draw the ball visible state.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Draw base elements (backdrop, field frame, message bar)
        self._draw_base(surface, "")
        
        # Draw ball
        self.ball.draw(surface)
