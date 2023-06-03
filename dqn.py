import torch as T
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class Linear_QNet(nn.Module):
    def __init__(self, input_size, first_size, second_size, output_size):
        """
        A simple neural network with 3 layers
        Args:
            input size - number of neurons in the input layer
            first_size - number of neurons in the first hidden layer
            second_size - number of neurons in the second hidden layer
            output_size - number of neurons in the ouput layer

        """
        super().__init__()
        self.linear1 = nn.Linear(input_size, first_size)
        self.linear2 = nn.Linear(first_size, second_size)
        self.linear3 = nn.Linear(second_size, output_size)

        self.device = T.device("cuda:0" if T.cuda.is_available() else "cpu")
        self.to(self.device)

    def forward(self, x):
        """
        Forward propagation of an instance x
        Args:
            x - the input
        Returns
            the output y
        """
        x = x.to(self.device)
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        return self.linear3(x)

    def save(self, file_name="model.pth"):
        """
        Save the weights of the Neural Network
        Args:
            file_name - the name of the file to save the weights to
            default is 'model.pth'
        Returns:
            Nothing
        """
        model_folder_path = "./model"
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        T.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma):
        """
        Training class using Q learning
        Args:
            model - the model used to train
            lr - the learning rate
            gamma - discount factor
        """
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.loss = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        """
        Train the model
        Args:
            state - the current state
            action - the action taken at 'state'
            reward - the reward recieved at 'state'
            next_state - the state reached by taking 'action' at 'state'
            done - T/F if transitioned to terminal state
        Returns:
            Nothing
        """
        state = T.tensor(state, dtype=T.float).to(self.model.device)
        action = T.tensor(action, dtype=T.float).to(self.model.device)
        reward = T.tensor(reward, dtype=T.float).to(self.model.device)
        next_state = T.tensor(next_state, dtype=T.float).to(self.model.device)

        if len(state.shape) == 1:
            # reshaping
            state = T.unsqueeze(state, 0)
            action = T.unsqueeze(action, 0)
            reward = T.unsqueeze(reward, 0)
            next_state = T.unsqueeze(next_state, 0)
            done = (done,)

        # get the predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for i in range(len(done)):
            Q_new = reward[i]
            if not done[i]:
                # apply R + y(max Q(next_state))
                Q_new = reward[i] + self.gamma * T.max(self.model(next_state[i]))

            target[i][T.argmax(action[i]).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.loss(target, pred)
        loss.backward()

        self.optimizer.step()
