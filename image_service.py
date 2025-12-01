import io
import base64
from typing import List, Optional
import torch
import numpy as np
from PIL import Image


def tensor_to_pil_image(tensor: torch.Tensor) -> Image.Image:
    t = tensor.detach().cpu()
    if t.ndim == 4:
        if t.shape[0] == 0:
            raise ValueError("Empty image batch.")
        t = t[0]
    np_image = (t.numpy() * 255).clip(0, 255).astype("uint8")
    if np_image.shape[-1] == 4:
        np_image = np_image[..., :3]
    return Image.fromarray(np_image, mode="RGB")


def pil_to_google_inline_data(pil: Image.Image):
    buffer = io.BytesIO()
    pil.save(buffer, format='PNG')
    data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return {
        "mimeType": "image/png",
        "data": data,
    }


def prepare_images_for_api(*images: Optional[torch.Tensor]) -> List[dict]:
    encoded_images: List[dict] = []
    for image in images:
        if image is None:
            continue
        if isinstance(image, torch.Tensor):
            pil_image = tensor_to_pil_image(image)
            encoded_images.append(pil_to_google_inline_data(pil_image))
    return encoded_images


def get_image_from_base64_to_tensor(base64_image: str) -> torch.Tensor:
    image_bytes = base64.b64decode(base64_image)
    pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    np_image = np.array(pil_image).astype(np.float32) / 255.0
    tensor = torch.from_numpy(np_image)[None, ...]
    return tensor
