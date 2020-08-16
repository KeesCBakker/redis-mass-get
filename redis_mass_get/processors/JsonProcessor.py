import json
from typing import Tuple

from .exceptions import ProcessorStreamNotOpenedException
from .TextProcessor import TextProcessor


class JsonProcessor(TextProcessor):

    def __init__(self, file: str, parse_value_as_json: bool):
        super().__init__(file)
        self.__parse_value_as_json = parse_value_as_json
        self.__first = True

    def open_stream(self):
        super().open_stream()
        self._destination.write("[")

    def close_stream(self):
        self._destination.write("]")
        super().close_stream()

    def process(self, data: [Tuple[str, str]]):

        if not self._destination:
            raise ProcessorStreamNotOpenedException("Stream is not open.")

        for d in data:

            if self.__first:
                self.__first = False
            else:
                self._destination.write(",")

            value = d[1]
            if self.__parse_value_as_json:
                value = json.loads(value)

            obj = {'key': d[0], 'value':  value }
            json.dump(obj, self._destination)
