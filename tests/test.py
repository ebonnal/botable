import time
from unittest import TestCase
from botable.record import is_recording, is_playing
from botable.record import Event, play, record

def button(event: Event) -> str:
    return event.button

class Test(TestCase):
    def test(self) -> None:
        events_to_record = [
            Event(
                button="'a'",
                pressed=True,
                pre_sleep=0.1,
                coordinates=None,
            ),
            Event(
                button="'a'",
                pressed=False,
                pre_sleep=0.1,
                coordinates=None,
            ),
            Event(
                button="'b'",
                pressed=True,
                pre_sleep=0.1,
                coordinates=None,
            ),
            Event(
                button="'b'",
                pressed=False,
                pre_sleep=0.1,
                coordinates=None,
            ),
        ]
        exit_event = Event(
            button="'c'",
            pressed=True,
            pre_sleep=0.1,
            coordinates=None,
        )

        self.assertFalse(is_recording())
        self.assertFalse(is_playing())
        recorded_events = record(exit_key="c")
        self.assertTrue(is_recording())
        played_events = play(events_to_record)
        self.assertFalse(is_playing())
        for _ in range(len(events_to_record)):
            next(played_events)
            self.assertTrue(is_playing())
        with self.assertRaises(StopIteration):
            next(played_events)
        self.assertFalse(is_playing())
        self.assertTrue(is_recording())
        self.assertEqual(
            button(next(play([exit_event]))),
            button(exit_event)
        )
        time.sleep(2)
        self.assertFalse(is_recording())
        self.assertEqual(
            list(map(button, recorded_events)),
            list(map(button, events_to_record)),
        )


