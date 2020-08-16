import json
import re
import tempfile

import pytest
from redis import StrictRedis

from redis_mass_get import (CsvProcessor, JsonProcessor, RedisQuery,
                            TextProcessor)


@pytest.fixture
def temp_file() -> str:
    return tempfile.NamedTemporaryFile(delete=True).name

class MockedRedis:

    def __init__(self):
        self.data = {}

    def add(self, data):
        for k in data.keys():
            self.data[k] = data[k]

    def keys(self, key: str):
        regex_str = f"^{key.replace('*', '.*')}$"
        r = re.compile(regex_str)
        return list([x for x in self.data.keys() if r.match(x)])

    def mget(self, keys: [str]):
        return list([self.data[x] if x in self.data else None for x in keys])


# monkeypatched requests.get moved to a fixture
@pytest.fixture
def mocked_redis(monkeypatch) -> MockedRedis:

    mr = MockedRedis()
    def g(*args, **kwargs):
        return mr

    monkeypatch.setattr(StrictRedis, "from_url", g)
    return mr


@pytest.fixture
def query() -> RedisQuery:
    return RedisQuery(None, False, 1000)


def test_single_value(mocked_redis: MockedRedis, query:RedisQuery):
    mocked_redis.add({
        'a': '1',
        'b': '2',
        'c': '3'
    })
    data = query.query("b")
    assert len(data) == 1
    assert data[0][0] == "b"
    assert data[0][1] == "2"


def test_multiple_values(mocked_redis: MockedRedis, query:RedisQuery):
    mocked_redis.add({
        'product:a': '11',
        'product:b': '22',
        'product:c': '33',
    })
    data = query.query("product:")
    assert len(data) == 3



def test_multiple_values(mocked_redis: MockedRedis, query:RedisQuery):
    mocked_redis.add({
        'product:a': '11',
        'product:b': '22',
        'product:c': '33',
        'something-else': '44'
    })
    data = query.query("product:")
    assert len(data) == 3


def test_csv(temp_file:str, mocked_redis: MockedRedis, query:RedisQuery):
    mocked_redis.add({
        'product:a': '11',
        'product:b': '22',
        'product:c': '33',
        'something-else': '44'
    })

    with CsvProcessor(temp_file) as p:
        query.query_with_processor("product:", p)

    with open(temp_file, "r") as f:
        lines = f.read().splitlines()

    assert lines ==  [
        'key,value', 
        'product:a,11',
        'product:b,22',
        'product:c,33'
    ]


def test_json(temp_file:str, mocked_redis: MockedRedis, query:RedisQuery):

    mocked_redis.add({
        'product:a': '{ "name": "kaas" }',
        'product:b': '{ "name": "kees" }',
        'product:c': '{ "name": "koos" }',
        'something-else': '{ "name": "kies" }',
    })

    with JsonProcessor(temp_file, False) as p:
        query.query_with_processor("product:", p)

    with open(temp_file, "r") as f:
        obj = json.load(f)

    assert obj == [
        {
            "key": "product:a", 
            "value": "{ \"name\": \"kaas\" }"},
        {
            "key": "product:b", 
            "value": "{ \"name\": \"kees\" }"},
        {
            "key": "product:c",
            "value": "{ \"name\": \"koos\" }"}
    ]

def test_json_decoded(temp_file:str, mocked_redis: MockedRedis, query:RedisQuery):
    mocked_redis.add({
        'product:a': '{ "name": "kaas" }',
        'product:b': '{ "name": "kees" }',
        'product:c': '{ "name": "koos" }',
        'something-else': '{ "name": "kies" }',
    })

    with JsonProcessor(temp_file, True) as p:
        query.query_with_processor("product:", p)

    with open(temp_file, "r") as f:
        obj = json.load(f)

    assert obj == [
        {
            "key": "product:a", 
            "value": { "name": "kaas" }
        },
        {
            "key": "product:b", 
            "value": { "name": "kees" }
        },
        {
            "key": "product:c",
            "value": { "name": "koos" }
        }
    ]


def test_txt(temp_file:str, mocked_redis: MockedRedis, query:RedisQuery):

    mocked_redis.add({
        'product:a': '11',
        'product:b': '22',
        'product:c': '33',
        'something-else': '44'
    })

    with TextProcessor(temp_file) as p:
        query.query_with_processor("product:", p)

    with open(temp_file, "r") as f:
        lines = f.read().splitlines()

    assert lines ==  [
        'product:a',
        '11',
        'product:b',
        '22',
        'product:c',
        '33'
    ]
