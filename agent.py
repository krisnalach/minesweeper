import torch as T
import random
import numpy as np
from game import Minesweeper
from collections import deque
import pygame
from sprites import load_images
from dqn import Linear_QNet, QTrainer
from plot_helper import plot
import time


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
        self.eps_start = 1
        self.eps_dec = eps_dec
        self.gamma = gamma  # discount factor
        self.max_mem = max_mem
        self.memory = deque(maxlen=self.max_mem)
        self.batch_size = batch_size
        self.lr = lr
        self.n = n
        self.model = Linear_QNet(n**2, 512, 512, n**2)
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

        self.eps_start = (
            self.eps_start - self.eps_dec
            if self.eps_start > self.epsilon
            else self.epsilon
        )

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

    def get_action(self, state, game):
        """
        Determine the action the agent will take at the current state
        Args:
            state - the current state of the board
            game - the game instance
        Returns:
            The action the agent chose (integer representing the index of the square to click)
        """
        if np.random.random() < self.eps_start:  # explorative factor
            action = np.random.choice(self.action_space)
        else:
            state0 = T.tensor(state, dtype=T.float)  # else, pick off of policy
            prediction = self.model(state0)

            temp = prediction.tolist()
            for j, i in enumerate(temp):  # getting rid of 'useless' moves
                x = j // game.n
                y = j % game.n
                if game.board[x][y] in {0, 1, 2, 3, 4, 5, 6, 7, 8}:
                    temp[j] = -np.Infinity

            action = np.argmax(temp)

        return int(action)


def train():
    # keeping track of training
    plot_win_rate = []
    plot_avg_reward = []
    wins = 0
    reward_tot = 0
    n = 8
    record = 0
    # initialize agent and game
    agent = Agent(
        epsilon=0.1,
        eps_dec=0.01,
        gamma=0,
        max_mem=100000,
        batch_size=1000,
        lr=0.001,
        n=8,
    )
    game = Minesweeper(n=8, mine_cnt=10)

    # initialize UI
    pygame.init()
    win_width, win_height = 600, 600
    play_width, play_height = 600, 600
    square_size = 75
    window = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Minesweeper")

    board_width, board_height = int(play_width / square_size), int(
        play_height / square_size
    )
    images = load_images()
    game.draw_board(board_width, board_height, images, window, square_size)
    pygame.display.update()

    while True:
        # get current state
        state_curr = agent.get_state(game)

        # get action
        final_action = agent.get_action(state_curr, game)

        # convert action into (x, y)
        x = final_action // n
        y = final_action % n

        # perform action and get new state
        reward, done, score = game.play((x, y))
        state_new = agent.get_state(game)
        reward_tot += reward

        # print(f"Move taken: ({x}, {y})")

        # draw the board to reflect the action taken
        game.draw_board(board_width, board_height, images, window, square_size)
        pygame.display.update()

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

            if score == n**2 - 10:  # win
                wins += 1

            # plotting
            if agent.n_games % 100 == 0:
                plot_win_rate.append(wins / 100)
                print(f"Average reward over this set: {reward_tot / 100}")
                wins = 0
                reward_tot = 0
                plot(plot_win_rate)


if __name__ == "__main__":
    train()
