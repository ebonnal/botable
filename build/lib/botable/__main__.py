import argparse

from botable.botable import play, record, stdin_button_events


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Record mouse and keyboard keys pressures/releases."
    )
    arg_parser.add_argument("mode", help="either record or play")
    arg_parser.add_argument(
        "--exit-key",
        required=False,
        type=str,
        default="f1",
        help="the key to press to end the ongoing recording or playback, default is f1",
    )
    arg_parser.add_argument(
        "--pause-key",
        required=False,
        type=str,
        default="f2",
        help="the key to press to pause/resume the ongoing recording or playback, default is f2",
    )
    arg_parser.add_argument(
        "--playback-loops",
        required=False,
        type=int,
        default=1,
        help="in 'play' mode: number of times to loop through recorded events, default is 1 single loop",
    )
    arg_parser.add_argument(
        "--playback-rate",
        required=False,
        type=float,
        default=1.0,
        help="in 'play' mode: speed coefficient to apply to the recording, default is x1.0",
    )
    arg_parser.add_argument(
        "--playback-delay",
        required=False,
        type=float,
        default=1.0,
        help="in 'play' mode: number of seconds to sleep before playing the recording, default is 1.0 second",
    )
    arg_parser.add_argument(
        "--playback-offset",
        required=False,
        type=int,
        default=0,
        help="in 'play' mode: how many events the first loop will skip, default is 0 event skipped",
    )
    arg_parser.add_argument(
        "--playback-noise",
        required=False,
        type=bool,
        help="in 'play' mode: to add noise to the time intervals between events",
    )
    args = arg_parser.parse_args()

    mode = args.mode

    if mode == "play":
        for button_event in play(
            button_events=stdin_button_events(),
            exit_key=args.exit_key,
            pause_key=args.pause_key,
            loops=args.playback_loops,
            rate=args.playback_rate,
            delay=args.playback_delay,
            offset=args.playback_offset,
            verbose=args.playback_verbose,
        ):
            print(tuple(button_event), flush=True)
    elif mode == "record":
        for button_event in record(
            exit_key=args.exit_key,
            pause_key=args.pause_key,
        ):
            print(tuple(button_event), flush=True)
    else:
        raise ValueError("unsupported mode")
