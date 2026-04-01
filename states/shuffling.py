"""Shuffling state for the game."""

import pygame
from backdrop import Backdrop
from states.base_state import BaseGameState


class Shuffling(BaseGameState):
    """The shuffling state of the game."""
    
    def __init__(self, game, ball_position: str):
        """Initialize the shuffling state.
        
        Args:
            game: Reference to the main Game instance
            ball_position: Which position the ball is hidden at
        """
        super().__init__(game)
        self.backdrop = Backdrop(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.ball_position = ball_position
        self.cups = game.cups
        print("Shuffling state initialized!")
    
    def on_key_down(self, key: int):
        """Handle key press events."""
        if key == pygame.K_SPACE:
            from game import GameState
            self.game.change_state(GameState.START_SCREEN)
    
    def update(self, dt: float):
        """Update the shuffling state."""
        self.backdrop.update(dt, direction="down")
    
    def draw(self, surface: pygame.Surface):
        """Draw the shuffling state."""
        # Draw backdrop
        self.backdrop.draw(surface)
        
        # Draw border
        self._draw_border(surface)
        
        # Draw cups
        for cup in self.cups:
            cup.draw(surface, debug=True)
        
        # Draw message bar
        self._draw_message_bar(surface, "Shuffling... (Coming soon!)")
