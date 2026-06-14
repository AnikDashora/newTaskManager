import streamlit as st
import os
import sys
import random
import pandas as pd
import numpy as np

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from streamlit_echarts import st_echarts
from datetime import datetime, timedelta, date

from components.metrics import active_days_metric, completion_trend_metric,average_completion_metric, goal_hit_rate_metric, leetcode_acceptance_rate_metric, leetcode_languages_used_metric, leetcode_submission_metric, leetcode_topics_coverage_metric, leetcode_total_solved_metric, monthly_rate_metric, needs_attendtion_metric, output_volume_metric, todays_progress_metric,total_progress_metric, weekly_rate_metric,productivity_streak_metric,leetcode_streak_metric
from session_state.app_state import to_calendar, to_settings, to_tasks
from services.tasks_service import fetch_leetcode_data, fetch_tasks_data

def change_theme():
    st.session_state['theme'] = 1 - st.session_state['theme']

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
        --ip-bg: #f0e8f5;
        --ip-fg: #8c5a9c;
        --im-bg: #e8f5f0;
        --im-fg: #3a9070;
        --io-bg: #fff4e0;
        --io-fg: #c07c10;
        --lc-easy: #3a9070;
        --lc-mid: #c07c10;
        --lc-hard: #9c5a5a;
        --lc-easy-bg: #e2f0ec;
        --lc-mid-bg: #fff0d6;
        --lc-hard-bg: #f5e8e8;
        --py: #3a7bd5;
        --py-bg: #e8f0fb;
        --java: #e07b39;
        --java-bg: #fdf0e6;
        --cpp: #9c5a9c;
        --cpp-bg: #f4e8f5;
        --js: #c0a010;
        --js-bg: #fdf8e0;
        --go: #3a9070;
        --go-bg: #e2f0ec;
        --mysql: #2b6cb0;
        --mysql-bg: #e6f0fa;
        --c: #5b7db8;
        --c-bg: #e9eef8;
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
        --c: #5b7db8;
        --c-bg: #e9eef8;
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
        max-width:1350px;
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

