from typing import List, Optional
import numpy as np
from src.logging_config import logger

class SudokuValidator:
    """
    Validation logic for Sudoku boards and moves.
    """
    
    @staticmethod
    def is_valid_board(board: List[List[int]]) -> bool:
        """Checks if the initial board config is valid (no duplicates in rows, cols, or boxes)."""
        if not board or len(board) != 9 or any(len(row) != 9 for row in board):
            logger.error("Invalid board dimensions")
            return False
            
        board_np = np.array(board)
        
        # Check rows and columns
        for i in range(9):
            if not SudokuValidator._is_valid_group(board_np[i, :]) or \
               not SudokuValidator._is_valid_group(board_np[:, i]):
                return False
                
        # Check 3x3 boxes
        for r in range(0, 9, 3):
            for c in range(0, 9, 3):
                box = board_np[r:r+3, c:c+3].flatten()
                if not SudokuValidator._is_valid_group(box):
                    return False
                    
        return True

    @staticmethod
    def _is_valid_group(group: np.ndarray) -> bool:
        """Helper to check for duplicates in a 1D array, ignoring zeros."""
        nums = group[group != 0]
        return len(nums) == len(set(nums))

    @staticmethod
    def is_safe_move(board: List[List[int]], row: int, col: int, num: int) -> bool:
        """Checks if placing num at board[row][col] is valid."""
        # Row check
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Column check
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Box check
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        
        return True

    @staticmethod
    def is_solved(board: List[List[int]]) -> bool:
        """Verifies if the board is completely and correctly filled."""
        board_np = np.array(board)
        if 0 in board_np:
            return False
            
        # If no zeros, just check if it's overall valid
        return SudokuValidator.is_valid_board(board)
