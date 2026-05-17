BOARD_SIZE = 9
WIN_COUNT = 4

AI = "O"
HUMAN = "X"
EMPTY = "."


def create_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def is_valid_move(board, row, col):
    return (
        0 <= row < BOARD_SIZE
        and 0 <= col < BOARD_SIZE
        and board[row][col] == EMPTY
    )


def make_move(board, row, col, player):
    if is_valid_move(board, row, col):
        board[row][col] = player
        return True
    return False


def undo_move(board, row, col):
    board[row][col] = EMPTY


def is_draw(board):
    return all(EMPTY not in row for row in board)


def check_win(board, player):
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1),
    ]

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] != player:
                continue

            for dr, dc in directions:
                count = 0

                for k in range(WIN_COUNT):
                    nr = row + dr * k
                    nc = col + dc * k

                    if (
                        0 <= nr < BOARD_SIZE
                        and 0 <= nc < BOARD_SIZE
                        and board[nr][nc] == player
                    ):
                        count += 1
                    else:
                        break

                if count == WIN_COUNT:
                    return True

    return False


def has_neighbor(board, row, col, distance=2):
    for r in range(max(0, row - distance), min(BOARD_SIZE, row + distance + 1)):
        for c in range(max(0, col - distance), min(BOARD_SIZE, col + distance + 1)):
            if board[r][c] != EMPTY:
                return True
    return False


def get_valid_moves(board):
    moves = []

    if all(cell == EMPTY for row in board for cell in row):
        center = BOARD_SIZE // 2
        return [(center, center)]

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == EMPTY and has_neighbor(board, row, col):
                moves.append((row, col))

    center = BOARD_SIZE // 2
    moves.sort(key=lambda m: abs(m[0] - center) + abs(m[1] - center))

    return moves