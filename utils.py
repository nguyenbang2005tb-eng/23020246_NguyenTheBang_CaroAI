from board import (
    BOARD_SIZE,
    AI,
    HUMAN,
    EMPTY,
    get_valid_moves,
    check_win,
)


def print_board(board):
    """
    In bàn cờ ra console để debug.
    """

    print()

    print("   ", end="")

    for col in range(BOARD_SIZE):
        print(col, end=" ")

    print()

    for row in range(BOARD_SIZE):
        print(row, end="  ")

        for col in range(BOARD_SIZE):
            print(board[row][col], end=" ")

        print()

    print()


def find_winning_moves(board, player):
    """
    Trả về danh sách các ô mà nếu player đánh vào thì thắng ngay.

    Ví dụ với luật thắng 4:

        X X X .

    Nếu HUMAN đánh vào ô trống thì thắng,
    vậy ô đó được đưa vào danh sách winning_moves.
    """

    winning_moves = []

    for row, col in get_valid_moves(board):

        board[row][col] = player

        if check_win(board, player):
            winning_moves.append((row, col))

        board[row][col] = EMPTY

    return winning_moves


def score_tactical_move(board, move, player):
    """
    Chấm điểm phụ cho các nước thắng/chặn.
    Dùng để chọn nước tốt hơn nếu có nhiều nước thắng/chặn cùng lúc.
    """

    row, col = move

    center = BOARD_SIZE // 2

    # Ưu tiên nước gần trung tâm hơn một chút
    center_score = BOARD_SIZE - (
        abs(row - center) + abs(col - center)
    )

    # Có thể mở rộng thêm sau nếu muốn
    return center_score


def choose_best_tactical_move(board, moves, player):
    """
    Nếu có nhiều nước tactical, chọn nước tốt nhất.
    """

    if not moves:
        return None

    best_move = moves[0]
    best_score = score_tactical_move(board, best_move, player)

    for move in moves[1:]:
        score = score_tactical_move(board, move, player)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def find_tactical_move(board):
    """
    Tìm nước đi chiến thuật bắt buộc trước khi chạy Minimax/Alpha-Beta.

    Thứ tự ưu tiên:

    1. Nếu AI có thể thắng ngay:
       AI đánh nước thắng.

    2. Nếu HUMAN có thể thắng ngay:
       AI đánh vào ô đó để chặn.

    3. Nếu không có tình huống khẩn cấp:
       trả về None.
    """

    # ==========================================
    # 1. AI CÓ THỂ THẮNG NGAY
    # ==========================================
    ai_winning_moves = find_winning_moves(board, AI)

    if ai_winning_moves:
        best_move = choose_best_tactical_move(
            board,
            ai_winning_moves,
            AI
        )

        return best_move, "AI_WIN"

    # ==========================================
    # 2. HUMAN CÓ THỂ THẮNG NGAY
    # ==========================================
    human_winning_moves = find_winning_moves(board, HUMAN)

    if human_winning_moves:
        best_move = choose_best_tactical_move(
            board,
            human_winning_moves,
            HUMAN
        )

        return best_move, "BLOCK_HUMAN_WIN"

    # ==========================================
    # 3. KHÔNG CÓ NƯỚC BẮT BUỘC
    # ==========================================
    return None, None