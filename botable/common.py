import random
from pynput.keyboard import Key, KeyCode  # type: ignore
from typing import NamedTuple, Optional, Tuple, Union


class Event(NamedTuple):
    button: str
    pressed: bool
    pre_sleep: float
    coordinates: Optional[Tuple[int, int]]

    @property
    def key(self) -> Union[Key, KeyCode]:
        return key_from_str(self.button)


def key_from_str(key: str) -> Union[Key, KeyCode]:
    try:
        return eval(f"Key.{key}")
    except:
        try:
            return KeyCode(int(key.strip("<>")))
        except:
            return KeyCode.from_char(key.strip("'"))


def add_noise(x: float) -> float:
    return x * (1 + random.betavariate(2, 5) / 2)


class Base:
    def __init__(
        self, *, pause_key: str = "f2", exit_key: str = "f1", noise: bool = False
    ) -> None:
        self.pause_key = key_from_str(pause_key)
        self.exit_key = key_from_str(exit_key)
        self.noise = noise
        self._paused_at: Optional[float] = None
        self._get_timeout = 1

    @property
    def is_paused(self) -> bool:
        return self._paused_at is not None
