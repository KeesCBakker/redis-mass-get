from typing import Tuple

from redis import StrictRedis

from .processors.CsvProcessor import CsvProcessor
from .processors.JsonProcessor import JsonProcessor
from .processors.MemoryProcessor import MemoryProcessor
from .processors.ProcessorBase import ProcessorBase
from .processors.TextProcessor import TextProcessor

p = print

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

class RedisQuery:

    def __init__(self, url: str, verbose: bool = False, chunks: int = 10000):

        self.__verbose = verbose
        self.__chucks = chunks

        self.print("Connecting... ")
        self.__client = StrictRedis.from_url(url, decode_responses=True)


    def print(self, msg: str, end:str="\n"):
        if self.__verbose:
            p(msg, end=end)


    def query(self, key) -> [Tuple[str, str]]:
        m = MemoryProcessor()
        self.query_with_processor(key, m)
        return m.data

    def query_with_processor(self, key, processor: ProcessorBase):

        self.print("Reading keys... ", end="")

        if not "*" in key:
            key = f"*{key}*"
        
        keys = self.__client.keys(key)
        self.print(f"{len(keys):,} keys found.")

        partitions = list(chunks(keys, self.__chucks))

        for i in range(0, len(partitions)):
            perf = (i/len(partitions)) * 100
            self.print(f"\rProcessing values... {perf:.2f}%", end="")

            partition_keys = partitions[i]
            values = self.__client.mget(partition_keys)

            data = zip(partition_keys, values)

            processor.process(data)

        self.print("\rProcessing values... 100.00%")
        self.print("Done!")

    def query_and_write_csv(self, key: str, file: str):
        with CsvProcessor(file) as p:
            self.query_with_processor(key, p)

    def query_and_write_json(self, key: str, file: str, parse_value_as_json: bool):
        with JsonProcessor(file, parse_value_as_json) as p:
            self.query_with_processor(key, p)

    def query_and_write_txt(self, key: str, file: str):
        with TextProcessor(file) as p:
            self.query_with_processor(key, p)