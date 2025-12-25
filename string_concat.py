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


    def concat_strings(self, string_a, string_b, separator):
        decoded_a = codecs.decode(string_a or "", "unicode_escape")
        decoded_b = codecs.decode(string_b or "", "unicode_escape")
        decoded_seperator = codecs.decode(separator or "", "unicode_escape")
        if string_b is None:
            return (string_a,)
        # print(decoded_a + decoded_seperator + decoded_b)
        return (decoded_a + decoded_seperator + decoded_b,)
