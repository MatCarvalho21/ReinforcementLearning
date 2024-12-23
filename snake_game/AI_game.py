import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

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
BOMB_COLOR_1 = (0, 0, 0)
BOMB_COLOR_2 = (33, 34, 38)
BACKGROUND_COLOR = (0,0,0)
FPS = 15

BLOCK_SIZE = 20
SPEED = 10

pygame.init()
font = pygame.font.Font('snake_game/assets/arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

class SnakeGameIA:
    def __init__(self, w=640, h=480):
        """
        Inicializa o jogo.
        """
        self.display_width = w
        self.display_height = h

        # INICIALIZANDO DISPLAY
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)
        self.reset()

    def reset(self):
        """
        Reseta o jogo, inicializando o estado do jogo.
        """
        # INICIALIZANDO INÍCIO DO JOGO
        self.enemy_direction = Direction.RIGHT
        self.enemy_head = Point(self.display_width/2, self.display_height/2)
        self.enemy_snake = [self.enemy_head, 
                      Point(self.enemy_head.x-BLOCK_SIZE, self.enemy_head.y),
                      Point(self.enemy_head.x-(2*BLOCK_SIZE), self.enemy_head.y)]
        
        self.count_star = 0
        self.count_bomb = 0
        self.score = 0
        self.enemy_food = None
        self.enemy_star = Point(-BLOCK_SIZE, -BLOCK_SIZE)
        self.enemy_has_star = False
        self.enemy_bomb = Point(-BLOCK_SIZE, -BLOCK_SIZE)
        self.enemy_has_bomb = False
        self._place_food()
        self._place_star()
        self.frame_iteration = 0

    def _place_food(self):
        """
        Coloca a comida em um ponto aleatório do jogo.
        """
        x = random.randint(1, (self.display_width-BLOCK_SIZE )//BLOCK_SIZE - 1)*BLOCK_SIZE 
        y = random.randint(1, (self.display_height-BLOCK_SIZE )//BLOCK_SIZE -1)*BLOCK_SIZE
        self.enemy_food = Point(x, y)

        # Se a comida estiver em cima da cobra, coloca a comida em outro lugar
        if self.enemy_food in self.enemy_snake:
            self._place_food()

    def _place_star(self):
        """
        Coloca a estrela em um ponto aleatório do jogo.
        """
        x = random.randint(1, (self.display_width-BLOCK_SIZE )//BLOCK_SIZE - 1)*BLOCK_SIZE 
        y = random.randint(1, (self.display_height-BLOCK_SIZE )//BLOCK_SIZE -1)*BLOCK_SIZE
        self.enemy_star = Point(x, y)

        # Se a estrela estiver em cima da cobra, coloca a estrela em outro lugar
        if self.enemy_star in self.enemy_snake:
            self._place_star()

    def _place_bomb(self):
        """
        Coloca a bomba em um ponto aleatório do jogo.
        """
        x = random.randint(1, (self.display_width-BLOCK_SIZE )//BLOCK_SIZE - 1)*BLOCK_SIZE 
        y = random.randint(1, (self.display_height-BLOCK_SIZE )//BLOCK_SIZE -1)*BLOCK_SIZE
        self.enemy_bomb = Point(x, y)

        # Se a bomba estiver em cima da cobra, coloca a bomba em outro lugar
        if self.enemy_bomb in self.enemy_snake:
            self._place_bomb()

    def play_step(self, action):
        """
        Função que roda a cada passo do jogo.
        """
        self.frame_iteration += 1
        self.count_star += 1
        self.count_bomb += 1

        if self.count_star >= FPS*10:
            self.enemy_has_star = True
            self.count_star = 0
            self._place_star()
        
        if self.count_bomb >= FPS*12:
            self.enemy_has_bomb = True
            self.count_bomb = 0
            self._place_bomb()

        # 1. Coletar a entrada do usuário
        for event in pygame.event.get():
            # Sair do jogo
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. Movimentar a cobra
        self._move(action) 
        self.enemy_snake.insert(0, self.enemy_head)

        # 3. Verificar se o jogo acabou
        reward = 0
        game_over = False
        if self.enemy_is_collision() or self.frame_iteration > 50*len(self.enemy_snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        # 4. Colocar nova comida ou apenas mover
        if self.enemy_head == self.enemy_food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.enemy_snake.pop()

        if self.enemy_head == self.enemy_star and self.enemy_has_star:
            self.score += 5
            reward = 50
            self.enemy_has_star = False
            for _ in range(5):
                self.enemy_snake.insert(0, self.enemy_head)

        # 5. Atualizar a interface e o relógio
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. Retornar recompensa, se o jogo acabou e a pontuação
        return reward, game_over, self.score
    
    def enemy_is_collision(self, pt=None):
        """
        Checa se a cobra colidiu com a parede ou com ela mesma
        """
        if pt is None:
            pt = self.enemy_head
        # Colisão com a parede
        if pt.x > self.display_width - BLOCK_SIZE - 20 or pt.x < 20 or pt.y > self.display_height - BLOCK_SIZE - 20 or pt.y < 20:
            return True
        # Colisão com a cobra
        if pt in self.enemy_snake[1:]:
            return True
        # Colisão com a bomba
        if pt == self.enemy_bomb and self.enemy_has_bomb:
            # Pinta explosão a partir de uma imagem e adiciona um som
            exp = pygame.image.load('snake_game/assets/explosion.png')
            exp = pygame.transform.scale(exp, (3*BLOCK_SIZE, 3*BLOCK_SIZE))
            self.display.blit(exp, (self.enemy_bomb.x - BLOCK_SIZE, self.enemy_bomb.y - BLOCK_SIZE)) 
            pygame.display.flip()
            pygame.time.delay(1000)
            return True

        return False

    def _update_ui(self):
        """
        Atualiza a interface do jogo
        """

        # Coloca uma imagem de fundo ajustada ao tamanho da tela
        bg = pygame.image.load('snake_game/assets/grass.png')
        bg = pygame.transform.scale(bg, (self.display_width, self.display_height))
        self.display.blit(bg, (0, 0))
        
        # Pinta a cobra
        for pt in self.enemy_snake:
            pygame.draw.rect(self.display, SNAKE_COLOR_1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, SNAKE_COLOR_2, pygame.Rect(pt.x+3, pt.y+3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))
            pygame.draw.rect(self.display, SNAKE_COLOR_3, pygame.Rect(pt.x+6, pt.y+6, BLOCK_SIZE - 12, BLOCK_SIZE - 12))
        
        # Pinta a fruta
        pygame.draw.rect(self.display, FRUIT_COLOR, pygame.Rect(self.enemy_food.x, self.enemy_food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, FRUIT_COLOR_2, pygame.Rect(self.enemy_food.x + BLOCK_SIZE/2 - 2, self.enemy_food.y - 4, 4, 4))
        pygame.draw.rect(self.display, FRUIT_COLOR_3, pygame.Rect(self.enemy_food.x + 3, self.enemy_food.y + 3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))

        # Pinta a estrela
        if self.enemy_has_star:
            pygame.draw.circle(self.display, STAR_COLOR_1, (self.enemy_star.x + BLOCK_SIZE//2, self.enemy_star.y + BLOCK_SIZE//2), BLOCK_SIZE//2)
            pygame.draw.circle(self.display, STAR_COLOR_2, (self.enemy_star.x + BLOCK_SIZE//2, self.enemy_star.y+ BLOCK_SIZE//2), BLOCK_SIZE//2 - 2)

        # Pinta a bomba
        if self.enemy_has_bomb:
            pygame.draw.rect(self.display, BOMB_COLOR_1, pygame.Rect(self.enemy_bomb.x, self.enemy_bomb.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BOMB_COLOR_2, pygame.Rect(self.enemy_bomb.x + 3, self.enemy_bomb.y + 3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))

        # Pinta a pontuação
        text = font.render("Score: " + str(self.score), True, SCORE_COLOR)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        """
        Move a cobra na direção especificada
        """

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.enemy_direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.enemy_direction = new_dir

        x = self.enemy_head.x
        y = self.enemy_head.y

        # Movimentação da cobra
        if self.enemy_direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.enemy_direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.enemy_direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.enemy_direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.enemy_head = Point(x, y)