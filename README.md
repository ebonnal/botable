[![pypi](https://github.com/ebonnal/botable/actions/workflows/pypi.yml/badge.svg?branch=main)](https://github.com/ebonnal/botable/actions)


# 🤖 `botable`

### *Record and play keyboard and mouse events*


## install
```bash
pip install botable
```
(installs `botable` in `PATH`)


## `botable` command

1. **record**: This records and saves events in a file.
    - Stop the recording by pressing f1 (see `--exit-key` option to override).
    - Press f2 to pause/resume the recording (see `--pause-key` option to override).
```bash
botable record > /tmp/recorded_events.jsonl
```
1. **play**: this plays the recorded events 3 times (`--loops`), doubling the original speed (`--rate`), and stores the played events into a file.
    - Stop the playback by pressing f1 (see `--exit-key` option to override).
    - Pause/resume the playback by pressing f2 (see `--pause-key` option to override):
```bash
cat /tmp/recorded_events.jsonl | botable play --loops 3 --rate 2 > /tmp/played_events.jsonl
```

## `botable` as a Python module
```python
from botable import record, play

# collects the recorded events
recorded_events = list(record())

# press f1 to stop the recording when you are done

# plays 3 times the recorded events and collects the played events
played_events = list(play(recorded_events, loops=3))
```
