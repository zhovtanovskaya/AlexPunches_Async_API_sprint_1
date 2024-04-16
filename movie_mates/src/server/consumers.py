from importlib import import_module
from typing import Callable


class Consumers:

    consumers: dict = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Consumers, cls).__new__(cls)
        return cls.instance

    def add(self, func, alias: str):
        if alias in self.consumers:
            raise Exception("Duplicate consumer " + alias)
        self.consumers[alias] = func

    def get(self, alias):
        return self.consumers.get(alias, None)

    @staticmethod
    def include(*args: str):
        for module_name in args:
            import_module(module_name)


def consumer() -> Callable:
    def func_wrapper(func):
        # print()
        print('@consumer')
        Consumers().add(func, func.__name__)
        return func
    return func_wrapper

