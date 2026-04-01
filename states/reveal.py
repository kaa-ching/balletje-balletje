"""Reveal state - show the ball and result."""

import pygame
from backdrop import Backdrop
from states.base_state import BaseGameState
import layout
from cup import Cup
from ball import Ball


class Reveal(BaseGameState):
    """State where the ball is revealed and result is shown."""
    
    def __init__(self, game, ball_position: str, player_guess: int):
        """Initialize the reveal state.
        
        Args:
            game: Reference to the main Game instance
            ball_position: Which position the ball is hidden at ('left', 'middle', 'right')
            player_guess: Which cup the player guessed (0, 1, or 2)
        """
        super().__init__(game)
        self.backdrop = Backdrop(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.ball_position = ball_position
        self.player_guess = player_guess
        self.cups = game.cups
        self.ball = game.ball_object if hasattr(game, 'ball_object') else None
        
        # Find which cup actually has the ball by checking has_ball property
        self.correct_index = self._find_cup_with_ball(self.cups)
        
        if self.correct_index is None:
            # Fallback if has_ball wasn't set properly
            position_map = {'left': 0, 'middle': 1, 'right': 2}
            self.correct_index = position_map.get(ball_position, 1)
        
        # Update ball position to match the center of the cup that has it
        if self.ball and self.correct_index is not None:
            cup_with_ball = self.cups[self.correct_index]
            # Center the ball in the cup (cup position is top-left, so add half the cup dimensions)
            self.ball.x = cup_with_ball.x + Cup.WIDTH // 2
            self.ball.y = cup_with_ball.y + Cup.HEIGHT // 2
        
        self.is_correct = (player_guess == self.correct_index)
        
        self.cups_moving = False
        self.wait_time = 0
        self.result_shown = False
        
        # Map correct cup to position name for display
        self.correct_position_name = self._get_position_name(self.correct_index)
        
        # Move cups away to the top
        self._move_cups_away()
        print(f"Reveal state initialized! Player guessed cup {player_guess}, ball was at cup {self.correct_index}")
    
    def _move_cups_away(self):
        """Move all cups away to the top of the screen."""
        target_y = -Cup.HEIGHT
        
        for cup in self.cups:
            cup.move_to(cup.x, target_y, duration=0.5)
            self.cups_moving = True
    
    def _get_position_name(self, cup_index: int) -> str:
        """Get the position name for a cup.
        
        Args:
            cup_index: Index of the cup (0, 1, or 2)
            
        Returns:
            Position name ('left', 'middle', or 'right') based on current x position
        """
        cup = self.cups[cup_index]
        # Find which position this cup is closest to
        left_dist = abs(cup.x - layout.POSITION_LEFT)
        middle_dist = abs(cup.x - layout.POSITION_MIDDLE)
        right_dist = abs(cup.x - layout.POSITION_RIGHT)
        
        min_dist = min(left_dist, middle_dist, right_dist)
        if min_dist == left_dist:
            return "left (1)"
        elif min_dist == middle_dist:
            return "middle (2)"
        else:
            return "right (3)"
    
    def on_key_down(self, key: int):
        """Handle key press events."""
        if key == pygame.K_SPACE and self.result_shown:
            from game import GameState
            self.game.change_state(GameState.START_SCREEN)
    
    def update(self, dt: float):
        """Update the reveal state."""
        self.backdrop.update(dt, direction="down")
        
        # Update cups
        for cup in self.cups:
            cup.update(dt)
        
        # Check if all cups have finished moving
        if self.cups_moving:
            if self._all_cups_stopped(self.cups):
                self.cups_moving = False
                self.result_shown = True
    
    def draw(self, surface: pygame.Surface):
        """Draw the reveal state."""
        # Draw backdrop
        self.backdrop.draw(surface)
        
        # Draw border
        self._draw_border(surface)
        
        # Draw the ball first (so cups appear on top)
        if self.ball:
            self.ball.draw(surface)
        
        # Draw cups on top of the ball (they're moving away)
        for cup in self.cups:
            cup.draw(surface, debug=True)
        
        # Draw message bar with result
        if self.result_shown:
            if self.is_correct:
                message = "Correct! Press SPACE"
            else:
                message = f"Wrong! Ball was at {self.correct_position_name}. SPACE"
            self._draw_message_bar(surface, message)
