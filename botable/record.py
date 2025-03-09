import time
from multiprocessing import Queue
from queue import Empty
from typing import Iterator, Optional, Tuple, Union

from pynput import keyboard, mouse  # type: ignore

from botable.common import Base, Event, KeyboardEvent, MouseEvent, add_noise


class Recorder(Base):
    _last_event_at: float
    _events: "Queue[Event]"
    is_recording: bool = False
    _paused_at: Optional[float] = None

    @property
    def is_paused(self) -> bool:
        return self._paused_at is not None

    def _save_events(
        self,
        button: Union[keyboard.Key, keyboard.KeyCode, mouse.Button],
        pressed: bool,
        position: Optional[Tuple[int, int]],
    ) -> None:
        if self.is_paused:
            return
        current_time = time.time()
        pre_sleep = current_time - self._last_event_at
        if self.noise:
            pre_sleep = add_noise(pre_sleep)

        if isinstance(button, mouse.Button):
            if not position:
                return
            self._events.put(
                MouseEvent(
                    str(button),
                    action="press" if pressed else "release",
                    wait_seconds=pre_sleep,
                    coordinates=position,
                )
            )
        else:
            self._events.put(
                KeyboardEvent(
                    str(button),
                    action="press" if pressed else "release",
                    wait_seconds=pre_sleep,
                )
            )
        self._last_event_at = current_time

    def _on_press(self, key: Optional[Union[keyboard.Key, keyboard.KeyCode]]) -> None:
        if not key:
            return
        if key == self.exit_key:
            self.is_recording = False
        elif key == self.pause_key:
            if self._paused_at:
                pause_time = time.time() - self._paused_at
                self._last_event_at += pause_time
                self._paused_at = None
            else:
                self._paused_at = time.time()
        else:
            self._save_events(key, True, None)

    def _on_release(self, key: Optional[Union[keyboard.Key, keyboard.KeyCode]]):
        if not key:
            return
        if key == self.pause_key:
            return
        self._save_events(key, False, None)

    def _on_click(self, x: int, y: int, button: mouse.Button, pressed: bool):
        self._save_events(button, pressed, (int(x), int(y)))

    def record(self) -> Iterator[Event]:
        """
        Launch the recording, yielding the keyboard and mouse click events as they occur.
        Pressing the `exit_key` will terminate the recording.
        Pressing the `pause_key` will pause/resume the recording.
        """
        self._events = Queue()
        self._last_event_at = time.time()
        keyboard.Listener(on_press=self._on_press, on_release=self._on_release).start()
        mouse.Listener(on_click=self._on_click).start()

        def recorded_events() -> Iterator[Event]:
            while not self._events.empty() or self.is_recording:
                try:
                    yield self._events.get(timeout=self._get_timeout)
                except Empty:
                    continue

        self.is_recording = True
        return recorded_events()


def record(
    *,
    pause_key: str = "Key.f2",
    exit_key: str = "Key.f1",
    noise: bool = False,
) -> Iterator[Event]:
    return Recorder(
        pause_key=pause_key,
        exit_key=exit_key,
        noise=noise,
    ).record()
