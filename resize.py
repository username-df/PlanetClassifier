from PIL import Image

class ImgResize(object):
    def __call__(self, img: Image, output_size=(256,256)):
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
    
class PadToSquare:
    '''
    Function that adds padding to make sure all images are 256x256 after resizing
    '''
    def __call__(self, img: Image):

        width, height = img.size
 
        target_size = max(width, height)

        new_img = Image.new("RGB", (target_size, target_size), (0, 0, 0))
  
        x_offset = (target_size - width) // 2
        y_offset = (target_size - height) // 2
        
        new_img.paste(img, (x_offset, y_offset))
        
        return new_img
    