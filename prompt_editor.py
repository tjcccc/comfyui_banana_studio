from .prompt_parse_service import remove_comments, get_variables, get_raw_prompt, get_prompt_output

class PromptEditor:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_code": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "The main prompt text to be edited."
                })
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)

    FUNCTION = "parse_prompt"

    CATEGORY = "Banana Studio"


    def parse_prompt(self, prompt_code):
        cleaned_prompt = remove_comments(prompt_code)
        variables = get_variables(cleaned_prompt)
        raw_prompt = get_raw_prompt(cleaned_prompt)
        parsed_prompt = get_prompt_output(raw_prompt, variables)
        return (parsed_prompt,)
