import streamlit as st
import os
import sys
import random
import pandas as pd
import numpy as np
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

def settings():
    st.title("Settings")
    st.write("This is the settings page. You can customize your dashboard here.")
    st.write("More settings options will be added in future updates.")  

    st.write("kpi card settings")

    st.toggle("Show completion trend", key="show_completion_trend")
    st.toggle("Show active days", key="show_active_days")



settings()