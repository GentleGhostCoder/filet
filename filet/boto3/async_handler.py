"""AsyncHandler Module - Creates and handles async sessions."""

import asyncio

import nest_asyncio
import uvloop


class AsyncHandler:
    """Create and handle an async session.

    :Example:

    .. code-block:: python

        >>> handler = AsyncHandler(limit_concurrency_count=5)
        >>> loop = handler.event_loop  # xdoctest: +SKIP
        >>> semaphore = handler.semaphore  # xdoctest: +SKIP
    """

    nest_asyncio.apply()
    uvloop.install()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    def __init__(self, limit_concurrency_count: int = 5, **kwargs):
        """Initialize the handler.

        :param limit_concurrency_count: Limit the number of concurrent operations.
        :type limit_concurrency_count: int
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.__semaphore = asyncio.BoundedSemaphore(limit_concurrency_count)
        self.__event_loop = asyncio.get_event_loop()

    @property
    def event_loop(self):
        """Close a running loop or start a new one and return the event loop.

        :return: The event loop.
        :rtype: asyncio.AbstractEventLoop

        :Example:

        .. code-block:: python

            >>> handler = AsyncHandler()
            >>> loop = handler.event_loop  # xdoctest: +SKIP
        """
        if self.__event_loop.is_running():
            self.__event_loop.close()
        if self.__event_loop.is_closed():
            self.__event_loop = asyncio.new_event_loop()
        return self.__event_loop

    @property
    def semaphore(self):
        """Get the semaphore for the async session.

        :return: The semaphore for the async session.
        :rtype: asyncio.BoundedSemaphore

        :Example:

        .. code-block:: python

            >>> handler = AsyncHandler()
            >>> semaphore = handler.semaphore  # xdoctest: +SKIP
        """
        return self.__semaphore
