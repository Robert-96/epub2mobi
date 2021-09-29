import pytest
from loguru import logger


@pytest.fixture(autouse=True, scope='session')
def setup_logging():
    logger.add("test.log")
