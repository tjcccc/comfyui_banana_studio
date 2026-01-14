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
                "identify_reference": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Identify Reference\nDefines the immutable facial identity anchor to ensure consistent character appearance across all generations."
                }),
                "subject_or_presence": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Subject / Identity\nDescribes how the subject emotionally, aesthetically, and physically occupies the frame in this specific moment."
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


    def make_banana_prompt(self, medium_or_tech, identify_reference="", subject_or_presence="", action_or_state="", environment="", clothing_body="", final_style=""):

        has_multiple_sections = any(
            s.strip()
            for s in (
                identify_reference,
                subject_or_presence,
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
        add_section(prompt_sections, "Identify Reference", identify_reference)
        add_section(prompt_sections, "Subject / Presence", subject_or_presence)
        add_section(prompt_sections, "Action / State", action_or_state)
        add_section(prompt_sections, "Environment", environment)
        add_section(prompt_sections, "Clothing / Body", clothing_body)
        add_section(prompt_sections, "Final Style", final_style)

        prompt = "\n\n".join(prompt_sections).strip()

        return (prompt,)
