# epub2mobi

Simple CLI tool that converts all the `.epub` files in a directory tree to `.mobi` files.

## Prerequisites

This script uses Calibri CLI tools to convert `.epub` files to `.mobi`.

## Install

```
$ pip install -e .
```

## Usage

```
$ epub2mobi . --output dist/
```

## Tests

```
$ pip install -r requirements-dev.txt
$ pytest tests
```

## License

This project is licensed under the [MIT License](LICENSE).
