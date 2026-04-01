"""Shuffle move implementations for the game."""

import layout
from cup import Cup


class ShuffleMove:
    """Represents a shuffle move in the game."""
    
    # Standard movement duration in seconds (halved speed = double duration)
    MOVE_DURATION = 1.0
    
    def __init__(self, move_type: str):
        """Initialize a shuffle move.
        
        Args:
            move_type: Type of move - 'none', 'l-m', 'm-r', 'l-r', 'l-m-r', or 'r-m-l'
        """
        self.move_type = move_type
    
    def execute(self, cups: list):
        """Execute the shuffle move on the cups.
        
        Args:
            cups: List of Cup objects
        """
        if self.move_type == "none":
            self._execute_none(cups)
        elif self.move_type == "l-m":
            self._execute_l_m(cups)
        elif self.move_type == "m-r":
            self._execute_m_r(cups)
        elif self.move_type == "l-r":
            self._execute_l_r(cups)
        elif self.move_type == "l-m-r":
            self._execute_l_m_r(cups)
        elif self.move_type == "r-m-l":
            self._execute_r_m_l(cups)
    
    def _get_sorted_cups(self, cups: list):
        """Return cups sorted by x position (left, middle, right)."""
        return sorted(cups, key=lambda c: c.x)
    
    def _execute_synchronized_moves(self, moves: list):
        """Execute multiple cup moves with synchronized timing.
        
        Args:
            moves: List of tuples (cup, target_x, target_y)
        """
        # Calculate maximum distance to determine duration
        max_distance = 0
        for cup, target_x, target_y in moves:
            dx = target_x - cup.x
            dy = target_y - cup.y
            distance = (dx**2 + dy**2)**0.5
            max_distance = max(max_distance, distance)
        
        # Execute all moves with synchronized duration
        for cup, target_x, target_y in moves:
            cup.move_to(target_x, target_y, duration=self.MOVE_DURATION)
    
    def _execute_none(self, cups: list):
        """Execute the 'none' move: all cups toggle vertically."""
        center_y = layout.get_cup_center_y()
        up_y = layout.get_cup_up_position()
        down_y = layout.get_cup_down_position()
        
        moves = []
        for cup in cups:
            if cup.y < center_y:
                moves.append((cup, cup.x, down_y))
            else:
                moves.append((cup, cup.x, up_y))
        
        self._execute_synchronized_moves(moves)
    
    def _execute_l_m(self, cups: list):
        """Execute the 'l-m' move: cups at left and middle swap horizontally, 
        cup at right toggles vertically."""
        center_y = layout.get_cup_center_y()
        up_y = layout.get_cup_up_position()
        down_y = layout.get_cup_down_position()
        
        sorted_cups = self._get_sorted_cups(cups)
        cup_left = sorted_cups[0]
        cup_middle = sorted_cups[1]
        cup_right = sorted_cups[2]
        
        moves = [
            (cup_left, layout.POSITION_MIDDLE, cup_left.y),
            (cup_middle, layout.POSITION_LEFT, cup_middle.y),
        ]
        
        # Right cup toggles vertically
        if cup_right.y < center_y:
            moves.append((cup_right, cup_right.x, down_y))
        else:
            moves.append((cup_right, cup_right.x, up_y))
        
        self._execute_synchronized_moves(moves)
    
    def _execute_m_r(self, cups: list):
        """Execute the 'm-r' move: cups at middle and right swap horizontally, 
        cup at left toggles vertically."""
        center_y = layout.get_cup_center_y()
        up_y = layout.get_cup_up_position()
        down_y = layout.get_cup_down_position()
        
        sorted_cups = self._get_sorted_cups(cups)
        cup_left = sorted_cups[0]
        cup_middle = sorted_cups[1]
        cup_right = sorted_cups[2]
        
        moves = [
            (cup_middle, layout.POSITION_RIGHT, cup_middle.y),
            (cup_right, layout.POSITION_MIDDLE, cup_right.y),
        ]
        
        # Left cup toggles vertically
        if cup_left.y < center_y:
            moves.append((cup_left, cup_left.x, down_y))
        else:
            moves.append((cup_left, cup_left.x, up_y))
        
        self._execute_synchronized_moves(moves)
    
    def _execute_l_r(self, cups: list):
        """Execute the 'l-r' move: cups at left and right swap positions diagonally 
        (both horizontally and vertically), cup at middle toggles vertically."""
        center_y = layout.get_cup_center_y()
        up_y = layout.get_cup_up_position()
        down_y = layout.get_cup_down_position()
        
        sorted_cups = self._get_sorted_cups(cups)
        cup_left = sorted_cups[0]
        cup_middle = sorted_cups[1]
        cup_right = sorted_cups[2]
        
        moves = [
            (cup_left, layout.POSITION_RIGHT, down_y if cup_left.y < center_y else up_y),   # Left moves to right, toggles vertical
            (cup_right, layout.POSITION_LEFT, down_y if cup_right.y < center_y else up_y),  # Right moves to left, toggles vertical
        ]
        
        # Middle cup toggles vertically
        if cup_middle.y < center_y:
            moves.append((cup_middle, cup_middle.x, down_y))
        else:
            moves.append((cup_middle, cup_middle.x, up_y))
        
        self._execute_synchronized_moves(moves)
    
    def _execute_l_m_r(self, cups: list):
        """Execute the 'l-m-r' move: cups rotate left -> middle -> right -> left.
        The cup moving from right to left (longest distance) also moves diagonally."""
        center_y = layout.get_cup_center_y()
        
        sorted_cups = self._get_sorted_cups(cups)
        cup_left = sorted_cups[0]
        cup_middle = sorted_cups[1]
        cup_right = sorted_cups[2]
        
        # Determine consistent vertical position - use the middle cup's position
        middle_y = cup_middle.y
        
        moves = [
            (cup_left, layout.POSITION_MIDDLE, cup_left.y),      # Left to middle, same vertical
            (cup_middle, layout.POSITION_RIGHT, cup_middle.y),    # Middle to right, same vertical
            (cup_right, layout.POSITION_LEFT, middle_y),          # Right to left, diagonal to middle height
        ]
        
        self._execute_synchronized_moves(moves)
    
    def _execute_r_m_l(self, cups: list):
        """Execute the 'r-m-l' move: cups rotate right -> middle -> left -> right.
        The cup moving from left to right (longest distance) also moves diagonally."""
        center_y = layout.get_cup_center_y()
        
        sorted_cups = self._get_sorted_cups(cups)
        cup_left = sorted_cups[0]
        cup_middle = sorted_cups[1]
        cup_right = sorted_cups[2]
        
        # Determine consistent vertical position - use the middle cup's position
        middle_y = cup_middle.y
        
        moves = [
            (cup_left, layout.POSITION_RIGHT, middle_y),          # Left to right, diagonal to middle height
            (cup_middle, layout.POSITION_LEFT, cup_middle.y),     # Middle to left, same vertical
            (cup_right, layout.POSITION_MIDDLE, cup_right.y),     # Right to middle, same vertical
        ]
        
        self._execute_synchronized_moves(moves)
