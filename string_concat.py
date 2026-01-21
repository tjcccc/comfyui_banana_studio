import codecs


class StringConcat:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string_a": ("STRING", {
                    "default": "",
                })
            },
            "optional": {
                "string_b": ("STRING", {
                    "default": "",
                }),
                "separator": ("STRING", {
                    "default": "\n\n",
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("a + b",)

    FUNCTION = "concat_strings"

    CATEGORY = "Banana Studio"


    def _maybe_unescape(self, s: str) -> str:
        s = s or ""
        if "\\" in s and all(ord(c) < 128 for c in s):
            try:
                return codecs.decode(s, "unicode_escape")
            except Exception:
                return s
        return s


    def concat_strings(self, string_a, string_b, separator):
        a = self._maybe_unescape(string_a)
        sep = self._maybe_unescape(separator)
        # decoded_a = codecs.decode(string_a or "", "unicode_escape")
        # decoded_b = codecs.decode(string_b or "", "unicode_escape")
        # decoded_seperator = codecs.decode(separator or "", "unicode_escape")
        if string_b is None:
            return (a,)
        b = self._maybe_unescape(string_b)
        # print(decoded_a + decoded_seperator + decoded_b)
        return (a + sep + b,)
