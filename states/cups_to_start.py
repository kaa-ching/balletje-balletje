"""Cups to start positions state for the game."""

import pygame
from cup import Cup
from states.base_state import BaseGameState
import layout


class CupsToStart(BaseGameState):
    """The state where cups move to their starting positions."""
    
    def __init__(self, game, ball_position: str):
        """Initialize the cups to start positions state.
        
        Args:
            game: Reference to the main Game instance
            ball_position: Which position the ball is hidden at ("left", "middle", or "right")
        """
        super().__init__(game)
        self.ball_position = ball_position
        
        # Get existing cups from previous state
        if hasattr(game, 'cups') and game.cups:
            self.cups = game.cups
        else:
            # Fallback: create cups (shouldn't happen in normal flow)
            self.cups = [
                Cup(0, layout.POSITION_LEFT - Cup.WIDTH // 2, layout.VERTICAL_CENTER - Cup.HEIGHT // 2),
                Cup(1, layout.POSITION_MIDDLE - Cup.WIDTH // 2, layout.VERTICAL_CENTER - Cup.HEIGHT // 2),
                Cup(2, layout.POSITION_RIGHT - Cup.WIDTH // 2, layout.VERTICAL_CENTER - Cup.HEIGHT // 2),
            ]
            if self.ball_position == "left":
                self.cups[0].set_has_ball(True)
            elif self.ball_position == "middle":
                self.cups[1].set_has_ball(True)
            else:
                self.cups[2].set_has_ball(True)
        
        # Move cups to starting positions (different heights)
        # Left and right cups move up, middle cup moves down
        center_y = layout.get_cup_center_y()
        up_y = layout.get_cup_up_position()
        down_y = layout.get_cup_down_position()
        
        self.cups[0].move_to(self.cups[0].x, up_y)  # Left moves up
        self.cups[1].move_to(self.cups[1].x, down_y)  # Middle moves down
        self.cups[2].move_to(self.cups[2].x, up_y)  # Right moves up
        
        self.animation_complete = False
    
    def on_key_down(self, key: int):
        """Handle key press events.
        
        Args:
            key: The pygame key code
        """
        pass  # No input needed - auto-transitions to shuffling
    
    def update(self, dt: float):
        """Update the cups to start positions state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update backdrop (moving up - ball hidden by cups)
        self.backdrop.update(dt, direction="up")
        
        # Update cups
        all_cups_stopped = True
        for cup in self.cups:
            cup.update(dt)
            if cup.moving:
                all_cups_stopped = False
        
        if all_cups_stopped and not self.animation_complete:
            self.animation_complete = True
            # Store cups in game for next state
            self.game.cups = self.cups
            print("Cups ready at starting positions!")
            # Auto-transition to shuffling
            from game import GameState
            self.game.change_state(GameState.SHUFFLING)
    
    def draw(self, surface: pygame.Surface):
        """Draw the cups to start positions state.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Message shows during positioning
        message = "Klaar? Let op de bekers..."
        
        # Draw base elements (backdrop, border, message bar)
        self._draw_base(surface, message)
        
        # Draw cups
        for cup in self.cups:
            cup.draw(surface)
