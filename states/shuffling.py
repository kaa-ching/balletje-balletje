"""Shuffling state for the game."""

import pygame
from backdrop import Backdrop
from states.base_state import BaseGameState
from shuffle_moves import ShuffleMove


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
        
        # Define the shuffle sequence - all 6 transitions repeated twice
        self.moves = [
            ShuffleMove("none"),
            ShuffleMove("l-m"),
            ShuffleMove("m-r"),
            ShuffleMove("l-r"),
            ShuffleMove("l-m-r"),
            ShuffleMove("r-m-l"),
            ShuffleMove("none"),
            ShuffleMove("l-m"),
            ShuffleMove("m-r"),
            ShuffleMove("l-r"),
            ShuffleMove("l-m-r"),
            ShuffleMove("r-m-l"),
        ]
        
        self.current_move_index = 0
        self.move_in_progress = False
        self.wait_time = 0
        
        # Execute the first move
        self._execute_next_move()
        print("Shuffling state initialized!")
    
    def _execute_next_move(self):
        """Execute the next move in the sequence."""
        if self.current_move_index < len(self.moves):
            self.moves[self.current_move_index].execute(self.cups)
            self.move_in_progress = True
            self.wait_time = 0
            self.current_move_index += 1
    
    def on_key_down(self, key: int):
        """Handle key press events."""
        if key == pygame.K_SPACE:
            from game import GameState
            self.game.change_state(GameState.START_SCREEN)
    
    def update(self, dt: float):
        """Update the shuffling state."""
        self.backdrop.update(dt, direction="down")
        
        # Update cups
        for cup in self.cups:
            cup.update(dt)
        
        # Check if all cups have finished moving
        if self.move_in_progress:
            all_stopped = all(not cup.moving for cup in self.cups)
            if all_stopped:
                self.wait_time += dt
                # Wait a moment before starting the next move
                if self.wait_time > 0.2:
                    if self.current_move_index < len(self.moves):
                        self._execute_next_move()
                    else:
                        self.move_in_progress = False
    
    def draw(self, surface: pygame.Surface):
        """Draw the shuffling state."""
        # Draw backdrop
        self.backdrop.draw(surface)
        
        # Draw border
        self._draw_border(surface)
        
        # Draw cups
        for cup in self.cups:
            cup.draw(surface, debug=True)
        
        # Draw message bar with progress
        move_number = min(self.current_move_index, len(self.moves))
        total_moves = len(self.moves)
        self._draw_message_bar(surface, f"Shuffling... ({move_number}/{total_moves})")
