import pygame

class Piece:
    def __init__(self, row, col, color, is_king=False):
        """Inicializa a peça"""
        self.row = row
        self.col = col
        self.color = color
        self.is_king = is_king

        self.crown = pygame.image.load('checkers/assets/crown.png')
        self.crown = pygame.transform.scale(self.crown, (35, 35))
    
    def move(self, row, col):
        """Atualiza a posição da peça"""
        self.row = row
        self.col = col

    def make_king(self):
        """Promove a peça para 'dama'"""
        self.is_king = True

    def draw(self, display):
        """Desenha a peça no tabuleiro"""
        radius = 20
        pygame.draw.circle(display, self.color[0], (self.col*50 + 95, self.row*50 + 15), radius)
        pygame.draw.circle(display, self.color[1], (self.col*50 + 95, self.row*50 + 15), radius - 5)
        if self.is_king:
            display.blit(self.crown, (self.col*50 + 77, self.row*50 - 4))