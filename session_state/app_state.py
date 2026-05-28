import streamlit as st
import numpy as np
import pandas as pd


def initialize_app_state():
    if 'pages'not in st.session_state:
        st.session_state['pages'] = ['Dashboard','Tasks','Calendar','Settings']

    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 0
    

def to_dashboard():
    st.session_state['current_page'] = 0

def to_tasks():
    st.session_state['current_page'] = 1

def to_calendar():
    st.session_state['current_page'] = 2
    
def to_settings():
    st.session_state['current_page'] = 3


    