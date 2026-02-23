import pytest
from src.solver.backtracking_solver import BacktrackingSolver
from src.solver.dlx_solver import DLXSolver
from src.solver.validator import SudokuValidator

@pytest.fixture
def easy_puzzle():
    return [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

@pytest.fixture
def invalid_puzzle():
    # Duplicate 5 in first row
    return [
        [5, 5, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

def test_validator_valid_board(easy_puzzle):
    assert SudokuValidator.is_valid_board(easy_puzzle) is True

def test_validator_invalid_board(invalid_puzzle):
    assert SudokuValidator.is_valid_board(invalid_puzzle) is False

def test_backtracking_solver(easy_puzzle):
    solver = BacktrackingSolver()
    result = solver.solve(easy_puzzle)
    assert result is not None
    assert SudokuValidator.is_solved(result) is True

def test_dlx_solver(easy_puzzle):
    solver = DLXSolver()
    result = solver.solve(easy_puzzle)
    assert result is not None
    assert SudokuValidator.is_solved(result) is True
