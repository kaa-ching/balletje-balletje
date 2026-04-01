"""Cups to start positions state for the game."""

import pygame
from backdrop import Backdrop
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
        self.backdrop = Backdrop(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
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
        center_y = layout.VERTICAL_CENTER - Cup.HEIGHT // 2
        offset = Cup.HEIGHT  # One cup height
        
        self.cups[0].move_to(self.cups[0].x, center_y - offset)  # Left moves up
        self.cups[1].move_to(self.cups[1].x, center_y + offset)  # Middle moves down
        self.cups[2].move_to(self.cups[2].x, center_y - offset)  # Right moves up
        
        self.animation_complete = False
    
    def on_key_down(self, key: int):
        """Handle key press events.
        
        Args:
            key: The pygame key code
        """
        # For now, space skips to start screen (for testing)
        if key == pygame.K_SPACE and self.animation_complete:
            from game import GameState
            self.game.change_state(GameState.SHUFFLING)
    
    def update(self, dt: float):
        """Update the cups to start positions state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update backdrop (moving down)
        self.backdrop.update(dt, direction="down")
        
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
    
    def draw(self, surface: pygame.Surface):
        """Draw the cups to start positions state.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Draw backdrop
        self.backdrop.draw(surface)
        
        # Draw border
        self._draw_border(surface)
        
        # Draw cups
        for cup in self.cups:
            cup.draw(surface, debug=True)
        
        # Draw message bar
        if self.animation_complete:
            self._draw_message_bar(surface, "Get ready! Watch the cups...")
        else:
            self._draw_message_bar(surface, "Setting up...")
