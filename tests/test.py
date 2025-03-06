import time
from unittest import TestCase
from botable import is_recording, is_playing
from botable import ButtonEvent, play, record

def button(event: ButtonEvent) -> str:
    return event.button

class Test(TestCase):
    def test(self) -> None:
        button_events_to_record = [
            ButtonEvent(
                button="'a'",
                pressed=True,
                pre_sleep=0.1,
                coordinates=None,
            ),
            ButtonEvent(
                button="'a'",
                pressed=False,
                pre_sleep=0.1,
                coordinates=None,
            ),
            ButtonEvent(
                button="'b'",
                pressed=True,
                pre_sleep=0.1,
                coordinates=None,
            ),
            ButtonEvent(
                button="'b'",
                pressed=False,
                pre_sleep=0.1,
                coordinates=None,
            ),
        ]
        exit_button_event = ButtonEvent(
            button="'c'",
            pressed=True,
            pre_sleep=0.1,
            coordinates=None,
        )

        self.assertFalse(is_recording())
        self.assertFalse(is_playing())
        recorded_events = record(exit_key="c")
        self.assertTrue(is_recording())
        played_events = play(button_events_to_record)
        self.assertFalse(is_playing())
        for _ in range(len(button_events_to_record)):
            next(played_events)
            self.assertTrue(is_playing())
        with self.assertRaises(StopIteration):
            next(played_events)
        self.assertFalse(is_playing())
        self.assertTrue(is_recording())
        self.assertEqual(
            button(next(play([exit_button_event]))),
            button(exit_button_event)
        )
        time.sleep(2)
        self.assertFalse(is_recording())
        self.assertEqual(
            list(map(button, recorded_events)),
            list(map(button, button_events_to_record)),
        )


