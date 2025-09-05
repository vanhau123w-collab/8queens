import tkinter as tk
import numpy as np
import queue
from PIL import Image, ImageTk
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
    # Kiểm tra cột
    for i in range(row):
        if board[i][col] == 1:
            return False
    # Kiểm tra đường chéo trái trên
    for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
        if board[i][j] == 1:
            return False
    # Kiểm tra đường chéo phải trên
    for i, j in zip(range(row-1, -1, -1), range(col+1, 8)):
        if board[i][j] == 1:
            return False
    return True

def Solve():
    q = queue.Queue()
    res = []
    board = np.zeros((8, 8), dtype=int)
    q.put((board, 0)) # (board, row)
    while not q.empty():
        b, r = q.get()
        if r == 8:
            res.append(b)
            continue
        for c in range(8):
            if is_safe(b, r, c):
                new_board = np.copy(b)
                new_board[r][c] = 1
                q.put((new_board, r + 1))
    return res

count = -1
def solve_click():  #Thiết lập lệnh cho nút Solve
    global solution, count
    solution = Solve()
    count = -1
    continue_click()

solve_button = tk.Button(root, text="Giải bài toán", #Thiết kế nút Solve
                         font=("Segoe UI", 15, "bold"),
                         bg="#2F4F4F", fg="#F0F8FF",
                         relief="flat", padx=20, pady=10)
solve_button.pack(pady=10)
solve_button.config(command=solve_click)

def continue_click():   #Thiết lập lệnh cho nút Continue
    global count
    count += 1 if count < len(solution) - 1 else 0
    cell_size = 560 // 8
    for i in range(8):
        for j in range(8):
            x = j * cell_size
            y = i * cell_size
            color = "#F8F8F8" if (i + j) % 2 == 0 else "#2F2F2F"
            if solution and solution[count][i][j] == 1:
                btn = tk.Label(frame2, image=queen_white, bg=color)
                btn.image = queen_white
                btn.place(x=x, y=y, width=cell_size, height=cell_size)
            else:
                btn = tk.Label(frame2, bg=color, relief="flat")
                btn.place(x=x, y=y, width=cell_size, height=cell_size)

continue_button = tk.Button(root, text="Phương án kế tiếp", #Thiết kế nút Continue
                            font=("Segoe UI", 15, "bold"),
                            bg="#2F4F4F", fg="#F0F8FF",
                            relief="flat", padx=20, pady=10)
continue_button.pack(pady=10) #Thiết lập lệnh cho nút Continue
continue_button.config(command=continue_click)

root.mainloop()
