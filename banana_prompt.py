class BananaPrompt:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "medium_or_tech": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Medium / Tech\nCamera, lens, medium, composition container."
                })
            },
            "optional": {
                "subject_or_identity": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Subject / Identity\nWho the subject is; identity and consistency."
                }),
                "action_or_state": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Action / State\nWhat the subject is doing or current state."
                }),
                "environment": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Environment\nLocation, time, lighting, surrounding world."
                }),
                "clothing_body": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Clothing / Body\nWhat the subject wears and how the body is presented."
                }),
                "final_style": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Final Style\nMood / aesthetic, applied last. Keep it soft."
                })
            },
        }


    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)

    FUNCTION = "make_banana_prompt"

    CATEGORY = "Banana Studio"


    def make_banana_prompt(self, medium_or_tech, subject_or_identity="", action_or_state="", environment="", clothing_body="", final_style=""):

        has_multiple_sections = any(
            s.strip()
            for s in (
                subject_or_identity,
                action_or_state,
                environment,
                clothing_body,
                final_style,
            )
        )
        if not has_multiple_sections:
            return (medium_or_tech,)

        def add_section(sections: list[str], title: str, body: str):
            body = (body or "").replace("\n", " ").strip()
            if not body:
                return
            sections.append(f"{title}: {body}")

        prompt_sections: list[str] = []

        medium_or_tech = (medium_or_tech or "").strip()
        if medium_or_tech:
            add_section(prompt_sections, "Medium / Tech", medium_or_tech)
        add_section(prompt_sections, "Subject / Identity", subject_or_identity)
        add_section(prompt_sections, "Action / State", action_or_state)
        add_section(prompt_sections, "Environment", environment)
        add_section(prompt_sections, "Clothing / Body", clothing_body)
        add_section(prompt_sections, "Final Style", final_style)

        prompt = "\n\n".join(prompt_sections).strip()

        return (prompt,)
