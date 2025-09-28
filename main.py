import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from board import show_board
from algorithms import *
from belief_space import *

# ---------- CẤU HÌNH ----------
AUTO_DELAY_MS = 250  # ms giữa các bước khi auto-run cho HC/SA/Beam/GA
# --------------------------------
root = tk.Tk()
root.title("8 QUEENS")
root.geometry("1400x900+50+0")
root.configure(bg="#F0F8FF")
main_frame = tk.Frame(root, bg="#F0F8FF")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)


# Load queen image
img = Image.open("queen_white.png")
img = img.resize((60, 60))
queen_white = ImageTk.PhotoImage(img)

# Hàm hiển thị trạng thái niềm tin chỉnh sửa
def create_belief_click():
    belief_board = generate_belief_state()
    show_board(frame_board, belief_board, queen_white)  # hiển thị lên frame_board

# Frame bàn cờ trái
frame1 = tk.Frame(main_frame, width=560, height=560+60, bg="#DCDCDC")  # +60 để chừa chỗ nút
frame1.pack(side="left", padx=10, pady=10)

# --- Frame cho nút ---
frame_button = tk.Frame(frame1, bg="#DCDCDC", height=50)
frame_button.pack(side="top", fill="x")

belief_button = tk.Button(frame_button, text="Tạo trạng thái niềm tin",
                          font=("Segoe UI", 12, "bold"),
                          bg="#2F4F4F", fg="#F0F8FF",
                          relief="flat", padx=10, pady=5,
                          command=create_belief_click)
belief_button.pack(pady=5)

# --- Frame cho bàn cờ ---
frame_board = tk.Frame(frame1, width=560, height=560, bg="#DCDCDC")
frame_board.pack(side="top", pady=5)

# Vẽ bàn cờ bằng Label lên frame_board
cell_size = 560 // 8
for i in range(8):
    for j in range(8):
        x = j * cell_size
        y = i * cell_size
        color = "#F8F8F8" if (i + j) % 2 == 0 else "#2F2F2F"
        lbl = tk.Label(frame_board, bg=color, relief="flat")
        lbl.place(x=x, y=y, width=cell_size, height=cell_size)

# Frame render bước phải
frame2 = tk.Frame(main_frame, width=560, height=560, bg="#DCDCDC")
frame2.pack(side="left", padx=10, pady=10)

# ========== Trạng thái chung ==========
solution_steps = []      # list of np.array boards (to show step-by-step)
solution_indices = []    # indices of boards which are full solutions (sum==8)
current_solution = 0     # chỉ số solution (dùng cho nhóm "nhiều nghiệm")
current_step = 0         # chỉ số step hiện tại (dùng cho auto-run hoặc step-by-step)
skip_flag = False
algo_running = ""        # tên thuật toán đang chạy
auto_running_job = None  # job id của root.after (để hủy nếu cần)

# ========== Hàm xử lý chính ==========
def solve_click():
    """Gọi khi bấm 'Giải bài toán'."""
    global solution_steps, solution_indices, current_solution, current_step, algo_running, auto_running_job

    # dừng auto cũ nếu đang chạy
    if auto_running_job is not None:
        try:
            root.after_cancel(auto_running_job)
        except Exception:
            pass
        auto_running_job = None

    current_solution = 0
    current_step = 0
    solution_steps = []
    solution_indices = []
    algo_running = algo_var.get()

    # Lấy steps từ algorithms.py
    if algo_running == "BFS":
        steps = Solve_BFS_steps()
    elif algo_running == "DFS":
        steps = Solve_DFS_steps()
    elif algo_running == "UCS":
        steps = Solve_UCS_steps()
    elif algo_running == "DLS":
        steps = Solve_DLS_steps()
    elif algo_running == "IDS":
        steps = Solve_IDS_steps()
    elif algo_running == "Greedy":
        steps = Solve_Greedy_steps()
    elif algo_running == "A*":
        steps = Solve_Astar_steps()
    elif algo_running == "Hill Climbing":
        steps = Solve_HillClimbing_steps()
    elif algo_running == "Simulated Annealing":
        steps = Solve_SimulatedAnnealing_steps()
    elif algo_running == "Beam Search":
        steps = Solve_BeamSearch_steps()
    elif algo_running == "Genetic Algorithm":
        steps = Solve_Genetic_steps()
    elif algo_running == "And-Or Search":
        # Khởi tạo board rỗng
        initial_board = np.zeros((8, 8), dtype=int)
        steps = and_or_search(initial_board)  # Trả về list các board tuần tự
        solution_indices = [len(steps)-1]     # Chỉ số nghiệm cuối cùng
        current_solution = 0
        current_step = 0
    else:
        steps = []

    solution_steps = steps or []

    # tìm các bước là nghiệm hoàn chỉnh (sum == 8)
    for idx, board in enumerate(solution_steps):
        if np.sum(board) == 8 and idx not in solution_indices:
            solution_indices.append(idx)

    # hiển thị bước đầu (nếu có)
    if solution_steps:
        show_board(frame2, solution_steps[0], queen_white)

    # Nhóm auto-run (chạy từng bước hết danh sách)
    if algo_running in ["Hill Climbing", "Simulated Annealing", "Beam Search", "Genetic Algorithm", "And-Or Search"]:
        if len(solution_steps) > 1:
            start_auto_run_all_steps()
    else:
        if solution_indices:
            auto_run_solution(current_solution)


