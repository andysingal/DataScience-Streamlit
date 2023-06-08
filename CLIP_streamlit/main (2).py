import io
import streamlit as st
import numpy as np
import pandas as pd
import torch
from PIL import Image
import requests

from transformers import CLIPProcessor, CLIPModel
from tqdm.auto import tqdm

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
TEXT_EMBED_URL = "https://www.dropbox.com/s/5gvkjyjkolehnn9/text_embeds.npy?dl=1"
CAPTION_URL = "https://www.dropbox.com/s/n6s30qh1ldycko7/url2caption.csv?dl=1"
DEFAULT_IMAGE = "https://carsguide-res.cloudinary.com/image/upload/f_auto%2Cfl_lossy%2Cq_auto%2Ct_default/v1/editorial/jaguar-xf-rosebaylac-2.jpg"


@st.cache(hash_funcs={CLIPModel: lambda _: None, CLIPProcessor: lambda _: None})
def load_model():
    # wget csv file with captions
    captions = pd.read_csv(CAPTION_URL)
    # wget text embeddings of above
    response = requests.get(TEXT_EMBED_URL)
    text_embeddings = torch.FloatTensor(np.load(io.BytesIO(response.content)))
    # huggingface model and processor
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32", from_tf=False).eval()
    for p in model.parameters():
        p.requires_grad = False
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    return model, processor, captions, text_embeddings


def get_image(url, model, processor):
    image = Image.open(requests.get(url, stream=True).raw)
    image_inputs = processor(images=image, return_tensors="pt",)
    image_inputs = {k: v.to(device) for k, v in image_inputs.items()}

    img_features = model.get_image_features(
        pixel_values=image_inputs["pixel_values"],
        output_attentions=False,
        output_hidden_states=False,
    )

    img_len = torch.sqrt((img_features ** 2).sum(dim=-1, keepdims=True))
    img_features = img_features / img_len
    return image, img_features


def get_best_captions(img_features, text_features, captions):
    similarity = img_features @ text_features.T
    img2text_similarity = similarity.softmax(dim=-1)
    _, idx = img2text_similarity.topk(dim=-1, k=5)

    st.write("## The closes captions are:")
    for caption in captions.loc[idx.cpu().numpy().ravel(), "caption"].values:
        st.write(caption)


model, processor, captions, text_embeddings = load_model()
st.header("Prototyping CLIP")
url = st.text_input("Insert url of image", value=DEFAULT_IMAGE)
image, img_features = get_image(url, model, processor)
st.image(image)

get_best_captions(img_features, text_embeddings, captions)

st.write("## Shameless self promotion")
st.write("If you enjoyed the tutorial buy me a coffee, or better yet [buy my course](https://www.udemy.com/course/machine-learning-and-data-science-2021/?referralCode=E79228C7436D74315787) (usually 90% off).")
