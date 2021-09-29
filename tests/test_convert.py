import pathlib

import pytest

from epub2mobi.convert import epub2mobi, is_epub, is_mobi


EPUB_FILE = "tests/data/H.+G.+Wells+-+Tales+of+Space+and+Time.epub"
MOBI_FILE = "tests/data/H.+G.+Wells+-+Tales+of+Space+and+Time.mobi"


@pytest.fixture
def cleanup():
    mobipath = pathlib.Path(MOBI_FILE)
    if mobipath.exists():
        mobipath.unlink()

    yield

    if mobipath.exists():
        mobipath.unlink()


def test_is_epub():
    assert is_epub(EPUB_FILE)


def test_is_mobi():
    assert is_mobi(MOBI_FILE)


def test_epub2mobi(cleanup):
    epub2mobi(EPUB_FILE)
    assert pathlib.Path(MOBI_FILE).exists()
