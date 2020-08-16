from typing import Tuple

from .ProcessorBase import ProcessorBase


class MemoryProcessor(ProcessorBase):

    def __init__(self):
        super().__init__()
        self.data: [Tuple[str, str]] = []

    def process(self, data: [Tuple[str, str]]):

        if not self.data:
            self.data = []
        
        self.data.extend(data)
