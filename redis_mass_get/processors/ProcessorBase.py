from abc import ABC
from typing import Tuple


class ProcessorBase(ABC):
    def process(self, data: [Tuple[str, str]]):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
