import pygame
import numpy as np

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.header = None

class DancingLinks:
    def __init__(self, size):
        self.header = Node(-1, -1)
        self.columns = [self.add_column(i) for i in range(size)]
        self.row_count = 0

    def add_column(self, index):
        new_node = Node(-1, index)
        new_node.header = new_node
        if self.header.right is None:
            self.header.right = new_node
            new_node.left = self.header
        else:
            last_column = self.header.right
            while last_column.right is not None:
                last_column = last_column.right
            last_column.right = new_node
            new_node.left = last_column
        new_node.right = None
        return new_node

    def add_row(self, row):
        self.row_count += 1
        nodes = []
        for col in row:
            new_node = Node(self.row_count, col)
            nodes.append(new_node)
            self.link(new_node, self.columns[col])

        # Link the row nodes together
        for i in range(len(nodes)):
            nodes[i].right = nodes[(i + 1) % len(nodes)]
            nodes[i].left = nodes[(i - 1) % len(nodes)]

    def link(self, node, header):
        if header.down is None:
            header.down = node
            node.up = header
        else:
            last_node = header.down
            while last_node.down is not None:
                last_node = last_node.down
            last_node.down = node
            node.up = last_node
        node.down = None
        node.header = header

    def cover(self, column):
        # Remove the column from the matrix
        column_node = column
        column_node.left.right = column_node.right
        if column_node.right:
            column_node.right.left = column_node.left

        # Remove all rows that have a 1 in this column
        node = column_node.down
        while node is not None:
            row_node = node
            while row_node is not None:
                row_node.up.down = row_node.down
                if row_node.down:
                    row_node.down.up = row_node.up
                row_node = row_node.right
            node = node.down

    def uncover(self, column):
        # Reinsert the column into the matrix
        column_node = column
        column_node.left.right = column_node
        if column_node.right:
            column_node.right.left = column_node

        # Reinsert all rows that were removed
        node = column_node.down
        while node is not None:
            row_node = node
            while row_node is not None:
                row_node.up.down = row_node
                if row_node.down:
                    row_node.down.up = row_node
                row_node = row_node.right
            node = node.down

    def search(self):
        if self.header.right is None:  # All columns covered
            return True

        # Choose the next column to cover (heuristic: choose the column with the least number of 1's)
        column = self.header.right
        min_count = float('inf')
        chosen_column = None
        while column is not None:
            count = self.get_count(column)
            if count < min_count:
                min_count = count
                chosen_column = column
            column = column.right

        self.cover(chosen_column)

        # Try each row in the chosen column
        row_node = chosen_column.down
        while row_node is not None:
            self.choose_row(row_node)
            if self.search():
                return True
            self.unchoose_row(row_node)
            row_node = row_node.down

        self.uncover(chosen_column)
        return False

    def get_count(self, column):
        count = 0
        node = column.down
        while node is not None:
            count += 1
            node = node.down
        return count

    def choose_row(self, row_node):
        # Cover all columns in the selected row
        column_node = row_node
        while column_node is not None:
            self.cover(column_node.header)
            column_node = column_node.right

    def unchoose_row(self, row_node):
        # Uncover all columns in the unselected row
        column_node = row_node
        while column_node is not None:
            self.uncover(column_node.header)
            column_node = column_node.right

def create_sudoku_matrix(sudoku):
    size = 324  # 81 cells, 9 rows, 9 columns, 9 boxes
    matrix = []
    for r in range(9):
        for c in range(9):
            if sudoku[r][c] == 0:
                for num in range(1, 10):
                    row = [0] * size
                    row[r * 9 + c] = 1  # Cell constraint
                    row[9 * r + (num - 1)] = 1  # Row constraint
                    row[9 * (c + 9)] = 1  # Column constraint
                    row[9 * (r // 3 * 3 + c // 3) + (num - 1) + 18] = 1  # Box constraint
                    matrix.append(row)
            else:
                num = sudoku[r][c]
                row = [0] * size
                row[r * 9 + c] = 1  # Cell constraint
                row[9 * r + (num - 1)] = 1  # Row constraint
                row[9 * (c + 9)] = 1  # Column constraint
                row[9 * (r // 3 * 3 + c // 3) + (num - 1) + 18] = 1  # Box constraint
                matrix.append(row)
    return matrix

def draw_sudoku(screen, sudoku):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 48)
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                text = font.render(str(sudoku[i][j]), True, BLACK)
                screen.blit(text, (j * 60 + 15, i * 60 + 15))

    for i in range(1, 9):
        pygame.draw.line(screen, BLACK, (i * 60, 0), (i * 60, 540), 3)
        pygame.draw.line(screen, BLACK, (0, i * 60), (540, i * 60), 3)

    pygame.display.flip()

def backtrack(sudoku, row=0, col=0):
    if row == 9:  # If we have filled all rows
        return True

    if col == 9:  # Move to the next row
        return backtrack(sudoku, row + 1, 0)

    if sudoku[row][col] != 0:  # Skip filled cells
        return backtrack(sudoku, row, col + 1)

    for num in range(1, 10):  # Try numbers 1-9
        if is_safe(sudoku, row, col, num):
            sudoku[row][col] = num
            if backtrack(sudoku, row, col + 1):
                return True
            sudoku[row][col] = 0  # Reset on backtrack

    return False

def is_safe(sudoku, row, col, num):
    # Check row
    if num in sudoku[row]:
        return False

    # Check column
    if num in (sudoku[i][col] for i in range(9)):
        return False

    # Check 3x3 box
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if sudoku[box_row_start + i][box_col_start + j] == num:
                return False

    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku Solver with Dancing Links and Backtracking")

    sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    # Draw the initial Sudoku grid
    draw_sudoku(screen, sudoku)

    # Solve Sudoku using backtracking
    if backtrack(sudoku):
        print("Sudoku solved!")
    else:
        print("No solution found.")

    # Draw the solved Sudoku grid
    draw_sudoku(screen, sudoku)

    # Main loop to keep the window open
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
