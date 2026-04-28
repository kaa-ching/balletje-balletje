"""Main game engine for Balletje-Balletje."""

import pygame
import logging
from enum import Enum
from typing import Optional
import layout
from backdrop import Backdrop

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('game')

# Import all state classes at the top
from states.start_screen import StartScreen
from states.ball_visible import BallVisible
from states.cups_moving import CupsMoving
from states.cups_to_start import CupsToStart
from states.shuffling import Shuffling
from states.guessing import Guessing
from states.monty_hall import MontyHall
from states.reveal import Reveal


class GameState(Enum):
    START_SCREEN = "start_screen"
    BALL_VISIBLE = "ball_visible"
    CUPS_MOVING = "cups_moving"
    CUPS_TO_START = "cups_to_start"
    SHUFFLING = "shuffling"
    GUESSING = "guessing"
    MONTY_HALL = "monty_hall"
    REVEAL = "reveal"


class Game:
    """Main game class managing the game loop and state."""
    
    # Layout constants - use centralized layout module
    SCREEN_WIDTH = layout.SCREEN_WIDTH
    SCREEN_HEIGHT = layout.SCREEN_HEIGHT
    BORDER_SIZE = layout.BORDER_SIZE
    MESSAGE_BAR_HEIGHT = layout.MESSAGE_BAR_HEIGHT
    FPS = 60
    
    # Centralized key mappings
    GLOBAL_QUIT_KEYS = [pygame.K_q, pygame.K_ESCAPE]
    
    def __init__(self):
        """Initialize the game."""
        logger.info("Initializing game...")
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Balletje-Balletje")
        self.clock = pygame.time.Clock()
        self.running = True
        self.backdrop = Backdrop(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.current_state = GameState.START_SCREEN
        self.state_instance = None
        self.ball_position = None  # Track ball position for cups_moving state
        self.ball_object = None  # Track ball object for cups_moving state
        self.cups = None  # Track cups for shuffling state
        self.player_guess = None  # Track player's cup guess
        self._load_state(self.current_state)
        logger.info("Game initialized successfully")
    
    def _load_state(self, state: GameState):
        """Load a new game state."""
        logger.debug(f"Loading state: {state.value}")
        if state.value == "start_screen":
            self.state_instance = StartScreen(self)
        elif state.value == "ball_visible":
            self.state_instance = BallVisible(self)
        elif state.value == "cups_moving":
            # Pass the ball position that was stored in the game
            self.state_instance = CupsMoving(self, self.ball_position)
        elif state.value == "cups_to_start":
            self.state_instance = CupsToStart(self, self.ball_position)
        elif state.value == "shuffling":
            self.state_instance = Shuffling(self, self.ball_position)
        elif state.value == "guessing":
            self.state_instance = Guessing(self, self.ball_position)
        elif state.value == "monty_hall":
            self.state_instance = MontyHall(self, self.ball_position, self.player_guess)
        elif state.value == "reveal":
            self.state_instance = Reveal(self, self.ball_position, self.player_guess)
        logger.info(f"State loaded: {state.value}")
    
    def change_state(self, new_state: GameState):
        """Change to a new game state."""
        logger.info(f"Changing state from {self.current_state.value} to {new_state.value}")
        self.current_state = new_state
        self._load_state(new_state)
    
    def _handle_global_input(self, key: int) -> bool:
        """Handle global input that applies to all states.
        
        Args:
            key: The pygame key code
            
        Returns:
            True if the key was handled globally, False otherwise
        """
        if key in self.GLOBAL_QUIT_KEYS:
            logger.info("Quit key pressed")
            self.running = False
            return True
        return False
    
    def _handle_state_input(self, key: int):
        """Handle state-specific input.
        
        Args:
            key: The pygame key code
        """
        if self.state_instance:
            # Pass all keys to the state - let the state decide what to handle
            self.state_instance.on_key_down(key)
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Quit event received")
                self.running = False
            elif event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                logger.debug(f"Key pressed: {key_name}")
                
                # First handle global input (quit keys)
                if self._handle_global_input(event.key):
                    continue
                    
                # Then handle state-specific input
                self._handle_state_input(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state_instance and hasattr(self.state_instance, 'on_mouse_click'):
                    logger.debug(f"Mouse clicked at: {event.pos}")
                    self.state_instance.on_mouse_click(event.pos)
    
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
        logger.info("Starting main game loop")
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000.0  # Convert to seconds
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()
        logger.info("Game loop ended")
        pygame.quit()
        logger.info("Game closed")


if __name__ == "__main__":
    logger.info("Starting Balletje-Balletje game")
    game = Game()
    game.run()
