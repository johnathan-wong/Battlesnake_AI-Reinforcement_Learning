import torch
import torch.nn as nn
import torch.nn.functional as F

class SnakeNet(nn.Module):
    def __init__(self, grid_channels=6, grid_size=11, stats_size=17, num_actions=4):
        super().__init__()

        # --- CNN branch (grid input) ---
        self.conv = nn.Sequential(
            nn.Conv2d(grid_channels, 16, kernel_size=3, stride=1, padding=1),  # (16, H, W)
            nn.ReLU(),
            nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1),             # (32, H, W)
            nn.ReLU(),
            nn.Flatten()
        )

        # compute flattened size dynamically
        dummy_grid = torch.zeros(1, grid_channels, grid_size, grid_size)
        conv_out_size = self.conv(dummy_grid).shape[1]

        # --- MLP branch (stats input) ---
        self.mlp_stats = nn.Sequential(
            nn.Linear(stats_size, 64),
            nn.ReLU()
        )

        # --- Combined head ---
        self.fc = nn.Sequential(
            nn.Linear(conv_out_size + 64, 128),
            nn.ReLU(),
            nn.Linear(128, num_actions)  # logits for actions
        )

    def forward(self, obs):
        # obs is a dict: {"grid": tensor, "stats": tensor}
        grid = obs["grid"].float()   # shape (B, C, H, W)
        stats = obs["stats"].float() # shape (B, stats_size)

        grid_feat = self.conv(grid)
        stats_feat = self.mlp_stats(stats)

        combined = torch.cat([grid_feat, stats_feat], dim=1)
        logits = self.fc(combined)

        return logits