# ========== Auto-run toàn bộ steps cho HC/SA/Beam/GA ==========
def start_auto_run_all_steps():
    """Auto-run toàn bộ solution_steps từ step 0 đến cuối (dùng cho HC/SA/Beam/GA)."""
    global auto_running_job
    def runner(idx):
        global auto_running_job
        if idx >= len(solution_steps):
            auto_running_job = None
            return
        show_board(frame2, solution_steps[idx], queen_white)
        auto_running_job = root.after(AUTO_DELAY_MS, runner, idx+1)
    # bắt đầu
    runner(0)

# ========== Auto-run theo solution_indices (nhóm nhiều nghiệm) ==========
def auto_run_solution(sol_idx):
    """Chạy từ start -> end (start = prev_solution+1 hoặc 0) cho solution tại sol_idx."""
    global skip_flag, auto_running_job
    if sol_idx >= len(solution_indices):
        return
    start = solution_indices[sol_idx-1] + 1 if sol_idx > 0 else 0
    end = solution_indices[sol_idx]

    def run_step(idx):
        global skip_flag, auto_running_job
        if skip_flag:
            # nếu user bấm Skip, nhảy thẳng tới end
            show_board(frame2, solution_steps[end], queen_white)
            skip_flag = False
            auto_running_job = None
            return
        if idx > end:
            auto_running_job = None
            return
        show_board(frame2, solution_steps[idx], queen_white)
        auto_running_job = root.after(200, run_step, idx+1)

    run_step(start)

# ========== Step tiếp theo / Phương án kế tiếp ==========
def continue_click():
    global current_solution, current_step, auto_running_job
    # nếu auto đang chạy thì không làm gì
    if auto_running_job is not None:
        return

    if algo_running in ["Hill Climbing", "Simulated Annealing", "Beam Search", "Genetic Algorithm"]:
        # xem từng bước thủ công cho nhóm này
        if current_step + 1 < len(solution_steps):
            current_step += 1
            show_board(frame2, solution_steps[current_step], queen_white)
    else:
        # nhóm nhiều nghiệm: chuyển sang solution tiếp theo (nếu có)
        current_solution += 1
        if current_solution < len(solution_indices):
            auto_run_solution(current_solution)
        else:
            current_solution = len(solution_indices) - 1

# ========== Bỏ qua ==========
def skip_click():
    global skip_flag, current_solution, auto_running_job
    # nếu auto đang chạy thì hủy và trực tiếp nhảy
    if auto_running_job is not None:
        try:
            root.after_cancel(auto_running_job)
        except Exception:
            pass
        auto_running_job = None

    skip_flag = True
    if algo_running in ["Hill Climbing", "Simulated Annealing", "Beam Search", "Genetic Algorithm"]:
        # nhảy tới bước cuối cùng của steps (nghiệm cuối nếu có)
        if solution_steps:
            show_board(frame2, solution_steps[-1], queen_white)
    else:
        # nhóm nhiều nghiệm: nhảy tới nghiệm hiện tại (end)
        if current_solution < len(solution_indices):
            idx = solution_indices[current_solution]
            show_board(frame2, solution_steps[idx], queen_white)

# ========== Giao diện: nút, radio ==========
# Frame nút nằm dưới cùng
bottom_frame = tk.Frame(root, bg="#F0F8FF")
bottom_frame.pack(side="bottom", fill="x", pady=10)

solve_button = tk.Button(bottom_frame, text="Giải bài toán",
                         font=("Segoe UI", 15, "bold"),
                         bg="#2F4F4F", fg="#F0F8FF",
                         relief="flat", padx=20, pady=10,
                         command=solve_click)
solve_button.pack(side="left", padx=10)

continue_button = tk.Button(bottom_frame, text="Phương án kế tiếp / Bước tiếp theo",
                            font=("Segoe UI", 15, "bold"),
                            bg="#2F4F4F", fg="#F0F8FF",
                            relief="flat", padx=20, pady=10,
                            command=continue_click)
continue_button.pack(side="left", padx=10)

skip_button = tk.Button(bottom_frame, text="Bỏ qua",
                        font=("Segoe UI", 15, "bold"),
                        bg="#2F4F4F", fg="#F0F8FF",
                        relief="flat", padx=20, pady=10,
                        command=skip_click)
skip_button.pack(side="left", padx=10)

# Frame thuật toán bên phải
right_frame = tk.Frame(main_frame, bg="#F0F8FF")
right_frame.pack(side="left", fill="y", padx=10)

algo_frame = tk.LabelFrame(right_frame, text="Chọn thuật toán",
                           font=("Segoe UI", 15, "bold"),
                           bg="#F0F8FF", fg="#2F4F4F",
                           padx=10, pady=10, bd=2, relief="groove")
algo_frame.pack(pady=20, anchor="n") 

algo_var = tk.StringVar(value="BFS")
algorithms = [
    "BFS", "DFS", "UCS", "DLS", "IDS",
    "Greedy", "A*", "Hill Climbing",
    "Simulated Annealing", "Beam Search",
    "Genetic Algorithm", "And-Or Search" 
]

for algo in algorithms:
    tk.Radiobutton(algo_frame, text=algo, variable=algo_var, value=algo,
                   font=("Segoe UI", 13), bg="#F0F8FF", fg="#2F4F4F",
                   selectcolor="#DCDCDC", padx=10, pady=5).pack(anchor="w")

# Start GUI
root.state("zoomed")
root.mainloop()
