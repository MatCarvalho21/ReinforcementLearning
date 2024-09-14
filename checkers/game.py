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

class CheckersGame:
    def __init__(self, w=640, h=480):
        """
        
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
        self.p1_npieces = 12
        self.p2_npieces = 12

        self.board = np.array([[1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 2, 0, 2, 0, 2, 0, 2],
                            [2, 0, 2, 0, 2, 0, 2, 0],
                            [0, 2, 0, 2, 0, 2, 0, 2]])
        
        self.selected_piece = None  # Para armazenar a peça selecionada
        self.valid_moves = []  # Para armazenar os movimentos válidos
        
    def game_loop(self):
        """
        
        """
        running = True
        while running:
            for event in pygame.event.get():
                # Sair do jogo
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._move(mouse_pos)
                   
            # Limpar a tela a cada frame
            self.display.fill(BACKGROUND)

            # Atualizar peças
            self._draw_board()
            self._draw_pieces()

            # Atualizar a tela
            pygame.display.update()

            if self.p1_npieces == 0 or self.p2_npieces == 0:
                running = False
                if self.p1_npieces == 0:
                    print("Player 2 ganhou!")
                else:
                    print("Player 1 ganhou!")

        pygame.quit()

    def _move(self, mouse_pos):
        """
        Manipula o movimento da peça selecionada e destaca possíveis movimentos
        """
        real_pos = (mouse_pos[1] - 40) // 50, (mouse_pos[0] - 120) // 50  # Coordenadas da peça clicada

        if self.selected_piece:  # Se já há uma peça selecionada
            piece = self.board[self.selected_piece[0]][self.selected_piece[1]]  # Obter a peça selecionada
            if real_pos in self.valid_moves:  # Verifica se o clique foi em um movimento válido
                # Atualiza o tabuleiro com o novo movimento
                self.board[self.selected_piece[0]][self.selected_piece[1]] = 0  # Remove peça da posição antiga
                self.board[real_pos[0]][real_pos[1]] = piece  # Coloca a peça na nova posição

                # Verificar se houve captura (comer peça)
                middle_x = (self.selected_piece[0] + real_pos[0]) // 2
                middle_y = (self.selected_piece[1] + real_pos[1]) // 2
                if abs(self.selected_piece[0] - real_pos[0]) == 2:  # Diferença de 2 indica salto (captura)
                    self.board[middle_x][middle_y] = 0  # Remove a peça comida

                # Verificar se a peça comum atingiu o lado oposto e deve ser promovida a dama
                if piece == 1 and real_pos[0] == 7:
                    self.board[real_pos[0]][real_pos[1]] = 3  # Jogador 1 virou dama
                elif piece == 2 and real_pos[0] == 0:
                    self.board[real_pos[0]][real_pos[1]] = 4  # Jogador 2 virou dama

                # Verificar se pode capturar mais peças
                if abs(self.selected_piece[0] - real_pos[0]) == 2:
                    self.valid_moves = self._get_valid_moves(real_pos, capturing=True)
                    if self.valid_moves:  # Se pode capturar mais, continua com a mesma peça
                        self.selected_piece = real_pos
                        return

                # Alterna turno
                self.valid_moves = []  # Limpa os movimentos válidos
                self.selected_piece = None  # Desseleciona a peça
                self.shift = 3 - self.shift  # Alterna turno

            else:
                self.selected_piece = None  # Se clicou fora dos movimentos válidos, desseleciona

        else:
            piece = self.board[real_pos[0]][real_pos[1]]  # Obter a peça clicada
            if piece == self.shift or piece == self.shift + 2:  # Verifica se é o turno da peça clicada (inclui damas)
                self.selected_piece = real_pos  # Armazena a peça selecionada
                self.valid_moves = self._get_valid_moves(real_pos)  # Obtém movimentos válidos



    def _draw_board(self):
        """
        
        """

        pygame.draw.rect(self.display, COR_BORDA, (110, 30, 420, 420))
        pygame.draw.rect(self.display, COR_1, (120, 40, 400, 400))

        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 0:
                    pygame.draw.rect(self.display, COR_2, (120 + j*50, 40 + i*50, 50, 50))

    def _get_valid_moves(self, pos, capturing=False):
        """
        Retorna uma lista de movimentos válidos para a peça selecionada.
        Se 'capturing' for True, só considera movimentos de captura.
        """
        x, y = pos
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Direções diagonais (frente e trás)

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
        Desenha as peças e destaca possíveis movimentos
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
                pygame.draw.circle(self.display, (128, 0, 128), (move[1] * 50 + 145, move[0] * 50 + 65), RADIUS, 3)  # Círculo roxo
            else:
                pygame.draw.circle(self.display, (255, 255, 0), (move[1] * 50 + 145, move[0] * 50 + 65), RADIUS, 3)  # Círculo amarelo


if __name__ == '__main__':
    game = CheckersGame()
    game.game_loop()

