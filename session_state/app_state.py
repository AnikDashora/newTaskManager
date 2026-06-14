import streamlit as st
import numpy as np
import pandas as pd


def initialize_app_state():
    if 'pages'not in st.session_state:
        st.session_state['pages'] = ['Dashboard','Tasks','Calendar','Settings']

    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 0

    if 'theme' not in st.session_state:
        st.session_state['theme'] = 0
    
    if('settings' not in st.session_state):
        st.session_state['settings'] = {
            'Todays Progress': True,
            'Completion Trend': True,
            'Average Completion': True,
            'Productivity Streak': True,
            'Total Progress': False,
            'Active Days': False,
            'Monthly Rate': False,
            'Needs Attention': False,
            'Weekly Rate': False,
            'Goal Hit Rate': False,
            'Output Volume': False,
            'LeetCode Total Solved': True,
            'LeetCode Acceptance Rate': True,
            'LeetCode Submission': True,
            'LeetCode Streak': True,
            'LeetCode Topics Coverage': False,
            'LeetCode Languages Used': False
        }
    

def to_dashboard():
    st.session_state['current_page'] = 0

def to_tasks():
    st.session_state['current_page'] = 1

def to_calendar():
    st.session_state['current_page'] = 2
    
def to_settings():
    st.session_state['current_page'] = 3

def change_kpi_setting(kpi_name):
    st.session_state['settings'][kpi_name] = not st.session_state['settings'][kpi_name]