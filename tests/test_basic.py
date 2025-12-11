"""Basic tests for the Streamlit app."""
import sys
import os

# Add parent directory to path to import app module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import get_title


def test_get_title_returns_non_empty_string():
    """Test that get_title returns a non-empty string."""
    title = get_title()
    assert isinstance(title, str)
    assert len(title) > 0


def test_get_title_contains_streamlit():
    """Test that get_title contains the word 'Streamlit'."""
    title = get_title()
    assert "Streamlit" in title
