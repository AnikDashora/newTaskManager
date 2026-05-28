import streamlit as st

from session_state.app_state import initialize_app_state
from view.dashboard import dashboard
from view.settings import settings

def main():
    initialize_app_state()

    if(st.session_state['current_page'] == 0):
        dashboard()
    elif(st.session_state['current_page'] == 1):
        pass
    elif(st.session_state['current_page'] == 2):
        pass
    elif(st.session_state['current_page'] == 3):
        settings()

if __name__ == "__main__":
    main()