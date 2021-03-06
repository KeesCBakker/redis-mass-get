# Redis Mass Get

Queries your Redis using KEYS and MGET to write the key/value to the _stdout_ or a file. It supports the formats: text, json and csv.


## Installation
Install from PIP:
```bash
pip install redis-mass-get
```


### CLI usage
The project can be used as a CLI tool:
```txt
usage: redis-mass-get [-h] [-q] [-f {text,csv,json}] [-d DESTINATION] [-jd] [-c CHUNCKS] [-och] url key

Queries Redis using KEYS and MGET. This will efficiently retreive all keys and values. They can be stored/visualized in different modes: - text (default): odd lines are keys, even lines values. - csv: comma-separated format. - json: JSON-array. Use -jd to decode the JSON value.

positional arguments:
  url                   Full Redis URL.
  key                   The key to query on.

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Don't show information about the progress.
  -f {text,csv,json}, --format {text,csv,json}
                        The format in which the keys of values should be.
  -d DESTINATION, --destination DESTINATION
                        Writes the output to a file.
  -jd, --json_decode    Enables JSON decode when writing to JSON.
  -c CHUNCKS, --chuncks CHUNCKS
                        How many keys should be queried at once? Default is 10,000.
  -och, --omit_csv_header
                        Don't render a CSV header.
```

The alias `rmg` or `redis_mass_get` will work as well in the console.


### API
The API can be used like this:

```python
from redis_mass_get import RedisQuery

# pluralize will return the result or None
q = RedisQuery("redis://my.amazing.redis.url")

# query data 
data = q.query("prefix*")
# data is returned as:
# [(key1, value1), (key2, value2)]

# write data to file
# TXT:
q.query_and_write_csv(self, "prefix*", "my.file.path.txt")

# CSV:
q.query_and_write_csv(self, "*postfix", "my.file.path.csv")

# JSON
q.query_and_write_csv(self, "*contains*", "my.file.path.csv", parse_value_as_json=True)
```

You could also write your own implementation of `ProcessorBase` and call `query_with_processor`.


## Development
If you want to contribute to local development, please consult <a href="https://github.com/KeesCBakker/redis-mass-get/blob/master/DEV.md">the local development page</a>. More information
on the reasoning behind this package can be found at this blog: <a href="https://keestalkstech.com/2020/08/reading-multiple-key-values-from-redis/">Reading multiple key/values from Redis</a>.


