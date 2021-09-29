from .conftest import EPUB_FILE, MOBI_FILE
from epub2mobi.convert import is_epub, is_mobi


def test_is_epub():
    assert is_epub(EPUB_FILE)


def test_is_mobi():
    assert is_mobi(MOBI_FILE)
