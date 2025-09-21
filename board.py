import tkinter as tk
import numpy as np

cell_size = 560 // 8

def is_safe(board, row, col):
    for i in range(row):
        if board[i][col] == 1:
            return False
    for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(row-1, -1, -1), range(col+1, 8)):
        if board[i][j] == 1:
            return False
    return True


def show_board(frame, board, queen_img):
    """Hiển thị bàn cờ với trạng thái board"""
    for widget in frame.winfo_children():
        widget.destroy()
    for i in range(8):
        for j in range(8):
            x = j * cell_size
            y = i * cell_size
            color = "#F8F8F8" if (i + j) % 2 == 0 else "#2F2F2F"
            if board[i][j] == 1:
                btn = tk.Label(frame, image=queen_img, bg=color)
                btn.image = queen_img
                btn.place(x=x, y=y, width=cell_size, height=cell_size)
            else:
                btn = tk.Label(frame, bg=color, relief="flat")
                btn.place(x=x, y=y, width=cell_size, height=cell_size)
