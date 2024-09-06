from new_agent import Agent
from new_game import SnakeGameIA

def test():
    agent = Agent()
    agent.model._load()

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

        if done:
            break
    
if __name__ == '__main__':
    test()