kpi_style = """
        .st-emotion-cache-tn0cau{
            gap:0rem;
        }
        .st-key-kpi-section {
            max-width: 1800px;
            margin: 0 auto;
        }

        .section-header {
            margin-bottom: 32px;
        }

        .leetcode-section-header {
            margin-top: 20px;
        }

        .section-title, .leetcode-section-title {
            font-size: 28px !important;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }

        .section-subtitle, .leetcode-section-subtitle {
            font-size: 15px;
            color: var(--text-muted);
            font-weight: 400;
        }
        .st-key-dashboard-grid, .st-key-leetcode-metrics {
            display: grid;
            gap: 20px;
            grid-template-columns: repeat(4, 1fr);
            grid-auto-rows: 1fr;   /* ← all rows same height */
            align-items: stretch;  /* ← cells stretch to fill */
            width: 100%;
        }

        /* Make Streamlit's wrapper elements stretch too */
        .st-key-dashboard-grid > .st-emotion-cache-3pwa5w,
        .st-key-dashboard-grid > .st-emotion-cache-3pwa5w > .stMarkdown,
        .st-key-dashboard-grid > .st-emotion-cache-3pwa5w > .stMarkdown > .st-emotion-cache-6c7yup,
        .st-key-dashboard-grid > .st-emotion-cache-3pwa5w > .stMarkdown > .st-emotion-cache-6c7yup > .st-emotion-cache-3o718f {
            height: 100%;
        }

        .st-key-leetcode-metrics > .st-emotion-cache-3pwa5w,
        .st-key-leetcode-metrics > .st-emotion-cache-3pwa5w > .stMarkdown,
        .st-key-leetcode-metrics > .st-emotion-cache-3pwa5w > .stMarkdown > .st-emotion-cache-6c7yup,
        .st-key-leetcode-metrics > .st-emotion-cache-3pwa5w > .stMarkdown > .st-emotion-cache-6c7yup > .st-emotion-cache-3o718f {
            height: 100%;
        }

        @media (max-width: 1100px) {
            .st-key-dashboard-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 640px) {
            .st-key-dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        /* ═══════════════════════════════════════════
       KPI CARD — glassmorphism
    ═══════════════════════════════════════════ */
        .kpi-card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(50px);
            -webkit-backdrop-filter: blur(50px);
            border: 1px solid rgba(255, 255, 255, 0.30);
            border-radius: 20px;
             box-shadow:
                0 8px 16px rgba(0, 0, 0, 0.35),
                inset 0 1px 1px rgba(255, 255, 255, 0.12); 
            cursor: default;
            display: flex;
            flex-direction: column;
            gap: 0px;
            overflow: hidden;
            padding: 22px;
            position: relative;
            transition: all 0.35s cubic-bezier(0.2, 0.8, 0.2, 1);
            height: 100%;          /* ← fill parent instead of fixed rem */
            min-height: 14.375rem;
        }

        /* top-edge shimmer */
         .kpi-card::before {
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.80), transparent);
            content: '';
            height: 1px;
            left: 0;
            position: absolute;
            right: 0;
            top: 0;
        }

        /* left-edge shimmer */
         .kpi-card::after {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.80), transparent, rgba(255, 255, 255, 0.30));
            content: '';
            height: 100%;
            left: 0;
            position: absolute;
            top: 0;
            width: 1px;
        } 

        .kpi-card:hover {
            background: rgba(255, 255, 255, 0.05);
            box-shadow:
                0 14px 40px rgba(0, 0, 0, 0.13),
                inset 0 1px 0 rgba(255, 255, 255, 0.70),
                inset 0 -1px 0 rgba(255, 255, 255, 0.15);
            transform: translateY(-4px) scale(1.01);
        }

        /* ═══════════════════════════════════════════
       CARD HEADER
    ═══════════════════════════════════════════ */
        .kpi-header {
            align-items: flex-start;
            display: flex;
            justify-content: space-between;
        }

        .kpi-title {
            color: var(--text-label) !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            letter-spacing: 0.01em !important;
            margin-top: 3px !important;
        }

        /* ═══════════════════════════════════════════
       ICON
    ═══════════════════════════════════════════ */
        .kpi-icon {
            align-items: center;
            border-radius: 13px;
            box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.90);
            display: flex;
            flex-shrink: 0;
            height: 40px;
            justify-content: center;
            width: 40px;
        }

        .kpi-icon svg {
            fill: none;
            height: 18px;
            stroke: currentColor;
            stroke-linecap: round;
            stroke-linejoin: round;
            stroke-width: 2.2px;
            width: 18px;
        }

        .icon-green {
            background: var(--ig-bg);
            color: var(--ig-fg);
        }

        .icon-blue {
            background: var(--ib-bg);
            color: var(--ib-fg);
        }

        .icon-sage {
            background: var(--is-bg);
            color: var(--is-fg);
        }

        .icon-teal {
            background: var(--it-bg);
            color: var(--it-fg);
        }

        .icon-red {
            background: var(--ir-bg);
            color: var(--ir-fg);
        }

        .icon-amber {
            background: var(--ia-bg);
            color: var(--ia-fg);
        }

        .icon-lavender {
            background: var(--il-bg);
            color: var(--il-fg);
        }

        .icon-sky {
            background: var(--ik-bg);
            color: var(--ik-fg);
        }

        .icon-mint {
            background: var(--im-bg);
            color: var(--im-fg);
        
        }
        .icon-orange {
            background: var(--io-bg);
            color: var(--io-fg);
        }

        .icon-purple {
            background: var(--ip-bg);
            color: var(--ip-fg);
        }

        /* ═══════════════════════════════════════════
       VALUE ROW
    ═══════════════════════════════════════════ */
        .kpi-value-row {
            align-items: center;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .kpi-value {
            color: var(--text-main);
            font-size: 32px;
            font-weight: 600;
            letter-spacing: -0.03em;
            line-height: 1;
        }

        .kpi-value .unit {
            font-size: 16px;
            font-weight: 400;
            opacity: 0.50;
        }

        .kpi-helper {
            color: var(--text-muted);
            font-size: 13px !important;
            font-weight: 400 !important;
        }

        /* ═══════════════════════════════════════════
       BADGE
    ═══════════════════════════════════════════ */
        .kpi-badge {
            align-items: center;
            border: 1px solid;
            border-radius: 20px;
            display: inline-flex;
            font-size: 12px;
            font-weight: 500;
            gap: 4px;
            padding: 4px 10px;
        }

        .kpi-badge svg {
            fill: none;
            height: 11px;
            stroke: currentColor;
            stroke-linecap: round;
            stroke-linejoin: round;
            stroke-width: 2.5px;
            width: 11px;
        }

        .badge-positive {
            background: rgba(80, 180, 110, 0.10);
            border-color: rgba(80, 180, 110, 0.22);
            color: #3f8a5e;
        }

        .badge-neutral {
            background: rgba(100, 130, 190, 0.09);
            border-color: rgba(100, 130, 190, 0.20);
            color: #5272a0;
        }

        .badge-warning {
            background: var(--ir-bg);
            color: var(--ir-fg);
            border-color: var(--ir-fg);
        }

        /* ═══════════════════════════════════════════
       STATUS DOT
    ═══════════════════════════════════════════ */
        .status-dot {
            border-radius: 50%;
            display: inline-block;
            flex-shrink: 0;
            height: 6px;
            position: relative;
            width: 6px;
        }

        .status-dot::after {
            animation: dot-pulse 2.6s infinite ease-in-out;
            background: inherit;
            border-radius: 50%;
            content: '';
            height: 12px;
            left: -3px;
            opacity: 0.25;
            position: absolute;
            top: -3px;
            width: 12px;
        }

        @keyframes dot-pulse {
            0% {
                opacity: 0.30;
                transform: scale(0.8);
            }

            50%,
            100% {
                opacity: 0;
                transform: scale(1.7);
            }
        }

        .dot-green {
            background: #4aaa72;
        }

        .dot-blue {
            background: #6a8ccf;
        }

        .dot-amber {
            background: #cc9030;
        }
        .dot-red {
            background: #c96b6b;
        }

        /* ═══════════════════════════════════════════
       SVG GRAPH WRAPPER
    ═══════════════════════════════════════════ */
        .graph-wrap {
            margin-top: 6px;
            width: 100%;
        }

        .graph-wrap svg {
            display: block;
            width: 100%;
            overflow: visible;
        }

        /* ═══════════════════════════════════════════
       DONUT
    ═══════════════════════════════════════════ */
        .donut-wrap {
            align-items: center;
            justify-content: space-between;
            display: flex;
            gap: 14px;
            margin-top: 4px;
        }

        .donut-legend {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .donut-legend-item {
            align-items: center;
            color: var(--text-muted);
            display: flex;
            font-size: 11px;
            gap: 6px;
        }

        .donut-swatch {
            border-radius: 2px;
            flex-shrink: 0;
            height: 8px;
            width: 8px;
        }

        /* ═══════════════════════════════════════════
       PROGRESS BAR
    ═══════════════════════════════════════════ */
        .progress-track {
            background: rgba(107, 130, 112, 0.18);
            border-radius: 6px;
            height: 10px;
            overflow: hidden;
            width: 100%;
        }

        .progress-fill {
            border-radius: 6px;
            height: 100%;
            transition: width 0.6s ease;
        }

        .progress-labels {
            color: var(--text-label);
            display: flex;
            font-size: 11px;
            justify-content: space-between;
            margin-top: 5px;
        }

        /* ═══════════════════════════════════════════
       ACTIVITY HEATMAP BARS
    ═══════════════════════════════════════════ */
        .activity-bars {
            align-items: flex-end;
            display: flex;
            gap: 3px;
            height: 50px;
            margin-top: 10px;
            width: 100%;
        }

        .activity-bar {
            border-radius: 3px 3px 0 0;
            flex: 1;
            min-height: 5px;
        }

        .mini-stat-row {
        display: flex;
        gap: 10px;
        margin-top: 4px;
        }

        .mini-stat {
        background: rgba(255, 255, 255, 0.45);
        border-radius: 10px;
        flex: 1;
        padding: 8px 10px;
        }

        .mini-stat-label {
        color: var(--text-label);
        font-size: 10px;
        font-weight: 500;
        letter-spacing: 0.02em;
        margin-bottom: 3px;
        }

        .mini-stat-val {
        color: var(--text-main);
        font-size: 15px;
        font-weight: 600;
        }

        .diff-row {
            display: flex;
            gap: 10px;
            margin-top: 6px;
        }

        .diff-pill {
            flex: 1;
            border-radius: 12px;
            padding: 10px 12px;
            display: flex;
            flex-direction: column;
            gap: 3px;
        }

        .diff-pill-label {
            font-size: 10px;
            font-weight: 500;
            letter-spacing: 0.04em;
        }

        .diff-pill-val {
            font-size: 20px;
            font-weight: 600;
            line-height: 1;
        }

        .diff-pill-sub {
            font-size: 10px;
            opacity: 0.70;
        }

        .topic-row {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-top: 4px;
        }

        .topic-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .topic-name {
            font-size: 11px;
            color: var(--text-muted);
            width: 80px;
            flex-shrink: 0;
        }

        .topic-bar-track {
            flex: 1;
            background: rgba(107, 130, 112, 0.15);
            border-radius: 4px;
            height: 7px;
            overflow: hidden;
        }

        .topic-bar-fill {
            height: 100%;
            border-radius: 4px;
        }

        .topic-count {
            font-size: 11px;
            font-weight: 600;
            color: var(--text-main);
            width: 28px;
            text-align: right;
            flex-shrink: 0;
        }

        .cal-grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 3px;
            margin-top: 6px;
        }

        .cal-cell {
            aspect-ratio: 1;
            border-radius: 3px;
        }

        .streak-row {
            display: flex;
            align-items: center;
            gap: 6px;
            margin-top: 8px;
        }

        .streak-badge {
            background: rgba(255, 255, 255, 0.55);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 10px;
            padding: 6px 10px;
            text-align: center;
            flex: 1;
        }

        .streak-badge-val {
            font-size: 18px;
            font-weight: 700;
            color: var(--text-main);
        }

        .streak-badge-label {
            font-size: 10px;
            color: var(--text-label);
        }

        .heatmap-grid {
            display: grid;
            grid-template-columns: repeat(20, 10px);
            gap: 3px
        }

        .hm-cell {
            width: 10px;
            height: 10px;
            border-radius: 2px
        }

        .hm-cell:hover {
            opacity: .7
        }

        .l0 {
            background: #e1f5ee
        }

        .l1 {
            background: #9fe1cb
        }

        .l2 {
            background: #5dcaa5
        }

        .l3 {
            background: #1d9e75
        }

        .l4 {
            background: #0f6e56
        }

        .hm-labels {
            display: flex;
            justify-content: space-between;
            margin-top: 6px
        }

        .hm-label {
            font-size: 10px;
            color: light-dark(rgba(115, 114, 108, 1), rgba(156, 154, 146, 1))
        }

        .hm-legend {
            display: flex;
            align-items: center;
            gap: 6px;
            margin-top: 10px
        }

        .hm-legend-label {
            font-size: 10px;
            color: light-dark(rgba(115, 114, 108, 1), rgba(156, 154, 146, 1))
        }

        .hm-legend-track {
            display: flex;
            gap: 2px
        }

        .hm-legend-step {
            width: 10px;
            height: 10px;
            border-radius: 2px
        }
        
        .progress-section {
            margin-top: 10px;
        }

        .progress-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px
        }

        .progress-label {
            font-size: 12px;
            color: light-dark(rgba(115, 114, 108, 1), rgba(156, 154, 146, 1))
        }

        .progress-pct {
            font-size: 12px;
            font-weight: 500;
            color: #854F0B
        }

        

        .progress-fill {
            height: 100%;
            border-radius: 99px;
            background: #EF9F27;
            width: 49%
        }

        .milestone-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 12px
        }

        .milestone {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px
        }

        .milestone-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%
        }

        .milestone-dot.done {
            background: #EF9F27
        }

        .milestone-dot.next {
            background: light-dark(rgba(31, 30, 29, 0.3), rgba(222, 220, 209, 0.3))
        }

        .milestone-num {
            font-size: 10px;
            color: light-dark(rgba(115, 114, 108, 1), rgba(156, 154, 146, 1))
        }

        .milestone-line {
            flex: 1;
            height: 1px;
            background:light-dark(rgba(31, 30, 29, 0.3), rgba(222, 220, 209, 0.3));
            margin: 0 2px;
            margin-bottom: 10px
        }

        /* ═══════════════════════════════════════════
       RESPONSIVE
    ═══════════════════════════════════════════ */
        @media (max-width: 950px) {

            .app-name,
            .username {
                display: none;
            }

            .profile-trigger {
                padding: 6px;
            }

            .dropdown-icon {
                display: none;
            }
        }

        @media (max-width: 650px) {
            .dashboard-header {
                height: auto;
                padding: 12px 16px;
                flex-wrap: wrap;
                gap: 16px;
            }

            .header-left,
            .header-right {
                flex: unset;
            }

            .header-right {
                flex-grow: 1;
            }

            .header-center {
                order: 3;
                width: 100%;
                justify-content: space-between;
                padding: 8px;
            }

            .nav-button {
                flex: 1;
                width: auto;
                height: 44px;
            }

            .section-title {
                font-size: 22px;
            }
        }
"""

