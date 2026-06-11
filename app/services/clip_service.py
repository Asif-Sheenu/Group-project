from transformers import CLIPModel,CLIPProcessor
from PIL import Image
import torch
from sklearn.metrics.pairwise import cosine_similarity
# load model
model= CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
)

processor= CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

def generate_clip_embedding(image_path):
    # open img
    image= Image.open(image_path)
# prep img for model
    inputs=processor(images=image,return_tensors='pt')

    # generate embbding

    with torch.no_grad():
        image_features= model.get_image_features(**inputs)

    return image_features[0].cpu().numpy().tolist()


def compare_embeddings(
    embedding1,
    embedding2
):

    similarity = cosine_similarity(
        [embedding1],
        [embedding2]
    )

    return similarity[0][0]