from asgiref.sync import sync_to_async
from django.db.transaction import Atomic

from src.core.db import aclose_old_connections


class AsyncAtomicContextManager(Atomic):
    def __init__(self, using=None, savepoint=True, durable=False):
        super().__init__(using, savepoint, durable)

    async def __aenter__(self):
        await sync_to_async(super().__enter__)()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await sync_to_async(super().__exit__)(exc_type, exc_value, traceback)


aatomic_manager = AsyncAtomicContextManager()


def aatomic(fun, *args, **kwargs):
    async def wrapper(*aargs, **akwargs):
        async with aatomic_manager:
            return await fun(*aargs, **akwargs)

    return wrapper


def safe_aatomic(func):
    @aclose_old_connections
    @aatomic
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
