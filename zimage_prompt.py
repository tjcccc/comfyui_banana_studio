class ZImagePrompt:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "composition_or_framing": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Composition / Framing\nShot type, camera distance, angle, and framing."
                })
            },
            "optional": {
                "subject_or_identity": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Subject / Identity\nThe main subject and identity traits."
                }),
                "wardrobe_or_appearance": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Wardrobe / Appearance\nClothing, hairstyle, makeup, and visible accessories."
                }),
                "environment_or_scene": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Environment / Scene\nThe surrounding scene or background."
                }),
                "lighting": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Lighting\nLight source, direction, softness, and contrast."
                }),
                "mood_or_style_or_quality": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Mood / Style / Quality\nOverall atmosphere, artistic intent, and realism level."
                }),
                "constraints": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Constraints\nHard requirements and exclusions.\nUse for must-have conditions such as photorealism, no text, no watermark, or avoiding unwanted artifacts."
                })
            },
        }


    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)

    FUNCTION = "make_zimage_prompt"

    CATEGORY = "Banana Studio"


    def make_zimage_prompt(self, composition_or_framing, subject_or_identity="", wardrobe_or_appearance="", environment_or_scene="", lighting="", mood_or_style_or_quality="", constraints=""):

        has_multiple_sections = any(
            s.strip()
            for s in (
                subject_or_identity,
                wardrobe_or_appearance,
                environment_or_scene,
                lighting,
                mood_or_style_or_quality,
                constraints,
            )
        )
        if not has_multiple_sections:
            return (composition_or_framing,)

        def add_section(sections: list[str], title: str, body: str):
            body = (body or "").replace("\n", " ").strip()
            if not body:
                return
            sections.append(f"[{title}] \n{body}")

        prompt_sections: list[str] = []

        composition_or_framing = (composition_or_framing or "").strip()
        if composition_or_framing:
            add_section(prompt_sections, "Composition / Framing", composition_or_framing)
        add_section(prompt_sections, "Subject / Identity", subject_or_identity)
        add_section(prompt_sections, "Wardrobe / Appearance", wardrobe_or_appearance)
        add_section(prompt_sections, "Environment / Scene", environment_or_scene)
        add_section(prompt_sections, "Lighting", lighting)
        add_section(prompt_sections, "Mood / Style / Quality", mood_or_style_or_quality)
        add_section(prompt_sections, "Constraints", constraints)

        prompt = "\n\n".join(prompt_sections).strip()

        return (prompt,)
