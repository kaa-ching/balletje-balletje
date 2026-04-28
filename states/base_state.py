"""Base state class for the game."""

import pygame
import layout
from backdrop import Backdrop


class BaseGameState:
    """Base class for all game states."""
    
    # Layout constants - imported from centralized layout module
    SCREEN_WIDTH = layout.SCREEN_WIDTH
    SCREEN_HEIGHT = layout.SCREEN_HEIGHT
    BORDER_SIZE = layout.BORDER_SIZE
    MESSAGE_BAR_HEIGHT = layout.MESSAGE_BAR_HEIGHT
    
    def __init__(self, game):
        """Initialize the game state.
        
        Args:
            game: Reference to the main Game instance
        """
        self.game = game
        self.backdrop = game.backdrop
    
    def on_key_down(self, key: int):
        """Handle key press events. Override in subclasses."""
        pass
    
    def get_valid_keys(self) -> dict:
        """Get a dictionary of valid key mappings for this state.
        
        Returns:
            Dictionary mapping key names to descriptions, e.g.,
            {'1': 'Left cup', '2': 'Middle cup', '3': 'Right cup'}
        """
        return {}
    
    def get_status_message(self) -> str:
        """Get the main status message for this state.
        
        Returns:
            The main message to display in the status bar
        """
        return ""
    
    def update(self, dt: float):
        """Update the game state. Override in subclasses."""
        pass
    
    def draw(self, surface: pygame.Surface):
        """Draw the game state. Override in subclasses."""
        pass
    
    def _draw_border(self, surface: pygame.Surface):
        """Draw the field frame when a margin is configured."""
        if self.BORDER_SIZE <= 0:
            return

        # Top frame
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, self.SCREEN_WIDTH, self.BORDER_SIZE))
        # Bottom frame (above message bar)
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (0, self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT - self.BORDER_SIZE, self.SCREEN_WIDTH, self.BORDER_SIZE)
        )
        # Left frame
        pygame.draw.rect(surface, (0, 0, 0), (0, self.BORDER_SIZE, self.BORDER_SIZE, self.SCREEN_HEIGHT - self.BORDER_SIZE - self.MESSAGE_BAR_HEIGHT))
        # Right frame
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (self.SCREEN_WIDTH - self.BORDER_SIZE, self.BORDER_SIZE, self.BORDER_SIZE, self.SCREEN_HEIGHT - self.BORDER_SIZE - self.MESSAGE_BAR_HEIGHT)
        )
    
    def _draw_message_bar(self, surface: pygame.Surface, main_message: str, key_hints: dict = None):
        """Draw the message bar at the bottom with optional key hints.
        
        Args:
            surface: The pygame surface to draw on
            main_message: The main message text to display
            key_hints: Dictionary of key mappings to show on the right side
        """
        # Draw message bar background
        message_bar_rect = pygame.Rect(
            0,
            self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT,
            self.SCREEN_WIDTH,
            self.MESSAGE_BAR_HEIGHT
        )
        pygame.draw.rect(surface, (40, 40, 60), message_bar_rect)
        pygame.draw.rect(surface, (100, 100, 150), message_bar_rect, 3)
        
        # Draw main message text (left-aligned)
        font = pygame.font.Font(None, 72)
        main_text = font.render(main_message, True, (200, 200, 255))
        main_text_rect = main_text.get_rect(midleft=(50, self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT // 2))
        surface.blit(main_text, main_text_rect)
        
        # Draw key hints on the right side
        if key_hints:
            self._draw_key_hints(surface, key_hints)
    
    def _draw_key_hints(self, surface: pygame.Surface, key_hints: dict):
        """Draw key hints on the right side of the message bar.
        
        Args:
            surface: The pygame surface to draw on
            key_hints: Dictionary mapping keys to descriptions
        """
        if not key_hints:
            return
            
        key_font = pygame.font.Font(None, 48)
        
        # Draw "Keys:" label on first line
        keys_label_y = self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT + 30
        keys_label = key_font.render("Keys:", True, (200, 200, 255))
        keys_label_rect = keys_label.get_rect(midright=(self.SCREEN_WIDTH - 50, keys_label_y))
        surface.blit(keys_label, keys_label_rect)
        
        # Draw keys horizontally on second line (below "Keys:")
        keys_y = self.SCREEN_HEIGHT - self.MESSAGE_BAR_HEIGHT + 80
        
        # Calculate starting position (right-aligned with margin)
        # First pass: calculate total width needed (including 20px spacing between keys)
        total_width = 0
        key_surfaces = []
        for i, key in enumerate(key_hints.keys()):
            if key == "space":
                key_text = "Spatie"
            elif key == "enter":
                key_text = "Enter"
            else:
                key_text = key.upper()
            key_surface = key_font.render(key_text, True, (255, 255, 255))
            key_surfaces.append(key_surface)
            total_width += key_surface.get_width()
            total_width += 20
        total_width -= 20  # Add spacing for all but last key
        
        # Start from right, leaving 50px margin (same as left margin for main text)
        x_pos = self.SCREEN_WIDTH - 50 - total_width
        
        # Draw each key left-to-right with consistent 20px spacing
        for i, key_surface in enumerate(key_surfaces):
            key_rect = key_surface.get_rect(midleft=(x_pos, keys_y - key_surface.get_height()//2))
            
            # Draw boxed background for the key
            bg_rect = key_rect.inflate(15, 8)
            pygame.draw.rect(surface, (60, 60, 80), bg_rect, border_radius=6)
            pygame.draw.rect(surface, (100, 100, 150), bg_rect, 2, border_radius=6)
            
            # Draw the key text on top
            surface.blit(key_surface, key_rect)
            
            # Move right by key width + 20px spacing
            x_pos += key_surface.get_width() + 20
    
    def _all_cups_stopped(self, cups: list) -> bool:
        """Check if all cups have finished moving.
        
        Args:
            cups: List of Cup objects to check
            
        Returns:
            True if all cups are stopped, False otherwise
        """
        return all(not cup.moving for cup in cups)
    
    def _find_cup_with_ball(self, cups: list) -> int:
        """Find the index of the cup that contains the ball.
        
        Args:
            cups: List of Cup objects
            
        Returns:
            Index of the cup with the ball, or None if not found
        """
        for i, cup in enumerate(cups):
            if cup.has_ball:
                return i
        return None
    
    def _draw_base(self, surface: pygame.Surface):
        """Draw the base elements (backdrop, field frame, message bar).
        Convenience method for states without custom content layering.
        
        Args:
            surface: The pygame surface to draw on
        """
        self._draw_state(surface)
    
    def _draw_base_background(self, surface: pygame.Surface):
        """Draw just the backdrop and field frame (without message bar).
        Useful for states that need custom content layering between frame and message.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Draw backdrop
        self.backdrop.draw(surface)
        
        # Draw field frame
        self._draw_border(surface)
    
    def _draw_state(self, surface: pygame.Surface, main_message: str = None, content_callback=None):
        """Draw a complete state with custom content between backdrop and message bar.
        This is the main drawing helper for all states.
        
        Args:
            surface: The pygame surface to draw on
            main_message: Message to display in the message bar (None or empty string for blank bar)
            content_callback: Optional function(surface) to call for drawing custom content
                            (called between backdrop/frame and message bar)
        """
        # Draw backdrop and field frame
        self._draw_base_background(surface)
        
        # Draw custom content if provided
        if content_callback:
            content_callback(surface)
        
        # Draw message bar (always visible, even if empty)
        key_hints = self.get_valid_keys()
        main_msg = self.get_status_message() or main_message or ""
        
        self._draw_message_bar(surface, main_msg, key_hints)
