import time
from typing import Iterable, Iterator, List, Optional
from pynput import keyboard, mouse  # type: ignore
from pynput.mouse import Button

from botable.common import Base, Event  # type: ignore

Button
from pynput.keyboard import KeyCode  # type: ignore

_PAUSE_SLEEP_INCREMENT = 0.5
_POST_PLAY_SLEEP = 0.2


class Player(Base):
    _EVENT_GET_TIMEOUT = 1
    _last_event_at: float

    def __init__(
        self,
        events: Iterable[Event],
        *,
        pause_key: str = "f2",
        exit_key: str = "f1",
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
        self.events = events
        self.loops = loops
        self.rate = rate
        self.delay = delay
        self.offset = offset

        self.is_playing = False
    
    def _on_press(self, key: keyboard.Key):
        if key == self.exit_key:
            self.is_playing = False
        elif key == self.pause_key:
            self._paused_at = None if self._paused_at else time.time()

    def play(
    ) -> Iterator[Event]:
        """
        Waits `delay` and then iterates on `events` to play them,
        optionally playing them at a modified speed `rate`,
        optionally skipping the first `offset` events,
        optionally adding noise to the time intervals between events (the original interval remains the minimum).
        Once `events` is exhausted the entire collected set of event will optionally be replayed additional times if `loops` > 1.
        Pressing the `exit_key` will terminate the recording.
        Pressing the `pause_key` will pause/resume the recording.
        """
        global _PLAYING
        _PLAYING = True
        try:
            time.sleep(delay)

            continue_ = True
            paused_at: Optional[float] = None
            loop_index, event_index = 0, 0
            mouse_ctrl = mouse.Controller()
            keyboard_ctrl = keyboard.Controller()

            exit_key_ = str_to_key(exit_key)
            pause_key_ = str_to_key(pause_key)


            keyboard.Listener(on_press=on_press).start()

            collected_events: List[Event] = []

            events_: Iterable[Event] = events

            for loop_index in range(loops):
                for event_index, event in enumerate(events_):
                    if loops > 1 and not loop_index:
                        collected_events.append(event)

                    if loop_index == 0 and offset > event_index:
                        continue

                    if event.coordinates is None:
                        ctrl = keyboard_ctrl
                    else:
                        mouse_ctrl.position = event.coordinates
                        ctrl = mouse_ctrl

                    if event.button.startswith("<") and event.button.endswith(
                        ">"
                    ):
                        evaluated_button = KeyCode(int(event.button[1:-1]))
                    else:
                        evaluated_button = eval(event.button)

                    if noise:
                        event = Event(
                            button=event.button,
                            pressed=event.pressed,
                            pre_sleep=_add_noise(event.pre_sleep),
                            coordinates=event.coordinates,
                        )

                    time.sleep(event.pre_sleep / rate)

                    while continue_ and paused_at:
                        time.sleep(_PAUSE_SLEEP_INCREMENT)

                    if event.pressed:
                        ctrl.press(evaluated_button)
                    else:
                        ctrl.release(evaluated_button)

                    yield event

                    if not continue_:
                        return

                events_ = collected_events

            time.sleep(_POST_PLAY_SLEEP)
        finally:
            _PLAYING = False
