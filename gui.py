import copy
import threading
import tkinter as tk
from tkinter import messagebox

from board import (
    BOARD_SIZE,
    AI,
    HUMAN,
    EMPTY,
    create_board,
    make_move,
    check_win,
    is_draw,
)

import minimax
import alphabeta


class CaroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Caro AI - Minimax vs Alpha-Beta")

        # Chế độ thuật toán:
        # minimax, alphabeta, compare
        self.algorithm = tk.StringVar(value="alphabeta")
        self.depth = tk.IntVar(value=2)

        # Dữ liệu cho chế độ 1 thuật toán
        self.board = create_board()
        self.buttons = []
        self.ai_history = []

        # Dữ liệu cho chế độ so sánh
        self.alpha_board = create_board()
        self.minimax_board = create_board()

        self.alpha_buttons = []
        self.minimax_buttons = []

        self.alpha_history = []
        self.minimax_history = []

        self.game_over = False

        # Dùng để tránh lỗi khi Reset/Menu trong lúc AI đang tính
        self.compare_run_id = 0
        self.pending_compare_results = {}

        self.create_menu()

    # =========================================================
    # XÓA TOÀN BỘ GIAO DIỆN HIỆN TẠI
    # =========================================================
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # =========================================================
    # MENU CHỌN CHẾ ĐỘ
    # =========================================================
    def create_menu(self):
        self.compare_run_id += 1
        self.clear_window()
        self.game_over = False

        menu_frame = tk.Frame(self.root)
        menu_frame.pack(expand=True)

        title = tk.Label(
            menu_frame,
            text="CARO AI",
            font=("Arial", 26, "bold"),
            fg="blue"
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            menu_frame,
            text="Minimax - Alpha-Beta - So sánh thuật toán",
            font=("Arial", 13)
        )
        subtitle.pack(pady=5)

        tk.Label(
            menu_frame,
            text="Chọn chế độ:",
            font=("Arial", 15, "bold")
        ).pack(pady=10)

        tk.Radiobutton(
            menu_frame,
            text="Minimax",
            variable=self.algorithm,
            value="minimax",
            font=("Arial", 13)
        ).pack(anchor="w", padx=80)

        tk.Radiobutton(
            menu_frame,
            text="Alpha-Beta",
            variable=self.algorithm,
            value="alphabeta",
            font=("Arial", 13)
        ).pack(anchor="w", padx=80)

        tk.Radiobutton(
            menu_frame,
            text="So sánh Alpha-Beta và Minimax",
            variable=self.algorithm,
            value="compare",
            font=("Arial", 13),
            fg="blue"
        ).pack(anchor="w", padx=80)

        tk.Label(
            menu_frame,
            text="Chọn độ sâu tìm kiếm:",
            font=("Arial", 15, "bold")
        ).pack(pady=15)

        depth_menu = tk.OptionMenu(
            menu_frame,
            self.depth,
            1,
            2,
            3,
            4
        )
        depth_menu.config(font=("Arial", 12), width=10)
        depth_menu.pack()

        tk.Button(
            menu_frame,
            text="PLAY",
            font=("Arial", 15, "bold"),
            width=15,
            command=self.start_game
        ).pack(pady=25)

    def start_game(self):
        if self.algorithm.get() == "compare":
            self.start_compare_game()
        else:
            self.start_single_game()

    # =========================================================
    # CHẾ ĐỘ 1 THUẬT TOÁN
    # =========================================================
    def start_single_game(self):
        self.compare_run_id += 1

        self.board = create_board()
        self.buttons = []
        self.ai_history = []
        self.game_over = False

        self.clear_window()

        title_text = "ALPHA-BETA" if self.algorithm.get() == "alphabeta" else "MINIMAX"

        title = tk.Label(
            self.root,
            text=title_text,
            font=("Arial", 22, "bold"),
            fg="blue" if self.algorithm.get() == "alphabeta" else "green"
        )
        title.pack(pady=8)

        self.status = tk.Label(
            self.root,
            text=f"Bạn là X, AI là O | Depth: {self.depth.get()}",
            font=("Arial", 12)
        )
        self.status.pack(pady=5)

        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10, anchor="center")

        # Bàn cờ
        board_frame = tk.Frame(main_frame)
        board_frame.pack(side=tk.LEFT, padx=12, anchor="n")

        # Lịch sử
        history_frame = tk.Frame(
            main_frame,
            bd=2,
            relief="groove"
        )
        history_frame.pack(side=tk.LEFT, padx=12, anchor="n")

        history_title = tk.Label(
            history_frame,
            text="LỊCH SỬ",
            font=("Arial", 13, "bold"),
            fg="blue"
        )
        history_title.pack(pady=5)

        history_header = tk.Label(
            history_frame,
            text="Lượt | Move | Score | Time | Nodes",
            font=("Arial", 9, "bold")
        )
        history_header.pack()

        self.history_text = tk.Text(
            history_frame,
            width=42,
            height=27,
            font=("Consolas", 9),
            state="disabled"
        )
        self.history_text.pack(padx=6, pady=6)

        # Tạo bàn cờ
        for row in range(BOARD_SIZE):
            button_row = []

            for col in range(BOARD_SIZE):
                btn = tk.Button(
                    board_frame,
                    text="",
                    width=5,
                    height=2,
                    font=("Arial", 16, "bold"),
                    command=lambda r=row, c=col: self.human_move(r, c)
                )
                btn.grid(row=row, column=col)
                button_row.append(btn)

            self.buttons.append(button_row)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=8)

        tk.Button(
            bottom_frame,
            text="Reset",
            font=("Arial", 11),
            command=self.start_single_game
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            bottom_frame,
            text="Back to Menu",
            font=("Arial", 11),
            command=self.create_menu
        ).pack(side=tk.LEFT, padx=10)

    def human_move(self, row, col):
        if self.game_over:
            return

        if self.board[row][col] != EMPTY:
            return

        make_move(self.board, row, col, HUMAN)

        self.buttons[row][col].config(
            text=HUMAN,
            state="disabled",
            fg="red"
        )

        if check_win(self.board, HUMAN):
            self.game_over = True
            messagebox.showinfo("Game Over", "Bạn thắng!")
            self.disable_single_board()
            return

        if is_draw(self.board):
            self.game_over = True
            messagebox.showinfo("Game Over", "Hòa!")
            self.disable_single_board()
            return

        self.ai_move()

    def ai_move(self):
        depth = self.depth.get()

        if self.algorithm.get() == "minimax":
            result = minimax.find_best_move(self.board, depth)
        else:
            result = alphabeta.find_best_move(self.board, depth)

        self.update_single_history(result)

        move = result["move"]

        if move is None:
            return

        row, col = move
        make_move(self.board, row, col, AI)

        self.buttons[row][col].config(
            text=AI,
            state="disabled",
            fg="blue"
        )

        tactical_text = self.get_tactical_text(result)

        self.status.config(
            text=(
                f"{result['algorithm']} | "
                f"Move: {move} | "
                f"Score: {result['score']} | "
                f"Depth: {result['depth']} | "
                f"Nodes: {result['nodes']} | "
                f"Time: {result['time']:.4f}s"
                f"{tactical_text}"
            )
        )

        if check_win(self.board, AI):
            self.game_over = True
            messagebox.showinfo("Game Over", "AI thắng!")
            self.disable_single_board()
            return

        if is_draw(self.board):
            self.game_over = True
            messagebox.showinfo("Game Over", "Hòa!")
            self.disable_single_board()
            return

    def update_single_history(self, result):
        turn_number = len(self.ai_history) + 1

        history_item = {
            "turn": turn_number,
            "move": result["move"],
            "score": result["score"],
            "time": result["time"],
            "nodes": result["nodes"],
            "depth": result["depth"],
            "tactical": result.get("tactical"),
        }

        self.ai_history.append(history_item)

        line = (
            f"#{turn_number:02d} | "
            f"M:{result['move']} | "
            f"S:{result['score']} | "
            f"T:{result['time']:.3f}s | "
            f"N:{result['nodes']}\n"
        )

        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, line)
        self.history_text.config(state="disabled")
        self.history_text.see(tk.END)

    def disable_single_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.buttons[row][col].config(state="disabled")

    # =========================================================
    # CHẾ ĐỘ SO SÁNH ALPHA-BETA VS MINIMAX
    # =========================================================
    def start_compare_game(self):
        self.compare_run_id += 1

        self.alpha_board = create_board()
        self.minimax_board = create_board()

        self.alpha_buttons = []
        self.minimax_buttons = []

        self.alpha_history = []
        self.minimax_history = []

        self.pending_compare_results = {}

        self.game_over = False

        self.clear_window()

        title = tk.Label(
            self.root,
            text=f"SO SÁNH ALPHA-BETA VÀ MINIMAX | Depth: {self.depth.get()}",
            font=("Arial", 16, "bold"),
            fg="blue"
        )
        title.pack(pady=5)

        self.compare_status = tk.Label(
            self.root,
            text="Bạn là X, AI là O. Nước đi của bạn sẽ được áp dụng cho cả hai bàn cờ.",
            font=("Arial", 11)
        )
        self.compare_status.pack(pady=5)

        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        # Bên trái: Alpha-Beta
        alpha_panel = self.create_compare_panel(
            parent=main_frame,
            title="ALPHA-BETA",
            title_color="blue",
            side=tk.LEFT
        )

        self.alpha_board_frame = alpha_panel["board_frame"]
        self.alpha_info_label = alpha_panel["info_label"]
        self.alpha_history_text = alpha_panel["history_text"]

        # Bên phải: Minimax
        minimax_panel = self.create_compare_panel(
            parent=main_frame,
            title="MINIMAX",
            title_color="green",
            side=tk.LEFT
        )

        self.minimax_board_frame = minimax_panel["board_frame"]
        self.minimax_info_label = minimax_panel["info_label"]
        self.minimax_history_text = minimax_panel["history_text"]

        self.create_compare_board_buttons()

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=8)

        tk.Button(
            bottom_frame,
            text="Reset",
            font=("Arial", 11),
            command=self.start_compare_game
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            bottom_frame,
            text="Back to Menu",
            font=("Arial", 11),
            command=self.create_menu
        ).pack(side=tk.LEFT, padx=10)

    def create_compare_panel(self, parent, title, title_color, side):
        panel = tk.Frame(
            parent,
            bd=2,
            relief="groove"
        )
        panel.pack(side=side, padx=6, pady=5, fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            panel,
            text=title,
            font=("Arial", 15, "bold"),
            fg=title_color
        )
        title_label.pack(pady=4)

        info_label = tk.Label(
            panel,
            text="Move: - | Score: - | Nodes: - | Time: -",
            font=("Arial", 9),
            wraplength=600,
            justify="center"
        )
        info_label.pack(pady=4)

        content_frame = tk.Frame(panel)
        content_frame.pack(pady=4, anchor="center")

        board_frame = tk.Frame(content_frame)
        board_frame.pack(side=tk.LEFT, padx=8, anchor="n")

        history_frame = tk.Frame(content_frame)
        history_frame.pack(side=tk.LEFT, padx=8, anchor="n")

        tk.Label(
            history_frame,
            text="Lịch sử",
            font=("Arial", 10, "bold")
        ).pack()

        tk.Label(
            history_frame,
            text="Lượt | Move | Score | Time | Nodes",
            font=("Arial", 8, "bold")
        ).pack()

        history_text = tk.Text(
            history_frame,
            width=36,
            height=25,
            font=("Consolas", 8),
            state="disabled"
        )
        history_text.pack(padx=3, pady=3)

        return {
            "panel": panel,
            "board_frame": board_frame,
            "info_label": info_label,
            "history_text": history_text,
        }

    def create_compare_board_buttons(self):
        for row in range(BOARD_SIZE):
            alpha_row = []
            minimax_row = []

            for col in range(BOARD_SIZE):
                alpha_btn = tk.Button(
                    self.alpha_board_frame,
                    text="",
                    width=4,
                    height=2,
                    font=("Arial", 13, "bold"),
                    command=lambda r=row, c=col: self.compare_human_move(r, c)
                )
                alpha_btn.grid(row=row, column=col)
                alpha_row.append(alpha_btn)

                minimax_btn = tk.Button(
                    self.minimax_board_frame,
                    text="",
                    width=4,
                    height=2,
                    font=("Arial", 13, "bold"),
                    command=lambda r=row, c=col: self.compare_human_move(r, c)
                )
                minimax_btn.grid(row=row, column=col)
                minimax_row.append(minimax_btn)

            self.alpha_buttons.append(alpha_row)
            self.minimax_buttons.append(minimax_row)

    def compare_human_move(self, row, col):
        if self.game_over:
            return

        # Vì 2 bàn có thể khác nhau, người chơi chỉ được đánh ô trống ở cả 2 bàn
        if self.alpha_board[row][col] != EMPTY or self.minimax_board[row][col] != EMPTY:
            messagebox.showwarning(
                "Nước đi không hợp lệ",
                "Ô này đã có quân ở ít nhất một trong hai bàn cờ."
            )
            return

        make_move(self.alpha_board, row, col, HUMAN)
        make_move(self.minimax_board, row, col, HUMAN)

        self.alpha_buttons[row][col].config(
            text=HUMAN,
            state="disabled",
            fg="red"
        )

        self.minimax_buttons[row][col].config(
            text=HUMAN,
            state="disabled",
            fg="red"
        )

        if check_win(self.alpha_board, HUMAN) or check_win(self.minimax_board, HUMAN):
            self.game_over = True
            messagebox.showinfo("Game Over", "Bạn thắng!")
            self.disable_compare_boards()
            return

        if is_draw(self.alpha_board) or is_draw(self.minimax_board):
            self.game_over = True
            messagebox.showinfo("Game Over", "Có bàn cờ đã hòa!")
            self.disable_compare_boards()
            return

        self.compare_ai_move()

    # =========================================================
    # CHẠY 2 THUẬT TOÁN SONG SONG
    # =========================================================
    def compare_ai_move(self):
        depth = self.depth.get()

        self.compare_run_id += 1
        run_id = self.compare_run_id

        self.pending_compare_results = {}

        self.compare_status.config(
            text="AI đang tính toán... Thuật toán nào xong trước sẽ hiện nước đi trước."
        )

        # Khóa bàn cờ khi AI đang suy nghĩ
        self.set_compare_buttons_state("disabled")

        # Tạo bản sao để thread tính toán, tránh sửa trực tiếp bàn cờ thật
        alpha_board_snapshot = copy.deepcopy(self.alpha_board)
        minimax_board_snapshot = copy.deepcopy(self.minimax_board)

        def run_alpha_beta():
            result = alphabeta.find_best_move(alpha_board_snapshot, depth)

            self.root.after(
                0,
                lambda: self.on_compare_result_ready("alpha", result, run_id)
            )

        def run_minimax():
            result = minimax.find_best_move(minimax_board_snapshot, depth)

            self.root.after(
                0,
                lambda: self.on_compare_result_ready("minimax", result, run_id)
            )

        threading.Thread(
            target=run_alpha_beta,
            daemon=True
        ).start()

        threading.Thread(
            target=run_minimax,
            daemon=True
        ).start()

    def on_compare_result_ready(self, algorithm_name, result, run_id):
        # Nếu kết quả thuộc lượt cũ sau khi Reset/Menu thì bỏ qua
        if run_id != self.compare_run_id:
            return

        if self.game_over:
            return

        self.pending_compare_results[algorithm_name] = result

        # Thuật toán nào xong trước thì vẽ nước đi trước
        if algorithm_name == "alpha":
            self.apply_compare_ai_result(
                board=self.alpha_board,
                buttons=self.alpha_buttons,
                result=result,
                info_label=self.alpha_info_label,
                history_text=self.alpha_history_text,
                history_list=self.alpha_history
            )

        elif algorithm_name == "minimax":
            self.apply_compare_ai_result(
                board=self.minimax_board,
                buttons=self.minimax_buttons,
                result=result,
                info_label=self.minimax_info_label,
                history_text=self.minimax_history_text,
                history_list=self.minimax_history
            )

        # Nếu mới chỉ có 1 thuật toán xong
        if len(self.pending_compare_results) == 1:
            if algorithm_name == "alpha":
                self.compare_status.config(
                    text=(
                        f"Alpha-Beta đã xong trước | "
                        f"Time: {result['time']:.4f}s | "
                        f"Nodes: {result['nodes']} | "
                        f"Đang chờ Minimax..."
                    )
                )
            else:
                self.compare_status.config(
                    text=(
                        f"Minimax đã xong trước | "
                        f"Time: {result['time']:.4f}s | "
                        f"Nodes: {result['nodes']} | "
                        f"Đang chờ Alpha-Beta..."
                    )
                )

            return

        # Nếu cả 2 thuật toán đều xong thì tổng kết
        if len(self.pending_compare_results) == 2:
            alpha_result = self.pending_compare_results["alpha"]
            minimax_result = self.pending_compare_results["minimax"]

            self.update_compare_summary(alpha_result, minimax_result)

            alpha_win = check_win(self.alpha_board, AI)
            minimax_win = check_win(self.minimax_board, AI)

            if alpha_win or minimax_win:
                self.game_over = True

                if alpha_win and minimax_win:
                    message = "Cả Alpha-Beta và Minimax đều thắng!"
                elif alpha_win:
                    message = "Alpha-Beta thắng!"
                else:
                    message = "Minimax thắng!"

                messagebox.showinfo("Game Over", message)
                self.disable_compare_boards()
                return

            if is_draw(self.alpha_board) or is_draw(self.minimax_board):
                self.game_over = True
                messagebox.showinfo("Game Over", "Có bàn cờ đã hòa!")
                self.disable_compare_boards()
                return

            # Mở lại các ô còn trống cho người chơi
            self.enable_valid_compare_moves()

    def apply_compare_ai_result(
        self,
        board,
        buttons,
        result,
        info_label,
        history_text,
        history_list
    ):
        move = result["move"]

        if move is not None:
            row, col = move

            if board[row][col] == EMPTY:
                make_move(board, row, col, AI)

                buttons[row][col].config(
                    text=AI,
                    state="disabled",
                    fg="blue"
                )

        tactical_text = self.get_tactical_text(result)

        info_label.config(
            text=(
                f"Move: {result['move']} | "
                f"Score: {result['score']} | "
                f"Depth: {result['depth']} | "
                f"Nodes: {result['nodes']} | "
                f"Time: {result['time']:.4f}s"
                f"{tactical_text}"
            )
        )

        turn_number = len(history_list) + 1

        history_item = {
            "turn": turn_number,
            "move": result["move"],
            "score": result["score"],
            "time": result["time"],
            "nodes": result["nodes"],
            "depth": result["depth"],
            "tactical": result.get("tactical"),
        }

        history_list.append(history_item)

        line = (
            f"#{turn_number:02d} | "
            f"M:{result['move']} | "
            f"S:{result['score']} | "
            f"T:{result['time']:.3f}s | "
            f"N:{result['nodes']}\n"
        )

        history_text.config(state="normal")
        history_text.insert(tk.END, line)
        history_text.config(state="disabled")
        history_text.see(tk.END)

    def update_compare_summary(self, alpha_result, minimax_result):
        if minimax_result["nodes"] > 0:
            reduction = (
                (minimax_result["nodes"] - alpha_result["nodes"])
                / minimax_result["nodes"]
                * 100
            )
        else:
            reduction = 0

        if alpha_result["move"] == minimax_result["move"]:
            same_move_text = "Hai thuật toán chọn CÙNG nước đi"
        else:
            same_move_text = "Hai thuật toán chọn KHÁC nước đi"

        self.compare_status.config(
            text=(
                f"{same_move_text} | "
                f"Alpha-Beta giảm {reduction:.2f}% số trạng thái xét so với Minimax | "
                f"Alpha-Beta nodes: {alpha_result['nodes']} | "
                f"Minimax nodes: {minimax_result['nodes']}"
            )
        )

    def set_compare_buttons_state(self, state):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.alpha_buttons[row][col].config(state=state)
                self.minimax_buttons[row][col].config(state=state)

    def enable_valid_compare_moves(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (
                    self.alpha_board[row][col] == EMPTY
                    and self.minimax_board[row][col] == EMPTY
                ):
                    self.alpha_buttons[row][col].config(state="normal")
                    self.minimax_buttons[row][col].config(state="normal")
                else:
                    self.alpha_buttons[row][col].config(state="disabled")
                    self.minimax_buttons[row][col].config(state="disabled")

    def disable_compare_boards(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                self.alpha_buttons[row][col].config(state="disabled")
                self.minimax_buttons[row][col].config(state="disabled")

    # =========================================================
    # HÀM PHỤ
    # =========================================================
    def get_tactical_text(self, result):
        tactical_text = ""

        if result.get("tactical") == "AI_WIN":
            tactical_text = " | Tactical: AI wins"
        elif result.get("tactical") == "BLOCK_HUMAN_WIN":
            tactical_text = " | Tactical: Block"

        return tactical_text