import random
from .helpers import valid

class SudokuGenerator:
    def __init__(self, difficulty='medium'):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.difficulty = difficulty

    def fill_diagonal(self):
        """Fills the three diagonal 3x3 matrices."""
        for i in range(0, 9, 3):
            self.fill_box(i, i)

    def fill_box(self, row, col):
        """Fills a 3x3 box with random numbers 1-9."""
        num_list = list(range(1, 10))
        random.shuffle(num_list)
        for i in range(3):
            for j in range(3):
                self.grid[row + i][col + j] = num_list.pop()

    def solve_grid(self):
        """Recursively fills the rest of the grid to create a complete valid Soduko."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if valid(self.grid, i, j, num):
                            self.grid[i][j] = num
                            if self.solve_grid():
                                return True
                            self.grid[i][j] = 0
                    return False
        return True

    def remove_digits(self):
        """Removes digits based on difficulty level."""
        count = {
            'easy': 30,
            'medium': 45,
            'hard': 55
        }.get(self.difficulty, 45)

        while count > 0:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if self.grid[i][j] != 0:
                self.grid[i][j] = 0
                count -= 1

    def generate_puzzle(self):
        """Generates a new random Sudoku puzzle."""
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_diagonal()
        self.solve_grid()
        self.remove_digits()
        return [row[:] for row in self.grid]

def generate_new_puzzle(difficulty='medium'):
    generator = SudokuGenerator(difficulty)
    return generator.generate_puzzle()
