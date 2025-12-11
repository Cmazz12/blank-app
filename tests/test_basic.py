from app import get_title


def test_get_title_non_empty_and_contains_streamlit():
    title = get_title()
    assert isinstance(title, str)
    assert len(title) > 0
    assert "Streamlit" in title
