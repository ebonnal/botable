from multiprocessing import Queue
import time
from typing import Iterator, Optional, Union, Tuple
from pynput import keyboard, mouse  # type: ignore
from botable.common import Base, Event

class Recorder(Base):
    _EVENT_GET_TIMEOUT = 1
    _last_event_at: float
    _events: "Queue[Event]"

    def __post_init__(self) -> None:
        self.is_recording = False
    
    @property
    def is_paused(self) -> bool:
        return self._paused_at is not None

    def _save_events(self, button: Union[keyboard.Key, mouse.Button], pressed: bool, position: Optional[Tuple[int, int]]):
        if self.is_paused:
            return
        current_time = time.time()
        self._events.put(
            Event(str(button), pressed, current_time - self._last_event_at, position)
        )
        self.last_event_at = current_time

    def _on_press(self, key: keyboard.Key) -> None:
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

    def _on_release(self, key: keyboard.Key):
        if key == self.pause_key:
            return
        self._save_events(str(key), False, None)

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
        self.is_recording = True
        try:
            keyboard.Listener(on_press=self._on_press, on_release=self._on_release).start()
            mouse.Listener(on_click=self._on_click).start()
            def recorded_events() -> Iterator[Event]:
                while self._events or self.is_recording:
                    yield self._events.get(timeout=self._EVENT_GET_TIMEOUT)
                    
            return recorded_events()
        except:
            self.is_recording = False
            raise
