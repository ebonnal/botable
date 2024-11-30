from collections import deque
from contextlib import suppress
import random
import time
from typing import Deque, Iterable, Iterator, List, Optional, Union, NamedTuple, Tuple
from pynput import keyboard, mouse  # type: ignore
from pynput.mouse import Button  # type: ignore
from pynput.keyboard import Key, KeyCode  # type: ignore


class ButtonEvent(NamedTuple):
    button: str
    pressed: bool
    seconds_since_last_event: float
    coordinates: Optional[Tuple[int, int]]


def input_button_events() -> Iterator[ButtonEvent]:
    with suppress(EOFError):
        while event := input():
            yield ButtonEvent(*eval(event))


def _to_key(key: str) -> Union[Key, KeyCode, str]:
    try:
        return eval(f"Key.{key}")
    except Exception:
        pass
    try:
        return eval(KeyCode(key[1:-1]))
    except Exception:
        pass
    return KeyCode.from_char(key)


RECORDING = False
PLAYING = False


def record(exit_key: str = "f1", pause_key: str = "f2") -> Iterator[ButtonEvent]:
    """
    Launch the recording, yielding the keyboard and mouse click events as they occur.
    Pressing the `exit_key` will terminate the recording.
    Pressing the `pause_key` will pause/resume the recording.
    """
    global PLAYING, RECORDING
    if PLAYING:
        raise RuntimeError("Attempt to record while playing")
    RECORDING = True
    try:
        paused_at: Optional[float] = None
        last_event_at = time.time()
        click_timestamps: List[float] = [time.time()]
        button_events: Deque[ButtonEvent] = deque()
        continue_ = True

        exit_key_ = _to_key(exit_key)
        pause_key_ = _to_key(pause_key)

        def save_button_events(button: str, pressed: bool, position):
            nonlocal paused_at, last_event_at
            if paused_at:
                return
            current_time = time.time()
            button_events.append(
                ButtonEvent(button, pressed, current_time - last_event_at, position)
            )
            last_event_at = current_time

        def on_press(key: keyboard.Key):
            nonlocal paused_at, last_event_at, continue_
            if key == exit_key_:
                continue_ = False
            elif key == pause_key_:
                if paused_at:
                    if click_timestamps:
                        pause_time = time.time() - paused_at
                        last_event_at += pause_time
                        paused_at = None
                else:
                    paused_at = time.time()
                return
            save_button_events(str(key), True, None)

        def on_release(key: keyboard.Key):
            if key == pause_key_:
                return
            save_button_events(str(key), False, None)

        def on_click(x: int, y: int, button: mouse.Button, pressed: bool):
            save_button_events(str(button), pressed, (int(x), int(y)))

        keyboard.Listener(on_press=on_press, on_release=on_release).start()

        mouse.Listener(on_click=on_click).start()

        while continue_:
            while button_events:
                yield button_events.popleft()
            time.sleep(0.1)
    finally:
        RECORDING = False


def play(
    button_events: Iterable[ButtonEvent],
    exit_key: str = "f1",
    pause_key: str = "f2",
    loops: int = 1,
    rate: float = 1.0,
    delay: float = 1.0,
    offset: int = 0,
    noise: bool = False,
) -> Iterator[ButtonEvent]:
    """
    Waits `delay` and then iterates on `events` to play them,
      optionally playing them at a modified speed `rate`,
      optionally skipping the first `offset` events,
      optionally adding noise to the time intervals between events (the original interval remains the minimum).
    Once `button_events` is exhausted the entire collected set of event will optionally be replayed additional times if `loops` > 1.
    Pressing the `exit_key` will terminate the recording.
    Pressing the `pause_key` will pause/resume the recording.
    """
    global PLAYING, RECORDING
    if RECORDING:
        raise RuntimeError("Attempt to play while recording")
    PLAYING = True
    try:
        time.sleep(delay)

        continue_ = True
        paused_at: Optional[float] = None
        loop_index, event_index = 0, 0
        mouse_ctrl = mouse.Controller()
        keyboard_ctrl = keyboard.Controller()

        exit_key_ = _to_key(exit_key)
        pause_key_ = _to_key(pause_key)

        def on_press(key: keyboard.Key):
            nonlocal paused_at, continue_
            if key == exit_key_:
                continue_ = False
            elif key == pause_key_:
                paused_at = None if paused_at else time.time()

        keyboard.Listener(on_press=on_press).start()

        collected_button_events: List[ButtonEvent] = []

        button_events_: Iterable[ButtonEvent] = button_events

        for loop_index in range(loops):
            for event_index, button_event in enumerate(button_events_):
                if loops > 1 and not loop_index:
                    collected_button_events.append(button_event)

                while continue_ and paused_at:
                    time.sleep(0.5)

                if loop_index == 0 and offset > event_index:
                    continue

                if button_event.coordinates is None:
                    ctrl = keyboard_ctrl
                else:
                    mouse_ctrl.position = button_event.coordinates
                    ctrl = mouse_ctrl

                if button_event.button.startswith("<") and button_event.button.endswith(
                    ">"
                ):
                    evaluated_button = KeyCode(int(button_event.button[1:-1]))
                else:
                    evaluated_button = eval(button_event.button)

                sleep_duration = button_event.seconds_since_last_event / rate
                if noise:
                    sleep_duration *= (1 + random.betavariate(2, 5) / 2)
                time.sleep(sleep_duration)

                if button_event.pressed:
                    ctrl.press(evaluated_button)
                else:
                    ctrl.release(evaluated_button)

                yield button_event

                if not continue_:
                    return

            button_events_ = collected_button_events

        time.sleep(0.2)
    finally:
        PLAYING = False