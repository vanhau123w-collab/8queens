import tkinter as tk
import numpy as np
import queue
from PIL import Image, ImageTk
import heapq

root = tk.Tk()
root.title("8 QUEENS")
root.minsize(600, 600)
root.geometry("1400x700+50+50")
root.configure(bg="#F0F8FF")

greeting = tk.Label(root, text="8 QUEENS \u2655",
                    font=("Segoe UI", 30, "bold"),
                    bg="#F0F8FF", fg="#2F4F4F")
greeting.pack(pady=10)

img = Image.open("queen_white.png")
img = img.resize((60, 60))
queen_white = ImageTk.PhotoImage(img)

frame1 = tk.Frame(root, width=560, height=560, bg="#DCDCDC")
frame1.pack(padx=20, pady=20, side='left')
cell_size = 560 // 8
for i in range(8):
    for j in range(8):
        x = j * cell_size
        y = i * cell_size
        color = "#F8F8F8" if (i + j) % 2 == 0 else "#2F2F2F"
        btn = tk.Label(frame1, bg=color, relief="flat")
        btn.place(x=x, y=y, width=cell_size, height=cell_size)

frame2 = tk.Frame(root, width=560, height=560, bg="#DCDCDC")
frame2.pack(padx=20, pady=20, side='right')

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

def Solve_BFS_steps():
    q = queue.Queue()
    steps = []
    board = np.zeros((8, 8), dtype=int)
    q.put((board, 0))
    while not q.empty():
        b, r = q.get()
        steps.append(np.copy(b))
        if r == 8:
            continue
        for c in range(8):
            if is_safe(b, r, c):
                new_board = np.copy(b)
                new_board[r][c] = 1
                q.put((new_board, r + 1))
    return steps

def Solve_UCS_steps():
    heap = []
    steps = []
    board = np.zeros((8, 8), dtype=int)
    counter = 0  # Biến đếm duy nhất cho mỗi trạng thái
    heapq.heappush(heap, (0, counter, board, 0))
    while heap:
        cost, _, b, r = heapq.heappop(heap)
        steps.append(np.copy(b))
        if r == 8:
            continue
        for c in range(8):
            if is_safe(b, r, c):
                new_board = np.copy(b)
                new_board[r][c] = 1
                counter += 1
                heapq.heappush(heap, (cost + 1, counter, new_board, r + 1))
    return steps

def Solve_DFS_steps():
    steps = []
    board = np.zeros((8, 8), dtype=int)
    def dfs(row):
        steps.append(np.copy(board))
        if row == 8:
            return
        for col in range(8):
            if is_safe(board, row, col):
                board[row][col] = 1
                dfs(row + 1)
                board[row][col] = 0
    dfs(0)
    return steps

def show_board(board):
    cell_size = 560 // 8
    for widget in frame2.winfo_children():
        widget.destroy()
    for i in range(8):
        for j in range(8):
            x = j * cell_size
            y = i * cell_size
            color = "#F8F8F8" if (i + j) % 2 == 0 else "#2F2F2F"
            if board[i][j] == 1:
                btn = tk.Label(frame2, image=queen_white, bg=color)
                btn.image = queen_white
                btn.place(x=x, y=y, width=cell_size, height=cell_size)
            else:
                btn = tk.Label(frame2, bg=color, relief="flat")
                btn.place(x=x, y=y, width=cell_size, height=cell_size)

# Biến lưu các bước và chỉ số các phương án
solution_steps = []
solution_indices = []
current_solution = 0

def solve_click():
    global solution_steps, solution_indices, current_solution
    if algo_var.get() == "BFS":
        steps = Solve_BFS_steps()
    elif algo_var.get() == "DFS":
        steps = Solve_DFS_steps()
    else:  # UCS
        steps = Solve_UCS_steps()
    solution_steps = steps
    solution_indices = []
    for idx, board in enumerate(steps):
        if np.sum(board) == 8:
            solution_indices.append(idx)
    current_solution = 0
    auto_run_solution(current_solution)

def auto_run_solution(sol_idx):
    if sol_idx >= len(solution_indices):
        return
    start = solution_indices[sol_idx-1]+1 if sol_idx > 0 else 0
    end = solution_indices[sol_idx]
    def run_step(idx):
        if idx > end:
            return
        show_board(solution_steps[idx])
        root.after(50, run_step, idx+1)
    run_step(start)

def continue_click():
    global current_solution
    current_solution += 1
    if current_solution < len(solution_indices):
        auto_run_solution(current_solution)

solve_button = tk.Button(root, text="Giải bài toán",
                         font=("Segoe UI", 15, "bold"),
                         bg="#2F4F4F", fg="#F0F8FF",
                         relief="flat", padx=20, pady=10)
solve_button.pack(pady=10)
solve_button.config(command=solve_click)

continue_button = tk.Button(root, text="Phương án kế tiếp",
                            font=("Segoe UI", 15, "bold"),
                            bg="#2F4F4F", fg="#F0F8FF",
                            relief="flat", padx=20, pady=10)
continue_button.pack(pady=10)
continue_button.config(command=continue_click)

algo_frame = tk.LabelFrame(root, text="Chọn thuật toán", font=("Segoe UI", 15, "bold"),
                          bg="#F0F8FF", fg="#2F4F4F", padx=10, pady=10, bd=2, relief="groove")
algo_frame.pack(pady=10)

algo_var = tk.StringVar(value="BFS")
bfs_radio = tk.Radiobutton(algo_frame, text="BFS", variable=algo_var, value="BFS",
                          font=("Segoe UI", 13), bg="#F0F8FF", fg="#2F4F4F", selectcolor="#DCDCDC", padx=10, pady=5)
dfs_radio = tk.Radiobutton(algo_frame, text="DFS", variable=algo_var, value="DFS",
                          font=("Segoe UI", 13), bg="#F0F8FF", fg="#2F4F4F", selectcolor="#DCDCDC", padx=10, pady=5)
ucs_radio = tk.Radiobutton(algo_frame, text="UCS", variable=algo_var, value="UCS",
                          font=("Segoe UI", 13), bg="#F0F8FF", fg="#2F4F4F", selectcolor="#DCDCDC", padx=10, pady=5)
bfs_radio.pack(anchor="w")
dfs_radio.pack(anchor="w")
ucs_radio.pack(anchor="w")

root.mainloop()