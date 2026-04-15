# Balletje-Balletje

A modern recreation of the classic 80s shell game, originally written
by John DRJ Vanderaert for the C64.

Three cups shuffle a ball. Can you follow it?

## Setup

Install dependencies first:

```bash
python -m pip install -r requirements.txt
```

## Running the game

### Linux

```bash
chmod +x runme.sh
./runme.sh
```

### Windows (PowerShell)

```powershell
.\Scripts\Activate.ps1
python .\game.py
```

## How to play

1. A ball appears at one of three positions.
2. Three cups drop over the ball and shuffle.
3. Press **1**, **2**, **3** or click a cup to make your guess.
4. Your cup highlights in gold. Press **J** (or Enter) to confirm.
5. Optionally press **N** for the Monty Hall help line — the host reveals a losing cup
   and you may switch to the remaining one.

## Controls

| Key | Action |
| --- | --- |
| Space | Start game / return to start screen |
| 1 / 2 / 3 | Select left / middle / right cup |
| J or Enter | Confirm guess |
| N | Monty Hall help line |
| W | Switch to the other cup (Monty Hall) |
| Z or Enter | Stay with your cup (Monty Hall) |

## Credits

Ball sprite: "Amigo Ball" (CC0 licence), from [opengameart.org](https://opengameart.org).
