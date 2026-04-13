"""Reveal state - show the ball and result."""

import pygame
import random
from states.base_state import BaseGameState
import layout
from cup import Cup
from ball import Ball


class Confetti:
    """Simple confetti particle system."""

    COLORS = [
        (255, 50, 50), (50, 220, 50), (50, 100, 255),
        (255, 220, 0), (255, 80, 200), (0, 220, 220), (255, 140, 0),
    ]

    def __init__(self, screen_width: int, screen_height: int, count: int = 200):
        self.screen_height = screen_height
        self.particles = []
        for _ in range(count):
            self.particles.append({
                'x': random.uniform(0, screen_width),
                'y': random.uniform(-screen_height * 0.5, -10),
                'vx': random.uniform(-60, 60),
                'vy': random.uniform(180, 400),
                'color': random.choice(self.COLORS),
                'w': random.randint(8, 22),
                'h': random.randint(4, 10),
                'angle': random.uniform(0, 360),
                'spin': random.uniform(-240, 240),
            })

    def update(self, dt: float):
        for p in self.particles:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['angle'] += p['spin'] * dt
        self.particles = [p for p in self.particles if p['y'] < self.screen_height + 60]

    def draw(self, surface: pygame.Surface):
        for p in self.particles:
            surf = pygame.Surface((p['w'], p['h']), pygame.SRCALPHA)
            surf.fill(p['color'])
            rotated = pygame.transform.rotate(surf, p['angle'])
            rect = rotated.get_rect(center=(int(p['x']), int(p['y'])))
            surface.blit(rotated, rect)


class Reveal(BaseGameState):
    """State where the ball is revealed and result is shown."""
    
    def __init__(self, game, ball_position: str, player_guess: int):
        """Initialize the reveal state.
        
        Args:
            game: Reference to the main Game instance
            ball_position: Which position the ball is hidden at ('left', 'middle', 'right')
            player_guess: Which cup the player guessed (0, 1, or 2)
        """
        super().__init__(game)
        self.ball_position = ball_position
        self.player_guess = player_guess
        self.cups = game.cups
        self.ball = game.ball_object if hasattr(game, 'ball_object') else None
        
        # Find which cup actually has the ball by checking has_ball property
        self.correct_index = self._find_cup_with_ball(self.cups)
        
        if self.correct_index is None:
            # Fallback if has_ball wasn't set properly
            position_map = {'left': 0, 'middle': 1, 'right': 2}
            self.correct_index = position_map.get(ball_position, 1)
        
        # Update ball position to match the center of the cup that has it
        if self.ball and self.correct_index is not None:
            cup_with_ball = self.cups[self.correct_index]
            # Center the ball in the cup (cup position is top-left, so add half the cup dimensions)
            self.ball.x = cup_with_ball.x + Cup.WIDTH // 2
            self.ball.y = cup_with_ball.y + Cup.HEIGHT // 2
        
        self.is_correct = (player_guess == self.correct_index)
        self.result_shown = True  # Show message immediately
        
        # Start confetti if the player guessed correctly
        self.confetti = Confetti(self.SCREEN_WIDTH, self.SCREEN_HEIGHT) if self.is_correct else None
        
        # Map correct cup to position name for display
        self.correct_position_name = self._get_position_name(self.correct_index)
        
        # Move cups away to the top
        self._move_cups_away()
        print(f"Reveal state initialized! Player guessed cup {player_guess}, ball was at cup {self.correct_index}")
    
    def _move_cups_away(self):
        """Move all cups away to the top of the screen."""
        target_y = -Cup.HEIGHT
        
        for cup in self.cups:
            cup.move_to(cup.x, target_y, duration=0.5)
    
    def _get_position_name(self, cup_index: int) -> str:
        """Get the position name for a cup.
        
        Args:
            cup_index: Index of the cup (0, 1, or 2)
            
        Returns:
            Position name ('left', 'middle', or 'right') based on current x position
        """
        cup = self.cups[cup_index]
        # Find which position this cup is closest to
        left_dist = abs(cup.x - layout.POSITION_LEFT)
        middle_dist = abs(cup.x - layout.POSITION_MIDDLE)
        right_dist = abs(cup.x - layout.POSITION_RIGHT)
        
        min_dist = min(left_dist, middle_dist, right_dist)
        if min_dist == left_dist:
            return "links (1)"
        elif min_dist == middle_dist:
            return "midden (2)"
        else:
            return "rechts (3)"
    
    def on_key_down(self, key: int):
        """Handle key press events."""
        if key == pygame.K_SPACE:
            from game import GameState
            self.game.change_state(GameState.START_SCREEN)
    
    def update(self, dt: float):
        """Update the reveal state."""
        self.backdrop.update(dt, direction="down")
        
        # Update ball animation
        self.ball.update(dt)
        
        # Update cups
        for cup in self.cups:
            cup.update(dt)
        
        # Update confetti
        if self.confetti:
            self.confetti.update(dt)
    
    def draw(self, surface: pygame.Surface):
        """Draw the reveal state."""
        # Determine message based on result
        if self.is_correct:
            message = "Goed geraden! Druk op SPATIE"
        else:
            message = f"Helaas! De bal lag bij {self.correct_position_name}. SPATIE"
        
        # Draw state with custom content (ball then cups for proper layering)
        def draw_content(s):
            if self.ball:
                self.ball.draw(s)
            for cup in self.cups:
                cup.draw(s)
            if self.confetti:
                self.confetti.draw(s)
        
        self._draw_state(surface, message, draw_content)
