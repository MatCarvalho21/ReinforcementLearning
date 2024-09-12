import pygame

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

        self.board = [1, 0, 1, 0, 1, 0, 1, 0,
                      0, 3, 0, 1, 0, 1, 0, 1,
                      1, 0, 1, 0, 1, 0, 1, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 
                      0, 0, 0, 0, 0, 0, 0, 0,
                      0, 2, 0, 2, 0, 2, 0, 2,
                      2, 0, 4, 0, 2, 0, 2, 0,
                      0, 2, 0, 2, 0, 2, 0, 2]
        
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
        
        """

        real_pos = (mouse_pos[1] - 40) // 50, (mouse_pos[0] - 120) // 50 # (X, Y)
        piece = self.board[real_pos[0]*8 + real_pos[1]]

        if piece == self.shift or piece == self.shift + 2:
            print("OK")

        else:
            print("NOT OK")

    def _draw_board(self):
        """
        
        """

        pygame.draw.rect(self.display, COR_BORDA, (110, 30, 420, 420))
        pygame.draw.rect(self.display, COR_1, (120, 40, 400, 400))

        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 0:
                    pygame.draw.rect(self.display, COR_2, (120 + j*50, 40 + i*50, 50, 50))

    def _draw_pieces(self):
        """
        
        """

        for each_pos in range(0, 64):

            real_pos = (each_pos % 8, each_pos // 8)

            if self.board[each_pos] == 1:

                pygame.draw.circle(self.display, P1_COR_1, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS)
                pygame.draw.circle(self.display, P1_COR_2, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS - 5)

            elif self.board[each_pos] == 2:

                pygame.draw.circle(self.display, P2_COR_1, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS)
                pygame.draw.circle(self.display, P2_COR_2, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS - 5)

            elif self.board[each_pos] == 3:

                pygame.draw.circle(self.display, P1_COR_1, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS)
                pygame.draw.circle(self.display, P1_COR_2, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS - 5)
                self.display.blit(self.crown, (real_pos[0]*50 + 130, real_pos[1]*50 + 49))

            elif self.board[each_pos] == 4:

                pygame.draw.circle(self.display, P2_COR_1, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS)
                pygame.draw.circle(self.display, P2_COR_2, (real_pos[0]*50 + 145, real_pos[1]*50 + 65), RADIUS - 5)
                self.display.blit(self.crown, (real_pos[0]*50 + 130, real_pos[1]*50 + 49))


if __name__ == '__main__':
    game = CheckersGame()
    game.game_loop()

