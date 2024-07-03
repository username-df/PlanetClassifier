import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from PIL import Image
from sklearn.model_selection import train_test_split

class ImgResize(object):
    def __call__(self, img: Image, output_size=(256,256)):
        image = img

        original_width, original_height = image.size
        aspect_ratio = original_width / original_height

        target_width, target_height = output_size
        if target_width / target_height > aspect_ratio:
            target_width = int(target_height * aspect_ratio)
        else:
            target_height = int(target_width / aspect_ratio)

        # Resize the image
        resized_image = image.resize((target_width, target_height), Image.LANCZOS)

        return resized_image
    
class PadToSquare:
    def __call__(self, img: Image):

        width, height = img.size
 
        target_size = max(width, height)

        new_img = Image.new("RGB", (target_size, target_size), (0, 0, 0))
  
        x_offset = (target_size - width) // 2
        y_offset = (target_size - height) // 2
        
        new_img.paste(img, (x_offset, y_offset))
        
        return new_img

BATCH_SIZE = 32

transform = transforms.Compose([
    ImgResize(),
    PadToSquare(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.2876, 0.2803, 0.2868], 
                         std=[0.2492, 0.2377, 0.2370])
])
    

dataset = ImageFolder("ImageData", transform=transform)

temp, test_set = train_test_split(dataset, test_size=0.2, random_state=0)
train_set, val_set = train_test_split(temp, test_size=0.25, random_state=0)

train_data = DataLoader(dataset=train_set,
                        batch_size=BATCH_SIZE,
                        shuffle=True)

val_data = DataLoader(dataset=val_set,
                        batch_size=BATCH_SIZE,
                        shuffle=False)

test_data = DataLoader(dataset=test_set,
                            batch_size=BATCH_SIZE,
                            shuffle=False)