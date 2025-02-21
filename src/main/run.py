import multiprocessing
import os
from typing import Callable, Any

from django.conf import settings
from gunicorn.app.base import BaseApplication
from uvicorn.workers import UvicornWorker

from src.main.asgi import application


def get_workers_count():
    return (multiprocessing.cpu_count() * 2) + 1


class MyUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "loop": "uvloop",
        "http": "httptools",
    }


class GunicornApp(BaseApplication):
    def __init__(self, app: Callable, options: dict[str, Any] = None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == "__main__":
    env = os.getenv("ENV", "dev")

    common_options = {
        "bind": f"{settings.HOST}:{settings.PORT}",
        "worker_class": MyUvicornWorker,
        "workers": get_workers_count(),
        "timeout": 120,
        "keepalive": 5,
    }

    env_configs = {
        "dev": {
            "reload": True,
            "max_requests": 100,
            **common_options,
        },
        "staging": {
            "reload": False,
            "max_requests": 500,
            **common_options,
        },
        "prod": {
            "reload": False,
            "max_requests": 1000,
            "max_requests_jitter": 50,
            **common_options,
        },
    }
    options = env_configs.get(env, env_configs["dev"])
    GunicornApp(application, options).run()
