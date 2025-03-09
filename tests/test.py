import time
from unittest import TestCase
from botable.play import Player
from botable.record import Recorder
from botable.record import Event


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
        self.assertEqual(button(next(Player().play([exit_event]))), button(exit_event))

        # wait for recorder to catch it
        time.sleep(2 * recorder._get_timeout)
        self.assertFalse(recorder.is_recording)

        # ensure recorded events are the played ones
        self.assertEqual(
            list(map(button, recorded_events)),
            list(map(button, events_to_record)),
        )
