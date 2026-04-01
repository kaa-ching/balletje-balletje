"""Main game engine for Balletje-Balletje."""

import pygame
from enum import Enum
from typing import Optional
import layout


class GameState(Enum):
    START_SCREEN = "start_screen"
    BALL_VISIBLE = "ball_visible"
    CUPS_MOVING = "cups_moving"
    CUPS_TO_START = "cups_to_start"
    SHUFFLING = "shuffling"


class Game:
    """Main game class managing the game loop and state."""
    
    # Layout constants - use centralized layout module
    SCREEN_WIDTH = layout.SCREEN_WIDTH
    SCREEN_HEIGHT = layout.SCREEN_HEIGHT
    BORDER_SIZE = layout.BORDER_SIZE
    MESSAGE_BAR_HEIGHT = layout.MESSAGE_BAR_HEIGHT
    FPS = 60
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Balletje-Balletje")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = GameState.START_SCREEN
        self.state_instance = None
        self.ball_position = None  # Track ball position for cups_moving state
        self.ball_object = None  # Track ball object for cups_moving state
        self.cups = None  # Track cups for shuffling state
        self._load_state(self.current_state)
    
    def _load_state(self, state: GameState):
        """Load a new game state."""
        if state.value == "start_screen":
            from states.start_screen import StartScreen
            self.state_instance = StartScreen(self)
        elif state.value == "ball_visible":
            from states.ball_visible import BallVisible
            self.state_instance = BallVisible(self)
        elif state.value == "cups_moving":
            from states.cups_moving import CupsMoving
            # Pass the ball position that was stored in the game
            self.state_instance = CupsMoving(self, self.ball_position)
        elif state.value == "cups_to_start":
            from states.cups_to_start import CupsToStart
            self.state_instance = CupsToStart(self, self.ball_position)
        elif state.value == "shuffling":
            from states.shuffling import Shuffling
            self.state_instance = Shuffling(self, self.ball_position)
    
    def change_state(self, new_state: GameState):
        """Change to a new game state."""
        self.current_state = new_state
        self._load_state(new_state)
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # Always allow 'q' to quit the game
                if event.key == pygame.K_q:
                    self.running = False
                elif self.state_instance:
                    self.state_instance.on_key_down(event.key)
    
    def update(self, dt: float):
        """Update game logic."""
        if self.state_instance:
            self.state_instance.update(dt)
    
    def draw(self):
        """Draw everything."""
        if self.state_instance:
            self.state_instance.draw(self.screen)
    
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000.0  # Convert to seconds
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
