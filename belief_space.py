import numpy as np
import random

def generate_belief_state(num_queens=4):
    """
    Tạo trạng thái niềm tin hợp lệ cho 8-Queens,
    chỉ đặt num_queens hậu (mặc định 4),
    đảm bảo không cắn nhau.
    """
    n = 8
    board = np.zeros((n, n), dtype=int)

    def is_safe(board, row, col):
        for r in range(n):
            for c in range(n):
                if board[r, c] == 1:
                    if r == row or c == col or abs(r - row) == abs(c - col):
                        return False
        return True

    rows = list(range(n))
    random.shuffle(rows)
    placed = 0

    for row in rows:
        # tìm tất cả cột an toàn trong row này
        safe_cols = [c for c in range(n) if is_safe(board, row, c)]
        if not safe_cols:
            continue
        col = random.choice(safe_cols)
        board[row, col] = 1
        placed += 1
        if placed >= num_queens:
            break

    return board
