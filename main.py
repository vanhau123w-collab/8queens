import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from board import show_board
from algorithms import *

root = tk.Tk()
root.title("8 QUEENS")
root.geometry("1400x900+50+0")
root.configure(bg="#F0F8FF")

# Load queen image (sau khi có root)
img = Image.open("queen_white.png")
img = img.resize((60, 60))
queen_white = ImageTk.PhotoImage(img)

# Frame trái
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

# Frame phải
frame2 = tk.Frame(root, width=560, height=560, bg="#DCDCDC")
frame2.pack(padx=20, pady=20, side='right')

solution_steps = []
solution_indices = []
current_solution = 0
skip_flag = False

def solve_click():
    global solution_steps, solution_indices, current_solution
    current_solution = 0

    algo = algo_var.get()
    if algo == "BFS":
        steps = Solve_BFS_steps()
    elif algo == "DFS":
        steps = Solve_DFS_steps()
    elif algo == "UCS":
        steps = Solve_UCS_steps()
    elif algo == "DLS":
        steps = Solve_DLS_steps()
    elif algo == "IDS":
        steps = Solve_IDS_steps()
    elif algo == "Greedy":
        steps = Solve_Greedy_steps()
    elif algo == "A*":
        steps = Solve_Astar_steps()
    elif algo == "Hill Climbing":
        steps = Solve_HillClimbing_steps()
    elif algo == "Simulated Annealing":
        steps = Solve_SimulatedAnnealing_steps()
    elif algo == "Beam Search":
        steps = Solve_BeamSearch_steps()
    elif algo == "Genetic Algorithm":
        steps = Solve_Genetic_steps()
    else:
        steps = []

    solution_steps = steps
    solution_indices = []

    for idx, board in enumerate(steps):
        if np.sum(board) == 8:
            solution_indices.append(idx)

    current_solution = 0

    if solution_indices:
        auto_run_solution(current_solution)

def auto_run_solution(sol_idx):
    global skip_flag
    if sol_idx >= len(solution_indices):
        return
    start = solution_indices[sol_idx-1]+1 if sol_idx > 0 else 0
    end = solution_indices[sol_idx]

    def run_step(idx):
        global skip_flag  
        if skip_flag:
            show_board(frame2, solution_steps[end], queen_white)
            skip_flag = False
            return
        if idx > end:
            return
        show_board(frame2, solution_steps[idx], queen_white)
        root.after(200, run_step, idx+1)
    run_step(start)

def continue_click():
    global current_solution
    current_solution += 1
    if current_solution < len(solution_indices):
        auto_run_solution(current_solution)

def skip_click():
    global skip_flag, current_solution
    skip_flag = True
    if current_solution < len(solution_indices):
        sol_idx = solution_indices[current_solution]
        show_board(frame2, solution_steps[sol_idx], queen_white)

# Buttons
solve_button = tk.Button(root, text="Giải bài toán",
                         font=("Segoe UI", 15, "bold"),
                         bg="#2F4F4F", fg="#F0F8FF",
                         relief="flat", padx=20, pady=10,
                         command=solve_click)
solve_button.pack(pady=10)

continue_button = tk.Button(root, text="Phương án kế tiếp",
                            font=("Segoe UI", 15, "bold"),
                            bg="#2F4F4F", fg="#F0F8FF",
                            relief="flat", padx=20, pady=10,
                            command=continue_click)
continue_button.pack(pady=10)

skip_button = tk.Button(root, text="Bỏ qua",
                        font=("Segoe UI", 15, "bold"),
                        bg="#2F4F4F", fg="#F0F8FF",
                        relief="flat", padx=20, pady=10,
                        command=skip_click)
skip_button.pack(pady=10)

algo_frame = tk.LabelFrame(root, text="Chọn thuật toán", font=("Segoe UI", 15, "bold"),
                          bg="#F0F8FF", fg="#2F4F4F", padx=10, pady=10, bd=2, relief="groove")
algo_frame.pack(pady=10)
algo_var = tk.StringVar(value="BFS")

algorithms = [
    "BFS", "DFS", "UCS", "DLS", "IDS",
    "Greedy", "A*", "Hill Climbing",
    "Simulated Annealing", "Beam Search",
    "Genetic Algorithm"
]

for algo in algorithms:
    tk.Radiobutton(algo_frame, text=algo, variable=algo_var, value=algo,
                   font=("Segoe UI", 13), bg="#F0F8FF", fg="#2F4F4F",
                   selectcolor="#DCDCDC", padx=10, pady=5).pack(anchor="w")

root.mainloop()
