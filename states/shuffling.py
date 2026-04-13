"""Shuffling state for the game."""

import pygame
import random
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
        self.ball_position = ball_position
        self.cups = game.cups
        
        # Define available shuffle transitions
        move_types = ["none", "l-m", "m-r", "l-r", "l-m-r", "r-m-l"]
        
        # Generate 10 random shuffle moves
        self.moves = [ShuffleMove(random.choice(move_types)) for _ in range(10)]
        
        self.current_move_index = 0
        self.move_in_progress = False
        self.wait_time = 0
        self.skip_to_reveal = False  # Flag to skip remaining moves
        
        # Diagonal movement cycling (clockwise: TL → TR → BR → BL → TL)
        self.diagonal_directions = ["top_left", "top_right", "bottom_right", "bottom_left"]
        self.current_diagonal_index = 0
        
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
            # Set flag to skip remaining moves after current one completes
            self.skip_to_reveal = True
    
    def update(self, dt: float):
        """Update the shuffling state."""
        # Update backdrop (moving diagonally, changing direction each move)
        current_direction = self.diagonal_directions[self.current_diagonal_index]
        self.backdrop.update(dt, direction=current_direction)
        
        # Update cups
        for cup in self.cups:
            cup.update(dt)
        
        # Check if all cups have finished moving
        if self.move_in_progress:
            if self._all_cups_stopped(self.cups):
                self.wait_time += dt
                # Wait a moment before starting the next move
                if self.wait_time > 0.2:
                    # Advance to next diagonal direction (clockwise)
                    self.current_diagonal_index = (self.current_diagonal_index + 1) % len(self.diagonal_directions)
                    
                    if self.skip_to_reveal:
                        # Player pressed SPACE - transition to guessing after current move
                        self.move_in_progress = False
                        self._transition_to_guessing()
                    elif self.current_move_index < len(self.moves):
                        self._execute_next_move()
                    else:
                        # All moves complete - transition to guessing
                        self.move_in_progress = False
                        self._transition_to_guessing()
    
    def _transition_to_guessing(self):
        """Transition to guessing state after shuffling completes."""
        from game import GameState
        self.game.change_state(GameState.GUESSING)
    
    def draw(self, surface: pygame.Surface):
        """Draw the shuffling state."""
        # Compute message with progress
        move_number = min(self.current_move_index, len(self.moves))
        total_moves = len(self.moves)
        message = f"Husselen... ({move_number}/{total_moves})"
        
        # Draw base elements (backdrop, border, message bar)
        self._draw_base(surface, message)
        
        # Draw cups
        for cup in self.cups:
            cup.draw(surface)
