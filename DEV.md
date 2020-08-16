# Local Development

## Stack
I'm using the following stack to develop this package:
- <a href="https://pypi.org/project/pipenv/">Pipenv</a>
- <a href="https://code.visualstudio.com/">Visual Studio Code</a>

## Kickstart local development
Please do the following:

1. Make sure you have <a href="https://pypi.org/project/pipenv/">Pipenv</a> installed.
1. Create virtual env: `pipenv --python 3.8`
1. If you are using Visual Studio code, run `pipenv run python -c "import sys;print(sys.executable)"` and add the path to `python.pythonPath` in your `.vscode\settings.json` file.
1. Install dependencies using: `pipenv sync --dev`.
1. To update depencencies to the latest version: `pipenv update`.

## Trigger tests
Some hints on testing:

1. Make sure your local development is set up correctly.
1. Run `pipenv run python -m pytest`
1. Make sure test files are prefixed with `test_`.
1. To run tests that match the _json_: `pipenv run python -m pytest -k json`. You can add `-vv` for a detailed overview.
