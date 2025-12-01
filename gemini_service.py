import os
import json
from typing import Optional, List, Dict, Any
import requests
from PIL import Image


GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
models = ["gemini-2.5-flash-image", "gemini-3-pro-image-preview"]


def send_request_to_gemini(
    api_key: str,
    model: str,
    prompt: str,
    encoded_inline_images: Optional[List[dict]] = None,
    aspect_ratio: str = "Auto",
    resolution: str = "1K",
    temperature: float = 0.5,
    top_p: float = 0.95,
    seed: int = -1,
    proxy: Optional[str] = None,
) -> Dict[str, Any]:
    if model not in models:
        raise ValueError(f"{model} is not a valid model")

    api_url = GEMINI_ENDPOINT.format(model=model)

    parts: List[Dict[str, Any]] = []

    if prompt:
        parts.append({"text": prompt.strip()})

    if encoded_inline_images:
        for encoded_inline_image in encoded_inline_images:
            if not encoded_inline_image:
                continue
            parts.append({
                "inlineData": encoded_inline_image
            })

    generation_config: Dict[str, Any] = {
        "topP": float(top_p),
        "responseModalities": ["TEXT", "IMAGE"],
    }

    if temperature >= 0:
        generation_config.update({
            "temperature": float(temperature),
        })

    if seed >= 0:
        generation_config["seed"] = seed

    # TODO: Thinking?

    image_config: Dict[str, str] = {}

    if aspect_ratio != "Auto":
        image_config.update({
            "aspectRatio": aspect_ratio
        })

    if model == "gemini-3-pro-image-preview":
        image_config.update({
            "imageSize": resolution
        })

    if image_config:
        generation_config["image_config"] = image_config

    body = {
        "contents": [
            {
                "role": "user",
                "parts": parts,
            }
        ],
        "generationConfig": generation_config,
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }

    proxies = None
    if proxy and proxy.strip():
        proxies = {
            "http": proxy,
            "https": proxy,
        }

    response = requests.post(api_url, headers=headers, json=body, timeout=180, proxies=proxies)
    response.raise_for_status()
    return response.json()


def parse_gemini_response(response_json):
    images = []
    texts = []

    for candidate in response_json.get("candidates", []):
        parts = candidate.get("content", {}).get("parts", [])
        for part in parts:
            if "text" in part:
                texts.append(part["text"])
            if "inlineData" in part:
                images.append(part["inlineData"]["data"])

    formated_texts = "\n".join(texts)

    return images, formated_texts
