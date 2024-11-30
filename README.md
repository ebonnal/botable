# 🤖 Botable
> Record and play keyboard and mouse clicks

[![Actions Status](https://github.com/ebonnal/botable/workflows/unittest/badge.svg)](https://github.com/ebonnal/botable/actions)
[![Actions Status](https://github.com/ebonnal/botable/workflows/PyPI/badge.svg)](https://github.com/ebonnal/botable/actions)

# install
```bash
pip install botable
```

# use as a lib
```python
from botable import record, play

# collects the recorded events
recorded_events = list(record())

# press f1 to stop the recording when you are done

# plays 3 times the recorded events and collects the played events
played_events = list(play(recorded_events, loops=3))
```

Help:
```python
help(record)
help(play)
```

# use as a cli
Here is the same scenario but using the command line interface:
```bash
# saves the recorded events in /tmp/recorded_events.py
python -m botable record > /tmp/recorded_events.py

# press f1 to stop the recording when you are done

# plays 3 times the recorded events and saves the played events in /tmp/played_events.py
cat ./recorded_events.py | python -m botable play --playback-loops 3 > /tmp/played_events.py
```

Help:
```bash
python -m botable --help
```

# ⏹️ Stop
Press **f1** to stop the recording/playback. This is configurable, for example if you prefer to press *escape*:

lib:
```python
play(recorded_events, exit_key="esc")
```
cli:
```bash
python -m botable [play/record] --exit-key esc
```

# ⏸️ Pause/Resume
Press **f2** to pause/resume the recording/playback. This is configurable, for example if you prefer to press *space*:

lib:
```python
play(recorded_events, pause_key="space")
```
cli:
```bash
python -m botable [play/record] --pause-key space
```
