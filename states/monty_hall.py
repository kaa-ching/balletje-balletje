"""Monty Hall state - host reveals an empty cup, player switches or stays."""

import pygame
from states.base_state import BaseGameState
from cup import Cup
import layout


class MontyHall(BaseGameState):
    """State where Monty Hall reveals an empty cup and asks the player to switch or stay."""

    PHASE_ANIMATING = "animating"      # reveal cup flying off-screen
    PHASE_SWITCH_OR_STAY = "deciding"  # waiting for W / Z / Enter
    PHASE_SWITCHING = "switching"      # brief highlight-move pause before reveal

    LIFT_DURATION = 1.0        # seconds to fly the reveal cup off-screen
    SWITCH_PAUSE = 1.0         # seconds to show the new highlight before revealing

    # Colors
    TITLE_COLOR = (255, 215, 0)        # gold
    ELLIPSIS_COLOR = (220, 220, 220)   # light grey

    def __init__(self, game, ball_position: str, player_guess: int):
        """Initialize the Monty Hall state.

        Args:
            game: Reference to the main Game instance
            ball_position: Which position the ball is hidden at
            player_guess: Index of the cup the player initially chose
        """
        super().__init__(game)
        self.ball_position = ball_position
        self.player_guess = player_guess
        self.cups = game.cups
        self.phase = self.PHASE_ANIMATING
        self._switch_timer = 0.0

        # Keep the player's chosen cup highlighted
        for i, cup in enumerate(self.cups):
            cup.highlighted = (i == player_guess)

        # Decide which cup the host will reveal (not player's, no ball)
        self.correct_index = self._find_cup_with_ball(self.cups)
        self.reveal_cup_index = self._pick_reveal_cup()
        self.remaining_cup_index = self._pick_remaining_cup()

        # Remember the revealed cup's resting position for the ellipsis marker
        reveal_cup = self.cups[self.reveal_cup_index]
        self._ellipsis_x = reveal_cup.x + Cup.WIDTH // 2
        self._ellipsis_y = reveal_cup.y + Cup.HEIGHT // 2

        # Fly the reveal cup off-screen to the top (and leave it there)
        off_screen_y = -(Cup.HEIGHT * 2)
        reveal_cup.move_to(reveal_cup.x, off_screen_y, duration=self.LIFT_DURATION)

        print(
            f"MontyHall: player chose {player_guess}, "
            f"revealing cup {self.reveal_cup_index}, "
            f"remaining cup is {self.remaining_cup_index}"
        )

    # --- helper methods ---------------------------------------------------

    def _pick_reveal_cup(self) -> int:
        """Return index of a cup that is not the player's guess and has no ball."""
        for i, cup in enumerate(self.cups):
            if i != self.player_guess and not cup.has_ball:
                return i
        return (self.player_guess + 1) % 3

    def _pick_remaining_cup(self) -> int:
        """Return the cup that is neither the player's guess nor the revealed cup."""
        for i in range(len(self.cups)):
            if i != self.player_guess and i != self.reveal_cup_index:
                return i
        return (self.player_guess + 1) % 3

    # --- input ------------------------------------------------------------

    def on_key_down(self, key: int):
        """Handle key press events."""
        if self.phase != self.PHASE_SWITCH_OR_STAY:
            return

        if key == pygame.K_w:
            # Switch: move highlight to the remaining cup, then wait
            self.cups[self.player_guess].highlighted = False
            self.cups[self.remaining_cup_index].highlighted = True
            self._final_guess = self.remaining_cup_index
            self._switch_timer = 0.0
            self.phase = self.PHASE_SWITCHING
        elif key in (pygame.K_z, pygame.K_RETURN, pygame.K_KP_ENTER):
            # Stay with original choice
            self._transition_to_reveal(self.player_guess)

    def _transition_to_reveal(self, final_guess: int):
        """Go to the reveal state with the given final guess."""
        for cup in self.cups:
            cup.highlighted = False
        from game import GameState
        self.game.player_guess = final_guess
        self.game.change_state(GameState.REVEAL)

    # --- update & draw ----------------------------------------------------

    def update(self, dt: float):
        """Update the Monty Hall state."""
        self.backdrop.update(dt, direction="down")

        for cup in self.cups:
            cup.update(dt)

        if self.phase == self.PHASE_ANIMATING:
            if not self.cups[self.reveal_cup_index].moving:
                self.phase = self.PHASE_SWITCH_OR_STAY

        elif self.phase == self.PHASE_SWITCHING:
            self._switch_timer += dt
            if self._switch_timer >= self.SWITCH_PAUSE:
                self._transition_to_reveal(self._final_guess)

    def draw(self, surface: pygame.Surface):
        """Draw the Monty Hall state."""
        if self.phase == self.PHASE_ANIMATING:
            message = "Monty Hall onthult een lege beker..."
        elif self.phase == self.PHASE_SWITCHING:
            message = "Gewisseld!"
        else:
            message = "Wisselen (W) of Zelfde (Z / Enter)?"

        def draw_content(s):
            # "Monty Hall" title above the cups
            font_title = pygame.font.Font(None, 120)
            title = font_title.render("Monty Hall", True, self.TITLE_COLOR)
            title_rect = title.get_rect(
                center=(self.SCREEN_WIDTH // 2, layout.PLAY_AREA_TOP + 80)
            )
            s.blit(title, title_rect)

            # Ellipsis at the revealed cup's resting spot (once it's gone)
            if self.phase in (self.PHASE_SWITCH_OR_STAY, self.PHASE_SWITCHING):
                font_ell = pygame.font.Font(None, 96)
                ell = font_ell.render("...", True, self.ELLIPSIS_COLOR)
                ell_rect = ell.get_rect(center=(self._ellipsis_x, self._ellipsis_y))
                s.blit(ell, ell_rect)

            # Draw cups
            for cup in self.cups:
                cup.draw(s)

        self._draw_state(surface, message, draw_content)
