import torch as T
import random
import numpy as np
from game import Minesweeper
from collections import deque
import pygame
from sprites import load_images
from dqn import Linear_QNet, QTrainer
from plot_helper import plot


class Agent:
    def __init__(self, epsilon, eps_dec, gamma, max_mem, batch_size, lr, n):
        """
        Create an RL Agent
        Args:
            epsilon - exploration rate
            eps_dec - how much we decrement epsilon by each training step
            gamma - discount factor
            max_mem - replay memory size
            batch_size - size of training batches
            lr - the learning rate
            n - the size of the board (lengthwise)
        """
        self.n_games = 0
        self.epsilon = epsilon  # exploration rate
        self.eps_dec = eps_dec
        self.gamma = gamma  # discount factor
        self.max_mem = max_mem
        self.memory = deque(maxlen=self.max_mem)
        self.batch_size = batch_size
        self.lr = lr
        self.n = n
        self.model = Linear_QNet(n**2, 256, 256, n**2)
        self.trainer = QTrainer(self.model, lr, self.gamma)
        self.action_space = np.array([i for i in range(n**2)], dtype=int)

    def get_state(self, game):
        """
        Get the current state of the game
        Args:
            game - the game instance
        Returns:
            The state of the board, represented as a flattened matrix
        """
        state = np.array([i for row in game.board for i in row], dtype=int)
        state[5] = -3
        return np.where(state == -3, -1, state)  # obscure mine positions to the agent

    def remember(self, state, action, reward, next_state, done):
        """
        Add an episode to the deque
        Args:
            state - the current state
            action - the action taken at 'state'
            reward - the reward recieved at 'state'
            next_state - the state reached by taking 'action' at 'state'
            done - T/F if transitioned to terminal state
        Returns:
            Nothing
        """
        self.memory.append((state, action, reward, next_state, done))  # popleft if full

    def train_long_memory(self):
        """
        Train the agent over an entire training batch
        Args:
            None
        Returns
            Nothing
        """
        if len(self.memory) > self.batch_size:
            mini_sample = random.sample(self.memory, self.batch_size)
        else:
            mini_sample = (
                self.memory
            )  # take entire replay memory if we have less than self.batch_size memories

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        """
        Train the agent over a single game step
        Args:
            state - the current state
            action - the action taken at 'state'
            reward - the reward recieved at 'state'
            next_state - the state reached by taking 'action' at 'state'
            done - T/F if transitioned to terminal state
        Returns:
            Nothing
        """
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        """
        Determine the action the agent will take at the current state
        Args:
            state - the current state of the board
        Returns:
            The action the agent chose (integer representing the index of the square to click)
        """
        if np.random.random() < self.epsilon:  # explorative factor
            action = np.random.choice(self.action_space)
        else:
            state0 = T.tensor(state, dtype=T.float)  # else, pick off of policy
            prediction = self.model(state0)
            action = T.argmax(prediction).item()
        return int(action)


def train():
    # keeping track of training
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    # initialize agent and game
    agent = Agent(
        epsilon=0,
        eps_dec=0.01,
        gamma=0.9,
        max_mem=100000,
        batch_size=1000,
        lr=0.001,
        n=15,
    )
    game = Minesweeper(n=15, mine_cnt=15)

    # initialize UI
    pygame.init()
    win_width, win_height = 600, 600
    play_width, play_height = 600, 600
    square_size, bar_height, square = 40, 10, 15
    window = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Minesweeper")

    board_width, board_height = int(play_width / square_size), int(
        play_height / square_size
    )
    images = load_images()
    game.draw_board(board_width, board_height, images, window)
    pygame.display.update()

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
                agent.model.save()

            print(f"Game: {agent.n_games}, Score: {score}, Record: {record}")

            # plotting
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == "__main__":
    train()
