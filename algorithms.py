import numpy as np
import queue, random, math
import heapq

# =========================
# HÀM HỖ TRỢ
# =========================

def is_safe(board, row, col):
    n = board.shape[0]
    for i in range(row):
        if board[i][col] == 1:
            return False
        if col - (row - i) >= 0 and board[i][col - (row - i)] == 1:
            return False
        if col + (row - i) < n and board[i][col + (row - i)] == 1:
            return False
    return True

def count_conflicts(board):
    """Đếm số xung đột giữa các quân hậu"""
    n = board.shape[0]
    positions = [(r, c) for r in range(n) for c in range(n) if board[r][c] == 1]
    conflicts = 0
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            r1, c1 = positions[i]
            r2, c2 = positions[j]
            if c1 == c2 or abs(c1 - c2) == abs(r1 - r2):
                conflicts += 1
    return conflicts

# =========================
# THUẬT TOÁN TÌM KIẾM
# =========================

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
    steps = []
    n = 8
    board = np.zeros((n, n), dtype=int)
    
    def cost_function(row, col):
        return abs(3.5 - row) + abs(3.5 - col)
    
    heap = []
    counter = 0
    heapq.heappush(heap, (0, counter, board, 0))
    
    all_steps = [] 
    
    while heap:
        cost, _, b, r = heapq.heappop(heap)
        all_steps.append(np.copy(b)) 
        if r == n:
            continue
        for c in range(n):
            if is_safe(b, r, c):
                new_board = np.copy(b)
                new_board[r][c] = 1
                counter += 1
                new_cost = cost + cost_function(r, c)
                heapq.heappush(heap, (new_cost, counter, new_board, r + 1))
    steps.extend(all_steps)
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
        best_col = None
        best_h = -1
        for col in range(8):
            if is_safe(board, row, col):
                h = heuristic(board, row, col)
                temp_board = np.copy(board)
                temp_board[row][col] = 1
                steps.append(temp_board) 
                if h > best_h:
                    best_h = h
                    best_col = col
        if best_col is not None:
            board[row][best_col] = 1
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
                board = best_board
                steps.append(np.copy(board))
            else:
                break
    return steps

def Solve_SimulatedAnnealing_steps(max_steps=100000, temp=1000, cooling=0.999):
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
            return steps
        r = random.randint(0, n-1)
        c = np.where(board[r] == 1)[0][0]
        new_c = random.randint(0, n-1)
        while new_c == c:
            new_c = random.randint(0, n-1)

        board[r][c] = 0
        board[r][new_c] = 1
        new_conflicts = count_conflicts(board)

        delta = new_conflicts - current_conflicts
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_conflicts = new_conflicts
            steps.append(np.copy(board))
        else:
            board[r][new_c] = 0
            board[r][c] = 1

        temp *= cooling
    return steps

import numpy as np

def Solve_BeamSearch_steps(beam_width=50):
    n = 8
    steps = []

    # Khởi tạo beam: mỗi board khác nhau cho row 0
    beam = []
    for col in range(min(beam_width, n)):
        b = np.zeros((n, n), dtype=int)
        b[0][col] = 1
        beam.append(b)
        steps.append(np.copy(b))

    # Duyệt các row từ 1 đến 7
    for row in range(1, n):
        candidates = []
        for b in beam:
            for col in range(n):
                if is_safe(b, row, col):
                    new_b = np.copy(b)
                    new_b[row][col] = 1
                    candidates.append(new_b)
                    steps.append(np.copy(new_b))

        # Nếu không còn candidate nào an toàn → loại board
        if not candidates:
            # Thử lại từ đầu hoặc tăng beam_width
            raise ValueError("Không còn candidate an toàn. Hãy tăng beam_width hoặc restart.")

        # Giữ beam_width board tốt nhất (không conflict)
        # Vì tất cả candidate đều an toàn nên conflict = 0
        beam = candidates[:beam_width]

    # Board cuối cùng hợp lệ
    return steps

def Solve_Genetic_steps(pop_size=50, generations=500, mutation_rate=0.1):
    steps = []
    n = 8

    def fitness(b):
        return 28 - count_conflicts(b)  # max = 28 (8 queens không ăn nhau)

    def random_board():
        b = np.zeros((n, n), dtype=int)
        for r in range(n):
            c = random.randint(0, n-1)
            b[r][c] = 1
        return b

    population = [random_board() for _ in range(pop_size)]
    steps.extend([np.copy(b) for b in population])

    for _ in range(generations):
        population.sort(key=lambda b: fitness(b), reverse=True)
        if fitness(population[0]) == 28:
            steps.append(np.copy(population[0]))
            return steps
        new_pop = population[:10]  # elitism
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(population[:20], 2)
            c = random.randint(1, n-2)
            child1 = np.vstack((p1[:c], p2[c:]))
            child2 = np.vstack((p2[:c], p1[c:]))
            for child in [child1, child2]:
                if random.random() < mutation_rate:
                    r = random.randint(0, n-1)
                    child[r] = np.zeros(n)
                    child[r][random.randint(0, n-1)] = 1
                new_pop.append(child)
        population = new_pop[:pop_size]
        steps.extend([np.copy(b) for b in population])
    return steps

def and_or_search(initial_state, N=8):
    """Trả về danh sách các board tuần tự để hiển thị"""
    steps = []
    def or_search(state, path):
        if is_goal(state, N):
            steps.append(state.copy())  # lưu board khi là goal
            return True
        if any(np.array_equal(state, p) for p in path):
            return False

        row = np.sum(np.any(state == 1, axis=1))
        if row >= N:
            return False

        actions = [(row, col) for col in range(N) if is_safe(state, row, col)]
        random.shuffle(actions)
        for r, c in actions:
            new_board = np.copy(state)
            new_board[r][c] = 1
            steps.append(new_board.copy())  
            if or_search(new_board, path + [state]):
                return True
            steps.append(state.copy())
        return False

    or_search(initial_state, [])
    return steps

def is_goal(board, N=8):
    queens = np.sum(board == 1)
    return queens == N and count_conflicts(board) == 0

