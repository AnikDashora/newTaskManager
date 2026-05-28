import streamlit as st
import os
import sys
import random
import pandas as pd
import numpy as np
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

root_variable = [# 0 for light , 1 for dark
    """:root{
        --page-bg: #f7f9f8;
        --header-bg: rgba(255, 255, 255, 0.75);
        --header-border: rgba(255, 255, 255, 0.85);
        --header-inner-shadow: rgba(255, 255, 255, 1);
        --text-main: #3b423f;
        --text-label: #8a9691;
        --text-muted: #74807a;
        --icon-color: #83928c;
        --nav-hover-bg: rgba(240, 245, 243, 0.8);
        --nav-active-bg: rgba(255, 255, 255, 0.95);
        --nav-active-text: #50665d;
        --nav-active-shadow: 0 4px 14px -3px rgba(80, 102, 93, 0.12), inset 0 0 0 1px rgba(255, 255, 255, 0.6);
        --accent-lavender: #eeeef3;
        --accent-lavender-icon: #928ba5;
        --badge-color: #e2a1a1;
        --online-color: #a4ceb5;
        --gradient-1: rgba(225, 234, 242, 0.6);
        --gradient-2: rgba(228, 238, 232, 0.6);
        --center-bg: rgba(246, 248, 247, 0.6);
        --center-border: rgba(255, 255, 255, 0.5);
        --action-hover-bg: rgba(255, 255, 255, 0.7);
        --profile-bg: rgba(255, 255, 255, 0.4);
        --profile-hover-bg: rgba(255, 255, 255, 0.95);
        --profile-hover-border: #fff;
        --avatar-bg: #e5e3de;
        --avatar-icon: #868074;

        /* KPI Icon Colors */
        --ig-bg: #e5efe9;
        --ig-fg: #55856b;
        --ib-bg: #e4edf5;
        --ib-fg: #5c7b9c;
        --is-bg: #e8eee8;
        --is-fg: #6b8270;
        --it-bg: #e2f0ee;
        --it-fg: #4a9189;
        --ir-bg: #f5e8e8;
        --ir-fg: #9c5a5a;
        --ia-bg: #f5ede0;
        --ia-fg: #9c7442;
        --il-bg: #edeaf5;
        --il-fg: #7d7096;
        --ik-bg: #e0eff7;
        --ik-fg: #4d8aaa;
        }
    """,
    """:root{
        --page-bg: #1c1f1d;
        --header-bg: rgba(45, 51, 48, 0.75);
        --header-border: rgba(90, 100, 95, 0.4);
        --header-inner-shadow: rgba(255, 255, 255, 0.05);
        --text-main: #e2e8e5;
        --text-label: #949a97;
        --text-muted: #949a97;
        --icon-color: #a0aba5;
        --nav-hover-bg: rgba(65, 75, 70, 0.8);
        --nav-active-bg: rgba(75, 87, 81, 0.95);
        --nav-active-text: #d8ede3;
        --nav-active-shadow: 0 4px 14px -3px rgba(0, 0, 0, 0.3), inset 0 0 0 1px rgba(255, 255, 255, 0.1);
        --accent-lavender: #32303c;
        --accent-lavender-icon: #b8afcd;
        --badge-color: #c96b6b;
        --online-color: #72a888;
        --gradient-1: rgba(45, 61, 75, 0.5);
        --gradient-2: rgba(47, 65, 55, 0.5);
        --center-bg: rgba(35, 41, 38, 0.6);
        --center-border: rgba(255, 255, 255, 0.08);
        --action-hover-bg: rgba(255, 255, 255, 0.1);
        --profile-bg: rgba(255, 255, 255, 0.05);
        --profile-hover-bg: rgba(255, 255, 255, 0.12);
        --profile-hover-border: rgba(255, 255, 255, 0.2);
        --avatar-bg: #2d3330;
        --avatar-icon: #a0aba5;

        /* Dark mode KPI Colors */
        --ig-bg: #1f3a2f;
        --ig-fg: #7fbb99;
        --ib-bg: #1f2f42;
        --ib-fg: #8aacce;
        --is-bg: #1f3a1f;
        --is-fg: #94b88a;
        --it-bg: #1f3a37;
        --it-fg: #72bfb0;
        --ir-bg: #3a1f1f;
        --ir-fg: #d48585;
        --ia-bg: #3a2a1f;
        --ia-fg: #d4a668;
        --il-bg: #2a1f3a;
        --il-fg: #b3a4ce;
        --ik-bg: #1f3a4d;
        --ik-fg: #7fb5d4;
        }
    """
]

