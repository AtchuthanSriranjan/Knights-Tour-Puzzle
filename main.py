"""
knights_tour_main.py

A Python script that finds a Knight's Tour on an N x N chessboard using Warnsdorff's heuristic

Usage examples:
python knights_tour_main.py --n 8
python knights_tour_main.py --n 8 --start 0 0

"""

from typing import List, Tuple, Optional
import argparse
import sys

# Knight moves all 8 possible moves counterclockwise
KNIGHT_MOVES: List[Tuple[int, int]] = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

class KnightsTour:
    def __init__(self, n: int, start: Tuple[int, int] = (0, 0)):
        """Initialize nxn board with -1 values and starting position. Each -1 means unvisted square"""
        if n < 1:
            raise ValueError("board size must be >= 1")
        self.n = n
        self.start = start
        self.board = [[-1 for i in range(n)] for i in range(n)]

    def _in_bounds(self, r: int, c: int):
         """Return True if (row, column) is inside the board boundaries."""
         return 0 <= r < self.n and 0 <= c < self.n

    def _is_free(self, r: int, c: int):
        """Return True if (row, column) is inside the board and unvisited"""
        return self._in_bounds(r, c) and self.board[r][c] == -1

    def _neighbors(self, r: int, c: int):
        """Generates all the possible moves which are legal"""
        return [(r + dr, c + dc) for dr, dc in KNIGHT_MOVES if self._is_free(r + dr, c + dc)]

    def _warnsdorff_sort(self, r: int, c: int):
        """Sort available moves by the number of onward moves"""
        moves = self._neighbors(r, c)
        moves.sort(key=lambda pos: len(self._neighbors(pos[0], pos[1])))
        return moves

    def solve_warnsdorff(self):
        """Attempt to find a tour using Warnsdorff's heuristic"""
        r0, c0 = self.start
        self.board = [[-1 for i in range(self.n)] for i in range(self.n)]
        """list to store the sequence of visited squares"""
        path: List[Tuple[int, int]] = []
        r, c = r0, c0
        for step in range(self.n * self.n):
            self.board[r][c] = step
            path.append((r, c))
            if step == self.n * self.n - 1:
                return path
            next_moves = self._warnsdorff_sort(r, c)
            if not next_moves:
                return None
            # pick first legal move with least options
            r, c = next_moves[0]
        return None

    def print_board(self):
        """Print board with knight moving on the board"""
        width = len(str(self.n * self.n - 1))
        for r in range(self.n):
            row = " ".join((str(self.board[r][c]).rjust(width) if self.board[r][c] != -1 else '.' .rjust(width)) for c in range(self.n))
            print(row)

    def print_path(self, path: List[Tuple[int, int]]):
        """Print sequence of squares visited."""
        print("Move sequence (row, col):")
        for i, (r, c) in enumerate(path):
            print(f"{i:3d}: ({r}, {c})")


def parse_args():
    parser = argparse.ArgumentParser(description="Knight's Tour solver (Warnsdorff)")
    parser.add_argument('--n', type=int, default=8, help='board size n (n x n)')
    parser.add_argument('--start', nargs=2, type=int, metavar=('R', 'C'), help='starting square row and col (0-indexed)')
    parser.add_argument('--method', choices=['warnsdorff'], default='warnsdorff', help='solving method')
    parser.add_argument('--quiet', action='store_true', help='only print whether solution found')
    return parser.parse_args()


def main():
    args = parse_args()
    start = tuple(args.start) if args.start else (0, 0)
    kt = KnightsTour(args.n, start)
    method = args.method

    print(f"Knight's Tour: {args.n}x{args.n}, start={start}, method={method}")

    if method == 'warnsdorff':
        path = kt.solve_warnsdorff()

    if path:
        print("Solution found!")
        if not args.quiet:
            kt.print_board()
            print()
            kt.print_path(path)
    else:
        print("No solution found with the chosen method / parameters.")


if __name__ == '__main__':
    main()
