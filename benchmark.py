import copy

from board import create_board, AI, HUMAN
import minimax
import alphabeta


def create_test_states():
    states = []

    # Test 1: đầu ván
    board1 = create_board()
    states.append(("Đầu ván", board1))

    # Test 2: giữa ván
    board2 = create_board()
    board2[4][4] = HUMAN
    board2[4][5] = AI
    board2[5][4] = HUMAN
    board2[3][4] = AI
    states.append(("Giữa ván", board2))

    # Test 3: AI có thể thắng ngay
    board3 = create_board()
    board3[4][3] = AI
    board3[4][4] = AI
    board3[4][5] = AI
    states.append(("AI có thể thắng ngay", board3))

    # Test 4: người sắp thắng, AI cần chặn
    board4 = create_board()
    board4[3][2] = HUMAN
    board4[3][3] = HUMAN
    board4[3][4] = HUMAN
    states.append(("Người sắp thắng", board4))

    # Test 5: hai bên cùng tấn công
    board5 = create_board()
    board5[4][4] = HUMAN
    board5[4][5] = HUMAN
    board5[5][4] = AI
    board5[5][5] = AI
    board5[3][3] = HUMAN
    board5[6][6] = AI
    states.append(("Hai bên cùng tấn công", board5))

    return states


def run_benchmark(depths=(1, 2, 3)):
    states = create_test_states()

    print("\n===== BENCHMARK MINIMAX VS ALPHA-BETA =====\n")

    results = []

    for state_name, board in states:
        for depth in depths:
            board_for_minimax = copy.deepcopy(board)
            board_for_alpha = copy.deepcopy(board)

            mini_result = minimax.find_best_move(board_for_minimax, depth)
            alpha_result = alphabeta.find_best_move(board_for_alpha, depth)

            reduction = 0

            if mini_result["nodes"] > 0:
                reduction = (
                    (mini_result["nodes"] - alpha_result["nodes"])
                    / mini_result["nodes"]
                    * 100
                )

            row = {
                "state": state_name,
                "depth": depth,
                "minimax_move": mini_result["move"],
                "alphabeta_move": alpha_result["move"],
                "minimax_score": mini_result["score"],
                "alphabeta_score": alpha_result["score"],
                "minimax_nodes": mini_result["nodes"],
                "alphabeta_nodes": alpha_result["nodes"],
                "minimax_time": mini_result["time"],
                "alphabeta_time": alpha_result["time"],
                "reduction": reduction,
            }

            results.append(row)

            print(f"State: {state_name}")
            print(f"Depth: {depth}")
            print(f"Minimax Move: {mini_result['move']}")
            print(f"AlphaBeta Move: {alpha_result['move']}")
            print(f"Minimax Nodes: {mini_result['nodes']}")
            print(f"AlphaBeta Nodes: {alpha_result['nodes']}")
            print(f"Reduction: {reduction:.2f}%")
            print(f"Minimax Time: {mini_result['time']:.4f}s")
            print(f"AlphaBeta Time: {alpha_result['time']:.4f}s")
            print("-" * 60)

    return results


if __name__ == "__main__":
    run_benchmark()