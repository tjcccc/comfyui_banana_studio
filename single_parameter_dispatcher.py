from typing import Tuple


class SingleParameterDispatcher:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {
                    "default": 0.0,
                    "step": 0.01,
                }),
                "delta": ("FLOAT", {
                    "default": 0.0,
                    "step": 0.01,
                }),
                "max_value": ("FLOAT", {
                    "default": 0.0,
                    "step": 0.01,
                }),
                "batch": ("INT", {
                    "default": 0,
                    "step": 1,
                }),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }

    _STATE = {}

    RETURN_TYPES = ("FLOAT", "INT","STRING")
    RETURN_NAMES = ("dispatch_value", "index", "log")

    FUNCTION = "run"

    CATEGORY = "Banana Studio"

    IS_CHANGED = True


    def _rebuild_queue(self, value, delta, max_value, batch):
        queue = []
        current = value

        if batch < 2:
            queue = [current]
        elif delta == 0.0:
            queue = [value for _ in range(batch)]
        else:
            for _ in range(batch):
                v = current
                if delta > 0 and v > max_value:
                    v = max_value
                elif delta < 0 and v < max_value:
                    v = max_value
                queue.append(v)
                current += delta

        return queue


    def run(self, value, delta, max_value, batch, unique_id=None) -> Tuple[float, int, str]:
        value: float = float(value)
        delta: float = float(delta)
        max_value: float = float(max_value)
        batch: int = int(batch)

        key = unique_id or "global"

        state = self._STATE.get(key, {
            "queue": [],
            "index": 0,
            "last_value": None,
            "last_delta": None,
            "last_max": None,
            "last_batch": None,
        })

        params_changed = (
            state["last_value"] != value
            or state["last_delta"] != delta
            or state["last_max"] != max_value
            or state["last_batch"] != batch
        )

        if params_changed or not state["queue"]:
            state["queue"] = self._rebuild_queue(value, delta, max_value, batch)
            state["index"] = 0
            state["last_value"] = value
            state["last_delta"] = delta
            state["last_max"] = max_value
            state["last_batch"] = batch

        if state["queue"]:
            current_value = state["queue"].pop(0)
        else:
            current_value = value

        current_index = state["index"]
        state["index"] = current_index + 1
        self._STATE[key] = state

        log = (
            f"[SingleParameterDispatcher]\n"
            f"batch_index={current_index + 1}/{batch}, current value={current_value}\n"
            f"(initial value={value}, delta={delta}, max={max_value})"
        )
        print(log)

        return float(current_value), int(current_index + 1), log
