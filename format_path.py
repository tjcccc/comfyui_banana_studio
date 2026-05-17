from __future__ import annotations

try:
    from .path_format import format_path
except ImportError:
    from path_format import format_path


class FormatPath:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path_template": (
                    "STRING",
                    {
                        "default": "%date:yyyy-MM-dd%/ComfyUI",
                        "tooltip": "Path template to format. Supports date tokens such as %date:yyyy-MM-dd%.",
                    },
                )
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_path",)

    FUNCTION = "run"

    CATEGORY = "Banana Studio"

    def run(self, path_template):
        return (format_path(path_template),)
