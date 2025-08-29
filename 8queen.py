import tkinter as tk
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
cell_size = 560 // 8
for i in range(8):
    for j in range(8):
        x = j * cell_size
        y = i * cell_size
        color = "#F8F8F8" if (i + j) % 2 == 0 else "#2F2F2F"
        if i == j:
            btn = tk.Label(frame2, image=queen_white, bg=color)
            btn.image = queen_white
            btn.place(x=x, y=y, width=cell_size, height=cell_size)
        else:
            btn = tk.Label(frame2, bg=color, relief="flat")
            btn.place(x=x, y=y, width=cell_size, height=cell_size)

root.mainloop()
