class BananaPrompt:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "medium_or_tech": ("STRING", {
                    "default": "",
                    "multiline": True,
                })
            },
            "optional": {
                "subject_or_identity": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
                "action_or_state": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
                "environment": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
                "final_style": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
                "others": ("STRING", {
                    "default": "",
                    "multiline": True,
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)

    FUNCTION = "make_banana_prompt"

    CATEGORY = "Banana Studio"

    def make_banana_prompt(self, medium_or_tech, subject_or_identity="", action_or_state="", environment="", final_style="", others=""):
        prompt = f"""
{"[Medium / Tech]" if subject_or_identity or action_or_state or environment or final_style or others else ""}
{medium_or_tech}

{"[Subject / Identity]" if subject_or_identity else ""}
{subject_or_identity}

{"[Action / State]" if action_or_state else ""}
{action_or_state}

{"[Environment]" if environment else ""}
{environment}

{"[Final Style]" if final_style else ""}
{final_style}

{"[Others]" if others else ""}
{others}
        """
        prompt = prompt.strip()
        print(prompt)
        return (prompt,)