token_expiry_warning = """
    .st-key-token-expiry-warning .st-emotion-cache-3o718f{
        display:flex;
        align-items:center;
        justify-content:center;
    }
    .token-banner {
            width: 100%;
            max-width: 700px;
            display: flex;
            align-items: center;
            gap: 18px;
            background: linear-gradient(135deg,
                    #ef4444,
                    #dc2626);
            border: none;
            border-radius: 18px;
            padding: 16px 24px;

            box-shadow:
                0 15px 35px rgba(220, 38, 38, 0.25),
                0 4px 10px rgba(0, 0, 0, 0.08);

            transition: all .25s ease;
        }

        .token-banner:hover {
            transform: translateY(-3px);
            box-shadow:
                0 20px 40px rgba(220, 38, 38, 0.35);
        }

        .token-banner__icon {
            width: 52px;
            height: 52px;

            display: flex;
            align-items: center;
            justify-content: center;

            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);

            color: white;
            border-radius: 14px;

            flex-shrink: 0;
        }

        .token-banner__title {
            font-size: 16px;
            font-weight: 700;
            color: white;
            margin-bottom:0px;
        }

        .token-banner__desc {
            font-size: 14px;
            line-height: 1.5;
            color: rgba(255, 255, 255, 0.85);
        }

        .token-banner__btn {
            border: none;
            outline: none;

            background: white;
            color: #dc2626;

            padding: 10px 18px;
            border-radius: 12px;

            font-size: 14px;
            font-weight: 700;

            cursor: pointer;
            transition: .2s ease;

            box-shadow:
                0 4px 12px rgba(0, 0, 0, 0.08);
        }

        .token-banner__btn:hover {
            transform: translateY(-2px);
            background: #fef2f2;
        }

        .token-banner__btn:active {
            transform: translateY(0);
        }

        .lang-tag {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            border: 1px solid;
        }

        .lang-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            flex-shrink: 0;
        }

        .lang-bar-row {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .lang-bar-name {
            font-size: 11px;
            color: var(--text-muted);
            width: 18px;
            font-weight: 600;
        }

        .lang-bar-track {
            flex: 1;
            background: rgba(107, 130, 112, 0.15);
            border-radius: 4px;
            height: 8px;
            overflow: hidden;
        }

        .lang-bar-fill {
            height: 100%;
            border-radius: 4px;
        }

        .lang-bar-pct {
            font-size: 11px;
            font-weight: 600;
            color: var(--text-main);
            width: 32px;
            text-align: right;
            flex-shrink: 0;
        }

        .trend-sparkline {
            margin-top: 6px;
            width: 100%;
        }

        .trend-sparkline svg {
            display: block;
            width: 100%;
            overflow: visible;
        }

        .diversity-dots {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 8px;
        }

        .diversity-lang {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
        }

        .diversity-circle {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: 700;
        }

        .diversity-lname {
            font-size: 10px;
            color: var(--text-label);
        }
"""

