import torch
from torch import nn
import os

class convModel(nn.Module):
    def __init__(self, input, hidden, output):
        super().__init__()

        self.convblock1 = nn.Sequential(
            nn.Conv2d(in_channels=input,
                    out_channels=hidden,
                    kernel_size=3, 
                    stride=2,
                    padding=1),
            nn.ReLU(),

            nn.Conv2d(in_channels=hidden,
                    out_channels=hidden,
                    kernel_size=3,
                    stride=1,
                    padding=1),
            nn.ReLU(),

            nn.MaxPool2d(kernel_size=3),
            nn.BatchNorm2d(hidden)
        )

        self.convblock2 = nn.Sequential(
            nn.Conv2d(in_channels=hidden,
                    out_channels=hidden,
                    kernel_size=3,
                    stride=1,
                    padding=1),

            nn.ReLU(),
            nn.Conv2d(in_channels=hidden,
                    out_channels=hidden,
                    kernel_size=3,
                    stride=1,
                    padding=1),

            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3),
            nn.BatchNorm2d(hidden)
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(hidden*14*14, output)
        )
    
    def forward(self, x):
        x = self.convblock1(x)
        x = self.convblock2(x)
        x = self.classifier(x)
        return x
    
    def save(self, file_name='saved.pth'):
        model_folder_path = './model'

        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        
        torch.save({
            'model_state_dict': self.state_dict(), 
            }, file_name)

    def load(self, file_name='saved.pth'):
        model_folder_path = './model'
        file_path = os.path.join(model_folder_path, file_name)

        if os.path.exists(file_path):
            load_model = torch.load(file_path)

            self.load_state_dict(load_model['model_state_dict'])
            
        else:
            print("No saved model found")

torch.manual_seed(0)
model = convModel(3, 24, 8)

LR = 0.00005
optimizer = torch.optim.Adam(params=model.parameters(), lr=LR)
lossfn = nn.CrossEntropyLoss()