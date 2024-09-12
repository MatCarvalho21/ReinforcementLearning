import pygame
from pieces import Piece

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

class CheckersGame:
    def __init__(self, w=640, h=480):

        # INICIALIZANDO DISPLAY
        self.display_width = w
        self.display_height = h
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Checkers Game')
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)

        # CONFIGURANDO JOGADOR 1
        self.p1_npieces = 12
        self.p1_pieces = [Piece(1, 1, (P1_COR_1, P1_COR_2), True), Piece(1, 3, (P1_COR_1, P1_COR_2), True), Piece(1, 5, (P1_COR_1, P1_COR_2)), Piece(1, 7, (P1_COR_1, P1_COR_2)),
                          Piece(2, 2, (P1_COR_1, P1_COR_2)), Piece(2, 4, (P1_COR_1, P1_COR_2)), Piece(2, 6, (P1_COR_1, P1_COR_2)), Piece(2, 8, (P1_COR_1, P1_COR_2)),
                          Piece(3, 1, (P1_COR_1, P1_COR_2)), Piece(3, 3, (P1_COR_1, P1_COR_2)), Piece(3, 5, (P1_COR_1, P1_COR_2)), Piece(3, 7, (P1_COR_1, P1_COR_2))]

        # CONFIGURANDO JOGADOR 2
        self.p2_npieces = 12
        self.p2_pieces = [Piece(6, 2, (P2_COR_1, P2_COR_2)), Piece(6, 4, (P2_COR_1, P2_COR_2)), Piece(6, 6, (P2_COR_1, P2_COR_2)), Piece(6, 8, (P2_COR_1, P2_COR_2)),
                          Piece(7, 1, (P2_COR_1, P2_COR_2)), Piece(7, 3, (P2_COR_1, P2_COR_2)), Piece(7, 5, (P2_COR_1, P2_COR_2)), Piece(7, 7, (P2_COR_1, P2_COR_2)),
                          Piece(8, 2, (P2_COR_1, P2_COR_2)), Piece(8, 4, (P2_COR_1, P2_COR_2)), Piece(8, 6, (P2_COR_1, P2_COR_2)), Piece(8, 8, (P2_COR_1, P2_COR_2))]
        
    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                # Sair do jogo
                if event.type == pygame.QUIT:
                    running = False

            # Limpar a tela a cada frame
            self.display.fill(BACKGROUND)

            # Atualizar peças
            self._draw_board()
            self._draw_pieces()

            # Atualizar a tela
            pygame.display.update()

            if self.p1_npieces == 0 or self.p2_npieces == 0:
                running = False

        pygame.quit()

    def _draw_board(self):
        
        pygame.draw.rect(self.display, COR_BORDA, (110, 30, 420, 420))
        pygame.draw.rect(self.display, COR_1, (120, 40, 400, 400))

        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 0:
                    pygame.draw.rect(self.display, COR_2, (120 + j*50, 40 + i*50, 50, 50))

    def _draw_pieces(self):
        for piece in self.p1_pieces + self.p2_pieces:
            piece.draw(self.display)

if __name__ == '__main__':
    game = CheckersGame()
    game.game_loop()

