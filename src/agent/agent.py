import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import random

if __name__ == 'agent.agent':
    from .model import SiamNet

class Siam:
    def __init__(self, state_dim, action_dim):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.use_cuda = torch.cuda.is_available()
        self.model = SiamNet(input_dim=self.state_dim, hidden_dim=512, output_dim=self.action_dim).double()

        if self.use_cuda:
            self.model = self.model.to(device='cuda')

        self.exploration_rate = 1
        self.exploration_rate_decay = 0.99999975
        self.exploration_rate_min = 0.1
        self.current_step = 0

        self.replay_buffer = deque(maxlen=int(1e5))
        self.batch_size = 32

        self.discount_rate = 0.9

        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.loss = nn.SmoothL1Loss()

        self.min_experience_before_training = self.batch_size * 10
        self.learn_every = 3
        self.sync_every = int(1e3)

    def act(self, state):
        if np.random.rand() < self.exploration_rate:
            action_value = np.random.randint(self.action_dim)
        else:
            state = torch.tensor(state.__array__()).cuda() if self.use_cuda else torch.tensor(state.__array__())
            state = torch.unsqueeze(state, 0)
            action_value = torch.argmax(self.model(state, model='online'), dim=1).item()

        self.exploration_rate = max(self.exploration_rate * self.exploration_rate_decay, self.exploration_rate_min)
        self.current_step = self.current_step + 1

        return action_value

    def cache(self, experience):
        state, next_state, action, reward, game_over = experience

        state = torch.tensor(state.__array__()).cuda() if self.use_cuda else torch.tensor(state.__array__())
        next_state = torch.tensor(next_state.__array__()).cuda() if self.use_cuda else torch.tensor(next_state.__array__())
        action = torch.tensor([action]).cuda() if self.use_cuda else torch.tensor([action])
        reward = torch.tensor([reward]).cuda() if self.use_cuda else torch.tensor([reward])
        game_over = torch.tensor([game_over]).cuda() if self.use_cuda else torch.tensor([game_over])

        self.replay_buffer.append((state, next_state, action, reward, game_over))

    def recall(self):
        batch = random.sample(self.replay_buffer, self.batch_size)
        states, next_states, actions, rewards, game_overs = map(torch.stack, zip(*batch))
        return states, next_states, actions.squeeze(), rewards.squeeze(), game_overs.squeeze()

    def compute_td_estimate(self, state, action):
        current_q_value = self.model(state, model='online')[np.arange(0, self.batch_size), action]
        return current_q_value

    @torch.no_grad()
    def compute_td_target(self, next_state, reward, game_over):
        next_action = torch.argmax(self.model(next_state, model='online'), dim=1)
        next_q_value = self.model(next_state, model='target')[np.arange(0, self.batch_size), next_action]
        return (reward + (1 - game_over.double()) * self.discount_rate * next_q_value).double()

    def update_q_online(self, td_estimate, td_target):
        loss = self.loss(td_estimate, td_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def sync_q_target(self):
        self.model.target.load_state_dict(self.model.online.state_dict())

    def learn(self):
        if self.current_step < self.min_experience_before_training:
            return None, None
        if self.current_step % self.learn_every != 0:
            return None, None
        if self.current_step % self.sync_every == 0:
            self.sync_q_target()

        states, next_states, actions, rewards, game_overs = self.recall()
        td_estimate = self.compute_td_estimate(states, actions)
        td_target = self.compute_td_target(next_states, rewards, game_overs)
        loss = self.update_q_online(td_estimate, td_target)

        return torch.mean(td_estimate).item(), loss
