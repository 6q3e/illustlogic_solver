from pyscript import document
import math

def get_config():
    size_input = document.getElementById('grid-size')
    N = int(size_input.value)
    M = round(N / 2)
    return N, M

def parse_hints(N, M):
    row_hints = []
    col_hints = []

    container = document.getElementById('nono-container')
    children = container.children
    total_width = M + N

    for r in range(N):
        hints = []
        grid_row = M + r
        for c in range(M):
            index = grid_row * total_width + c
            div = children[index]
            inp = div.querySelector('input')
            if inp and inp.value.strip():
                try:
                    hints.append(int(inp.value))
                except:
                    pass
        row_hints.append(hints)
    
    for c in range(N):
        hints = []
        grid_col = M + c
        for r in range(M):
            index = r * total_width + grid_col
            div = children[index]
            inp = div.querySelector('input')
            if inp and inp.value.strip():
                try:
                    hints.append(int(inp.value))
                except:
                    pass
        col_hints.append(hints)

    return row_hints, col_hints

def generate_line_possibilities(length, hints):
    if not hints:
        return [[0] * length]
    
    possibilities = []
    remain_hints = hints[1:]
    min_space_needed = sum(remain_hints) + len(remain_hints)
    current_block = hints[0]

    for i in range(length - min_space_needed - current_block + 1):
        pattern = [0] * i
        pattern += [1] * current_block

        if remain_hints:
            pattern.append(0)
            remain_len = length - len(pattern)
            sub_patterns = generate_line_possibilities(remain_len, remain_hints)
            for sub in sub_patterns:
                possibilities.append(pattern + sub)
        else:
            pattern += [0] * (length - len(pattern))
            possibilities.append(pattern)
        
    return possibilities

def solve_nonogram(event):
    message_el = document.getElementById("message")
    message_el.innerText = "計算中"

    try:
        N, M = get_config()
        row_hints, col_hints = parse_hints(N, M)
        board = [[None for _ in range(N)] for _ in range(N)]
        changed = True
        loop_count = 0

        while changed:
            changed = False
            loop_count += 1
            if loop_count > 100:
                break

            for r in range(N):
                hints = row_hints[r]
                possibilities = generate_line_possibilities(N, hints)
                valid_possibilities = []
                for p in possibilities:
                    is_valid = True
                    for c in range(N):
                        if board[r][c] is not None:
                            if board[r][c] == 1 and p[c] == 0:
                                is_valid = False
                            if board[r][c] == 0 and p[c] == 1:
                                is_valid = False
                    if is_valid:
                        valid_possibilities.append(p)
            
                if not valid_possibilities:
                    message_el.innerText = "解なし"
                    return
                
                for c in range(N):
                    if board[r][c] is None:
                        val = valid_possibilities[0][c]
                        if all(vp[c] == val for vp in valid_possibilities):
                            board[r][c] = val
                            changed = True

            for c in range(N):
                hints = col_hints[c]
                possibilities = generate_line_possibilities(N, hints)
                valid_possibilities = []
                for p in possibilities:
                    is_valid = True
                    for r in range(N):
                        if board[r][c] is not None:
                            if board[r][c] == 1 and p[r] == 0:
                                is_valid = False
                            if board[r][c] == 0 and p[r] == 1:
                                is_valid = False
                    if is_valid:
                        valid_possibilities.append(p)
                
                if not valid_possibilities:
                    message_el.innerText = "解なし"
                    return
                
                for r in range(N):
                    if board[r][c] is None:
                        val = valid_possibilities[0][r]
                        if all(vp[r] == val for vp in valid_possibilities):
                            board[r][c] = val
                            changed = True

        filled_count = 0
        for r in range(N):
            for c in range(N):
                cell = document.getElementById(f"main-{r}-{c}")
                if board[r][c] == 1:
                    cell.classList.add("filled")
                    filled_count += 1
                elif board[r][c] == 0:
                    cell.classList.add("empty-mark")
                    cell.classList.remove("filled")
        
        is_complete = all(board[r][c] is not None for r in range(N) for c in range(N))
        if is_complete:
            message_el.innerText = "解けました"
        else:
            message_el.innerText = "これ以上は解けません"
    
    except Exception as e:
        message_el.innerText = f"エラー： {e}"
        print(e)