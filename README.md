# Banana Studio for ComfyUI

Banana Studio is a ComfyUI custom node pack centered on Gemini image generation plus a small set of prompt-building and workflow utility nodes.

## Included Nodes

- `Banana Studio`: generate images with Gemini image models, with optional image inputs and batch support
- `Banana Prompt`: build a structured prompt from named sections
- `Z-Image Prompt`: build an image prompt with framing, subject, lighting, style, and constraints sections
- `Prompt Editor`: expand prompt variables and strip inline comments
- `String Concat`: join strings with an optional separator
- `Single Parameter Dispatcher`: emit per-batch values for parameter sweeps
- `Save Audio + (MP3)`: save generated audio as MP3 with `%date:...%` filename formatting

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

## Node Usage

### `Banana Studio`

Use this as the main Gemini image generation node.

- Set `prompt` to your text instruction.
- Set `model` to the Gemini image model you want to use.
- Set `batch_size` to generate multiple images in one run.
- Connect up to 6 optional `IMAGE` inputs when you want image-conditioned generation or reference images.
- Use `aspect_ratio` and `resolution` to control the output format.
- Use `temperature`, `top_p`, `thinking_level`, and `seed` when you want more control over sampling behavior.
- Leave `api_key` empty if you already configured `config.ini`.
- Set `proxy` only when you really need it. Large inline image uploads are more likely to fail through unstable proxies.

Outputs:

- `images`: generated image tensor output for downstream image nodes
- `logs`: text summary with generation status and token usage

Typical use:

1. Build a prompt directly or with `Banana Prompt`.
2. Connect that string to `Banana Studio`.
3. Optionally connect one or more input images.
4. Feed the returned `images` into preview, save, or post-processing nodes.

### `Banana Prompt`

Use this when you want a structured cinematic prompt assembled from labeled sections.

- `medium_or_tech` is the main required field. Use it for medium, camera, lens, and composition context.
- Fill optional sections such as `identify_reference`, `subject_or_presence`, `action_or_state`, `environment`, `clothing_body`, and `final_style` only when needed.
- If only `medium_or_tech` is filled, the node returns that value directly.
- If any optional section is filled, the node formats all non-empty sections into a readable multi-section prompt.

Output:

- `prompt`: the assembled text prompt string

Good fit:

- character consistency workflows
- portrait, fashion, editorial, and cinematic prompt writing
- reusable prompt blocks where each section has a clear role

### `Z-Image Prompt`

Use this when you want a separate structured image-prompt helper based on framing, subject, scene, lighting, and constraints.

- `composition_or_framing` is required and usually defines the shot first.
- Add `subject_or_identity`, `wardrobe_or_appearance`, `environment_or_scene`, `lighting`, `mood_or_style_or_quality`, and `constraints` as needed.
- The `constraints` field is useful for hard requirements like `no text`, `no watermark`, or `photorealistic`.
- If only the required field is filled, the node returns it directly.
- Otherwise it builds a bracketed multi-section prompt.

Output:

- `prompt`: the assembled text prompt string

Good fit:

- image prompting with explicit framing and lighting control
- prompts that need hard exclusions or quality constraints
- workflows outside the Banana Studio node

### `Prompt Editor`

Use this to turn prompt code into a final prompt string.

- Put your editable prompt source into `prompt_code`.
- The parser removes comments, extracts variables, resolves substitutions, and returns the final prompt text.
- This is useful when you want prompt templates instead of manually rewriting full prompts each time.

Output:

- `prompt`: the parsed final prompt string

Good fit:

- reusable prompt templates
- variable-driven prompt authoring
- prompt text that should stay maintainable over time

Example:

```text
# Variables
character = cinematic portrait of a young woman
location = neon street at night
style = soft rim light, shallow depth of field, highly detailed

# Prompt body
prompt = {
A realistatic photo.
{character}. She is in a {location}.
{style}.
}
```

Expected output:

```text
A realistatic photo.
cinematic portrait of a young woman. She is in a neon street at night.
soft rim light, shallow depth of field, highly detailed.
```

### `String Concat`

Use this to merge two text blocks before sending them into prompt-consuming nodes.

- `string_a` is required.
- `string_b` is optional.
- `separator` defaults to a blank line.
- Escape sequences such as `\n` are decoded when the input is plain ASCII text, so you can type separators like `\n`, `\n\n`, or `, ` directly.

Output:

- `a + b`: the merged string

Good fit:

- joining a base prompt and a style suffix
- appending reusable negative or constraint text
- building prompts from smaller blocks

### `Single Parameter Dispatcher`

Use this for simple batch-time parameter sweeps.

- `value` is the starting value.
- `delta` is the amount added for each next item.
- `max_value` clamps the sequence when increasing or decreasing.
- `batch` sets the total queue length.
- `reset_mark` forces the sequence to rebuild when changed.
- `output_tag_format` lets you generate a label string using placeholders:
  `%current_value%`, `%index%`, `%delta%`, `%max%`, `%batch%`

Outputs:

- `dispatch_value`: current numeric value for the current batch item
- `index`: 1-based position in the batch
- `output_tag`: formatted text tag using the placeholders above
- `log`: debug text for the current dispatched value

Good fit:

- varying guidance-like numeric inputs across queued runs
- generating per-image labels for save paths or metadata
- simple sweep workflows without a larger parameter system

### `Save Audio + (MP3)`

Use this like ComfyUI's built-in `Save Audio (MP3)` node when you want date-formatted audio output paths.

- `filename_prefix` supports custom date tokens such as `%date:yyyy-MM-dd%`, `%date:yyyyMMdd-HHmmss%`, and `%date:yyyy/MM/dd/ComfyUI%`.
- `quality` matches the built-in MP3 options: `V0`, `128k`, and `320k`.

## Notes

- If you use a proxy, upload timeouts can happen before Gemini returns a response, especially when sending large inline image payloads.
- The repository keeps `config.ini` git-ignored so local keys do not end up in commits.
- `banana_studio.py` resolves the API key before making the Gemini request, so saved workflows no longer need to store the real key when `config.ini` is present.

## Development

Relevant local validation for this repository:

```bash
python3 -m py_compile banana_studio.py gemini_service.py __init__.py
```

## Publish

To publish this node to the Comfy Registry manually:

```bash
pip install comfy-cli
comfy node publish
```

You will need a Registry publishing API key for publisher `tjcccc`.

This repository also includes [publish_action.yml](./.github/workflows/publish_action.yml). To enable automatic publishing on version bumps:

1. Create a repository secret named `REGISTRY_ACCESS_TOKEN`.
2. Put your Comfy Registry publishing API key in that secret.
3. Bump `version` in `pyproject.toml` and push to `main`.

## Version

Current project version: `0.6.0`
