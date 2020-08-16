from csv import DictWriter
from typing import Tuple

from .exceptions import ProcessorStreamNotOpenedException
from .TextProcessor import TextProcessor


class CsvProcessor(TextProcessor):

    def __init__(self, file: str):
        super().__init__(file)

    def open_stream(self):
        super().open_stream()
        fieldnames = ['key', 'value']
        self.__writer = DictWriter(self._destination, fieldnames=fieldnames)
        self.__writer.writeheader()

    def process(self, data: [Tuple[str, str]]):

        if not self._destination:
            raise ProcessorStreamNotOpenedException("Stream is not open.")

        for d in data:
            self.__writer.writerow({
                'key': d[0], 
                'value': d[1]
            })
