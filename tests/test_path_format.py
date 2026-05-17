from datetime import datetime
from unittest import TestCase

from path_format import _format_date_pattern, format_path


class PathFormatTests(TestCase):
    def test_format_date_pattern_supports_existing_tokens(self):
        now = datetime(2026, 5, 7, 3, 4, 5, 678000)

        self.assertEqual(_format_date_pattern("yyyy-MM-dd/HHmmss-SSS-a", now), "2026-05-07/030405-678-AM")

    def test_format_path_expands_date_tokens(self):
        formatted = format_path("audio/%date:yyyy%/%date:MM-dd%/ComfyUI")

        self.assertTrue(formatted.startswith("audio/"))
        self.assertTrue(formatted.endswith("/ComfyUI"))
        self.assertNotIn("%date:", formatted)
