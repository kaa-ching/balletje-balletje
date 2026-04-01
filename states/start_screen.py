"""Start screen state for the game."""

import pygame
from backdrop import Backdrop


class StartScreen:
    """The start screen state of the game."""
    
    # Layout constants (from game.py)
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    BORDER_SIZE = 100
    MESSAGE_BAR_HEIGHT = 150
    
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
            if self.title_y < -100:
                from game import GameState
                # For now, we'll stay on start screen, but this is where we'd transition
                # self.game.change_state(GameState.BALL_VISIBLE)
                self.waiting_for_space = True
                self.title_y = self.SCREEN_HEIGHT // 2 - 120
                self.title_alpha = 255
    
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
        self._draw_message_bar(surface)
    
    def _draw_border(self, surface: pygame.Surface):
        """Draw the border around the play area."""
        # Top border
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, self.SCREEN_WIDTH, self.BORDER_SIZE))
        # Bottom border (above message bar)
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (0, self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT, self.SCREEN_WIDTH, self.BORDER_SIZE)
        )
        # Left border
        pygame.draw.rect(surface, (0, 0, 0), (0, self.BORDER_SIZE, self.BORDER_SIZE, self.SCREEN_HEIGHT - self.BORDER_SIZE - self.MESSAGE_BAR_HEIGHT))
        # Right border
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (self.SCREEN_WIDTH - self.BORDER_SIZE, self.BORDER_SIZE, self.BORDER_SIZE, self.SCREEN_HEIGHT - self.BORDER_SIZE - self.MESSAGE_BAR_HEIGHT)
        )
    
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
    
    def _draw_message_bar(self, surface: pygame.Surface):
        """Draw the message bar at the bottom."""
        # Draw message bar background
        message_bar_rect = pygame.Rect(
            0,
            self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT,
            self.SCREEN_WIDTH,
            self.MESSAGE_BAR_HEIGHT
        )
        pygame.draw.rect(surface, (40, 40, 60), message_bar_rect)
        pygame.draw.rect(surface, (100, 100, 150), message_bar_rect, 3)
        
        # Draw message text - doubled size
        font = pygame.font.Font(None, 72)
        message = "Press SPACE to start"
        text = font.render(message, True, (200, 200, 255))
        text_rect = text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT // 2))
        surface.blit(text, text_rect)
