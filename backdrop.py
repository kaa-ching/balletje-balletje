"""Backdrop system for geometric patterns."""

import pygame
import math
import random


class Backdrop:
    """Manages the moving geometric backdrop."""
    
    def __init__(self, width: int, height: int):
        """Initialize the backdrop with dimensions."""
        self.width = width
        self.height = height
        self.speed = 140         # pixels per second (faster)
        self.pattern_size = 80  # bigger tiles = more visible
        self.offset_x = self.pattern_size * 0.5  # start mid-tile to avoid boundary jump when horizontal movement begins
        self.offset_y = 0.0
        self._time = 0.0         # for colour pulsing

    def update(self, dt: float, direction: str = "down"):
        """Update backdrop position."""
        self._time += dt

        if direction == "random":
            direction = random.choice(["top_left", "top_right", "bottom_left", "bottom_right"])

        dx = 0.0
        dy = 0.0

        if direction == "up":
            dy = -self.speed * dt
        elif direction == "down":
            dy = self.speed * dt
        elif direction == "left":
            dx = -self.speed * dt
        elif direction == "right":
            dx = self.speed * dt
        elif direction == "top_left":
            dx = -self.speed * dt
            dy = -self.speed * dt
        elif direction == "top_right":
            dx = self.speed * dt
            dy = -self.speed * dt
        elif direction == "bottom_left":
            dx = -self.speed * dt
            dy = self.speed * dt
        elif direction == "bottom_right":
            dx = self.speed * dt
            dy = self.speed * dt

        self.offset_x += dx
        self.offset_y += dy

    def draw(self, surface: pygame.Surface):
        """Draw the geometric backdrop to the surface."""
        fractional_offset_x = self.offset_x % self.pattern_size
        fractional_offset_y = self.offset_y % self.pattern_size

        # Pulse between two hues over ~3 seconds
        pulse = (math.sin(self._time * 2.1) + 1) / 2  # 0..1

        for y in range(-self.pattern_size, self.height + self.pattern_size, self.pattern_size):
            for x in range(-self.pattern_size, self.width + self.pattern_size, self.pattern_size):
                logical_x = x - self.offset_x
                logical_y = y - self.offset_y
                self._draw_pattern_tile(
                    surface,
                    x - fractional_offset_x,
                    y - fractional_offset_y,
                    logical_x, logical_y,
                    pulse,
                )

    def _draw_pattern_tile(self, surface: pygame.Surface, x: float, y: float,
                           logical_x: float, logical_y: float, pulse: float):
        """Draw a single pattern tile."""
        size = self.pattern_size

        tile_x = int(logical_x // size) % 2
        tile_y = int(logical_y // size) % 2
        is_light = (tile_x + tile_y) % 2 == 0

        # High-contrast pulsing colours
        if is_light:
            r = int(20 + pulse * 60)
            g = int(0  + pulse * 20)
            b = int(120 + pulse * 100)
            color = (r, g, b)
            line_color = (
                int(100 + pulse * 100),
                int(50  + pulse * 50),
                int(220 + pulse * 35),
            )
        else:
            r = int(80 - pulse * 60)
            g = int(0)
            b = int(30 + pulse * 30)
            color = (r, g, b)
            line_color = (
                int(160 - pulse * 80),
                int(0),
                int(80 + pulse * 40),
            )

        rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(surface, color, rect)

        # Bold diagonals
        pygame.draw.line(surface, line_color, (x, y), (x + size, y + size), 3)
        pygame.draw.line(surface, line_color, (x + size, y), (x, y + size), 3)

        # Extra cross lines to add visual noise
        mid_x = x + size // 2
        mid_y = y + size // 2
        pygame.draw.line(surface, line_color, (x, mid_y), (x + size, mid_y), 1)
        pygame.draw.line(surface, line_color, (mid_x, y), (mid_x, y + size), 1)
