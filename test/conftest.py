# test/conftest.py
import os
import pytest
from pathlib import Path

@pytest.fixture
def tmp_output(tmp_path):
    return tmp_path

@pytest.fixture(autouse=True)
def ensure_api_key():
    """Ensure NEWS_API_KEY is present. Skip tests if missing."""
    if "NEWS_API_KEY" not in os.environ:
        pytest.skip("NEWS_API_KEY not set — skipping real API tests")
