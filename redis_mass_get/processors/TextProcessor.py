import json
import sys
from typing import Tuple

from .ProcessorBase import ProcessorBase
from .exceptions import ProcessorStreamNotOpenedException

class TextProcessor(ProcessorBase):

    def __init__(self, file: str):
        super().__init__()
        self.__file = file

    def open_stream(self):
        if self.__file == 'stdout':
            self._destination = sys.stdout
        else:
            self._destination = open(self.__file, 'w', newline='\n', encoding='utf-8')

    def close_stream(self):
        if self._destination != sys.stdout:
            self._destination.close()

    def __enter__(self):
        self.open_stream()
        return self

    def __exit__(self, type, value, traceback):
        self.close_stream()
        return super().__exit__(type, value, traceback)

    def process(self, data: [Tuple[str, str]]):

        if not self._destination:
            raise ProcessorStreamNotOpenedException("Stream is not open.")

        for d in data:
            self._destination.write(d[0])
            self._destination.write("\n")
            self._destination.write(d[1])
            self._destination.write("\n")
