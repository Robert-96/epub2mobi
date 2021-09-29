import pathlib

import pytest
from loguru import logger


EPUB_FILE = "tests/data/H.+G.+Wells+-+Tales+of+Space+and+Time.epub"
MOBI_FILE = "tests/data/H.+G.+Wells+-+Tales+of+Space+and+Time.mobi"


@pytest.fixture(autouse=True, scope='session')
def setup_logging():
    logger.add("test.log")


@pytest.fixture
def cleanup():
    mobipath = pathlib.Path(MOBI_FILE)
    if mobipath.exists():
        mobipath.unlink()

    yield

    if mobipath.exists():
        mobipath.unlink()
