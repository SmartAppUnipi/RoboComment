import os
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def gcn(x):
    flat = x.view(x.size(0), 1, -1)
    mp = torch.mean(flat, dim=2)
    sp = torch.std(flat, dim=2) + 1e-7
    flat = (flat - mp.detach().unsqueeze(-1).expand_as(flat)) / sp.detach().unsqueeze(-1).expand_as(flat)
    return flat.view(x.shape[0], 1, 48, 48)


class DenseBlock(nn.Module):
    def __init__(self, input_channels, channels=8, n_layers=3, fs=3):
        super().__init__()

        in_channels = [i * channels + input_channels for i in range(n_layers)]

        layers = []
        for c in in_channels:
            layers.append(nn.Sequential(
                nn.Conv2d(c, channels, fs, padding=fs // 2),
                nn.ReLU(inplace=True),
            ))

        self.layers = nn.ModuleList(layers)

    def forward(self, x):
        features = x
        for layer in self.layers:
            new_features = layer(features)
            features = torch.cat((features, new_features), dim=1)

        return features


class DenseModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.convs = nn.Sequential(
            nn.Conv2d(1, 64, 5, stride=2, padding=2),
            nn.ReLU(inplace=True),
            DenseBlock(64, channels=16, n_layers=2),
            nn.MaxPool2d((2, 2)),
            DenseBlock(96, channels=16, n_layers=2),
            nn.MaxPool2d((2, 2)),
            nn.Conv2d(128, 12, 1),
            nn.ReLU(inplace=True)
        )
        self.fc = nn.Linear(12 * 6 * 6, 100)

    def forward(self, x):
        x = gcn(x)
        x = self.convs(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)