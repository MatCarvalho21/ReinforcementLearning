import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np  
from agent import Agent

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
ENEMY_SNAKE_COLOR_1 = (67, 45, 89)
ENEMY_SNAKE_COLOR_2 = (168, 108, 255)
ENEMY_SNAKE_COLOR_3 = (255, 255, 255)

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

class RealSnakeGame:

    def __init__(self, w=1300, h=480):
        self.display_width = w
        self.display_height = h

        # INICIALIZANDO DISPLAY
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.clock.tick(FPS)

        # INICIALIZANDO INÍCIO DO JOGO
        self.direction = Direction.RIGHT
        self.enemy_direction = Direction.RIGHT

        self.enemy_head = Point((self.display_width-20)/4, self.display_height/2)
        self.enemy_snake = [self.enemy_head, 
                      Point(self.enemy_head.x-BLOCK_SIZE, self.enemy_head.y),
                      Point(self.enemy_head.x-(2*BLOCK_SIZE), self.enemy_head.y)]
        
        self.head = Point((self.display_width-20)/4 + 640, self.display_height/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.enemy_food = None
        self.enemy_star = None
        self.enemy_has_star = False
        self.enemy_bomb = None
        self.enemy_has_bomb = False
        self._place_enemy_food()
        self.enemy_score = 0
        self.agent = Agent()
        self.agent.model._load()

        self.count_star = 0
        self.count_bomb = 0
        self.score = 0
        self.food = None
        self.star = None
        self.has_star = False
        self.bomb = None
        self.has_bomb = False
        self._place_players_food()

    def _place_players_food(self):
        """
        Coloca a comida em um ponto aleatório do jogo
        """
        x = random.randint(1, ((self.display_width-20)/2-BLOCK_SIZE)//BLOCK_SIZE -1)*BLOCK_SIZE + 640 
        y = random.randint(1, (self.display_height-BLOCK_SIZE )//BLOCK_SIZE -1)*BLOCK_SIZE
        self.food = Point(x, y)

        # Se a comida estiver em cima da cobra, coloca a comida em outro lugar
        if self.food in self.snake or self.food == self.star or self.food == self.bomb:
            self._place_players_food()

    def _place_enemy_food(self):
        """
        Coloca a comida em um ponto aleatório do jogo
        """
        x = random.randint(1, ((self.display_width-20)/2-BLOCK_SIZE)//BLOCK_SIZE -1)*BLOCK_SIZE 
        y = random.randint(1, (self.display_height-BLOCK_SIZE )//BLOCK_SIZE -1)*BLOCK_SIZE
        self.enemy_food = Point(x, y)

        # Se a comida estiver em cima da cobra, coloca a comida em outro lugar
        if self.enemy_food in self.enemy_snake or self.enemy_food == self.enemy_star or self.enemy_food == self.enemy_bomb:
            self._place_enemy_food()

    def _place_players_star(self):
        """
        Coloca a estrela em um ponto aleatório do jogo
        """
        x = random.randint(1, ((self.display_width-20)/2-BLOCK_SIZE)//BLOCK_SIZE -1)*BLOCK_SIZE + 640
        y = random.randint(1, (self.display_height-BLOCK_SIZE )//BLOCK_SIZE -1)*BLOCK_SIZE
        self.star = Point(x, y)

        # Se a estrela estiver em cima da cobra, coloca a estrela em outro lugar
        if self.star in self.snake or self.star == self.food or self.star == self.bomb:
            self._place_players_star()

    def _place_enemy_star(self):
        """
        Coloca a estrela em um ponto aleatório do jogo
        """
        x = random.randint(1, ((self.display_width-20)/2-BLOCK_SIZE)//BLOCK_SIZE -1)*BLOCK_SIZE
        y = random.randint(1, (self.display_height-BLOCK_SIZE )//BLOCK_SIZE -1)*BLOCK_SIZE
        self.enemy_star = Point(x, y)

        # Se a estrela estiver em cima da cobra, coloca a estrela em outro lugar
        if self.enemy_star in self.enemy_snake or self.enemy_star == self.enemy_food or self.enemy_star == self.enemy_bomb:
            self._place_enemy_star()

    def _place_players_bomb(self):
        """
        Coloca a bomba em um ponto aleatório do jogo
        """
        x = random.randint(1, ((self.display_width-20)/2-BLOCK_SIZE)//BLOCK_SIZE -1)*BLOCK_SIZE + 640
        y = random.randint(1, (self.display_height-BLOCK_SIZE )//BLOCK_SIZE -1)*BLOCK_SIZE
        self.bomb = Point(x, y)

        # Se a bomba estiver em cima da cobra, coloca a bomba em outro lugar
        if self.bomb in self.snake or self.bomb == self.food or self.bomb == self.star:
            self._place_players_bomb()

    def _place_enemy_bomb(self):
        """
        Coloca a estrela em um ponto aleatório do jogo
        """
        x = random.randint(1, ((self.display_width-20)/2-BLOCK_SIZE)//BLOCK_SIZE -1)*BLOCK_SIZE
        y = random.randint(1, (self.display_height-BLOCK_SIZE )//BLOCK_SIZE -1)*BLOCK_SIZE
        self.enemy_bomb = Point(x, y)

        # Se a estrela estiver em cima da cobra, coloca a estrela em outro lugar
        if self.enemy_bomb in self.enemy_snake or self.enemy_bomb == self.enemy_food or self.enemy_bomb == self.enemy_star:
            self._place_enemy_bomb()

    def play_step(self):
        """
        Função que roda a cada passo do jogo
        """
        self.count_star += 1
        self.count_bomb += 1

        if self.count_star >= FPS*10:
            self.has_star = True
            self.enemy_has_star = True
            self.count_star = 0
            self._place_players_star()
            self._place_enemy_star()
        
        if self.count_bomb >= FPS*12:
            self.has_bomb = True
            self.enemy_has_bomb = True
            self.count_bomb = 0
            self._place_players_bomb()
            self._place_enemy_bomb()

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
        self._player_move(self.direction) 
        self.snake.insert(0, self.head)

        # 3. Movimentar a cobra inimiga
        state_old = self.agent.get_state(self)
        action = self.agent.get_action(state_old)
        self._enemy_move(action)
        self.enemy_snake.insert(0, self.enemy_head)

        # 3. Checar se o jogo acabou
        game_over = False
        if self.player_is_collision():
            game_over = True
            return game_over, self.score, self.enemy_score
        
        if self.enemy_is_collision():
            game_over = True
            return game_over, self.score, self.enemy_score
        
        # 4. Colocar nova comida ou apenas mover
        if self.head == self.food:
            self.score += 1
            self._place_players_food()
        else:
            self.snake.pop()
        
        if self.enemy_head == self.enemy_food:
            self.enemy_score += 1
            self._place_enemy_food()
        else:
            self.enemy_snake.pop()

        if self.head == self.star and self.has_star:
            self.score += 5
            self.has_star = False
            for _ in range(5):
                self.snake.insert(0, self.head)

        if self.enemy_head == self.enemy_star and self.enemy_has_star:
            self.enemy_score += 5
            self.enemy_has_star = False
            for _ in range(5):
                self.enemy_snake.insert(0, self.enemy_head)

        # 5. Atualizar a interface e o relógio
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. Retornar se o jogo acabou e a pontuação
        return game_over, self.score, self.enemy_score
    
    def player_is_collision(self):
        """
        Checa se a cobra colidiu com a parede ou com ela mesma
        """
        # Colisão com a parede
        if self.head.x > self.display_width - 2*BLOCK_SIZE or self.head.x < BLOCK_SIZE + 640  or self.head.y > self.display_height - 2*BLOCK_SIZE or self.head.y < BLOCK_SIZE:
            return True
        # Colisão com a cobra
        if self.head in self.snake[1:]:
            return True
        # Colisão com a bomba
        if self.head == self.bomb and self.has_bomb:
            # Pinta explosão a partir de uma imagem e adiciona um som
            exp = pygame.image.load('snake_game/assets/explosion.png')
            exp = pygame.transform.scale(exp, (3*BLOCK_SIZE, 3*BLOCK_SIZE))
            self.display.blit(exp, (self.bomb.x - BLOCK_SIZE, self.bomb.y - BLOCK_SIZE))
            pygame.display.flip()
            pygame.time.delay(1000)
            return True

        return False
    
    def enemy_is_collision(self):
        """
        Checa se a cobra colidiu com a parede ou com ela mesma ou com a bomba
        """
        # Colisão com a parede
        if self.enemy_head.x > (self.display_width-20)/2 - BLOCK_SIZE or self.enemy_head.x < 20 or self.enemy_head.y > self.display_height - BLOCK_SIZE or self.enemy_head.y < 0:
            return True
        # Colisão com a cobra
        if self.enemy_head in self.enemy_snake[1:]:
            return True
        if self.enemy_head == self.enemy_bomb and self.enemy_has_bomb:
            # Pinta explosão a partir de uma imagem e adiciona um som
            exp = pygame.image.load('snake_game/assets/explosion.png')
            exp = pygame.transform.scale(exp, (3*BLOCK_SIZE, 3*BLOCK_SIZE))
            self.display.blit(exp, (self.enemy_bomb.x - BLOCK_SIZE, self.enemy_bomb.y - BLOCK_SIZE))
            pygame.display.flip()
            pygame.time.delay(1000)
            return True
    
    def _update_ui(self):
        """
        Atualiza a interface do jogo
        """

        # Coloca uma imagem de fundo ajustada ao tamanho da tela
        bg = pygame.image.load('snake_game/assets/grass_2.png')
        bg = pygame.transform.scale(bg, (self.display_width, self.display_height))
        self.display.blit(bg, (0, 0))
        
        # Pinta a cobra
        for pt in self.snake:
            pygame.draw.rect(self.display, SNAKE_COLOR_1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, SNAKE_COLOR_2, pygame.Rect(pt.x+3, pt.y+3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))
            pygame.draw.rect(self.display, SNAKE_COLOR_3, pygame.Rect(pt.x+6, pt.y+6, BLOCK_SIZE - 12, BLOCK_SIZE - 12))
 
        # Pinta a cobra (inimigo)
        for pt in self.enemy_snake:
            pygame.draw.rect(self.display, ENEMY_SNAKE_COLOR_1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, ENEMY_SNAKE_COLOR_2, pygame.Rect(pt.x+3, pt.y+3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))
            pygame.draw.rect(self.display, ENEMY_SNAKE_COLOR_3, pygame.Rect(pt.x+6, pt.y+6, BLOCK_SIZE - 12, BLOCK_SIZE - 12))
        
        # Pinta a fruta
        pygame.draw.rect(self.display, FRUIT_COLOR, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, FRUIT_COLOR_2, pygame.Rect(self.food.x + BLOCK_SIZE/2 - 2, self.food.y - 4, 4, 4))
        pygame.draw.rect(self.display, FRUIT_COLOR_3, pygame.Rect(self.food.x + 3, self.food.y + 3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))

        # Pinta a fruta (inimigo)
        pygame.draw.rect(self.display, FRUIT_COLOR, pygame.Rect(self.enemy_food.x, self.enemy_food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, FRUIT_COLOR_2, pygame.Rect(self.enemy_food.x + BLOCK_SIZE/2 - 2, self.enemy_food.y - 4, 4, 4))
        pygame.draw.rect(self.display, FRUIT_COLOR_3, pygame.Rect(self.enemy_food.x + 3, self.enemy_food.y + 3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))

        # Pinta a estrela
        if self.has_star:
            pygame.draw.circle(self.display, STAR_COLOR_1, (self.star.x + BLOCK_SIZE//2, self.star.y + BLOCK_SIZE//2), BLOCK_SIZE//2)
            pygame.draw.circle(self.display, STAR_COLOR_2, (self.star.x + BLOCK_SIZE//2, self.star.y+ BLOCK_SIZE//2), BLOCK_SIZE//2 - 2)

        # Pinta a estrela (inimigo)
        if self.enemy_has_star:
            pygame.draw.circle(self.display, STAR_COLOR_1, (self.enemy_star.x + BLOCK_SIZE//2, self.enemy_star.y + BLOCK_SIZE//2), BLOCK_SIZE//2)
            pygame.draw.circle(self.display, STAR_COLOR_2, (self.enemy_star.x + BLOCK_SIZE//2, self.enemy_star.y+ BLOCK_SIZE//2), BLOCK_SIZE//2 - 2)

        # Pinta a bomba
        if self.has_bomb:
            pygame.draw.rect(self.display, BOMB_COLOR_1, pygame.Rect(self.bomb.x, self.bomb.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BOMB_COLOR_2, pygame.Rect(self.bomb.x + 3, self.bomb.y + 3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))

        # Pinta a bomba (inimigo)
        if self.enemy_has_bomb:
            pygame.draw.rect(self.display, BOMB_COLOR_1, pygame.Rect(self.enemy_bomb.x, self.enemy_bomb.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BOMB_COLOR_2, pygame.Rect(self.enemy_bomb.x + 3, self.enemy_bomb.y + 3, BLOCK_SIZE - 6, BLOCK_SIZE - 6))

        # Pinta a pontuação
        text = font.render("Player's Score: " + str(self.score), True, SCORE_COLOR)
        self.display.blit(text, [660, 0])
        text = font.render("Enemy's Score: " + str(self.enemy_score), True, SCORE_COLOR)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _player_move(self, direction):
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

    def _enemy_move(self, action):
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

if __name__ == '__main__':
    game = RealSnakeGame()
    
    # game loop
    while True:
        game_over, score, enemy_score = game.play_step()
        
        if game_over == True:
            break
        
    print("Players's Final Score:", score)
    print("Enemy's Final Score:", enemy_score)

    pygame.quit()