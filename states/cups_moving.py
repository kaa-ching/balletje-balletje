"""Cups moving state for the game."""

import pygame
import logging
from cup import Cup
from states.base_state import BaseGameState
import layout

logger = logging.getLogger('cups_moving')


class CupsMoving(BaseGameState):
    """The cups moving state of the game."""
    
    def __init__(self, game, ball_position: str):
        """Initialize the cups moving state.
        
        Args:
            game: Reference to the main Game instance
            ball_position: Which position the ball is at ("left", "middle", or "right")
        """
        super().__init__(game)
        self.ball_position = ball_position
        self.ball = game.ball_object  # Get the ball object from the game
        self.ball_hidden = False  # Track if ball has been hidden
        
        # Calculate cup positions using centralized layout constants
        position_left = layout.POSITION_LEFT
        position_middle = layout.POSITION_MIDDLE
        position_right = layout.POSITION_RIGHT
        final_y = layout.VERTICAL_CENTER - Cup.HEIGHT // 2
        
        # Create cups starting from top of screen
        self.cups = [
            Cup(0, position_left - Cup.WIDTH // 2, -200),
            Cup(1, position_middle - Cup.WIDTH // 2, -200),
            Cup(2, position_right - Cup.WIDTH // 2, -200),
        ]
        
        # Set which cup has the ball
        if self.ball_position == "left":
            self.cups[0].set_has_ball(True)
        elif self.ball_position == "middle":
            self.cups[1].set_has_ball(True)
        else:  # right
            self.cups[2].set_has_ball(True)
        
        # Move cups to final position
        for cup in self.cups:
            cup.move_to(cup.x, final_y)
        
        self.animation_complete = False
    
    def get_valid_keys(self) -> dict:
        """Get valid key mappings for this state."""
        return {}  # No public keys for this state
    
    def get_status_message(self) -> str:
        """Get the main status message for this state."""
        return "Bekers komen eraan..."
    
    def on_key_down(self, key: int):
        """Handle key press events.
        
        Args:
            key: The pygame key code
        """
        pass  # No key handling needed for this state
    
    def update(self, dt: float):
        """Update the cups moving state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update backdrop (moving down)
        self.backdrop.update(dt, direction="down")
        
        # Update ball animation
        self.ball.update(dt)
        
        # Update cups
        all_cups_stopped = True
        for cup in self.cups:
            cup.update(dt)
            if cup.moving:
                all_cups_stopped = False
        
        if all_cups_stopped and not self.animation_complete:
            self.animation_complete = True
            self.ball_hidden = True  # Hide the ball once animation completes
            # Store cups in game for next state
            self.game.cups = self.cups
            logger.info(f"Cups animation complete! Ball was at position: {self.ball_position}")
            # Automatically transition to next state
            from game import GameState
            self.game.change_state(GameState.CUPS_TO_START)
    
    def draw(self, surface: pygame.Surface):
        """Draw the cups moving state.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Draw base elements (backdrop, field frame)
        self._draw_base_background(surface)
        
        # Draw ball (only if not hidden by cups)
        if not self.ball_hidden:
            self.ball.draw(surface)
        
        # Draw cups
        for cup in self.cups:
            cup.draw(surface)
        
        # Draw message bar (handled by base class)
        self._draw_message_bar(surface, self.get_status_message(), self.get_valid_keys())
