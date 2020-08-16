import argparse
from . import TextProcessor, CsvProcessor, JsonProcessor, TextProcessor, RedisQuery

def print_result(answer: str, verbose: bool, action: str, word: str):
    if answer:
        print(answer)
    elif verbose:
        print(f"Could not {action} '{word}'.")


def main():

    parser = argparse.ArgumentParser(description="""Queries Redis using KEYS and MGET. This will efficiently retreive all keys and values.
    They can be stored/visualized in different modes:
    - text (default): odd lines are keys, even lines values.
    - csv: comma-separated format.
    - json: JSON-array. Use -jd to decode the JSON value.
    """)
    parser.add_argument("url", help="Full Redis URL.")
    parser.add_argument('key', help='The key to query on.')
    parser.add_argument("-q",  "--quiet", help="Don't show information about the progress.", action="store_true")
    parser.add_argument("-f",  "--format", help="The format in which the keys of values should be.", choices=["text", "csv", "json"], default="x")
    parser.add_argument("-d",  "--destination", help="Writes the output to a file.", default=None)
    parser.add_argument("-jd",  "--json_decode", help="Enables JSON decode when writing to JSON.", action="store_true")
    parser.add_argument("-c", "--chuncks", help="How many keys should be queried at once? Default is 10,000.", default=10000)

    args = parser.parse_args()
    json_decode = args.json_decode
    destination = "stdout" if not args.destination else args.destination
    quiet = destination == "stdout" or args.quiet

    if args.format == "x":
        if destination.endswith(".csv"):
            args.format = "csv"
        elif destination.endswith(".json"):
            args.format = "json"
        else:
            args.format = "txt"

    processor = (
        CsvProcessor(destination) if args.format == "csv" else
        JsonProcessor(destination, json_decode) if args.format == 'json' else
        TextProcessor(destination)
    )

    q = RedisQuery(
        args.url,
        not quiet,
        int(args.chuncks))

    with processor as p:
        q.query_with_processor(args.key, p)


if __name__ == "__main__":
    main()