def dashboard():

    task_df,output_df,success = fetch_tasks_data()
    leetcode_data = fetch_leetcode_data()
    final_style = f"""
    <style>
    {root_variable[0]}
    {remove_header_footer}
    {page_setup}
    {header_style}
    {kpi_style}
    {token_expiry_warning}
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
                    icon = ":material/instant_mix:",
                    on_click=to_settings
                )

            with st.container(key = "header-right"):
                st.button(
                    label = "",
                    key = "action-button-1",
                    type = "tertiary",
                    icon = ":material/dark_mode:",
                    on_click=change_theme,
                    disabled=True
                )
                st.button(
                    label = "",
                    key = "action-button-2",
                    type = "tertiary",
                    icon = ":material/notifications:",
                    disabled=True
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
    success = True
    if not success:
        with st.container(key = "token-expiry-warning"):
            st.markdown(
                """
                <div class="token-banner" role="alert">
                    <div class="token-banner__icon">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                            <path d="M12 9V13" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                            <circle cx="12" cy="17" r="1" fill="currentColor" />
                            <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" />
                        </svg>
                    </div>
                    <div class="token-banner__body">
                        <p class="token-banner__title">Session token expired</p>
                        <p class="token-banner__desc">Your access token has expired. Please renew it to continue using the service.
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        return
        
    with st.container(key = "kpi-section"):
        st.markdown(
            """
            <div class="section-header">
            <h2 class="section-title">Key Performance Indicators</h2>
            <p class="section-subtitle">Track your productivity metrics and performance trends</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.container(key = "dashboard-grid"):

            todays_progress_metric(output_df,st.session_state['settings']['Todays Progress'])
            completion_trend_metric(output_df,st.session_state['settings']['Completion Trend'])
            average_completion_metric(output_df,st.session_state['settings']['Average Completion'])
            productivity_streak_metric(output_df,50,st.session_state['settings']['Productivity Streak'])
            total_progress_metric(output_df,st.session_state['settings']['Total Progress'])
            active_days_metric(output_df,st.session_state['settings']['Active Days'])
            monthly_rate_metric(output_df,st.session_state['settings']['Monthly Rate'])
            needs_attendtion_metric(output_df,st.session_state['settings']['Needs Attention'])
            weekly_rate_metric(output_df,st.session_state['settings']['Weekly Rate'])
            # goal_hit_rate_metric(st.session_state['settings']['Goal Hit Rate'])
            # output_volume_metric(st.session_state['settings']['Output Volume'])

        
        with st.container(key = "leetcode-metrics"):
            leetcode_total_solved_metric(leetcode_data,st.session_state['settings']['LeetCode Total Solved'])
            leetcode_acceptance_rate_metric(leetcode_data,st.session_state['settings']['LeetCode Acceptance Rate'])
            leetcode_submission_metric(leetcode_data,st.session_state['settings']['LeetCode Submission'])
            leetcode_streak_metric(leetcode_data,st.session_state['settings']['LeetCode Streak'])
            leetcode_topics_coverage_metric(leetcode_data,st.session_state['settings']['LeetCode Topics Coverage'])
            leetcode_languages_used_metric(leetcode_data,st.session_state['settings']['LeetCode Languages Used'])






            