remove_header_footer = """
    #MainMenu {visibility: hidden;}

    header {visibility: hidden;}

    footer {visibility: hidden;}

    /* Hide the orange loading progress bar */
    div[data-testid="stDecoration"] {
        display: none !important;
    }

    .stDeployButton{
        display:none;
    }

    /* Remove top padding to avoid white space */
    .block-container {
        padding-top: 1rem !important;
    }

"""

page_setup = """
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    body {
        background: var(--page-bg);
        font-family: 'Outfit', sans-serif;
        color: var(--text-main);
        min-height: 100vh;
        padding: 32px 24px;
        transition: background-color 0.4s ease, color 0.4s ease;
        background-image:
            radial-gradient(circle at 10% 40%, var(--gradient-1), transparent 25%),
            radial-gradient(circle at 90% 20%, var(--gradient-2), transparent 25%);
    }
    .stAppViewContainer{
        background: var(--page-bg);
        font-family: 'Outfit', sans-serif;
        color: var(--text-main);
        min-height: 100vh;
        padding: 0px;
        transition: background-color 0.4s ease, color 0.4s ease;
        background-image:
            radial-gradient(circle at 10% 40%, var(--gradient-1), transparent 25%),
            radial-gradient(circle at 90% 20%, var(--gradient-2), transparent 25%);
    }

"""

header_style = """
    .st-emotion-cache-1w723zb{
        max-width:1160px;
    }
    .st-key-header-container {
        max-width: 1160px;
        margin: 0 auto 32px;
    }
    
    .st-emotion-cache-3o718f{
        margin-bottom:0px;
    }

    .st-key-dashboard-header {
        display: flex;
        flex-direction:row !important;
        align-items: center;
        justify-content: space-between;
        height: 76px;
        padding: 0 16px 0 24px;
        background: var(--header-bg);
        backdrop-filter: blur(24px);
        border: 1px solid var(--header-border);
        border-radius: 28px;
        box-shadow:
            0 16px 42px -12px rgba(0, 0, 0, 0.1),
            0 4px 12px -4px rgba(0, 0, 0, 0.06),
            inset 0 1px 1px var(--header-inner-shadow);
    }

    .header-left,
    .st-key-header-right {
        display: flex;
        align-items: center;
        
    }
    .app-name{
        font-size:1.25rem!important;
        padding:1rem !important;
        font-weight:500!important;
    }

    .st-key-header-right {
        flex-direction:row !important;
        justify-content: center;
        gap: 12px;
    }

    .st-key-header-right > .st-emotion-cache-3pwa5w{
        width:fit-content;
    }

    .app-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 44px;
        height: 44px;
        background: var(--accent-lavender);
        border-radius: 16px;
        color: var(--accent-lavender-icon);
        box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.8);
    }

    .app-icon svg {
        width: 22px;
        height: 22px;
        stroke-width: 2.2px;
        stroke: currentColor;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    .st-key-header-center {
        display: flex;
        flex-direction:row !important;
        justify-content:center !important;
        gap: 6px;
        padding: 0px;
        background: var(--center-bg);
        border-radius: 24px;
        border: 1px solid var(--center-border);
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.015);
    }

    [class*="st-key-nav-button"] {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border: none;
        background: transparent;
        border-radius: 18px;
        color: var(--icon-color);
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    [class*="st-key-nav-button"] svg {
        width: 22px;
        height: 22px;
        stroke-width: 1.8px;
        stroke: currentColor;
        fill: none;
        transition: transform 0.25s ease;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    [class*="st-key-nav-button"]:hover {
        background: var(--nav-hover-bg);
        color: var(--text-main);
    }

    [class*="st-key-nav-button"] svg {
        transform: scale(1.08);
    }

    [class*="st-key-nav-button"].active {
        background: var(--nav-active-bg);
        color: var(--nav-active-text);
        box-shadow: var(--nav-active-shadow);
    }

    [class*="st-key-nav-button"].active svg {
        stroke-width: 2.2px;
    }

    [class*="st-key-action-button"] {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 46px;
        height: 46px;
        border: none;
        background: transparent;
        border-radius: 16px;
        color: var(--icon-color);
        cursor: pointer;
        position: relative;
        transition: all 0.25s ease;
    }

    [class*="st-key-action-button"]:hover {
        background: var(--action-hover-bg);
        color: var(--text-main);
    }

    [class*="st-key-action-button"] svg {
        width: 20px;
        height: 20px;
        stroke-width: 1.8px;
        stroke: currentColor;
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
    }

    .notification-dot {
        position: absolute;
        top: 11px;
        right: 12px;
        width: 7.5px;
        height: 7.5px;
        background: var(--badge-color);
        border-radius: 50%;
        border: 1.5px solid var(--header-bg);
    }

    .profile-trigger {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 6px 16px 6px 6px;
        border: 1px solid transparent;
        background: var(--profile-bg);
        border-radius: 22px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .profile-trigger:hover {
        background: var(--profile-hover-bg);
        border-color: var(--profile-hover-border);
        box-shadow: 0 6px 18px -4px rgba(0, 0, 0, 0.04);
        transform: translateY(-1px);
    }

    .avatar-wrapper {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 38px;
        height: 38px;
        border-radius: 16px;
    }

    .avatar-wrapper svg {
        width: 38px;
        height: 38px;
        border-radius: 16px;
        background: var(--avatar-bg);
        stroke: var(--avatar-icon);
        stroke-width: 1.5px;
        fill: none;
        padding: 6px;
    }

    .online-indicator {
        position: absolute;
        bottom: -1px;
        right: -1px;
        width: 11px;
        height: 11px;
        background: var(--online-color);
        border-radius: 50%;
        border: 2px solid var(--header-bg);
        z-index: 10;
    }

    .profile-name {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .username {
        font-size: 14.5px;
        font-weight: 500;
        color: var(--text-main);
    }

    .dropdown-icon {
        width: 16px;
        height: 16px;
        color: #9ba7a2;
    }

"""

