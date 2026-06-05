from PIL import Image
import imagehash

def generate_image_hash(image_path):
    image=Image.open(image_path)
    image_hash=imagehash.average_hash(image)
    return str(image_hash)

def is_duplicate_image(new_hash,old_hash):
    hash_difference=(
        imagehash.hex_to_hash(new_hash)
        -
        imagehash.hex_to_hash(old_hash)
    )

    return hash_difference < 5