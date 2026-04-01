"""Guessing state - waiting for player to select cup."""

import pygame
from states.base_state import BaseGameState
import layout
from cup import Cup


class Guessing(BaseGameState):
    """State where player selects which cup has the ball."""
    
    def __init__(self, game, ball_position: str):
        """Initialize the guessing state.
        
        Args:
            game: Reference to the main Game instance
            ball_position: Which position the ball is hidden at ('left', 'middle', 'right')
        """
        super().__init__(game)
        self.ball_position = ball_position
        self.cups = game.cups
        self.player_guess = None
        self.cups_moving = False
        self.wait_time = 0
        
        # Move cups to central vertical position (middle row)
        self._move_cups_to_center()
        print("Guessing state initialized!")
    
    def _move_cups_to_center(self):
        """Move all cups to central vertical position."""
        center_y = layout.get_cup_center_y()
        
        for cup in self.cups:
            if cup.y != center_y:
                cup.move_to(cup.x, center_y, duration=0.5)
                self.cups_moving = True
    
    def on_key_down(self, key: int):
        """Handle key press events."""
        # Ignore input if cups are still moving
        if self.cups_moving:
            return
        
        # Convert position number to position coordinate
        if key == pygame.K_1:
            guessed_position = layout.POSITION_LEFT
        elif key == pygame.K_2:
            guessed_position = layout.POSITION_MIDDLE
        elif key == pygame.K_3:
            guessed_position = layout.POSITION_RIGHT
        else:
            return
        
        # Find which cup is at the guessed position
        self.player_guess = self._find_cup_at_position(guessed_position)
        self._transition_to_reveal()
    
    def _find_cup_at_position(self, target_x: float) -> int:
        """Find which cup is at a given x position.
        
        Args:
            target_x: The x position to check
            
        Returns:
            Index of the cup closest to that position
        """
        closest_cup = 0
        closest_distance = abs(self.cups[0].x - target_x)
        
        for i in range(1, len(self.cups)):
            distance = abs(self.cups[i].x - target_x)
            if distance < closest_distance:
                closest_distance = distance
                closest_cup = i
        
        return closest_cup
    
    def on_mouse_click(self, pos: tuple):
        """Handle mouse clicks on cups."""
        # Ignore input if cups are still moving
        if self.cups_moving:
            return
        
        x, y = pos
        for i, cup in enumerate(self.cups):
            cup_rect = pygame.Rect(cup.x, cup.y, Cup.WIDTH, Cup.HEIGHT)
            if cup_rect.collidepoint(x, y):
                self.player_guess = i  # Cup at this position
                self._transition_to_reveal()
                break
    
    def _transition_to_reveal(self):
        """Transition to reveal state after player makes a guess."""
        from game import GameState
        self.game.player_guess = self.player_guess
        self.game.change_state(GameState.REVEAL)
    
    def update(self, dt: float):
        """Update the guessing state."""
        self.backdrop.update(dt, direction="down")
        
        # Update cups
        for cup in self.cups:
            cup.update(dt)
        
        # Check if all cups have finished moving
        if self.cups_moving:
            if self._all_cups_stopped(self.cups):
                self.cups_moving = False
    
    def draw(self, surface: pygame.Surface):
        """Draw the guessing state."""
        # Draw base elements (backdrop, border, message bar)
        self._draw_base(surface, "Which cup has the ball? (1-3 or click)")
        
        # Draw cups
        for cup in self.cups:
            cup.draw(surface, debug=True)