def settings():
    final_style = f"""
    <style>
    {root_variable[1]}
    {remove_header_footer}
    {page_setup}
    {header_style}
    </style>
    """
    st.markdown(final_style, unsafe_allow_html=True)
    with st.container(key = "header-container"):
        with st.container(key = "dashboard-header"):
            st.markdown(
                """
                <div class="header-left">
                    <div class="app-icon">
                        <svg viewBox="0 0 24 24">
                            <path d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z" />
                        </svg>
                    </div>
                    <h1 class="app-name">Productivity Dashboard</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.container(key = "header-center"):
                st.button(
                    label = "",
                    key = "nav-button-1",
                    type = "tertiary",
                    icon = ":material/dashboard:"
                )
                st.button(
                    label = "",
                    key = "nav-button-2",
                    type = "tertiary",
                    icon = ":material/task:"
                )
                st.button(
                    label = "",
                    key = "nav-button-3",
                    type = "tertiary",
                    icon = ":material/trending_up:"
                )
                st.button(
                    label = "",
                    key = "nav-button-4",
                    type = "tertiary",
                    icon = ":material/calendar_today:"
                )
                st.button(
                    label = "",
                    key = "nav-button-5",
                    type = "tertiary",
                    icon = ":material/instant_mix:"
                )

            with st.container(key = "header-right"):
                st.button(
                    label = "",
                    key = "action-button-1",
                    type = "tertiary",
                    icon = ":material/dark_mode:"
                )
                st.button(
                    label = "",
                    key = "action-button-2",
                    type = "tertiary",
                    icon = ":material/notifications:"
                )
                st.markdown(
                    """
                    <div class="profile-trigger" aria-label="User Menu">
                        <div class="avatar-wrapper">
                            <svg viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
                                <circle cx="12" cy="7" r="4" />
                            </svg>
                            <div class="online-indicator"></div>
                        </div>
                        <div class="profile-name">
                            <span class="username">Anik Dashora</span>
                            <svg class="dropdown-icon" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
                                fill="none" stroke-linecap="round" stroke-linejoin="round">
                                <path d="m6 9 6 6 6-6" />
                            </svg>
                        </div>
                    </div>
                    """
                    ,unsafe_allow_html = True
                )
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




