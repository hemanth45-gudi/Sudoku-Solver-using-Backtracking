"""
compare_algorithms.py
=====================
Head-to-head benchmark: Backtracking vs DLX (Dancing Links).

Run from the project root:
    python compare_algorithms.py
"""

import time
import copy
from typing import Optional

# ── Load existing backtracking solver ─────────────────────────────────────────
try:
    from src.solver.solver import solve_sudoku as backtrack_solve  # adjust if needed
    BACKTRACK_AVAILABLE = True
except ImportError:
    BACKTRACK_AVAILABLE = False

from src.solver.dlx_solver import DLXSolver


# ── Reference backtracking (self-contained fallback) ──────────────────────────

def _backtrack(board: list[list[int]]) -> bool:
    """Standard recursive backtracking solver (in-place)."""
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                for d in range(1, 10):
                    if _is_valid(board, r, c, d):
                        board[r][c] = d
                        if _backtrack(board):
                            return True
                        board[r][c] = 0
                return False
    return True


def _is_valid(board, row, col, num) -> bool:
    if num in board[row]:
        return False
    if num in [board[r][col] for r in range(9)]:
        return False
    br, bc = (row // 3) * 3, (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            if board[r][c] == num:
                return False
    return True


def solve_backtrack(board: list[list[int]]) -> tuple[Optional[list[list[int]]], float]:
    """Return (solved_board_or_None, elapsed_seconds)."""
    b = copy.deepcopy(board)
    t0 = time.perf_counter()
    solved = _backtrack(b)
    elapsed = time.perf_counter() - t0
    return (b if solved else None), elapsed


def solve_dlx(board: list[list[int]]) -> tuple[Optional[list[list[int]]], float]:
    """Return (solved_board_or_None, elapsed_seconds)."""
    solver = DLXSolver()
    result = solver.solve(board)   # timing is done internally too
    return result, solver.solve_time


# ── Test puzzles ───────────────────────────────────────────────────────────────

PUZZLES = {
    "Easy": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ],
    "Medium": [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ],
    "Hard": [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0],
    ],
    "Expert (Arto Inkala)": [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0],
    ],
}


# ── Pretty printer ─────────────────────────────────────────────────────────────

SEP_THICK = "╔═══════╦═══════╦═══════╗"
SEP_MID   = "╠═══════╬═══════╬═══════╣"
SEP_BOT   = "╚═══════╩═══════╩═══════╝"
SEP_THIN  = "║───────║───────║───────║"


def print_board(board: list[list[int]]):
    print(SEP_THICK)
    for r, row in enumerate(board):
        if r in (3, 6):
            print(SEP_MID)
        line = "║"
        for c, val in enumerate(row):
            line += f" {val if val else '·'}"
            if c in (2, 5):
                line += " ║"
        line += " ║"
        print(line)
    print(SEP_BOT)


# ── Benchmark runner ───────────────────────────────────────────────────────────

RUNS = 5   # average over multiple runs for stable timings


def benchmark(name: str, puzzle: list[list[int]]):
    print(f"\n{'━'*60}")
    print(f"  Puzzle: {name}")
    print(f"{'━'*60}")

    # --- Backtracking ---
    bt_times = []
    bt_result = None
    for _ in range(RUNS):
        bt_result, elapsed = solve_backtrack(puzzle)
        bt_times.append(elapsed)
    bt_avg = sum(bt_times) / RUNS * 1000   # ms

    # --- DLX ---
    dlx_solver = DLXSolver()
    dlx_times = []
    dlx_result = None
    for _ in range(RUNS):
        dlx_result = dlx_solver.solve(puzzle)
        dlx_times.append(dlx_solver.solve_time)
    dlx_avg = sum(dlx_times) / RUNS * 1000   # ms

    speedup = bt_avg / dlx_avg if dlx_avg > 0 else float("inf")

    print(f"\n  {'Algorithm':<22} {'Avg Time (ms)':>14}")
    print(f"  {'─'*38}")
    print(f"  {'Backtracking':<22} {bt_avg:>14.3f}")
    print(f"  {'DLX (Dancing Links)':<22} {dlx_avg:>14.3f}")
    print(f"\n  📊 DLX is {speedup:.1f}× {'faster' if speedup >= 1 else 'slower'} than Backtracking")
    print(f"  📍 DLX nodes visited : {dlx_solver.nodes_visited}")
    print(f"  📍 DLX backtracks    : {dlx_solver.backtracks}")

    if bt_result:
        print("\n  ✅ Backtracking solution:")
        print_board(bt_result)
    if dlx_result:
        print("\n  ✅ DLX solution (same board):")
        print_board(dlx_result)

    return {
        "puzzle": name,
        "bt_ms": bt_avg,
        "dlx_ms": dlx_avg,
        "speedup": speedup,
    }


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("\n" + "═" * 60)
    print("   Backtracking vs DLX – Sudoku Solver Performance Benchmark")
    print("═" * 60)

    results = []
    for name, puzzle in PUZZLES.items():
        results.append(benchmark(name, puzzle))

    # Summary table
    print(f"\n\n{'═'*72}")
    print(f"{'  SUMMARY TABLE':^72}")
    print(f"{'═'*72}")
    print(f"  {'Puzzle':<28} {'Backtrack (ms)':>14} {'DLX (ms)':>10} {'Speedup':>10}")
    print(f"  {'─'*66}")
    for r in results:
        bar = "▲" if r["speedup"] >= 1 else "▼"
        print(f"  {r['puzzle']:<28} {r['bt_ms']:>14.3f} {r['dlx_ms']:>10.3f} {bar}{r['speedup']:>8.1f}×")
    print(f"  {'─'*66}")
    print("\n  ▲ = DLX faster   ▼ = Backtracking faster")
    print(f"{'═'*72}\n")


if __name__ == "__main__":
    main()
