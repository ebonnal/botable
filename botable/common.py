import json
import random
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Literal, NamedTuple, Optional, Tuple, Union, cast

from pynput.keyboard import Key, KeyCode  # type: ignore
from pynput.mouse import Button  # type: ignore


@dataclass
class Event(ABC):
    button_str: str
    action: Literal["press", "release"]
    wait_seconds: float

    @abstractmethod
    def button(self) -> Union[Button, KeyCode, Key]: ...

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(json_content: str) -> "Event":
        d = json.loads(json_content)
        try:
            return MouseEvent(**d)
        except TypeError:
            return KeyboardEvent(**d)


@dataclass
class KeyboardEvent(Event):
    def button(self) -> Union[KeyCode, Key]:
        return key_from_str(self.button_str)


@dataclass
class MouseEvent(Event):
    coordinates: Optional[Tuple[int, int]]

    def button(self) -> Button:
        return eval(self.button_str)


def key_from_str(key: str) -> Union[KeyCode, Key]:
    try:
        return eval(key)
    except:
        try:
            return KeyCode(int(key.strip("<>")))  # type: ignore
        except:
            potential_char = key.strip("'")
            if len(potential_char) == 1:
                return KeyCode.from_char(potential_char)
            raise ValueError(f"cannot convert key '{key}' into KeyCode or Key")


def add_noise(x: float) -> float:
    return x * (1 + random.betavariate(2, 5) / 2)


class Base:
    def __init__(
        self,
        *,
        pause_key: str = "Key.f2",
        exit_key: str = "Key.f1",
        noise: bool = False,
    ) -> None:
        self.pause_key = key_from_str(pause_key)
        self.exit_key = key_from_str(exit_key)
        self.noise = noise
        self._get_timeout = 1
