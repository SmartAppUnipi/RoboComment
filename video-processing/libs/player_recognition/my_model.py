import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from tqdm import tqdm

"""        self.convs = nn.Sequential(
            # 48
            nn.Conv2d(3, 64, 5),
            nn.ReLU(),
            # 44
            nn.Conv2d(64, 128, 3, padding=1, stride=2),
            nn.ReLU(),
            # 22
            nn.Conv2d(128, 128, 3, padding=1),
            nn.ReLU(),
            # 22
            nn.Conv2d(128, 128, 3, padding=1, stride=2),
            nn.ReLU(),
            # 11
            nn.Conv2d(128, 64, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 16, 3),
            nn.ReLU()
        )
        self.fc1 = nn.Linear(16 * 9 * 9, 512)
        self.fc2 = nn.Linear(512, 100)
"""


def gcn(x):
    flat = x.view(x.size(0), 3, -1)
    mp = torch.mean(flat, dim=2)
    sp = torch.std(flat, dim=2) + 1e-7
    flat = (flat - mp.detach().unsqueeze(-1).expand_as(flat)) / sp.detach().unsqueeze(-1).expand_as(flat)
    return flat.view(x.shape[0], 3, 48, 48)


class ModelEff(nn.Module):
    def __init__(self):
        super().__init__()
        self.convs = nn.Sequential(
            nn.Conv2d(3, 64, 5, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3),
            nn.ReLU(),
            nn.Conv2d(64, 128, 3, padding=1, stride=2),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1, stride=2),
            nn.ReLU(),
            nn.Conv2d(128, 64, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 16, 3),
            nn.ReLU()
        )
        self.fc1 = nn.Linear(16 * 9 * 9, 512)
        self.fc2 = nn.Linear(512, 100)

    def forward(self, x):
        x = gcn(x)
        x = self.convs(x)
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        return self.fc2(x)
