from importlib import import_module
from typing import Callable


class Consumers:

    consumers = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Consumers, cls).__new__(cls)
        return cls.instance

    def add(self, func, alias: str):
        self.consumers[alias] = func

    def get(self, alias):
        return self.consumers.get(alias, None)

    @staticmethod
    def include(*args: str):
        for module_name in args:
            import_module(module_name)


def consumer(alias: str) -> Callable:
    def func_wrapper(func):
        print('@consumer')
        Consumers().add(func, alias)
        return func
    return func_wrapper

