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
    kpi,graph = st.columns(2)
    with kpi:
        st.header("kpi card settings")

        st.toggle("Show completion trend", key="show_completion_trend")
        st.toggle("Show Total Progress", key="show_total_progress")
        st.toggle("Show Average Completion", key="show_average_completion")
        st.toggle("Show Today's Progress", key="show_today_progress")
        st.toggle("Show active days", key="show_active_days")
        st.toggle("Show Monthly Rate", key="show_monthly_rate")
        st.toggle("Show Needs Attention", key="show_needs_attention")
        st.toggle("Show Productivity Streak", key="show_productivity_streak")
        st.toggle("Show Weekly Rate", key="show_weekly_rate")
    
    with graph:
        st.header("Graph settings")
        st.toggle("Show Task Type Distribution", key="show_task_type_distribution")
        st.toggle("Show Weekly Progress", key="show_weekly_progress")
        st.toggle("Show Monthly Progress", key="show_monthly_progress")
        st.toggle("Show Productivity Streak", key="show_productivity_streak_graph")




