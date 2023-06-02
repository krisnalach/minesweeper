import torch as T
import random
import numpy as np
from game import Minesweeper, run_game
from collections import deque


class Agent:
    def __init__(self, max_mem, batch_size, lr):
        """
        Create an RL Agent
        Args:
            max_mem - replay memory size
            batch_size - size of training batches
            lr - the learning rate
        """
        self.n_games = 0
        self.epsilon = 0  # exploration rate
        self.gamma = 0  # discount factor
        self.max_mem = max_mem
        self.memory = deque(maxlen=self.max_mem)
        self.batch_size = batch_size
        self.lr = lr
        # TODO: model, trainer

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass


def train():
    # keeping track of training
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    # initialize agent and game
    agent = Agent(max_mem=100000, batch_size=64, lr=0.001)
    game = Minesweeper()
    while True:
        # get current state
        state_curr = agent.get_state(game)

        # get action
        final_action = agent.get_action(state_curr)

        # perform action and get new state
        reward, done, score = game.play(final_action)
        state_new = agent.get_state(game)

        # train short memory of agent
        agent.train_short_memory(state_curr, final_action, reward, state_new, done)

        # remember what happened
        agent.remember(state_curr, final_action, reward, state_new, done)

        if done:
            # train the long memory of agent, plot results
            game.restart_game()
            agent.n_games += 1
            agent.train_long_memory()

            # book keeping
            if score > record:
                record = score
                # agent.model.save()

            print(f"Game: {agent.n_games}, Score: {score}, Record: {record}")

            # TODO: plot


if __name__ == "__main__":
    train()
