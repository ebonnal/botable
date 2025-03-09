import argparse
import json
import sys

from botable import Event, Player, Recorder


def main() -> int:
    arg_parser = argparse.ArgumentParser(
        description="record/play mouse and keyboard keys events."
    )
    arg_parser.add_argument(
        "--exit-key",
        required=False,
        type=str,
        default="Key.f1",
        help="The key to press to end the ongoing recording or playback, default is f1",
    )
    arg_parser.add_argument(
        "--pause-key",
        required=False,
        type=str,
        default="Key.f2",
        help="The key to press to pause/resume the ongoing recording or playback, default is f2",
    )
    arg_parser.add_argument(
        "--noise",
        action="store_true",
        help="To add noise to the intervals between events",
    )

    mode_subparser_action = arg_parser.add_subparsers(
        dest="mode", required=True
    )  # Required subcommand

    mode_subparser_action.add_parser(
        "record",
        help="Record until you press the exit key (default: f1). Pause and resume the recording via the pause key (default: f2).",
    )
    play_arg_parser = mode_subparser_action.add_parser(
        "play",
        help="Play recorded events passed via stdin, until you press the exit key (default: f1). Pause and resume the playback via the pause key (default: f2).",
    )

    play_arg_parser.add_argument(
        "--loops",
        required=False,
        type=int,
        default=1,
        help="Number of times to loop through recorded events (default: 1 loop).",
    )
    play_arg_parser.add_argument(
        "--rate",
        required=False,
        type=float,
        default=1.0,
        help="Playback rate to apply to the recording (default: 1.0, i.e. recording speed).",
    )
    play_arg_parser.add_argument(
        "--delay",
        required=False,
        type=float,
        default=1.0,
        help="Number of seconds to wait before playing the recording (default: 1 second)",
    )
    play_arg_parser.add_argument(
        "--offset",
        required=False,
        type=int,
        default=0,
        help="How many incoming events to skip (default: 0).",
    )

    args = arg_parser.parse_args()

    if args.mode == "play":
        for event in Player(
            exit_key=args.exit_key,
            pause_key=args.pause_key,
            loops=args.loops,
            rate=args.rate,
            delay=args.delay,
            offset=args.offset,
            noise=args.noise,
        ).play(map(lambda line: Event.from_json(line), sys.stdin)):
            print(event.to_json(), flush=True)
    elif args.mode == "record":
        for event in Recorder(
            exit_key=args.exit_key,
            pause_key=args.pause_key,
        ).record():
            print(event.to_json(), flush=True)
    else:
        raise ValueError("unsupported mode")

    return 0


if __name__ == "__main__":
    main()
