import streamlit as st


def get_title():
    """Return the application title."""
    return "Hello, Streamlit!"


if __name__ == "__main__":
    st.title(get_title())
