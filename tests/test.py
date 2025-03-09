import time
from typing import List
from unittest import TestCase

from pynput import keyboard  # type: ignore

from botable import play, record
from botable.common import KeyboardEvent, MouseEvent, key_from_str
from botable.play import Player
from botable.record import Event, Recorder

events_to_record: List[Event] = [
    KeyboardEvent(
        button_str="'a'",
        action="press",
        wait_seconds=0.1,
    ),
    KeyboardEvent(
        button_str="'a'",
        action="release",
        wait_seconds=0.1,
    ),
    MouseEvent(
        button_str="Button.left",
        action="press",
        wait_seconds=0.1,
        coordinates=(1131, 27),
    ),
    MouseEvent(
        button_str="Button.left",
        action="release",
        wait_seconds=0.1,
        coordinates=(1131, 27),
    ),
]
exit_event = KeyboardEvent(
    button_str="'c'",
    action="press",
    wait_seconds=0.1,
)


class Test(TestCase):
    def test_classes(self) -> None:
        recorder = Recorder(exit_key="c")
        self.assertFalse(recorder.is_recording)
        player = Player()
        self.assertFalse(player.is_playing)

        recorded_events = recorder.record()
        self.assertTrue(recorder.is_recording)

        played_events = player.play(events_to_record)
        self.assertFalse(player.is_playing)

        # play events
        for event_to_record in events_to_record:
            self.assertEqual(
                next(played_events),
                event_to_record,
            )
            self.assertTrue(player.is_playing)

        # finish playback
        with self.assertRaises(StopIteration):
            next(played_events)
        self.assertFalse(player.is_playing)

        # still recording
        self.assertTrue(recorder.is_recording)

        # play recording exit key
        self.assertEqual(next(Player().play([exit_event])).button, exit_event.button)

        # wait for recorder to catch it
        time.sleep(2 * recorder._get_timeout)
        self.assertFalse(recorder.is_recording)

        # ensure recorded events are the played ones
        self.assertEqual(
            list(map(Event.button, recorded_events)),
            list(map(Event.button, events_to_record)),
        )

    def test_functions(self) -> None:
        recorded_events = record(exit_key="c")

        played_events = list(play(events_to_record))

        # play recording exit key
        self.assertEqual(
            next(play([exit_event])).button,
            exit_event.button,
        )

        # ensure recorded events are the played ones
        self.assertEqual(
            list(map(Event.button, recorded_events)),
            list(map(Event.button, events_to_record)),
        )

    def test_readme(self) -> None:
        from botable import record, play

        print("# collects the recorded events")
        recorded_events = list(record())

        print("# press f1 to stop the recording when you are done")
        print("recorded_events: ", recorded_events)

        print("# plays 3 times the recorded events and collects the played events")
        played_events = list(play(recorded_events, loops=3))

    def test_key_from_str(self) -> None:
        self.assertEqual(key_from_str("Key.f1"), keyboard.Key.f1)
        self.assertEqual(
            repr(key_from_str("'a'")),
            str(keyboard.KeyCode.from_char("a")),
        )
        self.assertEqual(
            key_from_str("<63>"),
            keyboard.KeyCode(63),  # type: ignore
        )
