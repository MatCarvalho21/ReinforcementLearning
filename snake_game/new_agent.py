import torch
import random 
import numpy as np
from collections import deque
from new_game import SnakeGameIA, Direction, Point
from new_model import Linear_QNet, QTrainer
from new_helper import plot
import os

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001
EXPLORATION_LIMIT = 50
HISTORICAL_RECORD = 10
MOVEMENT_MEAN = 20

class Agent:

    def __init__(self):
        self.n_games = 0    
        self.epsilon = 0 # control the random
        self.gamma = 0.9 # discount rate [0,1]
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(19, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game): # game is a array of parameters 
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight (cobre a bomba)
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right (cobre a bomba)
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left (cobre a bomba)
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y,  # food down

            # Star Location
            game.star.x < game.head.x and game.has_star,  # star left
            game.star.x > game.head.x and game.has_star,  # star right
            game.star.y < game.head.y and game.has_star,  # star up
            game.star.y > game.head.y and game.has_star,  # star down

            # Bomb Location
            game.bomb.x < game.head.x and game.has_bomb,  # bomb left
            game.bomb.x > game.head.x and game.has_bomb,  # bomb right
            game.bomb.y < game.head.y and game.has_bomb,  # bomb up
            game.bomb.y > game.head.y and game.has_bomb # bomb down
            ]

        return np.array(state, dtype=int) 

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft() se exceder o limite

    def train_long_memory(self):
        # Vai treinar a memória de longo prazo
        if len(self.memory) > BATCH_SIZE:
            # Pega um mini lote aleatório
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            # Pega a memória inteira
            mini_sample = self.memory
        
        # Pega os valores de cada coluna
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Ações aleatórias o início (explorando o ambiente)
        self.epsilon = EXPLORATION_LIMIT - self.n_games
        final_move = [0,0,0]

        # Se o número aleatório for menor que epsilon, então vamos explorar o ambiente
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        # Caso contrário, vamos usar a rede neural para prever a melhor ação
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
    
def train():

    plot_scores = []
    plot_mean_scores = []
    plot_move_mean = []
    total_score = 0
    record = 0
    agent = Agent()

    try:
        agent.model._load()
        print("Modelo carregado com sucesso.")
    except:
        print("Não foi possível carregar o modelo.")
        pass

    game = SnakeGameIA()
    game.reset()

    while True:
        # Pega o estado antigo
        state_old = agent.get_state(game)
        # Com base no estado antigo, pega a ação
        final_move = agent.get_action(state_old)    
        # Realiza a ação e recebe a recompensa
        reward, done, score = game.play_step(final_move)
        # Pega o novo estado
        state_new = agent.get_state(game)
        # Treina a memória com a nova experiência
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        # Armazena a nova experiência na memória
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Treina o modelo (memória de longa)
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
            if record > HISTORICAL_RECORD:
                agent.model.save()
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot_move_mean.append(sum(plot_scores[-MOVEMENT_MEAN:])/MOVEMENT_MEAN)
            plot(plot_scores, plot_mean_scores, plot_move_mean)

            print('Nº Jogos:', agent.n_games, '- Score:', score, '- Record:', record, end=" ")
            print("- Média Móvel (20):", sum(plot_scores[-MOVEMENT_MEAN:])/MOVEMENT_MEAN)

if __name__ == '__main__':
    train()