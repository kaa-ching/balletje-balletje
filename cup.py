"""Cup class for the game."""

import pygame
import math


class Cup:
    """Represents a cup that can hide a ball."""
    
    # Cup dimensions - sized to be slightly larger than the ball (radius 90)
    WIDTH = 200
    HEIGHT = 200
    CORNER_RADIUS = 30
    
    # Colors
    COLOR_MAIN = (139, 90, 43)  # Brown
    COLOR_DARK = (101, 67, 33)  # Darker brown for text
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Ease-in-out cubic easing function for smooth natural motion.
        
        Args:
            t: Progress value from 0 to 1
            
        Returns:
            Eased progress value from 0 to 1
        """
        if t < 0.5:
            return 4 * t * t * t
        else:
            p = 2 * t - 2
            return 0.5 * p * p * p + 1
    
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
        self.highlighted = False
        self.target_x = x
        self.target_y = y
        self.moving = False
        self.move_speed = 300  # pixels per second
        self.duration = 0  # Duration for this move (if set)
        self.elapsed_time = 0  # Time elapsed in current move
        self._start_x = x  # Start position for duration-based moves
        self._start_y = y  # Start position for duration-based moves
        self._delay_remaining = 0  # Seconds to wait before starting move
        self._pending_target_x = x
        self._pending_target_y = y
        self._pending_duration = None
    
    def set_has_ball(self, has_ball: bool):
        """Set whether this cup contains the ball."""
        self.has_ball = has_ball
    
    def move_to(self, target_x: float, target_y: float, duration: float = None, delay: float = 0):
        """Start moving the cup to a target position.
        
        Args:
            target_x: Target X position
            target_y: Target Y position
            duration: Time in seconds to complete the move. If None, uses fixed speed.
            delay: Seconds to wait before starting to move.
        """
        self.moving = True
        if delay > 0:
            self._delay_remaining = delay
            self._pending_target_x = target_x
            self._pending_target_y = target_y
            self._pending_duration = duration
        else:
            self._delay_remaining = 0
            self._start_x = self.x
            self._start_y = self.y
            self.target_x = target_x
            self.target_y = target_y
            self.duration = duration
            self.elapsed_time = 0
    
    def update(self, dt: float):
        """Update cup position."""
        if self.moving:
            if self._delay_remaining > 0:
                self._delay_remaining -= dt
                if self._delay_remaining <= 0:
                    self._delay_remaining = 0
                    self._start_x = self.x
                    self._start_y = self.y
                    self.target_x = self._pending_target_x
                    self.target_y = self._pending_target_y
                    self.duration = self._pending_duration
                    self.elapsed_time = 0
                else:
                    return
            if self.duration is not None:
                # Duration-based movement with easing
                self.elapsed_time += dt
                if self.elapsed_time >= self.duration:
                    self.x = self.target_x
                    self.y = self.target_y
                    self.moving = False
                else:
                    # Apply easing function for natural motion
                    progress = self.elapsed_time / self.duration
                    eased_progress = self.ease_in_out_cubic(progress)
                    self.x = self._start_x + (self.target_x - self._start_x) * eased_progress
                    self.y = self._start_y + (self.target_y - self._start_y) * eased_progress
            else:
                # Speed-based movement
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
        
        # Draw gold highlight glow behind the cup when selected
        if self.highlighted:
            glow_rect = pygame.Rect(self.x - 10, self.y - 10, self.WIDTH + 20, self.HEIGHT + 20)
            pygame.draw.rect(surface, (255, 215, 0), glow_rect, border_radius=self.CORNER_RADIUS + 8)
        
        # Draw main cup body
        pygame.draw.rect(surface, self.COLOR_MAIN, rect, border_radius=self.CORNER_RADIUS)
        pygame.draw.rect(surface, self.COLOR_DARK, rect, 3, border_radius=self.CORNER_RADIUS)
        
        # Draw "CooTV" text in center
        font = pygame.font.Font(None, 48)
        text = font.render("CooTV", True, self.COLOR_DARK)
        text_rect = text.get_rect(center=(self.x + self.WIDTH // 2, self.y + self.HEIGHT // 2))
        surface.blit(text, text_rect)
    
    def get_rect(self) -> pygame.Rect:
        """Get the rectangle for collision detection."""
        return pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
