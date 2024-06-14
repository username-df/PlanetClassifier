import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from PIL import Image
from resize import ImgResize, PadToSquare
import numpy
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

BATCH_SIZE = 32

transform = transforms.Compose([
    ImgResize(),
    PadToSquare(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.29179502, 0.27263689, 0.27018078], 
                         std=[0.32638136, 0.30372527, 0.31044443])
    ])

dataset = ImageFolder("ImageData", transform=transform)
train_set, test_set = train_test_split(dataset, test_size=0.2, random_state=0)

train_data = DataLoader(dataset=train_set,
                        batch_size=BATCH_SIZE,
                        shuffle=True)

test_data = DataLoader(dataset=test_set,
                            batch_size=BATCH_SIZE,
                            shuffle=False)
