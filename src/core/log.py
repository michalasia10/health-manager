from typing import Literal

from loguru import logger

LEVELS = Literal["info", "error", "warning"]


def log(__message, level: LEVELS = "info", extra=None, *args, **kwargs):
    if extra is None:
        extra = {}
    getattr(logger.bind(**extra), level)(__message, *args, **kwargs)
