from __future__ import annotations

import re
from datetime import datetime

from comfy_api.latest import IO, UI


_DATE_PATTERN = re.compile(r"%date:([^%]+)%")


def _format_date_pattern(pattern: str, now: datetime | None = None) -> str:
    now = now or datetime.now()
    replacements = {
        "yyyy": f"{now.year:04d}",
        "yy": f"{now.year % 100:02d}",
        "MM": f"{now.month:02d}",
        "M": str(now.month),
        "dd": f"{now.day:02d}",
        "d": str(now.day),
        "HH": f"{now.hour:02d}",
        "H": str(now.hour),
        "hh": f"{(now.hour % 12) or 12:02d}",
        "h": str((now.hour % 12) or 12),
        "mm": f"{now.minute:02d}",
        "m": str(now.minute),
        "ss": f"{now.second:02d}",
        "s": str(now.second),
        "SSS": f"{now.microsecond // 1000:03d}",
        "a": "AM" if now.hour < 12 else "PM",
    }

    output = []
    index = 0
    tokens = sorted(replacements, key=len, reverse=True)
    while index < len(pattern):
        for token in tokens:
            if pattern.startswith(token, index):
                output.append(replacements[token])
                index += len(token)
                break
        else:
            output.append(pattern[index])
            index += 1

    return "".join(output)


def expand_date_tokens(filename_prefix: str) -> str:
    return _DATE_PATTERN.sub(lambda match: _format_date_pattern(match.group(1)), filename_prefix)


class SaveAudioMP3Plus(IO.ComfyNode):
    @classmethod
    def define_schema(cls):
        return IO.Schema(
            node_id="SaveAudioMP3Plus",
            search_aliases=["export mp3", "save audio date"],
            display_name="Save Audio + (MP3)",
            category="audio",
            essentials_category="Audio",
            inputs=[
                IO.Audio.Input("audio"),
                IO.String.Input(
                    "filename_prefix",
                    default="audio/%date:yyyy-MM-dd%/ComfyUI",
                    tooltip="The prefix for the file to save. Supports date formatting such as %date:yyyy-MM-dd%.",
                ),
                IO.Combo.Input("quality", options=["V0", "128k", "320k"], default="V0"),
            ],
            hidden=[IO.Hidden.prompt, IO.Hidden.extra_pnginfo],
            is_output_node=True,
        )

    @classmethod
    def execute(cls, audio, filename_prefix="ComfyUI", format="mp3", quality="128k") -> IO.NodeOutput:
        filename_prefix = expand_date_tokens(filename_prefix)
        return IO.NodeOutput(
            ui=UI.AudioSaveHelper.get_save_audio_ui(
                audio, filename_prefix=filename_prefix, cls=cls, format=format, quality=quality
            )
        )

    save_mp3 = execute  # TODO: remove
