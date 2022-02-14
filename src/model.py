import torch
import torch.nn as nn
import copy
import os

class SiamNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SiamNet, self).__init__()
        height, width, channels = input_dim

        assert height == 84, f'Expected height 84. Input height {height}.'
        assert width == 84, f'Expected width 84. Input width {width}.'

        self.online = nn.Sequential(
            nn.Conv2d(in_channels=channels, out_channels=32, kernel_size=(8, 8), stride=(4, 4)),
            nn.ReLU(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(4, 4), stride=(2, 2)),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=(3, 3), stride=(1, 1)),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(3136, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
        self.target = copy.deepcopy(self.online)

        for parameter in self.target.parameters():
            parameter.requires_grad = False

    def forward(self, x, model):
        if model == 'online':
            return self.online(x)
        elif model == 'target':
            return self.target(x)

    def save(self, filename='model.pt'):
        if not os.path.exists('../models'):
            os.makedirs('../models')

        torch.save(self.state_dict(), f'../models/{filename}')
