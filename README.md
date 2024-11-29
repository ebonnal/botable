# 🤖 Botable
> Record and play keyboard and mouse clicks

[![Actions Status](https://github.com/ebonnal/botable/workflows/unittest/badge.svg)](https://github.com/ebonnal/botable/actions)
[![Actions Status](https://github.com/ebonnal/botable/workflows/PyPI/badge.svg)](https://github.com/ebonnal/botable/actions)

# install
```bash
pip install botable
```

# use
## as a lib
```python
from botable import record, play

events: list = record()
play(events, loops=10, rate=1.5)
```

## as a cli

```
python -m botable record > ./events.py
cat ./events.py | python -m botable play --playback-loops 10 --playback-rate 1.5
```
