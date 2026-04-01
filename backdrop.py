"""Backdrop system for geometric patterns."""

import pygame
import math


class Backdrop:
    """Manages the moving geometric backdrop."""
    
    def __init__(self, width: int, height: int):
        """Initialize the backdrop with dimensions."""
        self.width = width
        self.height = height
        self.offset_y = 0.0  # Ensure this is a float
        self.speed = 80  # pixels per second
        self.pattern_size = 40  # Size of repeating pattern
    
    def update(self, dt: float, direction: str = "down"):
        """Update backdrop position.
        
        Args:
            dt: Delta time in seconds
            direction: "down", "up", or corner directions like "top_left"
        """
        if direction == "up":
            self.offset_y -= self.speed * dt
        else:  # default to down
            self.offset_y += self.speed * dt
    
    def draw(self, surface: pygame.Surface):
        """Draw the geometric backdrop to the surface."""
        # Calculate fractional offset within the pattern for seamless tiling
        fractional_offset = self.offset_y % self.pattern_size
        
        # Draw tiles with offset applied to create scrolling effect
        for y in range(-self.pattern_size, self.height + self.pattern_size, self.pattern_size):
            for x in range(0, self.width, self.pattern_size):
                # Calculate the logical tile position (for pattern determination)
                logical_y = y - self.offset_y
                self._draw_pattern_tile(surface, x, y - fractional_offset, logical_y)
    
    def _draw_pattern_tile(self, surface: pygame.Surface, x: int, visual_y: float, logical_y: float):
        """Draw a single pattern tile.
        
        Args:
            surface: The pygame surface to draw on
            x: X coordinate
            visual_y: Y coordinate for visual positioning (with fractional offset)
            logical_y: Y coordinate for pattern calculation (without offset applied)
        """
        size = self.pattern_size
        
        # Use alternating colors - black and blue boxes
        color1 = (20, 20, 40)  # Dark blue
        color2 = (0, 0, 0)  # Black
        
        # Create a repeating pattern based on logical position
        pattern_x = (int(x // size) // 2) % 2
        pattern_y = (int(logical_y // size) // 2) % 2
        is_light = (pattern_x + pattern_y) % 2 == 0
        
        color = color2 if is_light else color1
        
        # Draw the tile at the visual position
        rect = pygame.Rect(x, visual_y, size, size)
        pygame.draw.rect(surface, color, rect)
        
        # Draw diagonal lines
        line_color = (60, 60, 120) if is_light else (30, 30, 60)
        pygame.draw.line(surface, line_color, (x, visual_y), (x + size, visual_y + size), 2)
        pygame.draw.line(surface, line_color, (x + size, visual_y), (x, visual_y + size), 2)
