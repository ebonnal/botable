import argparse
from contextlib import suppress
import os
import time
from typing import List, Optional, Tuple
from pynput import keyboard, mouse  # type: ignore
from pynput.mouse import Button  # type: ignore
from pynput.keyboard import Key, KeyCode  # type: ignore

PAUSED_AT: Optional[float] = None

PLAYBACK_PAUSE_SLEEP_INCREMENT = 0.5

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Record mouse and keyboard keys pressures/releases.")
    arg_parser.add_argument("mode", help="either record or play")
    arg_parser.add_argument("--exit-key", required=False, type=str, default="f1", help="the key to press to end the ongoing recording or playback, default is f1")
    arg_parser.add_argument("--pause-key", required=False, type=str, default="f2", help="the key to press to pause/resume the ongoing recording or playback, default is f2")
    arg_parser.add_argument("--playback-loops", required=False, type=int, default=1, help="in 'play' mode: number of times to loop through recorded events, default is 1 single loop")
    arg_parser.add_argument("--playback-rate", required=False, type=float, default=1.0, help="in 'play' mode: speed coefficient to apply to the recording, default is x1.0")
    arg_parser.add_argument("--playback-delay", required=False, type=float, default=1.0, help="in 'play' mode: number of seconds to sleep before playing the recording, default is 1.0 second")
    arg_parser.add_argument("--playback-offset", required=False, type=int, default=0, help="in 'play' mode: how many events the first loop will skip, default is 0 event skipped")
    arg_parser.add_argument("--playback-verbose", required=False, type=bool)
    args = arg_parser.parse_args()

    mode = args.mode
    exit_key = eval(f"Key.{args.exit_key}")
    pause_key = eval(f"Key.{args.pause_key}")

    if mode == "play":
        time.sleep(1)
        event_index = 0

        playback_loops = args.playback_loops
        offset = args.offset
        playback_rate = args.playback_rate
        verbose = args.playback_verbose
        loop_index = 0

        def on_press(key: keyboard.Key):
            global PAUSED_AT
            if key == exit_key:
                print(f"resume with: python -m clicks play --num-loops {playback_loops - loop_index} --offset {event_index + offset}", flush=True)
                os._exit(0)
            elif key == pause_key:
                PAUSED_AT = None if PAUSED_AT else time.time()

        mouse_ctrl = mouse.Controller()
        keyboard_ctrl = keyboard.Controller()

        keyboard.Listener(on_press=on_press).start()

        recording: List[Tuple[float, str, bool, Optional[Tuple[int, int]]]] = []

        with suppress(EOFError):
            while event := input():
                recording.append(eval(event))

        for loop_index in range(playback_loops):
            for event_index, (seconds, button, pressed, position) in enumerate(recording):

                while PAUSED_AT:
                    time.sleep(PLAYBACK_PAUSE_SLEEP_INCREMENT)

                if verbose:
                    print("loop_index =", loop_index, "; event_index", event_index)

                if loop_index == 0 and offset > event_index:
                    continue

                if position is None:
                    ctrl = keyboard_ctrl
                else:
                    mouse_ctrl.position = position
                    ctrl = mouse_ctrl

                if len(button) == 1:
                    evaluated_button = button
                elif button.startswith("<") and button.endswith(">"):
                    evaluated_button = KeyCode(int(button[1:-1]))
                else:
                    evaluated_button = eval(button)

                time.sleep(seconds/playback_rate)
                if pressed:
                    ctrl.press(evaluated_button)
                else:
                    ctrl.release(evaluated_button)

            last_click_at = None

        time.sleep(0.5)

    elif mode == "record":
        recording = []
        click_timestamps: List[float] = [time.time()]

        def save_event(button: str, pressed: bool, position):
            global PAUSED_AT
            if PAUSED_AT:
                return
            current_time = time.time()
            recording.append(
                (current_time - click_timestamps[-1], button, pressed, position)
            )
            click_timestamps.append(current_time)

        def on_press(key: keyboard.Key):
            global PAUSED_AT
            if key == exit_key:
                print("\n".join(map(repr, recording)), flush=True)
                os._exit(0)
            elif key == pause_key:
                if PAUSED_AT:
                    if click_timestamps:
                        pause_time = (time.time() - PAUSED_AT)
                        click_timestamps[-1] += pause_time
                        PAUSED_AT = None        
                else:
                    PAUSED_AT = time.time()
                return
            save_event(str(key), True, None)

        def on_release(key: keyboard.Key):
            if key == pause_key:
                return
            save_event(str(key), False, None)
        
        def on_click(x: int, y: int, button: mouse.Button, pressed: bool):
            save_event(str(button), pressed, (int(x), int(y)))

        keyboard.Listener(on_press=on_press, on_release=on_release).start()

        mouse.Listener(on_click=on_click).start()

        while True:
            time.sleep(60)

    else:
        raise ValueError("unsupported mode")
