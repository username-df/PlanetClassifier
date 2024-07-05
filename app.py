import os
import torch
from flask import Flask, render_template, request,  url_for
from io import BytesIO
import base64
from PIL import Image
from convModel import model
from create_dataset import transform, ImgResize

app = Flask(__name__)
model.load()
class_names = ["Earth", "Jupiter", "Mars", "Mercury", "Neptune", "Saturn", "Uranus", "Venus"]

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
    app.run()