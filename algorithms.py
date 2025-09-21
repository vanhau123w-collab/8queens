import numpy as np
import queue, random, math
import heapq
from board import is_safe

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

def Solve_UCS_steps():
    heap = []
    steps = []
    board = np.zeros((8, 8), dtype=int)
    counter = 0  

    def cost_function(row, col):
        return abs(3.5 - row) + abs(3.5 - col)

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
                new_cost = cost + cost_function(r, c)
                heapq.heappush(heap, (new_cost, counter, new_board, r + 1))
    return steps

def Solve_DLS_steps(limit=8):
    steps = []
    board = np.zeros((8, 8), dtype=int)

    def dls(row, depth_limit):
        steps.append(np.copy(board))
        if row == 8 or row == depth_limit:
            return
        for col in range(8):
            if is_safe(board, row, col):
                board[row][col] = 1
                dls(row + 1, depth_limit)
                board[row][col] = 0
    dls(0, limit)
    return steps

def Solve_IDS_steps():
    steps = []
    board = np.zeros((8, 8), dtype=int)

    def dls(row, depth_limit):
        steps.append(np.copy(board))
        if row == 8 or row == depth_limit:
            return
        for col in range(8):
            if is_safe(board, row, col):
                board[row][col] = 1
                dls(row + 1, depth_limit)
                board[row][col] = 0

    for depth in range(1, 9): 
        dls(0, depth)
    return steps

goal_state = Solve_BFS_steps()[-1] 
def Solve_Greedy_steps():
    steps = []
    board = np.zeros((8, 8), dtype=int)

    def heuristic(b, row, col):
        temp = np.copy(b)
        temp[row][col] = 1
        return np.sum((temp == 1) & (goal_state == 1))

    for row in range(8):
        steps.append(np.copy(board))
        best_col = None
        best_h = -1
        for col in range(8):
            if is_safe(board, row, col):
                h = heuristic(board, row, col)
                if h > best_h:
                    best_h = h
                    best_col = col
        if best_col is not None:
            board[row][best_col] = 1
            steps.append(np.copy(board))
        else:
            break
    return steps

def Solve_Astar_steps():
    heap = []
    steps = []
    board = np.zeros((8, 8), dtype=int)
    counter = 0  

    def g_cost(row):
        return row

    def h_cost(b, row, col):
        temp = np.copy(b)
        temp[row][col] = 1
        return np.sum((temp == 1) & (goal_state == 1))

    heapq.heappush(heap, (0, counter, board, 0, 0))  

    while heap:
        f, _, b, r, g = heapq.heappop(heap)
        steps.append(np.copy(b))
        if r == 8:
            continue
        for c in range(8):
            if is_safe(b, r, c):
                new_board = np.copy(b)
                new_board[r][c] = 1
                counter += 1
                g_new = g_cost(r+1)
                h_new = h_cost(b, r, c)
                f_new = g_new + h_new
                heapq.heappush(heap, (f_new, counter, new_board, r+1, g_new))
    return steps

def count_conflicts(board):
    n = 8
    conflicts = 0
    cols = np.where(board == 1)[1]
    for i in range(n):
        for j in range(i+1, n):
            if cols[i] == cols[j] or abs(cols[i]-cols[j]) == abs(i-j):
                conflicts += 1
    return conflicts

def Solve_HillClimbing_steps(max_restarts=100):
    steps = []
    n = 8

    for _ in range(max_restarts):
        # Khởi tạo ngẫu nhiên
        board = np.zeros((n, n), dtype=int)
        for r in range(n):
            c = random.randint(0, n-1)
            board[r][c] = 1
        steps.append(np.copy(board))

        while True:
            current_conflicts = count_conflicts(board)
            if current_conflicts == 0:
                # tìm thấy nghiệm hợp lệ
                return steps  

            best_board = None
            best_conflicts = current_conflicts

            # thử di chuyển từng hậu
            for r in range(n):
                c = np.where(board[r] == 1)[0][0]
                board[r][c] = 0
                for new_c in range(n):
                    board[r][new_c] = 1
                    conf = count_conflicts(board)
                    if conf < best_conflicts:
                        best_conflicts = conf
                        best_board = np.copy(board)
                    board[r][new_c] = 0
                board[r][c] = 1

            if best_board is not None:
                # cập nhật nếu có trạng thái tốt hơn
                board = best_board
                steps.append(np.copy(board))
            else:
                # nếu không cải thiện → restart
                break  

    # fallback nếu không tìm thấy (rất hiếm)
    return steps

def Solve_SimulatedAnnealing_steps(max_steps=10000, temp=1000, cooling=0.99):
    steps = []
    n = 8
    board = np.zeros((n, n), dtype=int)
    for r in range(n):
        c = random.randint(0, n-1)
        board[r][c] = 1
    steps.append(np.copy(board))

    current_conflicts = count_conflicts(board)

    for _ in range(max_steps):
        if current_conflicts == 0:
            break
        r = random.randint(0, n-1)
        c = np.where(board[r] == 1)[0][0]
        new_c = random.randint(0, n-1)
        while new_c == c:
            new_c = random.randint(0, n-1)

        board[r][c] = 0
        board[r][new_c] = 1
        new_conflicts = count_conflicts(board)

        delta = new_conflicts - current_conflicts
        if delta < 0 or random.random() < math.exp(-delta/temp):
            current_conflicts = new_conflicts
            steps.append(np.copy(board))
        else:
            board[r][new_c] = 0
            board[r][c] = 1

        temp *= cooling

    return steps