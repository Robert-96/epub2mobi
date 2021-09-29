import pathlib

from .conftest import EPUB_FILE, MOBI_FILE
from epub2mobi.convert import epub2mobi


def test_epub2mobi(cleanup):
    epub2mobi(EPUB_FILE)
    assert pathlib.Path(MOBI_FILE).exists()
