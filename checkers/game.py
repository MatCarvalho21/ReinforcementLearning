import pygame
import numpy as np

# VARIÁVEIS GLOBAIS 
FPS = 60
COR_BORDA = (115, 60, 29)
COR_1 = (146, 89, 38)
COR_2 = (0, 0, 0)
P2_COR_1 = (30, 41, 186)
P2_COR_2 = (40, 69, 255)
P1_COR_1 = (161, 23, 43)
P1_COR_2 = (184, 54, 76)
BACKGROUND = (255, 255, 255)
RADIUS = 20
MOVE_COLOR_1 = (217, 187, 41)
MOVE_COLOR_2 = (95, 50, 140)

class CheckersGame:
    def __init__(self, w=640, h=480):
        """
        Método de inicialização da classe CheckersGame
        """

        self.display_width = w
        self.display_height = h
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Checkers Game')
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)
        self.crown = pygame.image.load('checkers/assets/crown.png')
        self.crown = pygame.transform.scale(self.crown, (30, 30))
        self.shift = 2

        self.board = np.array([[1, 0, 1, 0, 1, 0, 1, 0],
                                [0, 1, 0, 1, 0, 1, 0, 1],
                                [1, 0, 1, 0, 1, 0, 1, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 2, 0, 2, 0, 2, 0, 2],
                                [2, 0, 2, 0, 2, 0, 2, 0],
                                [0, 2, 0, 2, 0, 2, 0, 2]])
        
        self.selected_piece = None  
        self.valid_moves = []  
        
    def game_loop(self):
        """
        Método principal do jogo
        """

        running = True
        while running:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._move(mouse_pos)
                   
            self.display.fill(BACKGROUND)
            self._draw_board()
            self._draw_pieces()
            pygame.display.update()

        pygame.quit()

    def _move(self, mouse_pos):
        """
        Método para mover as peças no tabuleiro
        """
        real_pos = (mouse_pos[1] - 40) // 50, (mouse_pos[0] - 120) // 50  # Coordenadas da peça clicada (Y, X)

        # verifica se uma peça foi selecionada e acessa ela  
        if self.selected_piece:  
            piece = self.board[self.selected_piece[0]][self.selected_piece[1]]  

            # verifica se o clique foi um movimento válido e atualiza o tabuleiro
            if real_pos in self.valid_moves:
                self.board[self.selected_piece[0]][self.selected_piece[1]] = 0 
                self.board[real_pos[0]][real_pos[1]] = piece

                # Verificar se houve captura (comer peça) e remover a peça capturada
                middle_x = (self.selected_piece[0] + real_pos[0]) // 2
                middle_y = (self.selected_piece[1] + real_pos[1]) // 2
                if abs(self.selected_piece[0] - real_pos[0]) == 2: 
                    self.board[middle_x][middle_y] = 0  

                # Verificar se a peça comum atingiu o lado oposto e deve ser promovida a dama
                if piece == 1 and real_pos[0] == 7:
                    self.board[real_pos[0]][real_pos[1]] = 3 
                elif piece == 2 and real_pos[0] == 0:
                    self.board[real_pos[0]][real_pos[1]] = 4 

                # Verificar se pode capturar mais peças
                if abs(self.selected_piece[0] - real_pos[0]) == 2:
                    self.valid_moves = self._get_valid_moves(real_pos, capturing=True)
                    if self.valid_moves:
                        self.selected_piece = real_pos
                        return

                # Alterna turno
                self.valid_moves = []  # Limpa os movimentos válidos
                self.selected_piece = None  # Desseleciona a peça
                self.shift = 3 - self.shift  # Alterna turno

                # Verificar se algum jogador ficou sem peças
                self._check_winner()

            else:
                # Verifica se o jogador clicou em outra peça do mesmo time
                new_piece = self.board[real_pos[0]][real_pos[1]]

                if new_piece == self.shift or new_piece == self.shift + 2:
                    # Redefinir para a nova peça selecionada
                    self.selected_piece = real_pos
                    self.valid_moves = self._get_valid_moves(real_pos) 

        else:
            piece = self.board[real_pos[0]][real_pos[1]]  # Obter a peça clicada
            if piece == self.shift or piece == self.shift + 2:  # Verifica se é o turno da peça clicada (inclui damas)
                self.selected_piece = real_pos  
                self.valid_moves = self._get_valid_moves(real_pos) 

    def _check_winner(self):
        """
        Métotodo para verificar se algum jogador ganhou
        """
        p1_pieces = np.count_nonzero((self.board == 1) | (self.board == 3))  # Jogador 1 (peças comuns e damas)
        p2_pieces = np.count_nonzero((self.board == 2) | (self.board == 4))  # Jogador 2 (peças comuns e damas)

        if p1_pieces == 0:
            print("Player 2 ganhou!")
            pygame.quit()
            exit()

        elif p2_pieces == 0:
            print("Player 1 ganhou!")
            pygame.quit()
            exit()

    def _draw_board(self):
        """
        Método para desenhar o tabuleiro
        """

        pygame.draw.rect(self.display, COR_BORDA, (110, 30, 420, 420))
        pygame.draw.rect(self.display, COR_1, (120, 40, 400, 400))

        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 0:
                    pygame.draw.rect(self.display, COR_2, (120 + j*50, 40 + i*50, 50, 50))

    def _get_valid_moves(self, pos, capturing=False):
        """
        Método para obter movimentos válidos
        """
        x, y = pos
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        piece = self.board[x][y]

        for dx, dy in directions:
            # Se a peça for uma peça normal (não uma dama)
            if piece == 1 and dx == -1 or piece == 2 and dx == 1:
                continue  # Peças normais não podem andar para trás

            nx, ny = x + dx, y + dy
            # Verifica se a posição está dentro do tabuleiro
            if 0 <= nx < 8 and 0 <= ny < 8:
                if self.board[nx][ny] == 0 and not capturing:  # Movimentos normais (não captura)
                    moves.append((nx, ny))

                # Captura de peça
                if 0 <= nx + dx < 8 and 0 <= ny + dy < 8 and self.board[nx][ny] == 3 - self.shift:
                    # Verifica se há uma peça adversária e uma posição vazia depois dela
                    if self.board[nx + dx][ny + dy] == 0:
                        moves.append((nx + dx, ny + dy))

        return moves

    def _draw_pieces(self):
        """
        Método para desenhar as peças no tabuleiro
        """

        for each_x in range(0, 8):
            for each_y in range(0, 8):

                real_pos = (each_x, each_y)

                if self.board[each_y][each_x] == 1:
                    pygame.draw.circle(self.display, P1_COR_1, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS)
                    pygame.draw.circle(self.display, P1_COR_2, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS - 5)

                elif self.board[each_y][each_x] == 2:
                    pygame.draw.circle(self.display, P2_COR_1, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS)
                    pygame.draw.circle(self.display, P2_COR_2, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS - 5)

                elif self.board[each_y][each_x] == 3:
                    pygame.draw.circle(self.display, P1_COR_1, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS)
                    pygame.draw.circle(self.display, P1_COR_2, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS - 5)
                    self.display.blit(self.crown, (real_pos[0]*50 + 130, real_pos[1]*50 + 49))

                elif self.board[each_y][each_x] == 4:
                    pygame.draw.circle(self.display, P2_COR_1, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS)
                    pygame.draw.circle(self.display, P2_COR_2, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS - 5)
                    self.display.blit(self.crown, (real_pos[0]*50 + 130, real_pos[1]*50 + 49))

        # Destaque de movimentos válidos
        for move in self.valid_moves:
            if abs(self.selected_piece[0] - move[0]) == 2:  # Se for uma captura
                pygame.draw.circle(self.display, MOVE_COLOR_2, (move[1] * 50 + 145, move[0] * 50 + 65), RADIUS, 3)  # Círculo roxo
            else:
                pygame.draw.circle(self.display, MOVE_COLOR_1, (move[1] * 50 + 145, move[0] * 50 + 65), RADIUS, 3)  # Círculo amarelo


if __name__ == '__main__':
    game = CheckersGame()
    game.game_loop()

