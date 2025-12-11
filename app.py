import streamlit as st

def get_title() -> str:
    """
    Return the app title used by the Streamlit UI.
    Kept as a small function so it can be unit tested.
    """
    return "Hello, Streamlit!"

def main() -> None:
    st.title(get_title())
    st.write("This is a minimal starter Streamlit app.")

if __name__ == "__main__":
    main()
