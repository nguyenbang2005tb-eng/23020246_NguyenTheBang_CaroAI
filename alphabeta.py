import math
import time

from board import (
    get_valid_moves,
    check_win,
    is_draw,
    AI,
    HUMAN,
    EMPTY,
)

from evaluation import evaluate
from utils import find_tactical_move


nodes_expanded = 0


def order_moves_with_tactical_priority(board, moves):
    """
    Nếu có nước thắng ngay hoặc nước chặn ngay,
    đưa nước đó lên đầu danh sách.

    Lưu ý:
    - Không return luôn.
    - Vẫn để Alpha-Beta chạy.
    """

    tactical_move, tactical_type = find_tactical_move(board)

    if tactical_move is None:
        return moves, None

    ordered_moves = []

    if tactical_move in moves:
        ordered_moves.append(tactical_move)

    for move in moves:
        if move != tactical_move:
            ordered_moves.append(move)

    return ordered_moves, tactical_type


def alphabeta(board, depth, alpha, beta, is_maximizing):
    """
    Thuật toán Minimax có Alpha-Beta pruning.

    alpha: giá trị tốt nhất hiện tại của MAX.
    beta: giá trị tốt nhất hiện tại của MIN.
    """

    global nodes_expanded
    nodes_expanded += 1

    # ==========================================
    # TRẠNG THÁI KẾT THÚC
    # ==========================================
    if check_win(board, AI):
        return 1_000_000 + depth

    if check_win(board, HUMAN):
        return -1_000_000 - depth

    if is_draw(board):
        return 0

    # ĐẠT GIỚI HẠN ĐỘ SÂU
    if depth == 0:
        return evaluate(board)

    moves = get_valid_moves(board)

    # MAX PLAYER - LƯỢT AI
    if is_maximizing:
        best_score = -math.inf

        for row, col in moves:
            board[row][col] = AI

            score = alphabeta(
                board,
                depth - 1,
                alpha,
                beta,
                False
            )

            board[row][col] = EMPTY

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            # CẮT TỈA
            if beta <= alpha:
                break

        return best_score

    # MIN PLAYER - LƯỢT HUMAN
    else:
        best_score = math.inf

        for row, col in moves:
            board[row][col] = HUMAN

            score = alphabeta(
                board,
                depth - 1,
                alpha,
                beta,
                True
            )

            board[row][col] = EMPTY

            best_score = min(best_score, score)
            beta = min(beta, best_score)

            # CẮT TỈA
            if beta <= alpha:
                break

        return best_score


def find_best_move(board, depth):
    """
    Tìm nước đi tốt nhất cho AI bằng Alpha-Beta.

    Khác bản trước:
    - Không return sớm khi có nước thắng/chặn.
    - Vẫn chạy Alpha-Beta.
    - Nếu có tactical move thì chỉ ưu tiên xét trước.
    """

    global nodes_expanded
    nodes_expanded = 0

    start_time = time.time()

    best_score = -math.inf
    best_move = None

    alpha = -math.inf
    beta = math.inf

    moves = get_valid_moves(board)

    # Chỉ ưu tiên tactical move lên đầu, không chọn ngay
    moves, tactical_type = order_moves_with_tactical_priority(board, moves)

    for row, col in moves:
        board[row][col] = AI

        score = alphabeta(
            board,
            depth - 1,
            alpha,
            beta,
            False
        )

        board[row][col] = EMPTY

        if score > best_score:
            best_score = score
            best_move = (row, col)

        alpha = max(alpha, best_score)

    elapsed_time = time.time() - start_time

    return {
        "move": best_move,
        "score": best_score,
        "nodes": nodes_expanded,
        "time": elapsed_time,
        "depth": depth,
        "algorithm": "Alpha-Beta",
        "tactical": tactical_type,
    }