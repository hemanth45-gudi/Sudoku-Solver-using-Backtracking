"""
dlx_solver.py
=============
Dancing Links (DLX) implementation of Donald Knuth's Algorithm X
for solving Sudoku puzzles by reducing them to an Exact Cover problem.

References:
  - Knuth, D.E. (2000). "Dancing Links". arXiv:cs/0011047
  - https://en.wikipedia.org/wiki/Dancing_Links
"""

import time
from typing import Optional


# ---------------------------------------------------------------------------
# Column / Node data structures
# ---------------------------------------------------------------------------

class Node:
    """Circular doubly-linked list node (up/down/left/right + column header)."""

    __slots__ = ("left", "right", "up", "down", "column", "row_id")

    def __init__(self):
        self.left: "Node" = self
        self.right: "Node" = self
        self.up: "Node" = self
        self.down: "Node" = self
        self.column: Optional["ColumnNode"] = None
        self.row_id: int = -1  # index into the solution row list


class ColumnNode(Node):
    """Header node for a column in the Dancing Links matrix."""

    __slots__ = ("size", "name")

    def __init__(self, name: str):
        super().__init__()
        self.size: int = 0          # number of 1s in this column
        self.name: str = name
        self.column = self          # column header points to itself


# ---------------------------------------------------------------------------
# DLX Solver
# ---------------------------------------------------------------------------

class DLXSolver:
    """
    Solves 9×9 Sudoku using Algorithm X with Dancing Links (DLX).

    Constraint types (4 * 81 = 324 columns total):
      0–80   : cell constraint   – each cell has exactly one digit
      81–161 : row constraint    – each row contains each digit once
      162–242: column constraint – each column contains each digit once
      243–323: box constraint    – each 3×3 box contains each digit once
    """

    COLS = 324          # total constraint columns
    N = 9               # grid size

    def __init__(self):
        self.solution_rows: list[int] = []
        self.result: Optional[list[list[int]]] = None
        self.nodes_visited: int = 0
        self.backtracks: int = 0
        self.solve_time: float = 0.0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def solve(self, board: list[list[int]]) -> Optional[list[list[int]]]:
        """
        Solve a 9×9 Sudoku board (0 = empty cell).

        Returns the solved board (list[list[int]]) or None if unsolvable.
        """
        self.nodes_visited = 0
        self.backtracks = 0
        self.result = None
        self.solution_rows = []

        start = time.perf_counter()

        # Build the exact-cover matrix
        header, row_map = self._build_matrix(board)

        # Run Algorithm X
        self._search(header)

        self.solve_time = time.perf_counter() - start

        if self.result is not None:
            return self._decode(self.result, row_map)
        return None

    # ------------------------------------------------------------------
    # Matrix Construction
    # ------------------------------------------------------------------

    def _build_matrix(self, board: list[list[int]]):
        """Build the sparse exact-cover matrix for the given board state."""
        N = self.N

        # Create column headers
        header = ColumnNode("root")
        col_headers: list[ColumnNode] = []
        for i in range(self.COLS):
            c = ColumnNode(str(i))
            c.left = header.left
            c.right = header
            header.left.right = c
            header.left = c
            col_headers.append(c)

        # row_map[row_id] -> (r, c, d)  so we can decode the solution
        row_map: list[tuple[int, int, int]] = []

        for r in range(N):
            for c in range(N):
                digit_start = 1 if board[r][c] == 0 else board[r][c]
                digit_end   = 9 if board[r][c] == 0 else board[r][c]

                for d in range(digit_start, digit_end + 1):
                    row_id = len(row_map)
                    row_map.append((r, c, d))

                    # Compute the four constraint column indices
                    box = (r // 3) * 3 + (c // 3)
                    cols4 = [
                        r * N + c,                   # cell constraint
                        81  + r * N + (d - 1),       # row constraint
                        162 + c * N + (d - 1),       # col constraint
                        243 + box * N + (d - 1),     # box constraint
                    ]

                    nodes: list[Node] = []
                    for ci in cols4:
                        col_hdr = col_headers[ci]
                        node = Node()
                        node.column = col_hdr
                        node.row_id = row_id

                        # Link into column (above column header)
                        node.up = col_hdr.up
                        node.down = col_hdr
                        col_hdr.up.down = node
                        col_hdr.up = node
                        col_hdr.size += 1

                        nodes.append(node)

                    # Link nodes in this row left-to-right circularly
                    for i, node in enumerate(nodes):
                        node.left  = nodes[(i - 1) % 4]
                        node.right = nodes[(i + 1) % 4]

        return header, row_map

    # ------------------------------------------------------------------
    # Algorithm X (recursive search)
    # ------------------------------------------------------------------

    def _search(self, header: ColumnNode):
        if self.result is not None:
            return  # already found a solution

        self.nodes_visited += 1

        if header.right is header:
            # All constraints satisfied → solution found
            self.result = list(self.solution_rows)
            return

        # Choose column with minimum size (S-heuristic)
        col = self._choose_column(header)
        if col.size == 0:
            self.backtracks += 1
            return   # dead end

        self._cover(col)

        row_node = col.down
        while row_node is not col:
            self.solution_rows.append(row_node.row_id)

            # Cover all other columns in this row
            j = row_node.right
            while j is not row_node:
                self._cover(j.column)
                j = j.right

            self._search(header)

            if self.result is not None:
                return  # propagate solution upward immediately

            # Undo (backtrack)
            self.solution_rows.pop()
            j = row_node.left
            while j is not row_node:
                self._uncover(j.column)
                j = j.left

            row_node = row_node.down
            if self.result is None and row_node is col:
                self.backtracks += 1

        self._uncover(col)

    # ------------------------------------------------------------------
    # Cover / Uncover operations (O(1) pointer manipulation)
    # ------------------------------------------------------------------

    def _choose_column(self, header: ColumnNode) -> ColumnNode:
        """Select the column with the fewest 1s (minimum remaining values)."""
        best: Optional[ColumnNode] = None
        c = header.right
        while c is not header:
            if best is None or c.size < best.size:
                best = c
            c = c.right
        return best

    def _cover(self, col: ColumnNode):
        """Remove column and all rows containing a 1 in this column."""
        col.right.left = col.left
        col.left.right = col.right

        i = col.down
        while i is not col:
            j = i.right
            while j is not i:
                j.down.up = j.up
                j.up.down = j.down
                j.column.size -= 1
                j = j.right
            i = i.down

    def _uncover(self, col: ColumnNode):
        """Restore column and all rows that were removed by cover."""
        i = col.up
        while i is not col:
            j = i.left
            while j is not i:
                j.column.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up

        col.right.left = col
        col.left.right = col

    # ------------------------------------------------------------------
    # Decode solution row IDs → 9×9 board
    # ------------------------------------------------------------------

    def _decode(
        self,
        solution: list[int],
        row_map: list[tuple[int, int, int]],
    ) -> list[list[int]]:
        board = [[0] * 9 for _ in range(9)]
        for row_id in solution:
            r, c, d = row_map[row_id]
            board[r][c] = d
        return board


# ---------------------------------------------------------------------------
# Quick self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # World's hardest Sudoku (Arto Inkala, 2012)
    puzzle = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0],
    ]

    solver = DLXSolver()
    result = solver.solve(puzzle)

    if result:
        print("Solved!")
        for row in result:
            print(row)
        print(f"\nNodes visited : {solver.nodes_visited}")
        print(f"Backtracks    : {solver.backtracks}")
        print(f"Time          : {solver.solve_time*1000:.3f} ms")
    else:
        print("No solution found.")
