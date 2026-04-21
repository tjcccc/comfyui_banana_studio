import configparser
import random
from pathlib import Path
from typing import Tuple, Optional
import torch
from .image_service import prepare_images_for_api, get_image_from_base64_to_tensor
from .gemini_service import send_request_to_gemini, parse_gemini_response


CONFIG_FILE_PATH = Path(__file__).resolve().parent / "config.ini"


class BananaStudio:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "",
                }),
                "model": (["gemini-3.1-flash-image-preview", "gemini-3-pro-image-preview", "gemini-2.5-flash-image"], {
                    "default": "gemini-3-pro-image-preview",
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Hello, Banana Studio,",
                }),
                "batch_size": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 8,
                }),
                "aspect_ratio": (["Auto", "1:1", "9:16", "16:9", "3:4", "4:3", "3:2", "2:3", "5:4", "4:5", "21:9", "4:1", "1:4", "8:1", "1:8"], {
                    "default": "Auto",
                    "tooltip": "Only for gemini-3-pro-image-preview. 4:1, 1:4, 8:1, and 1:8 are only for gemini-3.1-flash-image-preview."
                }),
            },
            "optional": {
                "resolution": (["512", "1K", "2K", "4K"], {
                    "default": "1K",
                    "tooltip": "Only for gemini-3-pro-image-preview. 512 is only for gemini-3.1-flash-image-preview."
                }),
                "temperature": ("FLOAT", {
                    "default": 0.5,
                    "min": -1.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "The temperature range from 0 to 1. Set minus value to disable it.",
                }),
                "top_p": ("FLOAT", {
                    "default": 0.95,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "thinking_level": (["Minimal", "High"], {
                    "default": "Minimal",
                    "tooltip": "Only for gemini-3.1-flash-image-preview. It controls how much the model thinks before generating images. High thinking level may lead to better quality but longer generation time."
                }),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 102400,
                    "control_after_generate": True,
                }),
                "image_1": ("IMAGE", {}),
                "image_2": ("IMAGE", {}),
                "image_3": ("IMAGE", {}),
                "image_4": ("IMAGE", {}),
                "image_5": ("IMAGE", {}),
                "image_6": ("IMAGE", {}),
                "proxy": ("STRING", {
                    "default": "",
                }),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("images", "logs")

    FUNCTION = "generate_images"

    CATEGORY = "Banana Studio"

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        # Always re-execute when seed is random; otherwise let ComfyUI cache normally.
        if seed is None or seed < 0:
            return float("NaN")
        return seed


    @staticmethod
    def has_no_prompt_and_images(prompt: str, *images: Optional[torch.Tensor]) -> bool:
        prompt = prompt or ""
        if prompt and prompt.strip():
            return False
        return all(image is None for image in images)


    @staticmethod
    def get_api_key_from_config() -> str:
        if not CONFIG_FILE_PATH.exists():
            return ""

        parser = configparser.ConfigParser()
        parser.read(CONFIG_FILE_PATH, encoding="utf-8")

        default_key = parser.defaults().get("gemini_api_key", "").strip()
        if default_key:
            return default_key

        for section in parser.sections():
            api_key = parser.get(section, "GEMINI_API_KEY", fallback="").strip()
            if api_key:
                return api_key

        return ""


    @classmethod
    def resolve_api_key(cls, api_key: str) -> str:
        config_api_key = cls.get_api_key_from_config()
        if config_api_key:
            return config_api_key

        node_api_key = (api_key or "").strip()
        if node_api_key:
            return node_api_key

        raise ValueError(
            "[BananaStudio] Gemini API key is missing. Add GEMINI_API_KEY to config.ini "
            "or enter it in the node input."
        )


    def generate_single_image(
        self,
        api_key = "",
        model = "gemini-3-pro-image-preview",
        prompt: Optional[str] = None,
        aspect_ratio = "Auto",
        resolution = "1K",
        temperature:float = -1.0,
        top_p = 0.95,
        thinking_level = "Minimal",
        seed = -1,
        image_1: Optional[torch.Tensor] = None,
        image_2: Optional[torch.Tensor] = None,
        image_3: Optional[torch.Tensor] = None,
        image_4: Optional[torch.Tensor] = None,
        image_5: Optional[torch.Tensor] = None,
        image_6: Optional[torch.Tensor] = None,
        proxy: Optional[str] = None,
    ) -> Tuple[Optional[torch.Tensor], str]:
        resolved_api_key = self.resolve_api_key(api_key)
        encoded_inline_images = prepare_images_for_api(image_1, image_2, image_3, image_4, image_5, image_6)
        response_json = send_request_to_gemini(resolved_api_key, model, prompt, encoded_inline_images, aspect_ratio, resolution, temperature, top_p, thinking_level, seed, proxy)
        base64_images, text_output = parse_gemini_response(response_json)

        if not base64_images:
            raise ValueError(f"[BananaStudio] No images returned from {model} (likely blocked by safety policy). Response:\n{text_output}")

        image_tensors = [get_image_from_base64_to_tensor(base64_image) for base64_image in base64_images]

        return image_tensors[0], text_output


    def generate_images(
        self,
        api_key = "",
        model = "gemini-3-pro-image-preview",
        prompt: Optional[str] = None,
        batch_size = 1,
        aspect_ratio = "Auto",
        resolution = "1K",
        temperature = 0.5,
        top_p = 0.95,
        thinking_level = "Minimal",
        seed = -1,
        image_1: Optional[torch.Tensor] = None,
        image_2: Optional[torch.Tensor] = None,
        image_3: Optional[torch.Tensor] = None,
        image_4: Optional[torch.Tensor] = None,
        image_5: Optional[torch.Tensor] = None,
        image_6: Optional[torch.Tensor] = None,
        proxy: Optional[str] = None,
    ) -> Tuple[torch.Tensor, str]:
        if self.has_no_prompt_and_images(prompt, image_1, image_2, image_3, image_4, image_5, image_6):
            raise ValueError("[BananaStudio] No prompt or images provided.")
        if batch_size == 1:
            return self.generate_single_image(api_key, model, prompt, aspect_ratio, resolution, temperature, top_p, thinking_level, seed, image_1, image_2, image_3, image_4, image_5, image_6, proxy)

        if seed is None or seed < 0:
            base_seed = random.randint(1, 102400)
        else:
            base_seed = int(seed)

        all_images: list[torch.Tensor] = []
        last_log: str = ""

        for i in range(batch_size):
            current_seed = base_seed + i
            try:
                image_tensor, log_text = self.generate_single_image(api_key, model, prompt, aspect_ratio, resolution, temperature, top_p, thinking_level, current_seed, image_1, image_2, image_3, image_4, image_5, image_6, proxy)
                all_images.append(image_tensor)
                last_log = log_text
            except Exception as e:
                print(f"[BananaStudio] Batch item {i + 1}/{batch_size} failed: {e}")

        if not all_images:
            raise ValueError(f"[BananaStudio] All {batch_size} batch requests returned no images. Last response:\n{last_log}")

        batched_images = torch.cat(all_images, dim=0)

        final_log = (
            f"Generated {batched_images.shape[0]} image(s). "
            f"Last call log:\n{last_log}"
        )

        return batched_images, final_log
