import torch
import torch.nn as nn
import copy
import os

class SiamNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SiamNet, self).__init__()
        channels, height, width = input_dim

        assert height == 32, f'Expected height 32. Input height {height}.'
        assert width == 32, f'Expected width 32. Input width {width}.'

        self.online = nn.Sequential(
            nn.Conv2d(in_channels=channels, out_channels=16, kernel_size=(5, 5), stride=(1, 1), padding=(2, 2)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=(5, 5), stride=(1, 1), padding=(0, 0)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(5, 5), stride=(1, 1), padding=(0, 0)),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(256, hidden_dim),
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

    def save(self, modeldir, filename, current_episode):
        if not os.path.exists(modeldir):
            os.makedirs(modeldir)

        torch.save(dict(model=self.state_dict(), current_episode=current_episode), f'{modeldir}/{filename}')
