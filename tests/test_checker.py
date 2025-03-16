import pytest
from src.checker.technical_writing_checker import TechnicalWritingChecker

@pytest.fixture
def checker():
    return TechnicalWritingChecker()

def test_check_text_basic(checker):
    text = "Turn shaft assembly."
    result = checker.check_text(text)
    assert result.improved_text != ""
    assert isinstance(result.violations, list)

@pytest.mark.asyncio
async def test_check_text_async(checker):
    text = "Turn shaft assembly."
    result = await checker.check_text_async(text)
    assert result.improved_text != ""
    assert isinstance(result.violations, list)

