import hashlib
import os
import random
import time
from diffusers import StableDiffusionPipeline
import torch

model_id = "sd-legacy/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
pipe = pipe.to("cpu")


def create_img_name() -> str:
    unique_data = f"{time.time()}{os.getpid()}{random.random()}".encode('utf-8')
    unique_hash = hashlib.md5(unique_data).hexdigest()
    return unique_hash


def create_image(prompt: str) -> str:
    image = pipe(prompt).images[0]
    img_name = f"{create_img_name()}.png"
    image.save(img_name)
    return img_name
