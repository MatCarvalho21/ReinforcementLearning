import pygame
import random
from enum import Enum
from collections import namedtuple

# HIPERPARÂMETROS

SCORE_COLOR = (255, 255, 255)
FRUIT_COLOR = (242, 92, 5)
FRUIT_COLOR_2 = (2, 38, 1)
FRUIT_COLOR_3 = (242, 163, 65)
SNAKE_COLOR_1 = (117, 17, 18)
SNAKE_COLOR_2 = (32, 33, 28)
SNAKE_COLOR_3 = (250, 238, 10)
STAR_COLOR_1 = (250, 238, 10)
STAR_COLOR_2 = (255, 255, 142)
BACKGROUND_COLOR = (0,0,0)
FPS = 15

BLOCK_SIZE = 20
SPEED = 10

pygame.init()
font = pygame.font.Font('snake_game/arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

class SnakeGame:

    def __init__(self, w=640, h=480):
        self.display_width = w
        self.display_height = h

        # INICIALIZANDO DISPLAY
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)

        # INICIALIZANDO INÍCIO DO JOGO
        self.direction = Direction.RIGHT
        self.head = Point(self.display_width/2, self.display_height/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.count = 0
        self.score = 0
        self.food = None
        self.star = None
        self.has_star = False
        self._place_food()
        self._place_star()

    def _place_food(self):
        """
        Coloca a comida em um ponto aleatório do jogo
        """
        x = random.randint(0, (self.display_width-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.display_height-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)

        # Se a comida estiver em cima da cobra, coloca a comida em outro lugar
        if self.food in self.snake:
            self._place_food()

    def _place_star(self):
        """
        Coloca a estrela em um ponto aleatório do jogo
        """
        x = random.randint(0, (self.display_width-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.display_height-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.star = Point(x, y)

        # Se a estrela estiver em cima da cobra, coloca a estrela em outro lugar
        if self.star in self.snake:
            self._place_star()

    def play_step(self):
        """
        Função que roda a cada passo do jogo
        """
        self.count += 1
        if self.count >= FPS*10:
            self.has_star = True
            self.count = 0
            self._place_star()

        # 1. Coletar a entrada do usuário
        for event in pygame.event.get():
            # Sair do jogo
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Movimentação da cobra
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # 2. Movimentar a cobra
        self._move(self.direction) 
        self.snake.insert(0, self.head)

        # 3. Checar se o jogo acabou
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        
        # 4. Colocar nova comida ou apenas mover
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        if self.head == self.star and self.has_star:
            self.score += 5
            self.has_star = False
            for _ in range(5):
                self.snake.insert(0, self.head)

        # 5. Atualizar a interface e o relógio
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. Retornar se o jogo acabou e a pontuação
        return game_over, self.score
    
    def _is_collision(self):
        """
        Checa se a cobra colidiu com a parede ou com ela mesma
        """
        # Colisão com a parede
        if self.head.x > self.display_width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.display_height - BLOCK_SIZE or self.head.y < 0:
            return True
        # Colisão com a cobra
        if self.head in self.snake[1:]:
            return True

        return False
    
    def _update_ui(self):
        """
        Atualiza a interface do jogo
        """

        # Coloca uma imagem de fundo ajustada ao tamanho da tela
        bg = pygame.image.load('snake_game/grass.png')
        bg = pygame.transform.scale(bg, (self.display_width, self.display_height))
        self.display.blit(bg, (0, 0))
        
        # Pinta a cobra
        for pt in self.snake:
            pygame.draw.rect(self.display, SNAKE_COLOR_1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, SNAKE_COLOR_2, pygame.Rect(pt.x+3, pt.y+3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))
            pygame.draw.rect(self.display, SNAKE_COLOR_3, pygame.Rect(pt.x+6, pt.y+6, BLOCK_SIZE - 12, BLOCK_SIZE - 12))
        
        # Pinta a fruta
        pygame.draw.rect(self.display, FRUIT_COLOR, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, FRUIT_COLOR_2, pygame.Rect(self.food.x + BLOCK_SIZE/2 - 2, self.food.y - 4, 4, 4))
        pygame.draw.rect(self.display, FRUIT_COLOR_3, pygame.Rect(self.food.x + 3, self.food.y + 3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))

        # Pinta a estrela
        if self.has_star:
            pygame.draw.circle(self.display, STAR_COLOR_1, (self.star.x + BLOCK_SIZE//2, self.star.y + BLOCK_SIZE//2), BLOCK_SIZE//2)
            pygame.draw.circle(self.display, STAR_COLOR_2, (self.star.x + BLOCK_SIZE//2, self.star.y+ BLOCK_SIZE//2), BLOCK_SIZE//2 - 2)

        # Pinta a pontuação
        text = font.render("Score: " + str(self.score), True, SCORE_COLOR)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        """
        Move a cobra na direção especificada
        """
        x = self.head.x
        y = self.head.y

        # Movimentação da cobra
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
    pygame.quit()