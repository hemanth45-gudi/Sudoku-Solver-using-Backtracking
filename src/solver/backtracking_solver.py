import time
from typing import List, Optional, Tuple
from src.solver.validator import SudokuValidator
from src.solver.benchmarker import Benchmarker
from src.logging_config import logger

class BacktrackingSolver:
    """
    Core backtracking algorithm for Sudoku solving.
    Production-ready, modular, and performant.
    """
    def __init__(self):
        self.steps = 0
        self.backtracks = 0
        self.solve_time: float = 0.0
        self.start_time: float = 0.0
        self.benchmarker = Benchmarker()

    def solve(self, board: List[List[int]]) -> Optional[List[List[int]]]:
        """
        Solves the Sudoku board using backtracking.
        Returns the solved board or None if unsolvable.
        """
        self.steps = 0
        self.backtracks = 0
        self.solve_time = 0.0
        
        if not SudokuValidator.is_valid_board(board):
            logger.error("Initial board state is invalid")
            return None
            
        self.benchmarker.start_benchmark()
        
        board_copy = [row[:] for row in board]
        if self._backtrack(board_copy):
            bench = self.benchmarker.end_benchmark("Backtracking", self.steps, self.backtracks)
            self.solve_time = bench.execution_time
            return board_copy
            
        logger.warning("No solution found for the provided puzzle")
        return None

    def _backtrack(self, board: List[List[int]]) -> bool:
        find = self._find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            self.steps += 1
            if SudokuValidator.is_safe_move(board, row, col, i):
                board[row][col] = i

                if self._backtrack(board):
                    return True

                self.backtracks += 1
                board[row][col] = 0

        return False

    def _find_empty(self, board: List[List[int]]) -> Optional[Tuple[int, int]]:
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)
        return None

class VisualSolver(BacktrackingSolver):
    """
    Visual version of the backtracking solver for GUI integration.
    """
    def __init__(self, gui_app):
        super().__init__()
        self.app = gui_app

    def visual_solve(self, board: List[List[int]]) -> bool:
        """Backtracking algorithm with real-time visualization for GUI."""
        import pygame # Local import to avoid dependency in non-GUI context
        
        find = self._find_empty(board)
        if not find:
            return True
        else:
            row, col = find
            self.app.current_pos = (row, col)

        for i in range(1, 10):
            self.steps += 1
            if SudokuValidator.is_safe_move(board, row, col, i):
                board[row][col] = i
                self.app.cell_state[(row, col)] = "TRYING"
                
                self.app.update_display()
                pygame.time.delay(int(self.app.solve_speed * 1000))

                if self.visual_solve(board):
                    self.app.cell_state[(row, col)] = "STABLE"
                    return True

                self.backtracks += 1
                board[row][col] = 0
                self.app.cell_state[(row, col)] = "BACKTRACK"
                self.app.update_display()
                pygame.time.delay(int(self.app.solve_speed * 1000))
                
        return False

    def run_solve(self, board: List[List[int]]) -> bool:
        """Wrapper for GUI to start the visual solve."""
        self.steps = 0
        self.backtracks = 0
        self.solve_time = 0.0
        self.app.cell_state.clear()
        
        if not SudokuValidator.is_valid_board(board):
            logger.error("Initial board state is invalid for visual solve")
            return False
            
        self.start_time = time.perf_counter()
        self.benchmarker.start_benchmark()
        success = self.visual_solve(board)
        bench = self.benchmarker.end_benchmark("Visual Backtracking", self.steps, self.backtracks)
        self.solve_time = bench.execution_time
        return success
