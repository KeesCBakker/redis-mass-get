__version__ = "0.0.11"

__all__ = ['RedisQuery', 'CsvProcessor', 'JsonProcessor',
           'MemoryProcessor', 'TextProcessor']

from .processors.CsvProcessor import CsvProcessor
from .processors.JsonProcessor import JsonProcessor
from .processors.MemoryProcessor import MemoryProcessor
from .processors.TextProcessor import TextProcessor
from .query import RedisQuery