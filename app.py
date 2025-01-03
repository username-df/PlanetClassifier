import torch
import torchvision.transforms as transforms
from flask import Flask, render_template, request
from io import BytesIO
import base64
from PIL import Image
from convModel import model

app = Flask(__name__, template_folder="templates")
model.load()
class_names = ["Earth", "Jupiter", "Mars", "Mercury", "Neptune", "Saturn", "Uranus", "Venus"]

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
    
transform = transforms.Compose([
    ImgResize(),
    PadToSquare(),
    transforms.RandomRotation(36),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.26316062, 0.24574313, 0.24588147], 
                         std=[0.2500974, 0.23573072, 0.22842711])
])

@app.route('/')
def start():
    return render_template('webpage.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return 'File not found'

    file = request.files['image']

    if file.filename == '':
        return 'No Selected file'
    

    output = BytesIO()
    uploaded_img = Image.open(BytesIO(file.read()))
    uploaded_img = uploaded_img.convert('RGB')

    X = transform(uploaded_img)
    X = X.unsqueeze(0)

    model.eval()
    with torch.inference_mode():
        prd = model(X)
        result = f"The model has identified this image as {class_names[prd.argmax(dim=1)]}!"

    resizer = ImgResize()
    uploaded_img = resizer(img=uploaded_img, output_size=(500, 500))

    uploaded_img.save(output, format='JPEG')
    uploaded_img = (base64.b64encode(output.getvalue())).decode('utf-8')
    output.seek(0)

    return render_template('uploadpage.html', uploaded_img=uploaded_img, result=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)