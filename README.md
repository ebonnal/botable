# 🤖 Botable
> Record and play keyboard and mouse clicks

[![Actions Status](https://github.com/ebonnal/botable/workflows/unittest/badge.svg)](https://github.com/ebonnal/botable/actions)
[![Actions Status](https://github.com/ebonnal/botable/workflows/PyPI/badge.svg)](https://github.com/ebonnal/botable/actions)

# install
```bash
pip install botable
```

# use
Note: Press f1 to end the recording/playback and f2 to pause/resume it (both keys configurable as function paramater or cli option).
## as a lib
```python
from botable import record, play

# this collects the recorded events
recorded_events = list(record())

# this plays the recorded events and collects the played events
played_events = list(play(recording, loops=3))
````

Help:
```python
help(record)
help(play)
```

## as a cli
Here is the same scenario but using the command line interface:
```bash
python -m botable record > ./recorded_events.py
cat ./recorded_events.py | python -m botable play --playback-loops 3 > ./played_events.py
```

Help:
```bash
python -m botable --help
```
