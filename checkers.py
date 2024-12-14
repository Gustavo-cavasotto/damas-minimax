import random
import math

class CheckersAI:
    def __init__(self, depth):
        self.depth = depth  # Profundidade máxima do algoritmo Minimax

    def evaluate_board(self, board, player):
        """ Avalia o tabuleiro e retorna uma pontuação para o jogador. """
        # Exemplo simples: quantidade de peças de cada jogador (incluindo bônus para reis)
        player_pieces = sum(row.count(player) + 2 * row.count(player + 'K') for row in board)
        opponent = 'W' if player == 'B' else 'B'
        opponent_pieces = sum(row.count(opponent) + 2 * row.count(opponent + 'K') for row in board)
        return player_pieces - opponent_pieces

    def get_valid_moves(self, board, player):
        moves = []
        rows, cols = len(board), len(board[0])
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Direções válidas (diagonais)

        for row in range(rows):
            for col in range(cols):
                if board[row][col] in {player, player + 'K'}:  # Inclui reis
                    piece_is_king = board[row][col].endswith('K')
                    for dr, dc in directions:
                        # Reis podem se mover em ambas as direções; peças normais apenas para frente
                        if not piece_is_king and ((player == 'B' and dr < 0) or (player == 'W' and dr > 0)):
                            continue

                        new_row, new_col = row + dr, col + dc

                        # Verifica movimento simples
                        if 0 <= new_row < rows and 0 <= new_col < cols and board[new_row][new_col] == '.':
                            moves.append(((row, col), (new_row, new_col)))

                        # Verifica captura
                        capture_row, capture_col = row + 2 * dr, col + 2 * dc
                        if (
                            0 <= capture_row < rows
                            and 0 <= capture_col < cols
                            and board[new_row][new_col] not in {'.', player, player + 'K'}
                            and board[capture_row][capture_col] == '.'
                        ):
                            moves.append(((row, col), (capture_row, capture_col)))

        return moves

    def make_move(self, board, move):
        """ Aplica um movimento no tabuleiro e retorna o novo estado do tabuleiro. """
        start, end = move
        new_board = [row[:] for row in board]
        piece = new_board[start[0]][start[1]]
        new_board[end[0]][end[1]] = piece
        new_board[start[0]][start[1]] = '.'  # Limpa a posição anterior

        # Verifica captura
        if abs(start[0] - end[0]) == 2:  # Movimento de captura (pula sobre uma peça)
            captured_row, captured_col = (start[0] + end[0]) // 2, (start[1] + end[1]) // 2
            new_board[captured_row][captured_col] = '.'

        # Verifica promoção para rei
        if piece == 'B' and end[0] == len(board) - 1:
            new_board[end[0]][end[1]] = 'BK'
        elif piece == 'W' and end[0] == 0:
            new_board[end[0]][end[1]] = 'WK'

        return new_board

    def minimax(self, board, depth, alpha, beta, maximizing_player, player):
        """ Implementação do algoritmo Minimax com poda Alpha-Beta. """
        opponent = 'W' if player == 'B' else 'B'

        if depth == 0 or self.is_game_over(board):
            return self.evaluate_board(board, player), None

        if maximizing_player:
            max_eval = -math.inf
            best_move = None
            for move in self.get_valid_moves(board, player):
                new_board = self.make_move(board, move)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, False, player)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None
            for move in self.get_valid_moves(board, opponent):
                new_board = self.make_move(board, move)
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, True, player)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def is_game_over(self, board):
        """ Verifica se o jogo acabou. """
        # Jogo termina se um jogador não tiver peças ou movimentos válidos
        players = ['B', 'W']
        for player in players:
            if any(self.get_valid_moves(board, player)):
                return False
        return True

# Função para imprimir o tabuleiro com numeração
def print_board_with_numbers(board):
    # Imprime os números das colunas
    print("   " + "  ".join(map(str, range(len(board[0])))))
    for i, row in enumerate(board):
        # Imprime o número da linha e o conteúdo
        print(f"{i}  " + "  ".join(row))

# Função principal para jogar
def play_checkers():
    board = [
        ['.', 'B', '.', 'B', '.', 'B', '.', 'B'],
        ['B', '.', 'B', '.', 'B', '.', 'B', '.'],
        ['.', 'B', '.', 'B', '.', 'B', '.', 'B'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['W', '.', 'W', '.', 'W', '.', 'W', '.'],
        ['.', 'W', '.', 'W', '.', 'W', '.', 'W'],
        ['W', '.', 'W', '.', 'W', '.', 'W', '.']
    ]

    ai = CheckersAI(depth=3)
    current_player = 'B'  # Jogador começa com as peças pretas ('B')

    while not ai.is_game_over(board):
        print_board_with_numbers(board)
        if current_player == 'B':
            print("Your turn! Here are your valid moves:")
            moves = ai.get_valid_moves(board, current_player)
            for i, move in enumerate(moves):
                print(f"{i}: {move}")

            if not moves:
                print("No valid moves left! You lose.")
                break

            move_index = int(input("Choose your move (enter the number): "))
            while move_index < 0 or move_index >= len(moves):
                move_index = int(input("Invalid choice. Choose a valid move: "))

            board = ai.make_move(board, moves[move_index])
        else:
            print("AI's turn!")
            _, best_move = ai.minimax(board, ai.depth, -math.inf, math.inf, True, current_player)
            if best_move:
                print(f"AI chose: {best_move}")
                board = ai.make_move(board, best_move)
            else:
                print("AI has no valid moves! You win.")
                break

        # Alterna o jogador
        current_player = 'W' if current_player == 'B' else 'B'

    print("Game over!")
    print_board_with_numbers(board)

# Para jogar o jogo, basta chamar:
play_checkers()
