import random
from pynput.keyboard import Key, KeyCode  # type: ignore
from typing import NamedTuple, Optional, Tuple, Union


class Event(NamedTuple):
    button: str
    pressed: bool
    pre_sleep: float
    coordinates: Optional[Tuple[int, int]]

def _to_key(key: str) -> Union[Key, KeyCode, str]:
    try:
        return eval(f"Key.{key}")
    except:
        try:
            return eval(KeyCode(key))
        except:
            return KeyCode.from_char(key)

def _add_noise(x: float) -> float:
    return x * (1 + random.betavariate(2, 5) / 2)

class Base:
    def __init__(self, *, pause_key: str = "f2", exit_key: str = "f1", noise: bool = False) -> None:
        self.pause_key = _to_key(pause_key)
        self.exit_key = _to_key(exit_key)
        self.noise = noise
        self._paused_at: Optional[float] = None
    
    @property
    def is_paused(self) -> bool:
        return self._paused_at is not None
            
