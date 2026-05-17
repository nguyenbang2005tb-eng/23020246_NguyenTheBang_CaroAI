from board import BOARD_SIZE, AI, HUMAN, EMPTY, WIN_COUNT


def create_pattern_dict():
    """
    Hàm tạo bảng điểm pattern cho Caro 4 quân thắng.

    Quy ước:
    - Điểm dương: có lợi cho AI
    - Điểm âm: có lợi cho HUMAN
    """

    pattern_scores = {}

    for player in [AI, HUMAN]:

        if player == AI:
            sign = 1
            opponent = HUMAN
        else:
            sign = -1
            opponent = AI

        # ==========================================
        # THẮNG NGAY: 4 quân liên tiếp
        # Ví dụ: O O O O
        # ==========================================
        pattern_scores[(player, player, player, player)] = 1_000_000 * sign

        # ==========================================
        # 3 SỐNG HAI ĐẦU
        # Ví dụ: . O O O .
        # Với luật thắng 4, đây là thế cực mạnh
        # ==========================================
        pattern_scores[(EMPTY, player, player, player, EMPTY)] = 100_000 * sign

        # ==========================================
        # 3 BỊ CHẶN MỘT ĐẦU
        # Ví dụ: X O O O .
        # Ví dụ: . O O O X
        # ==========================================
        pattern_scores[(opponent, player, player, player, EMPTY)] = 50_000 * sign
        pattern_scores[(EMPTY, player, player, player, opponent)] = 50_000 * sign

        # ==========================================
        # 3 CÓ KHOẢNG TRỐNG Ở GIỮA
        # Ví dụ: O O . O
        # Ví dụ: O . O O
        # ==========================================
        pattern_scores[(player, player, EMPTY, player)] = 80_000 * sign
        pattern_scores[(player, EMPTY, player, player)] = 80_000 * sign

        # Ví dụ: O . O . O
        pattern_scores[(player, EMPTY, player, EMPTY, player)] = 40_000 * sign

        # ==========================================
        # 2 SỐNG
        # Ví dụ: . O O .
        # Ví dụ: . O . O .
        # ==========================================
        pattern_scores[(EMPTY, player, player, EMPTY)] = 2_000 * sign
        pattern_scores[(EMPTY, player, EMPTY, player, EMPTY)] = 1_500 * sign

        # ==========================================
        # 2 BỊ CHẶN MỘT ĐẦU
        # Ví dụ: X O O .
        # Ví dụ: . O O X
        # ==========================================
        pattern_scores[(opponent, player, player, EMPTY)] = 500 * sign
        pattern_scores[(EMPTY, player, player, opponent)] = 500 * sign

        # ==========================================
        # 2 CÓ KHOẢNG TRỐNG
        # Ví dụ: O . O
        # ==========================================
        pattern_scores[(player, EMPTY, player)] = 700 * sign

        # ==========================================
        # 1 QUÂN CÓ KHÔNG GIAN
        # Ví dụ: . O .
        # ==========================================
        pattern_scores[(EMPTY, player, EMPTY)] = 50 * sign

    return pattern_scores


PATTERN_DICT = create_pattern_dict()


def get_all_lines(board):
    """
    Lấy tất cả hàng ngang, dọc, chéo chính, chéo phụ.
    """

    lines = []

    # ==========================================
    # HÀNG NGANG
    # ==========================================
    for row in range(BOARD_SIZE):
        line = []

        for col in range(BOARD_SIZE):
            line.append(board[row][col])

        lines.append(line)

    # ==========================================
    # HÀNG DỌC
    # ==========================================
    for col in range(BOARD_SIZE):
        line = []

        for row in range(BOARD_SIZE):
            line.append(board[row][col])

        lines.append(line)

    # ==========================================
    # CHÉO CHÍNH "\"
    # ==========================================

    # Bắt đầu từ hàng 0
    for start_col in range(BOARD_SIZE):
        line = []

        row = 0
        col = start_col

        while row < BOARD_SIZE and col < BOARD_SIZE:
            line.append(board[row][col])
            row += 1
            col += 1

        if len(line) >= WIN_COUNT:
            lines.append(line)

    # Bắt đầu từ cột 0
    for start_row in range(1, BOARD_SIZE):
        line = []

        row = start_row
        col = 0

        while row < BOARD_SIZE and col < BOARD_SIZE:
            line.append(board[row][col])
            row += 1
            col += 1

        if len(line) >= WIN_COUNT:
            lines.append(line)

    # ==========================================
    # CHÉO PHỤ "/"
    # ==========================================

    # Bắt đầu từ hàng 0
    for start_col in range(BOARD_SIZE):
        line = []

        row = 0
        col = start_col

        while row < BOARD_SIZE and col >= 0:
            line.append(board[row][col])
            row += 1
            col -= 1

        if len(line) >= WIN_COUNT:
            lines.append(line)

    # Bắt đầu từ cột cuối
    for start_row in range(1, BOARD_SIZE):
        line = []

        row = start_row
        col = BOARD_SIZE - 1

        while row < BOARD_SIZE and col >= 0:
            line.append(board[row][col])
            row += 1
            col -= 1

        if len(line) >= WIN_COUNT:
            lines.append(line)

    return lines


def count_pattern_in_line(line, pattern):
    """
    Đếm số lần một pattern xuất hiện trong một dòng.
    """

    count = 0
    pattern_length = len(pattern)

    for i in range(len(line) - pattern_length + 1):
        window = tuple(line[i:i + pattern_length])

        if window == pattern:
            count += 1

    return count


def evaluate(board):
    """
    Hàm đánh giá trạng thái bàn cờ.

    AI có lợi      => điểm dương
    HUMAN có lợi   => điểm âm
    Càng gần thắng => điểm càng lớn
    """

    total_score = 0

    lines = get_all_lines(board)

    for line in lines:
        for pattern, score in PATTERN_DICT.items():
            total_score += count_pattern_in_line(line, pattern) * score

    return total_score