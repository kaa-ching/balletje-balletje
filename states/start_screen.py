"""Start screen state for the game."""

import pygame
from backdrop import Backdrop
from states.base_state import BaseGameState
import layout


class StartScreen(BaseGameState):
    """The start screen state of the game."""
    
    def __init__(self, game):
        """Initialize the start screen.
        
        Args:
            game: Reference to the main Game instance
        """
        self.game = game
        self.backdrop = Backdrop(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.title_y = self.SCREEN_HEIGHT // 2 - 120  # Center vertically (adjusted for larger text)
        self.title_alpha = 255
        self.waiting_for_space = True
        self.has_transitioned = False  # Track if we've already transitioned
    
    def on_key_down(self, key: int):
        """Handle key press events.
        
        Args:
            key: The pygame key code
        """
        if key == pygame.K_SPACE and self.waiting_for_space:
            # Transition to next state or start animation
            self.start_title_exit_animation()
    
    def start_title_exit_animation(self):
        """Start the animation where the title exits upward."""
        self.waiting_for_space = False
        # This will be handled in update
    
    def update(self, dt: float):
        """Update the start screen state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update backdrop (moving down)
        self.backdrop.update(dt, direction="down")
        
        # If space was pressed, animate title moving up
        if not self.waiting_for_space:
            self.title_y -= 300 * dt  # Move up at 300 pixels/second
            self.title_alpha = max(0, self.title_alpha - 255 * dt)  # Fade out
            
            # When title is completely off screen and faded, transition to next state
            if self.title_y < -100 and not self.has_transitioned:
                self.has_transitioned = True
                from game import GameState
                self.game.change_state(GameState.BALL_VISIBLE)
    
    def draw(self, surface: pygame.Surface):
        """Draw the start screen.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Draw backdrop
        self.backdrop.draw(surface)
        
        # Draw border
        self._draw_border(surface)
        
        # Draw title text "balletje-balletje" in 2 lines
        self._draw_title(surface)
        
        # Draw message bar
        self._draw_message_bar(surface, "Press SPACE to start")
    
    def _draw_title(self, surface: pygame.Surface):
        """Draw the title text."""
        # Create italic font - doubled size
        font = pygame.font.Font(None, 360)
        font.set_italic(True)
        
        # Create surface with alpha for fading
        if self.title_alpha > 0:
            title_surface = pygame.Surface((self.SCREEN_WIDTH, 600), pygame.SRCALPHA)
            
            # Render text
            line1 = font.render("balletje-", True, (200, 200, 255))
            line2 = font.render("balletje", True, (200, 200, 255))
            
            # Position lines in center with more vertical space
            line1_rect = line1.get_rect(center=(self.SCREEN_WIDTH // 2, 120))
            line2_rect = line2.get_rect(center=(self.SCREEN_WIDTH // 2, 340))
            
            title_surface.blit(line1, line1_rect)
            title_surface.blit(line2, line2_rect)
            
            # Apply alpha
            title_surface.set_alpha(int(self.title_alpha))
            
            # Blit to main surface
            surface.blit(title_surface, (0, self.title_y - 280))
