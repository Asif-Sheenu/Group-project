from PIL import Image
import imagehash

def generate_image_hash(image_path):
    image=Image.open(image_path)
    image_hash=imagehash.average_hash(image)
    return str(image_hash)