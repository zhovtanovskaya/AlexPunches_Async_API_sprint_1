from abc import ABC, abstractmethod


class AsyncSearchEngine(ABC):
    @abstractmethod
    async def get(self, id: str, **kwargs):
        pass

    @abstractmethod
    async def search(self, **kwargs):
        pass

    @abstractmethod
    async def open_point_in_time(self, index: str, keep_alive: str, **kwargs):
        pass
