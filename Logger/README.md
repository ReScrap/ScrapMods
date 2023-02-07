# Logger

Logger for logging stuff. Thanks to @earthnuker.

Quick snippet for initialisation in your `.py` file

```python
logger = None

try:
    logger = __import__("Logger").Logger("Police")
except Exception:
    pass


def log(msg):
    if logger is not None:
        logger.info(msg)
    else:
        Scrap.Print("[Logger][File] " + str(msg) + "\n")


log("Starting module")

logger.info("A")
logger.error("OH NO!")
```

NOTE: Never do something like:

```python
if logger:
    this
else:
    that
```

It will crahs.

TODO: come up with better system
