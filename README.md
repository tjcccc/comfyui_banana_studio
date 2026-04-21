# Banana Studio for ComfyUI

Banana Studio is a ComfyUI custom node pack centered on Gemini image generation plus a small set of prompt-building and workflow utility nodes.

## Included Nodes

- `Banana Studio`: generate images with Gemini image models, with optional image inputs and batch support
- `Banana Prompt`: build a structured prompt from named sections
- `Z-Image Prompt`: build an image prompt with framing, subject, lighting, style, and constraints sections
- `Prompt Editor`: expand prompt variables and strip inline comments
- `String Concat`: join strings with an optional separator
- `Single Parameter Dispatcher`: emit per-batch values for parameter sweeps

## Installation

Clone this repository into `ComfyUI/custom_nodes`:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/tjcccc/comfyui_banana_studio.git
```

Restart ComfyUI after installation.

## Gemini API Key

Create a local `config.ini` file in the repository root:

```ini
[auth]
GEMINI_API_KEY = your_gemini_api_key_here
```

You can copy [`config.ini.example`](./config.ini.example) to `config.ini` and replace the placeholder value.

API key resolution order in the `Banana Studio` node:

1. `config.ini`
2. The node `api_key` input
3. Raise an error if neither is set

The `api_key` input remains available for temporary local testing, but `config.ini` takes priority when both are present.

## Main Node Inputs

The `Banana Studio` node supports:

- Gemini image models:
  `gemini-3.1-flash-image-preview`, `gemini-3-pro-image-preview`, `gemini-2.5-flash-image`
- text prompt input
- optional image inputs for image-conditioned generation
- batch generation
- aspect ratio, resolution, temperature, `top_p`, thinking level, seed, and proxy controls

## Notes

- If you use a proxy, upload timeouts can happen before Gemini returns a response, especially when sending large inline image payloads.
- The repository keeps `config.ini` git-ignored so local keys do not end up in commits.
- `banana_studio.py` resolves the API key before making the Gemini request, so saved workflows no longer need to store the real key when `config.ini` is present.

## Development

Relevant local validation for this repository:

```bash
python3 -m py_compile banana_studio.py gemini_service.py __init__.py
```

## Version

Current project version: `0.6.0`
