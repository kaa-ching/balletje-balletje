# BALLETJE-BALLETJE — Implementation Spec

> For project overview, game rules, and controls see [README.md](README.md).

## Layout and backdrop

During the entire game, there's a moving geometric backdrop. It is a scrolling checkerboard
of large (80px) tiles in vivid purple tones, with bold diagonal and cross lines within each
tile. The tile colours pulse slowly using a sine wave, making the background hypnotic and
hard to ignore.

Depending on where we are in the game, the backdrop scrolls down, up, or towards a corner.

The play field fills the full screen area above the message bar, without a surrounding border.

At the bottom of the screen (150px reserved) is a message bar with all player prompts.

## Cups

The cups are a brown rounded square (200×200px), slightly larger than the ball.
Each cup displays the text "CooTV" in a darker brown in the centre.

When the player has selected a cup, it is highlighted with a gold border (10px glow behind
the cup drawn in gold / #FFD700).

## Ball

The ball uses the "Amigo Ball" sprite sheet (amigo_big_strip.png, CC0 license, from opengameart.org).
It is an animated sprite rendered at 85% of its original frame size (226x220 pixels per frame, 10 frames total).
The sprite animates continuously wherever the ball is visible.

## Technology

The game is object-oriented, written in Python with pygame.
A `Cup` class knows whether it has a ball and can animate movement between positions.

## Game States

### Start screen

Displays "Balletje-" and "Balletje" (two lines) in large italic letters, centred vertically.
Message bar: "Druk op SPATIE om te starten".
On SPACE the title animates upward off-screen and the game transitions to Ball Visible.

### Ball visible

A ball appears at a random position (left / middle / right).
Message bar is empty.
After 1.5 seconds the cups automatically drop in from the top.

### Cups moving (covering the ball)

The cups descend from the top; each cup registers whether it covers the ball.
The ball itself becomes hidden.
Message bar: "Bekers komen eraan..."

### Cups to start positions

Left and right cups move one cup-height up; middle cup moves one cup-height down.
Message bar: "Klaar? Let op de bekers..."

### Shuffling

The cups execute 20 random shuffle moves:

- none  — cups move to the other vertical position.
- l-m   — l and m swap horizontally; r bobs vertically.
- m-r   — m and r swap horizontally; l bobs vertically.
- l-r   — l and r swap diagonally (fast); m bobs vertically.
- l-m-r — rotate: l→m, m→r, r→l.
- r-m-l — rotate: r→m, m→l, l→r.

All cups in a transition move simultaneously and arrive at the same time.
Message bar: "Husselen... (x/y)".

### Guessing — phase 1: picking

Cups return to the central vertical position.
Message bar: "Welke beker? (1-3 of klik)".
Player presses 1/2/3 or clicks a cup.

### Guessing — phase 2: confirming

The chosen cup gets a gold highlight.
Message bar: "Weet je het zeker? (J of N — hulplijn)".

- J or Enter → reveal (see below).
- N         → Monty Hall mode (see below).

Clicking the highlighted cup confirms; clicking a different cup re-selects.

### Reveal

The ball is shown at its correct location; all cups slide off-screen to the top (0.5s).

- Correct: message "Goed geraden! Druk op SPATIE" + confetti shower.
- Wrong: message "Helaas! De bal lag bij {positie}. SPATIE" + screen shake (0.6s, ±22px, decaying) + red flash overlay (0.9s, fades from alpha 180).
SPACE returns to the start screen.

### Monty Hall mode

Activated by pressing N at the confirmation screen.
The player's already-highlighted cup remains their initial choice.

  1. The host picks a cup that is NOT the player's choice and does NOT have the ball.
     That cup flies off-screen to the top (1s animation) and stays gone.
     An ellipsis ("...") is drawn at the spot where it was.
     "Monty Hall" is displayed in large gold text above the cups.
     Message bar: "Monty Hall onthult een lege beker..."

  2. Message bar: "Wisselen (W) of Zelfde (Z / Enter)?".
     - W     → highlight moves to the remaining cup; "Gewisseld!" shown for 1 second,
               then proceed to Reveal with the new cup.
     - Z / Enter → proceed to Reveal with the original cup.

  3. Reveal proceeds as normal (confetti on correct, shake+flash on wrong).
     The highlight is cleared before the reveal.

### Space bar

- Start screen → starts the game (triggers title exit animation)
- Reveal       → returns to the start screen
