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
        self.skip_to_reveal = False  # Flag to skip remaining moves
        
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
        self.backdrop.update(dt, direction="down")
        
        # Update cups
        for cup in self.cups:
            cup.update(dt)
        
        # Check if all cups have finished moving
        if self.move_in_progress:
            if self._all_cups_stopped(self.cups):
                self.wait_time += dt
                # Wait a moment before starting the next move
                if self.wait_time > 0.2:
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
