import copy
import time
from typing import Optional, List, Dict, Any
import requests


GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
models = ["gemini-2.5-flash-image", "gemini-3-pro-image-preview"]


def strip_useless_data(obj):
    """
    Recursively remove base64 image data and thoughtSignature data from Gemini response JSON.
    Keeps inlineData.mimeType but clears inlineData.data.
    """
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            if k == "inlineData":
                # Keep mimeType but drop base64 data
                new_obj["inlineData"] = {
                    "mimeType": v.get("mimeType", "")
                }
            elif k == "thoughtSignature":
                new_obj["thoughtSignature"] = "(removed)"
            else:
                new_obj[k] = strip_useless_data(v)
        return new_obj

    if isinstance(obj, list):
        return [strip_useless_data(x) for x in obj]

    return obj


def save_json_debug(data, prefix="gemini"):
    import json, os, time

    log_dir = os.path.dirname(__file__)
    os.makedirs(log_dir, exist_ok=True)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{prefix}_{timestamp}.json"

    path = os.path.join(log_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[BananaStudio] Saved JSON: {path}")



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
    max_retries = 5
    delay = 2.0

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

    for attempt in range(max_retries):
        response = requests.post(api_url, headers=headers, json=body, timeout=(10, 90), proxies=proxies)
        if response.status_code == 503:
            print(f"Gemini 503, maybe model overloaded, retry {attempt + 1} / {max_retries}...")
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay = min(delay * 2, 20)
                continue
        if not response.ok:
            print("Gemini error response:", response.text)
            response.raise_for_status()

        # debug
        clean_json = copy.deepcopy(response.json())
        clean_json = strip_useless_data(clean_json)
        save_json_debug(clean_json)

        return response.json()

    return {}


def parse_gemini_response(response_json):
    images = []
    texts = []

    candidates = response_json.get("candidates", [])

    for candidate in candidates:
        parts = candidate.get("content", {}).get("parts", [])
        for part in parts:
            text_content = part.get("text")
            if isinstance(text_content, str):
                texts.append(text_content)
            if "inlineData" in part:
                images.append(part["inlineData"]["data"])

    lines = []

    if images:
        lines.append("Image(s) generated successfully.")
    else:
        lines.append("No images return from Gemini.")

    usage = response_json.get("usageMetadata", {})
    if usage:
        prompt_token_count = usage.get("promptTokenCount")
        candidates_token_count = usage.get("candidatesTokenCount")
        thoughts_token_count = usage.get("thoughtsTokenCount")
        total_token_count = usage.get("totalTokenCount")

        tokens_lines = []
        if prompt_token_count is not None:
            tokens_lines.append(f"- prompt token: {prompt_token_count}")
        if candidates_token_count is not None:
            tokens_lines.append(f"- candidates token: {candidates_token_count}")
        if thoughts_token_count is not None:
            tokens_lines.append(f"- thoughts token: {thoughts_token_count}")
        if total_token_count is not None:
            tokens_lines.append(f"- total tokens: {total_token_count}")

        if tokens_lines:
            tokens_lines_str = "\n".join(tokens_lines)
            lines.append(f"Tokens count:\n{tokens_lines_str}")

    formatted_texts = "\n".join(lines)
    return images, formatted_texts


