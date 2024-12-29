from asgiref.sync import SyncToAsync, sync_to_async
from django.db import close_old_connections


class DatabaseSyncToAsync(SyncToAsync):
    """
    SyncToAsync version that cleans up old database connections when it exits.

    Note: It's copy paste from `channels.db.DatabaseSyncToAsync` to not depend on channels

    """

    def thread_handler(self, loop, *args, **kwargs):
        close_old_connections()
        try:
            return super().thread_handler(loop, *args, **kwargs)
        finally:
            close_old_connections()


# The class is TitleCased, but we want to encourage use as a callable/decorator
database_sync_to_async = DatabaseSyncToAsync


async def aclose_old_connections_func():
    return await sync_to_async(close_old_connections)()

def aclose_old_connections(fun, *args, **kwargs):
    async def wrapper():
        await aclose_old_connections_func()
        return await fun(*args, **kwargs)

    return wrapper