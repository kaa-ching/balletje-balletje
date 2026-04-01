"""Cup class for the game."""

import pygame


class Cup:
    """Represents a cup that can hide a ball."""
    
    # Cup dimensions
    WIDTH = 80
    HEIGHT = 80
    CORNER_RADIUS = 15
    
    # Colors
    COLOR_MAIN = (139, 90, 43)  # Brown
    COLOR_DARK = (101, 67, 33)  # Darker brown for text
    
    def __init__(self, position_index: int, x: float, y: float):
        """Initialize a cup.
        
        Args:
            position_index: 0 (left), 1 (middle), or 2 (right)
            x: X position
            y: Y position
        """
        self.position_index = position_index
        self.x = x
        self.y = y
        self.has_ball = False
        self.target_x = x
        self.target_y = y
        self.moving = False
        self.move_speed = 300  # pixels per second
    
    def set_has_ball(self, has_ball: bool):
        """Set whether this cup contains the ball."""
        self.has_ball = has_ball
    
    def move_to(self, target_x: float, target_y: float):
        """Start moving the cup to a target position."""
        self.target_x = target_x
        self.target_y = target_y
        self.moving = True
    
    def update(self, dt: float):
        """Update cup position."""
        if self.moving:
            # Calculate distance to target
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = (dx**2 + dy**2)**0.5
            
            if distance > 1:
                # Move towards target
                move_distance = self.move_speed * dt
                if move_distance >= distance:
                    self.x = self.target_x
                    self.y = self.target_y
                    self.moving = False
                else:
                    # Normalize and move
                    self.x += (dx / distance) * move_distance
                    self.y += (dy / distance) * move_distance
            else:
                self.x = self.target_x
                self.y = self.target_y
                self.moving = False
    
    def draw(self, surface: pygame.Surface, debug: bool = False):
        """Draw the cup to the surface."""
        rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        
        # Draw main cup body
        pygame.draw.rect(surface, self.COLOR_MAIN, rect, border_radius=self.CORNER_RADIUS)
        pygame.draw.rect(surface, self.COLOR_DARK, rect, 3, border_radius=self.CORNER_RADIUS)
        
        # Draw "CooTV" text in center
        font = pygame.font.Font(None, 24)
        text = font.render("CooTV", True, self.COLOR_DARK)
        text_rect = text.get_rect(center=(self.x + self.WIDTH // 2, self.y + self.HEIGHT // 2))
        surface.blit(text, text_rect)
        
        # Debug: show cup number and ball indicator
        if debug:
            debug_font = pygame.font.Font(None, 18)
            ball_indicator = "*" if self.has_ball else ""
            debug_text = debug_font.render(f"{self.position_index}{ball_indicator}", True, (255, 255, 0))
            surface.blit(debug_text, (self.x + 5, self.y + 5))
    
    def get_rect(self) -> pygame.Rect:
        """Get the rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
