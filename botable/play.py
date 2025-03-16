import time
from multiprocessing import Queue
from queue import Empty
from typing import Any, Iterable, Iterator, List, Optional, Union

from pynput import keyboard, mouse  # type: ignore

from botable.common import Base, Event, KeyboardEvent, MouseEvent, add_noise


class Player(Base):
    _resume_signal: "Queue[Any]"

    def __init__(
        self,
        *,
        pause_key: str = "Key.f2",
        exit_key: str = "Key.f1",
        loops: int = 1,
        rate: float = 1.0,
        delay: float = 1.0,
        offset: int = 0,
        noise: bool = False,
    ) -> None:
        super().__init__(
            pause_key=pause_key,
            exit_key=exit_key,
            noise=noise,
        )
        self.loops = loops
        self.rate = rate
        self.delay = delay
        self.offset = offset
        self.is_playing = False
        self.is_paused = False

    def _on_press(self, key: Optional[Union[keyboard.Key, keyboard.KeyCode]]):
        if key == self.exit_key:
            self.is_playing = False
        elif key == self.pause_key:
            self.is_paused = not self.is_paused

    def play(self, events: Iterable[Event]) -> Iterator[Event]:
        """
        Waits `delay` and then iterates on `events` to play them,
        optionally playing them at a modified speed `rate`,
        optionally skipping the first `offset` events,
        optionally adding noise to the time intervals between events (the original interval remains the minimum).
        Once `events` is exhausted the entire collected set of event will optionally be replayed additional times if `loops` > 1.
        Pressing the `exit_key` will terminate the recording.
        Pressing the `pause_key` will pause/resume the recording.
        """
        self.is_playing = True
        try:
            time.sleep(self.delay)

            self._resume_signal: "Queue[Any]" = Queue()
            loop_index, event_index = 0, 0
            mouse_ctrl = mouse.Controller()
            keyboard_ctrl = keyboard.Controller()

            keyboard.Listener(on_press=self._on_press).start()

            collected_events: List[Event] = []

            for loop_index in range(self.loops):
                for event_index, event in enumerate(events):
                    if self.loops > 1 and not loop_index:
                        collected_events.append(event)

                    if loop_index == 0 and self.offset > event_index:
                        continue

                    if self.noise:
                        event.wait_seconds = add_noise(event.wait_seconds)

                    # point mouse to click coordinates before waiting for click time
                    if isinstance(event, MouseEvent) and event.coordinates:
                        mouse_ctrl.position = event.coordinates

                    time.sleep(event.wait_seconds / self.rate)

                    while self.is_playing and self.is_paused:
                        time.sleep(0.1)

                    if not self.is_playing:
                        return

                    if isinstance(event, KeyboardEvent):
                        if event.action == "press":
                            keyboard_ctrl.press(event.button())
                        elif event.action == "release":
                            keyboard_ctrl.release(event.button())
                    elif isinstance(event, MouseEvent):
                        if event.action == "press":
                            mouse_ctrl.press(event.button())
                        elif event.action == "release":
                            mouse_ctrl.release(event.button())
                    else:
                        raise TypeError(f"event of type {type(event)} is not supported")
                    yield event

                events = collected_events
        finally:
            self.is_playing = False


def play(
    events: Iterable[Event],
    *,
    pause_key: str = "Key.f2",
    exit_key: str = "Key.f1",
    loops: int = 1,
    rate: float = 1.0,
    delay: float = 1.0,
    offset: int = 0,
    noise: bool = False,
) -> Iterator[Event]:
    return Player(
        pause_key=pause_key,
        exit_key=exit_key,
        loops=loops,
        rate=rate,
        delay=delay,
        offset=offset,
        noise=noise,
    ).play(events)
