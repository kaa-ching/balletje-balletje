"""Ball class for the game."""

import pygame
import os
import layout


class Ball:
    """Represents the ball in the game."""
    
    # Ball dimensions
    RADIUS = 90  # For collision detection purposes
    
    # Positions - use centralized layout constants
    POSITION_LEFT = layout.POSITION_LEFT
    POSITION_MIDDLE = layout.POSITION_MIDDLE
    POSITION_RIGHT = layout.POSITION_RIGHT
    VERTICAL_CENTER = layout.VERTICAL_CENTER
    
    # Sprite sheet constants
    SPRITE_PATH = os.path.join(os.path.dirname(__file__), "amigo_big_strip.png")
    FRAME_WIDTH = 226
    FRAME_HEIGHT = 220
    
    def __init__(self, position: str = "left"):
        """Initialize the ball at a given position.
        
        Args:
            position: "left", "middle", or "right"
        """
        self.position = position
        
        # Set x position based on position string
        if position == "left":
            self.x = self.POSITION_LEFT
        elif position == "middle":
            self.x = self.POSITION_MIDDLE
        else:  # right
            self.x = self.POSITION_RIGHT
        
        self.y = self.VERTICAL_CENTER
        
        # Load sprite sheet
        self.sprite_sheet = None
        self.frames = []
        self.current_frame = 0
        self.frame_counter = 0
        self.load_sprite()
    
    def load_sprite(self):
        """Load the Amiga ball sprite sheet."""
        try:
            if os.path.exists(self.SPRITE_PATH):
                self.sprite_sheet = pygame.image.load(self.SPRITE_PATH)
                # Extract individual frames from the strip
                sheet_width = self.sprite_sheet.get_width()
                num_frames = sheet_width // self.FRAME_WIDTH
                
                for i in range(num_frames):
                    frame = self.sprite_sheet.subsurface(
                        pygame.Rect(i * self.FRAME_WIDTH, 0, self.FRAME_WIDTH, self.FRAME_HEIGHT)
                    )
                    self.frames.append(frame.copy())
        except Exception as e:
            logger.warning(f"Could not load sprite sheet: {e}")
            self.frames = []
    
    def update(self, dt: float = 0):
        """Update animation frame."""
        if self.frames:
            self.frame_counter += 1
            if self.frame_counter >= 5:  # Change frame every 5 updates
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
    
    def draw(self, surface: pygame.Surface):
        """Draw the ball to the surface."""
        if not self.frames:
            # Fallback to simple circle if sprite can't load
            pygame.draw.circle(surface, (240, 240, 200), (int(self.x), int(self.y)), self.RADIUS)
            return
        
        frame = self.frames[self.current_frame]
        # Scale to 90% and center the sprite at the ball position
        scaled = pygame.transform.scale(frame, (int(self.FRAME_WIDTH * 0.85), int(self.FRAME_HEIGHT * 0.85)))
        rect = scaled.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(scaled, rect)


