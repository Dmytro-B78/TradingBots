import pytest
import logging
from bot_ai.core import logging_setup

def test_default_logger_creation():
    logger = logging_setup.setup_logging()
    assert isinstance(logger, logging.Logger)
    assert logger.level == logging.INFO

def test_logger_with_custom_level():
    logger = logging_setup.setup_logging(level='DEBUG')
    assert logger.level == logging.DEBUG

def test_logger_with_file(tmp_path):
    log_file = tmp_path / "test.log"
    logger = logging_setup.setup_logging(log_file=log_file)
    logger.info("test message")
    logger.handlers[-1].flush()
    content = log_file.read_text(encoding='utf-8')
    assert "test message" in content

def test_logger_format(monkeypatch):
    records = []
    class DummyHandler(logging.Handler):
        def emit(self, record):
            records.append(record)
    logger = logging_setup.setup_logging()
    logger.addHandler(DummyHandler())
    logger.info("format test")
    assert any("format test" in r.getMessage() for r in records)
