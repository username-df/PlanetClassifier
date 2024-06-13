from PIL import Image

def resize(img: Image, output_size):
    '''
    Function that resizes the image to the correct size while
    keeping the original aspect ratio.
    '''
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

class ImgResize(object):
    '''
    Creating class so that resize can be used with transforms.Compose
    '''
    def __init__(self, output_size):
        self.output_size = output_size

    def __call__(self, image):
        return resize(image, self.output_size)