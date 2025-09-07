import pytest
from config.settings import settings

@pytest.mark.skipif(not settings.TEST_MODE, reason="测试模式未启用")

def test_placeholder():
    """
    A placeholder test to ensure pytest runs correctly.
    """
    assert True
