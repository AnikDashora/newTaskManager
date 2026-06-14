import math

from matplotlib.pyplot import bar
import streamlit as st
import os
import sys
import random
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts
from datetime import datetime, time, timedelta, date, timezone
import json
import time

def completion_trend_metric(df,show_kpi):
    if not show_kpi:
        return
    if df.empty:

        percent_change = 0

        current_week_avg = 0

        previous_week_avg = 0

        values = [0] * 8

    else:

        # =====================================
        # DATE CONVERSION
        # =====================================

        df = df.copy()

        df["date"] = pd.to_datetime(
            df["date"],
            format="%d-%m-%Y",
            errors="coerce"
        )

        # Remove invalid dates
        df = df.dropna(subset=["date"])

        # =====================================
        # CHECK AGAIN AFTER CLEANING
        # =====================================

        if df.empty:

            percent_change = 0

            current_week_avg = 0

            previous_week_avg = 0

            values = [0] * 8

        else:

            # =================================
            # WEEK CREATION
            # =================================

            df["week"] = df["date"].dt.strftime(
                "%Y-%U"
            )

            # =================================
            # WEEKLY DATA
            # =================================

            weekly_data = (
                df.groupby("week")[
                    "completion_percentage"
                ]
                .mean()
                .reset_index()
            )

            # =================================
            # CURRENT WEEK AVG
            # =================================

            current_week_avg = weekly_data.iloc[-1][
                "completion_percentage"
            ]

            # =================================
            # PREVIOUS WEEK AVG
            # =================================

            if len(weekly_data) >= 2:

                previous_week_avg = weekly_data.iloc[-2][
                    "completion_percentage"
                ]

            else:

                previous_week_avg = 0

            # =================================
            # PERCENT CHANGE
            # =================================

            if previous_week_avg == 0:

                percent_change = int(
                    round(current_week_avg, 2)
                )

            else:

                percent_change = int(
                    round(
                        (
                            (
                                current_week_avg
                                - previous_week_avg
                            )
                            / previous_week_avg
                        )
                        * 100,
                        2
                    )
                )

            # =================================
            # LAST 8 DAYS
            # =================================

            last_8_days = (
                df.sort_values("date")
                .tail(8)
            )

            values = last_8_days[
                "completion_percentage"
            ].fillna(0).tolist()

            # =================================
            # ENSURE MINIMUM 2 VALUES
            # =================================

            if len(values) == 1:

                values.append(values[0])

            elif len(values) == 0:

                values = [0] * 8

    # =========================================
    # SVG GRAPH GENERATION
    # =========================================

    svg_width = 200
    svg_height = 50

    min_val = min(values)
    max_val = max(values)

    # Avoid division by zero
    if max_val == min_val:

        max_val += 1

    points = []

    for i, value in enumerate(values):

        # Avoid division by zero
        if len(values) == 1:

            x = 0

        else:

            x = (
                i / (len(values) - 1)
            ) * svg_width

        y = svg_height - (
            (
                (
                    value - min_val
                )
                / (
                    max_val - min_val
                )
            )
            * svg_height
        )

        points.append(f"{x},{y}")

    polyline_points = " ".join(points)

    # =========================================
    # AREA FILL
    # =========================================

    polygon_points = (
        f"0,{svg_height} "
        + polyline_points
        + f" {svg_width},{svg_height}"
    )

    # =========================================
    # UI COLORS
    # =========================================

    badge_class = (

        "badge-positive"

        if percent_change >= 0

        else "badge-warning"
    )

    badge_text = (

        "Improving"

        if percent_change >= 0

        else "Declining"
    )

    trend1 = (

        "22 7 13.5 15.5 8.5 10.5 2 17"

        if percent_change >= 0

        else "2 7 8.5 13.5 13.5 8.5 22 17"
    )

    trend2 = (

        "16 7 22 7 22 13"

        if percent_change >= 0

        else "16 17 22 17 22 11"
    )

    arrow = (

        "18 15 12 9 6 15"

        if percent_change >= 0

        else "6 9 12 15 18 9"
    )

    icon_color = (

        "green"

        if percent_change >= 0

        else "red"
    )

    graph_color = (

        "#55856b"

        if percent_change >= 0

        else "#c96868"
    )
    return st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <h2 class="kpi-title">Completion Trend</h2>
                        <div class="kpi-icon icon-{icon_color}">
                            <svg viewBox="0 0 24 24">
                                <polyline points="{trend1}" />
                                <polyline points="{trend2}" />
                            </svg>
                        </div>
                    </div>
                    <div class="kpi-value-row">
                        <div class="kpi-value">{percent_change}%</div>
                        <span class="kpi-badge {badge_class}">
                            <svg viewBox="0 0 24 24">
                                <polyline points="{arrow}" />
                            </svg>
                            {badge_text}
                        </span>
                    </div>
                    <p class="kpi-helper">vs last week</p>
                    <div class="graph-wrap">
                        <svg viewBox="0 0 200 50" height="50" preserveAspectRatio="none"
                            aria-label="Completion trend: rising from 52% to 78%">
                            <defs>
                                <linearGradient id="g-green" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stop-color="{graph_color}" stop-opacity="0.28" />
                                    <stop offset="100%" stop-color="{graph_color}" stop-opacity="0.02" />
                                </linearGradient>
                            </defs>
                            <polygon
                                points="{polygon_points}"
                                fill="url(#g-green)" />
                            <polyline
                                points="{polyline_points}"
                                fill="none" stroke="{graph_color}" stroke-width="2" stroke-linejoin="round"
                                stroke-linecap="round" />
                        </svg>
                    </div>
                </div>
                """,
                unsafe_allow_html = True
            )

def average_completion_metric(df,show_kpi):
    if not show_kpi:
        return

    if df.empty:

        average_completion = 0
        remaining = 0
    else:

        # =================================
        # MEAN CALCULATION
        # =================================

        average_completion = round(

            df["completion_percentage"]
            .fillna(0)
            .mean(),

            2
        )

        if pd.isna(average_completion):

            average_completion = 0
            remaining = 0
        else:

            average_completion = max(
                0,
                min(100, average_completion)
            )

            remaining = 100 - average_completion

    # =====================================
    # DONUT CHART LOGIC
    # =====================================

    radius = 24

    circumference = (
        2 * math.pi * radius
    )

    # =====================================
    # STROKE CALCULATION
    # =====================================

    completed_stroke = (
        average_completion / 100
    ) * circumference

    remaining_stroke = (
        circumference
        - completed_stroke
    )

    # =====================================
    # DASH ARRAY
    # =====================================

    dash_array = (
        f"{completed_stroke:.2f} "
        f"{remaining_stroke:.2f}"
    )
    return st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <h2 class="kpi-title">Average Completion</h2>
                        <div class="kpi-icon icon-blue">
                            <svg viewBox="0 0 24 24">
                                <circle cx="12" cy="12" r="10" />
                                <circle cx="12" cy="12" r="6" />
                                <circle cx="12" cy="12" r="2" />
                            </svg>
                        </div>
                    </div>
                    <div class="kpi-value-row">
                        <div class="kpi-value">{average_completion:.0f}%</div>
                        <span class="kpi-badge badge-neutral">
                            <span class="status-dot dot-blue"></span>
                            Steady
                        </span>
                    </div>
                    <p class="kpi-helper">Task completion efficiency</p>
                    <div class="donut-wrap">
                        <svg width="68" height="68" viewBox="0 0 68 68" style="flex-shrink:0"
                            aria-label="Donut chart: {average_completion:.0f}% done, {remaining:.0f}% remaining">
                            <circle cx="34" cy="34" r="24" fill="none" stroke="#dce8f0" stroke-width="8" />
                            <circle cx="34" cy="34" r="24" fill="none" stroke="#5c7b9c" stroke-width="8"
                                stroke-linecap="round" stroke-dasharray="{dash_array}" transform="rotate(-90 34 34)" />
                            <!-- <text x="34" y="38" text-anchor="middle" font-family="Outfit,sans-serif" font-size="12"
                                font-weight="600" fill="#2e3834">78%</text> -->
                        </svg>
                        <div class="donut-legend">
                            <div class="donut-legend-item">
                                <span class="donut-swatch" style="background:#5c7b9c;"></span>Done &nbsp;{average_completion:.0f}%
                            </div>
                            <div class="donut-legend-item">
                                <span class="donut-swatch" style="background:#dce8f0;"></span>Left &nbsp;{remaining:.0f}%
                            </div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

def total_progress_metric(df,show_kpi):
    if not show_kpi:
        return
    completed_tasks = df["total_completed_task"].sum()
    total_tasks = df["total_task"].sum()
    progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    return st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <h2 class="kpi-title">Total Progress</h2>
                        <div class="kpi-icon icon-sage">
                            <svg viewBox="0 0 24 24">
                                <rect x="3" y="18" width="18" height="4" rx="2" />
                                <rect x="3" y="10" width="14" height="4" rx="2" />
                                <rect x="3" y="2" width="10" height="4" rx="2" />
                            </svg>
                        </div>
                    </div>
                    <div class="kpi-value-row">
                        <div class="kpi-value">{completed_tasks} <span class="unit">/ {total_tasks}</span></div>
                    </div>
                    <p class="kpi-helper">Completed task progress</p>
                    <div style="margin-top:24px;">
                        <div class="progress-track">
                            <div class="progress-fill" style="width:{progress_percentage:.1f}%; background:var(--is-fg);"></div>
                        </div>
                        <div class="progress-labels">
                            <span>0</span><span>{progress_percentage:.1f}% complete</span><span>{total_tasks}</span>
                        </div>
                    </div>             
                </div>
                """,
                unsafe_allow_html=True
            )

def monthly_rate_metric(df,show_kpi):
    if not show_kpi:
        return
        # -----------------------------
    # DATE FORMATTING
    # -----------------------------

    df["date"] = pd.to_datetime(
        df["date"],
        format="%d-%m-%Y"
    )

    # Sort dataframe
    df = df.sort_values("date")

    # -----------------------------
    # FILTER CURRENT YEAR
    # -----------------------------

    current_year = pd.Timestamp.today().year

    current_year_df = df[
        df["date"].dt.year == current_year
    ]

    # -----------------------------
    # MONTHLY AVERAGE
    # -----------------------------

    monthly_avg_df = (
        current_year_df
        .groupby(current_year_df["date"].dt.month)
        ["completion_percentage"]
        .mean()
        .round(2)
        .reset_index()
    )

    # Rename columns
    monthly_avg_df.columns = [
        "month",
        "avg_completion_percentage"
    ]

    # Dynamic month names
    monthly_avg_df["month_name"] = pd.to_datetime(
        monthly_avg_df["month"],
        format="%m"
    ).dt.strftime("%b")

    # -----------------------------
    # CURRENT MONTH AVG
    # -----------------------------

    current_month = pd.Timestamp.today().month

    current_month_data = monthly_avg_df[
        monthly_avg_df["month"] == current_month
    ]

    current_month_avg = (
        int(current_month_data[
            "avg_completion_percentage"
        ].values[0])
        if not current_month_data.empty
        else 0
    )

    # -----------------------------
    # SVG GRAPH LOGIC
    # -----------------------------

    month_name = []
    circle_text = []
    line_points = []

    # Convert percentage -> SVG Y position
    def get_y(value):

        # 100% = top
        # 0% = bottom

        return round(
            52 - ((value / 100) * 40),
            2
        )

    # Generate graph points
    for i, row in monthly_avg_df.iterrows():

        value = row["avg_completion_percentage"]
        month_label = row["month_name"]

        # X coordinate
        x = 4 + (i * 30)

        # Y coordinate
        y = get_y(value)

        # Store line point
        line_points.append(f"{x},{y}")

        # -----------------------------
        # GRAPH CIRCLES
        # -----------------------------

        # Highlight last point
        if i == len(monthly_avg_df) - 1:

            circle_text.append(
                f'<circle cx="{x}" cy="{y}" r="4" fill="#4d8aaa" /> <circle cx="{x}" cy="{y}" r="7" fill="#4d8aaa" fill-opacity="0.18" />'
            )

        else:

            circle_text.append(
                f'<circle cx="{x}" cy="{y}" r="3.2" fill="#fff" stroke="#4d8aaa" stroke-width="2" /> '
            )

        # -----------------------------
        # MONTH LABELS
        # -----------------------------

        month_name.append(
            f'<text x="{x}" y="63" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8.5" fill="#8a9691"> {month_label} </text>'
        )

    # -----------------------------
    # GRAPH PATHS
    # -----------------------------

    # Line graph points
    polyline_points = " ".join(line_points)

    # Area fill polygon
    polygon_points = (
        f"4,52 "
        f"{polyline_points} "
        f"196,52"
    )
    
    return st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <h2 class="kpi-title">Monthly Rate</h2>
                        <div class="kpi-icon icon-sky">
                            <svg viewBox="0 0 24 24">
                                <path d="M3 3v18h18" />
                                <path d="m19 9-5 5-4-4-3 3" />
                            </svg>
                        </div>
                    </div>
                    <div class="kpi-value-row">
                        <div class="kpi-value">{current_month_avg}%</div>
                        <span class="kpi-badge badge-neutral">
                            <span class="status-dot dot-blue"></span>
                            Stable
                        </span>
                    </div>
                    <p class="kpi-helper">Monthly productivity consistency</p>
                    <div class="graph-wrap">
                        <svg viewBox="0 0 200 64" height="64" aria-label="Monthly rate: Jan 68% to Jun 74%">
                            <defs>
                                <linearGradient id="g-blue" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stop-color="#4d8aaa" stop-opacity="0.25" />
                                    <stop offset="100%" stop-color="#4d8aaa" stop-opacity="0.03" />
                                </linearGradient>
                            </defs>
                            <line x1="4" y1="44" x2="196" y2="44" stroke="#d8e8f0" stroke-width="0.6" />
                            <line x1="4" y1="32" x2="196" y2="32" stroke="#d8e8f0" stroke-width="0.6" />
                            <line x1="4" y1="20" x2="196" y2="20" stroke="#d8e8f0" stroke-width="0.6" />
                            <polygon points="{polygon_points}" fill="url(#g-blue)" />
                            <polyline points="{polyline_points}" fill="none" stroke="#4d8aaa"
                                stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />{''.join(circle_text)}{''.join(month_name)}</svg>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

def active_days_metric(df,show_kpi):
    if not show_kpi:
        return

    df["date"] = pd.to_datetime(
        df["date"],
        format="%d-%m-%Y"
    )
    df.sort_values("date", inplace=True)
    last_30_df = df.tail(30)

    active_df = df[df["total_task"] != 0]
    active_days = len(active_df)

    bar_html = []

    for _, row in last_30_df.iterrows():

        completion = row["completion_percentage"]

        # Minimum height visibility
        height = max(completion, 8)

        # Opacity based on completion %
        opacity = max(completion / 100, 0.15)
        bar_html.append(f'<div class="activity-bar" style="height:{height}%; background:rgba(74, 145, 137,{opacity});"></div>')


    return  st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <h2 class="kpi-title">Active Days</h2>
                        <div class="kpi-icon icon-teal">
                            <svg viewBox="0 0 24 24">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                                <line x1="16" x2="16" y1="2" y2="6" />
                                <line x1="8" x2="8" y1="2" y2="6" />
                                <line x1="3" x2="21" y1="10" y2="10" />
                                <path d="m9 16 2 2 4-4" />
                            </svg>
                        </div>
                    </div>
                    <div class="kpi-value-row">
                        <div class="kpi-value">{active_days} <span class="unit">Days</span></div>
                    </div>
                    <p class="kpi-helper">Days with completed activity</p>
                    <div class="activity-bars" aria-label="Activity heatmap: {active_days} active days">{''.join(bar_html)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

def weekly_rate_metric(df,show_kpi):
    if not show_kpi:
        return

    df["date"] = pd.to_datetime(
        df["date"],
        format="%d-%m-%Y"
    )

    # Sort by date
    df.sort_values("date", inplace=True)

    # -----------------------------
    # CURRENT WEEK FILTER
    # -----------------------------

    today = pd.Timestamp.today()

    current_week = today.isocalendar().week
    current_year = today.year

    current_week_df = df[
        (df["date"].dt.isocalendar().week == current_week) &
        (df["date"].dt.year == current_year)
    ]

    # -----------------------------
    # DAILY AVG COMPLETION %
    # -----------------------------

    weekly_avg_df = (
        current_week_df
        .groupby(current_week_df["date"].dt.day_name())
        ["completion_percentage"]
        .mean()
        .round(2)
        .reset_index()
    )

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    weekly_avg_df["day"] = pd.Categorical(
        weekly_avg_df["date"],
        categories=day_order,
        ordered=True
    )

    weekly_avg_df.sort_values("day", inplace=True)

    # -----------------------------
    # CURRENT WEEK AVG
    # -----------------------------

    current_week_avg = int(
        round(
            current_week_df["completion_percentage"].mean(),
            0
        )
    ) if not current_week_df.empty else 0

    # -----------------------------
    # SVG GRAPH LOGIC
    # -----------------------------

    bars_html = []
    labels_html = []

    for i, row in weekly_avg_df.iterrows():

        value = row["completion_percentage"]

        # Bar dimensions
        height = (value / 100) * 40

        y = 52 - height

        x = i * 31.33

        opacity = max(value / 100, 0.35)

        # Bar
        bars_html.append(
            f'<rect x="{x}" y="{y}" width="22" height="{height}" rx="3" fill="rgba(125,112,150,{opacity})" />'
        )

        # Labels
        labels_html.append(
            f'<text x="{x + 11}" y="63" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8.5" fill="#8a9691"> {row["date"][:3]} </text>'
        )

    return st.markdown(
                f"""
                <div class="kpi-card">
                <div class="kpi-header">
                    <h2 class="kpi-title">Weekly Rate</h2>
                    <div class="kpi-icon icon-lavender">
                        <svg viewBox="0 0 24 24">
                            <line x1="18" x2="18" y1="20" y2="10" />
                            <line x1="12" x2="12" y1="20" y2="4" />
                            <line x1="6" x2="6" y1="20" y2="14" />
                        </svg>
                    </div>
                </div>
                <div class="kpi-value-row">
                    <div class="kpi-value">{current_week_avg}%</div>
                    <!--<span class="kpi-badge badge-positive">
                        <svg viewBox="0 0 24 24">
                            <polyline points="18 15 12 9 6 15" />
                        </svg>
                        +4%
                    </span>-->
                </div>
                <p class="kpi-helper">Tasks completed this week</p>
                <div class="graph-wrap">
                    <svg viewBox="0 0 200 64" height="64" aria-label="Weekly completion: Mon 70% to Sun 82%"><line x1="0" y1="52" x2="200" y2="52" stroke="#ddd" stroke-width="0.8" />{''.join(bars_html)}{''.join(labels_html)}</svg>
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )

def productivity_streak_metric(df, expected_percentage_streak,show_kpi):
    if not show_kpi:
        return
    df["date"] = pd.to_datetime(
        df["date"],
        format="%d-%m-%Y"
    )

    # Sort by date
    df.sort_values("date", inplace=True)

    # Reset index
    df.reset_index(drop=True, inplace=True)

    # -----------------------------
    # FIND STREAK START
    # -----------------------------

    # -----------------------------
# FIND LONGEST PRODUCTIVE CYCLE
# -----------------------------

    max_len = 0
    curr_len = 0

    streak_start_index = 0
    streak_end_index = -1

    temp_start = 0

    for i in range(len(df)):

        completion = df.loc[i, "completion_percentage"]

        if completion >= expected_percentage_streak:

            if curr_len == 0:
                temp_start = i

            curr_len += 1

            if curr_len > max_len:
                max_len = curr_len
                streak_start_index = temp_start
                streak_end_index = i

        else:

            curr_len = 0

    # -----------------------------
    # STREAK DATAFRAME
    # -----------------------------

    if max_len > 0:
        streak_df = df.iloc[streak_start_index:streak_end_index + 1]
    else:
        streak_df = pd.DataFrame(columns=df.columns)

    # Total streak days
    streak_days = max_len

    # -----------------------------
    # CREATE BARS
    # -----------------------------

    bars_html = []

    for i, row in streak_df.iterrows():

        completion = row["completion_percentage"]

        # Dynamic height
        height = max(completion, 8)

        # Dynamic opacity
        opacity = max(completion / 100, 0.35)

        # Last bar highlight
        if i == streak_df.index[-1]:

            bars_html.append(
                f'<div class="activity-bar" style=" height:{height}%; background:#c4914a;"></div>'
            )

        else:

            bars_html.append(
                f'<div class="activity-bar" style=" height:{height}%; background:rgba(156,116,66,{opacity});"></div>'
            )

    # -----------------------------
    # STATUS TEXT
    # -----------------------------

    if streak_days >= 14:
        status_text = "On Fire"
        badge = 'badge-positive'
        dot = "dot-green"

    elif streak_days >= 7:
        status_text = "Strong"
        badge = 'badge-neutral'
        dot = "dot-blue"

    elif streak_days >= 3:
        status_text = "Good"
        badge = 'badge-neutral'
        dot = "dot-blue"

    else:
        status_text = "Starting"
        badge = 'badge-neutral'
        dot = "dot-blue"
    return  st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <h2 class="kpi-title">Productivity Streak</h2>
                        <div class="kpi-icon icon-amber">
                            <svg viewBox="0 0 24 24">
                                <path
                                    d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z" />
                            </svg>
                        </div>
                    </div>
                    <div class="kpi-value-row">
                        <div class="kpi-value">{streak_days} <span class="unit">Days</span></div>
                        <span class="kpi-badge {badge}">
                            <span class="status-dot {dot}"></span>
                            {status_text}
                        </span>
                    </div>
                    <p class="kpi-helper">Consecutive productive days</p>
                    <div class="activity-bars" aria-label="Daily productivity scores over 14 days" >{''.join(bars_html)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

def needs_attendtion_metric(df,show_kpi):
    if not show_kpi:
        return

    df["date"] = pd.to_datetime(
        df["date"],
        format="%d-%m-%Y"
    )

    # Sort by date
    df.sort_values("date", inplace=True)

    # -----------------------------
    # INCOMPLETE TASKS
    # -----------------------------

    # New column
    df["incomplete_task"] = (
        df["total_task"] -
        df["total_completed_task"]
    )

    # Last 7 days
    last_7_df = df.tail(7)

    # Total incomplete tasks
    total_incomplete_tasks = int(
        last_7_df["incomplete_task"].sum()
    )

    # -----------------------------
    # SVG GRAPH LOGIC
    # -----------------------------

    line_points = []
    circle_html = []
    label_html = []

    # Dynamic Y scaling
    max_value = max(
        last_7_df["incomplete_task"].max(),
        1
    )

    # Convert task count -> SVG Y
    def get_y(value):

        return round(
            52 - ((value / max_value) * 36),
            2
        )

    # Create graph
    for i, (_, row) in enumerate(last_7_df.iterrows()):

        incomplete = row["incomplete_task"]

        x = round(i * 33.33, 2)

        y = get_y(incomplete)

        # Line points
        line_points.append(f"{x},{y}")

        # Circles
        if i == len(last_7_df) - 1:

            circle_html.append(
                f'<circle cx="{x}" cy="{y}" r="4" fill="#c96868" /> <circle cx="{x}" cy="{y}" r="7" fill="#c96868" fill-opacity="0.18" />'
            )

        else:

            circle_html.append(
                f'<circle cx="{x}" cy="{y}" r="3" fill="#fff" stroke="#c96868" stroke-width="1.8" />'
            )

        # Labels
        label_html.append(
            f'<text x="{x}" y="63" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8.5" fill="#8a9691"> D{i+1} </text>'
        )

    # Polyline
    polyline_points = " ".join(line_points)

    # Area fill
    polygon_points = (
        f"0,56 "
        f"{polyline_points} "
        f"200,56"
    )

    return st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <h2 class="kpi-title">Needs Attention</h2>
                        <div class="kpi-icon icon-red">
                            <svg viewBox="0 0 24 24">
                                <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" />
                                <line x1="12" x2="12" y1="9" y2="13" />
                                <line x1="12" x2="12.01" y1="17" y2="17" />
                            </svg>
                        </div>
                    </div>
                    <div class="kpi-value-row">
                        <div class="kpi-value">{total_incomplete_tasks} <span class="unit">Tasks</span></div>
                        <span class="kpi-badge badge-warning">
                            <span class="status-dot dot-red"></span>
                            Overdue
                        </span>
                    </div>
                    <p class="kpi-helper">Overdue or aging tasks</p>
                    <div class="graph-wrap">
                        <svg viewBox="0 0 200 64" height="64" aria-label="Overdue tasks: rising from 5 to 12 over 7 days">
                            <defs>
                                <linearGradient id="g-red" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="0%" stop-color="#c96868" stop-opacity="0.25" />
                                    <stop offset="100%" stop-color="#c96868" stop-opacity="0.03" />
                                </linearGradient>
                            </defs>
                            <line x1="0" y1="46.55" x2="200" y2="46.55" stroke="#e8dada" stroke-width="0.6" />
                            <line x1="0" y1="37.82" x2="200" y2="37.82" stroke="#e8dada" stroke-width="0.6" />
                            <line x1="0" y1="28.73" x2="200" y2="28.73" stroke="#e8dada" stroke-width="0.6" />
                            <line x1="0" y1="15.09" x2="200" y2="15.09" stroke="#e8dada" stroke-width="0.6" />
                            <polygon points="{polygon_points}"
                                fill="url(#g-red)" />
                            <polyline points="{polyline_points}" fill="none"
                                stroke="#c96868" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />{''.join(circle_html)}{''.join(label_html)}
                        </svg>
                    </div>
                </div>
                    """,
                    unsafe_allow_html=True
                )

def todays_progress_metric(df,show_kpi):
    if not show_kpi:
        return
    df["date"] = pd.to_datetime(
        df["date"],
        format="%d-%m-%Y"
    )

    # Today's date
    today = pd.Timestamp.today().normalize()

    # -----------------------------
    # FILTER TODAY DATA
    # -----------------------------

    today_df = df[
        df["date"].dt.normalize() == today
    ]

    # -----------------------------
    # TASK CALCULATIONS
    # -----------------------------

    completed_tasks = int(
        today_df["total_completed_task"].sum()
    )

    total_tasks = int(
        today_df["total_task"].sum()
    )

    progress_percentage = (
        (completed_tasks / total_tasks) * 100
        if total_tasks > 0
        else 0
    )
    return st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-header">
                        <h2 class="kpi-title">Today's Progress</h2>
                        <div class="kpi-icon icon-sage">
                            <svg viewBox="0 0 24 24">
                                <rect x="3" y="18" width="18" height="4" rx="2" />
                                <rect x="3" y="10" width="14" height="4" rx="2" />
                                <rect x="3" y="2" width="10" height="4" rx="2" />
                            </svg>
                        </div>
                    </div>
                    <div class="kpi-value-row">
                        <div class="kpi-value">{completed_tasks} <span class="unit">/ {total_tasks}</span></div>
                    </div>
                    <p class="kpi-helper">Completed task progress</p>
                    <div style="margin-top:24px;">
                        <div class="progress-track">
                            <div class="progress-fill" style="width:{progress_percentage:.1f}%; background:var(--is-fg);"></div>
                        </div>
                        <div class="progress-labels">
                            <span>0</span><span>{progress_percentage:.1f}% complete</span><span>{total_tasks}</span>
                        </div>
                    </div>             
                </div>
                """,
                unsafe_allow_html=True
            )

def goal_hit_rate_metric(show_kpi):
    if not show_kpi:
        return
    return st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-header">
                <h2 class="kpi-title">Goal Hit Rate</h2>
                <div class="kpi-icon icon-mint">
                <svg viewBox="0 0 24 24"> <path d="m9 11 3 3L22 4"/> <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/> </svg>
                </div>
            </div>
            <div class="kpi-value-row">
                <div class="kpi-value">7 <span class="unit">/ 9</span></div>
                <span class="kpi-badge badge-positive"><span class="status-dot dot-green"></span>On track</span>
            </div>
            <p class="kpi-helper">Goals achieved this month</p>
            <div style="display:flex;flex-direction:column;gap:7px;margin-top:4px;">
                <div>
                <div
                    style="display:flex;justify-content:space-between;font-size:11px;color:var(--text-label);margin-bottom:3px;">
                    <span>Daily goals</span><span>91%</span></div>
                <div class="progress-track">
                    <div class="progress-fill" style="width:91%;background:#3a9070;"></div>
                </div>
                </div>
                <div>
                <div
                    style="display:flex;justify-content:space-between;font-size:11px;color:var(--text-label);margin-bottom:3px;">
                    <span>Weekly goals</span><span>78%</span></div>
                <div class="progress-track">
                    <div class="progress-fill" style="width:78%;background:#4a9189;"></div>
                </div>
                </div>
                <div>
                <div
                    style="display:flex;justify-content:space-between;font-size:11px;color:var(--text-label);margin-bottom:3px;">
                    <span>Monthly goals</span><span>56%</span></div>
                <div class="progress-track">
                    <div class="progress-fill" style="width:56%;background:var(--ia-fg);"></div>
                </div>
                </div>
            </div>
            </div>
        """,
        unsafe_allow_html=True
    )

def output_volume_metric(show_kpi):
    if not show_kpi:
        return
    return st.markdown(
        """
        <div class="kpi-card">
            <div class="kpi-header">
                <h2 class="kpi-title">Output Volume</h2>
                <div class="kpi-icon icon-sky">
                <svg viewBox="0 0 24 24">
                    <rect x="2" y="3" width="20" height="14" rx="2" />
                    <line x1="8" x2="16" y1="21" y2="21" />
                    <line x1="12" x2="12" y1="17" y2="21" />
                </svg>
                </div>
            </div>
            <div class="kpi-value-row">
                <div class="kpi-value">143 <span class="unit">Tasks</span></div>
                <span class="kpi-badge badge-positive"><svg viewBox="0 0 24 24">
                    <polyline points="18 15 12 9 6 15" />
                </svg>+12</span>
            </div>
            <p class="kpi-helper">Delivered this month</p>
            <div class="graph-wrap">
                <!-- Planned vs Actual per week W1..W4
                Planned: 32 35 38 38 | Actual: 28 34 40 41
                viewBox 0 0 200 52, yBase=46, range 20..45 (25 units), plotH=40
                y(v)=46-((v-20)/25)*40
                P:32→20.8 35→12 38→3.2 38→3.2 | A:28→28 34→14.4 40→0 41→-1.6→clip to 1
                bar w=16, gap between pairs=6, between groups=12
                group centres: 22, 72, 122, 172
                planned bar: cx-10 to cx-2; actual: cx+2 to cx+10
            -->
                <svg viewBox="0 0 200 52" height="52" aria-label="Output volume planned vs actual W1 to W4">
                <line x1="0" y1="46" x2="200" y2="46" stroke="#ddd" stroke-width="0.8" />
                <!-- W1 -->
                <rect x="12" y="20.8" width="14" height="25.2" rx="2" fill="rgba(77,138,170,0.35)" title="Planned 32" />
                <rect x="28" y="28" width="14" height="18" rx="2" fill="#4d8aaa" title="Actual 28" />
                <!-- W2 -->
                <rect x="62" y="12" width="14" height="34" rx="2" fill="rgba(77,138,170,0.35)" title="Planned 35" />
                <rect x="78" y="14.4" width="14" height="31.6" rx="2" fill="#4d8aaa" title="Actual 34" />
                <!-- W3 -->
                <rect x="112" y="3.2" width="14" height="42.8" rx="2" fill="rgba(77,138,170,0.35)" title="Planned 38" />
                <rect x="128" y="1" width="14" height="45" rx="2" fill="#55856b" title="Actual 40" />
                <!-- W4 -->
                <rect x="162" y="3.2" width="14" height="42.8" rx="2" fill="rgba(77,138,170,0.35)" title="Planned 38" />
                <rect x="178" y="1" width="14" height="45" rx="2" fill="#55856b" title="Actual 41" />
                <text x="27" y="60" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8.5"
                    fill="#8a9691">W1</text>
                <text x="77" y="60" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8.5"
                    fill="#8a9691">W2</text>
                <text x="127" y="60" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8.5"
                    fill="#8a9691">W3</text>
                <text x="177" y="60" text-anchor="middle" font-family="Outfit,sans-serif" font-size="8.5"
                    fill="#8a9691">W4</text>
                </svg>
            </div>
            <div style="display:flex;gap:12px;font-size:10px;color:var(--text-label);margin-top:20px;">
                <span style="display:flex;align-items:center;gap:4px;">
                    <span style="width:8px;height:8px;border-radius:2px;background:rgba(77,138,170,0.35);display:inline-block;"></span>
                    Planned
                </span>
                <span style="display:flex;align-items:center;gap:4px;"><span style="width:8px;height:8px;border-radius:2px;background:#4d8aaa;display:inline-block;"></span>Actual</span>
                <span style="display:flex;align-items:center;gap:4px;"><span
                    style="width:8px;height:8px;border-radius:2px;background:#55856b;display:inline-block;"></span>Exceeded</span><br><br>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def leetcode_total_solved_metric(leetcode_data,show_kpi):
    if not show_kpi:
        return
    solved = leetcode_data["solved"]

    total_solved = solved["solvedProblem"]

    easy = solved["easySolved"]
    medium = solved["mediumSolved"]
    hard = solved["hardSolved"]

    easy_pct = round((easy / total_solved) * 100) if total_solved else 0
    medium_pct = round((medium / total_solved) * 100) if total_solved else 0
    hard_pct = round((hard / total_solved) * 100) if total_solved else 0

    TOTAL_LEETCODE_PROBLEMS = 3958
    solved_pct = round(
        (total_solved / TOTAL_LEETCODE_PROBLEMS) * 100,
        1
    )
    return st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-header">
            <h2 class="kpi-title">Total Solved</h2>
            <div class="kpi-icon icon-green">
            <svg viewBox="0 0 24 24">
                <path d="m9 11 3 3L22 4" />
                <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
            </svg>
            </div>
        </div>
        <div class="kpi-value-row">
            <div class="kpi-value">{total_solved}</div>
            <span class="kpi-badge badge-positive"><svg viewBox="0 0 24 24">
                <polyline points="18 15 12 9 6 15" />
            </svg>+12 this week</span>
        </div>
        <p class="kpi-helper">of {TOTAL_LEETCODE_PROBLEMS}+ available problems</p>
        <div style="margin-top:4px;">
            <div class="progress-track">
            <div class="progress-fill" style="width:{solved_pct}%;background:#55856b;"></div>
            </div>
            <div class="progress-labels"><span>0</span><span>{solved_pct}% solved</span><span>{TOTAL_LEETCODE_PROBLEMS}</span></div>
        </div>
        <!-- difficulty pills -->
        <div class="diff-row">
            <div class="diff-pill" style="background:var(--lc-easy-bg);">
            <span class="diff-pill-label" style="color:var(--lc-easy);">EASY</span>
            <span class="diff-pill-val" style="color:var(--lc-easy);">{easy}</span>
            <span class="diff-pill-sub" style="color:var(--lc-easy);">{easy_pct}%</span>
            </div>
            <div class="diff-pill" style="background:var(--lc-mid-bg);">
            <span class="diff-pill-label" style="color:var(--lc-mid);">MEDIUM</span>
            <span class="diff-pill-val" style="color:var(--lc-mid);">{medium}</span>
            <span class="diff-pill-sub" style="color:var(--lc-mid);">{medium_pct}%</span>
            </div>
            <div class="diff-pill" style="background:var(--lc-hard-bg);">
            <span class="diff-pill-label" style="color:var(--lc-hard);">HARD</span>
            <span class="diff-pill-val" style="color:var(--lc-hard);">{hard}</span>
            <span class="diff-pill-sub" style="color:var(--lc-hard);">{hard_pct}%</span>
            </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def leetcode_acceptance_rate_metric(leetcode_data,show_kpi):
    if not show_kpi:
        return
    ac_data = leetcode_data["solved"]["acSubmissionNum"]

    easy_data = next(
        item for item in ac_data
        if item["difficulty"] == "Easy"
    )

    medium_data = next(
        item for item in ac_data
        if item["difficulty"] == "Medium"
    )

    hard_data = next(
        item for item in ac_data
        if item["difficulty"] == "Hard"
    )

    easy_rate = round(
        easy_data["count"] /
        easy_data["submissions"] * 100,
        1
    ) if easy_data["submissions"] else 0

    medium_rate = round(
        medium_data["count"] /
        medium_data["submissions"] * 100,
        1
    ) if medium_data["submissions"] else 0

    hard_rate = round(
        hard_data["count"] /
        hard_data["submissions"] * 100,
        1
    ) if hard_data["submissions"] else 0

    overall_rate = round(
        (
            easy_data["count"] +
            medium_data["count"] +
            hard_data["count"]
        ) /
        (
            easy_data["submissions"] +
            medium_data["submissions"] +
            hard_data["submissions"]
        ) * 100,
        1
    )

    return st.markdown(
        f"""
        <div class="kpi-card">
      <div class="kpi-header">
        <h2 class="kpi-title">Acceptance Rate</h2>
        <div class="kpi-icon icon-blue">
          <svg viewBox="0 0 24 24">
            <polyline points="22 7 13.5 15.5 8.5 10.5 2 17" />
            <polyline points="16 7 22 7 22 13" />
          </svg>
        </div>
      </div>
      <div class="kpi-value-row">
        <div class="kpi-value">{overall_rate}%</div>
        <span class="kpi-badge badge-positive"><svg viewBox="0 0 24 24">
            <polyline points="18 15 12 9 6 15" />
          </svg>+3%</span>
      </div>
      <p class="kpi-helper">First-attempt acceptance rate</p>
      <div style="display:flex;flex-direction:column;gap:7px;margin-top:4px;">
        <div>
          <div
            style="display:flex;justify-content:space-between;font-size:11px;color:var(--text-label);margin-bottom:3px;">
            <span>Easy</span><span style="color:var(--lc-easy);">{easy_rate}%</span></div>
          <div class="progress-track">
            <div class="progress-fill" style="width:{easy_rate}%;background:var(--lc-easy);"></div>
          </div>
        </div>
        <div>
          <div
            style="display:flex;justify-content:space-between;font-size:11px;color:var(--text-label);margin-bottom:3px;">
            <span>Medium</span><span style="color:var(--lc-mid);">{medium_rate}%</span></div>
          <div class="progress-track">
            <div class="progress-fill" style="width:{medium_rate}%;background:var(--lc-mid);"></div>
          </div>
        </div>
        <div>
          <div
            style="display:flex;justify-content:space-between;font-size:11px;color:var(--text-label);margin-bottom:3px;">
            <span>Hard</span><span style="color:var(--lc-hard);">{hard_rate}%</span></div>
          <div class="progress-track">
            <div class="progress-fill" style="width:{hard_rate}%;background:var(--lc-hard);"></div>
          </div>
        </div>
      </div>
    </div>
        """,
        unsafe_allow_html=True
    )

def leetcode_topics_coverage_metric(leetcode_data,show_kpi):
    if not show_kpi:
        return
    skill_data = leetcode_data["skill"]

    all_topics = []

    for level in ["fundamental", "intermediate", "advanced"]:
        if level in skill_data:
            all_topics.extend(skill_data[level])

    if not all_topics:
        return

    all_topics = sorted(
        all_topics,
        key=lambda x: x["problemsSolved"],
        reverse=True
    )

    top_topics = all_topics[:5]

    total_tags = len(all_topics)

    max_solved = max(
        topic["problemsSolved"]
        for topic in top_topics
    )

    colors = [
        "#55856b",
        "#4a9189",
        "#5c7b9c",
        "#8c5a9c",
        "#9c7442",
        "#4d8aaa"
    ]

    topics_html = ""

    for idx, topic in enumerate(top_topics):

        name = topic["tagName"]

        solved = topic["problemsSolved"]

        width = max(
            10,
            int((solved / max_solved) * 100)
        )

        color = colors[idx % len(colors)]

        topics_html += f"""<div class="topic-item"><span class="topic-name">{name}</span> <div class="topic-bar-track"><div class="topic-bar-fill" style="width:{width}%; background:{color};"></div></div><span class="topic-count">{solved}</span></div>"""
    return st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-header">
            <h2 class="kpi-title">Top Topics</h2>
            <div class="kpi-icon icon-purple">
            <svg viewBox="0 0 24 24">
                <rect x="3" y="3" width="18" height="18" rx="2" />
                <path d="M9 9h1v6H9z" />
                <path d="M14 9h1v6h-1z" />
            </svg>
            </div>
        </div>
        <div class="kpi-value-row">
            <div class="kpi-value">{total_tags} <span class="unit">tags</span></div>
        </div>
        <p class="kpi-helper">Problem categories attempted</p>
        <div class="topic-row">
            {topics_html}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def leetcode_languages_used_metric(leetcode_data,show_kpi):
    if not show_kpi:
        return
    languages = leetcode_data["language"]["languageProblemCount"]

    if not languages:
        return st.markdown(
            """
            <div class="kpi-card">
                <h2 class="kpi-title">Most Used Language</h2>
                <p>No language data available</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    total = sum(lang["problemsSolved"] for lang in languages)

    languages = sorted(
        languages,
        key=lambda x: x["problemsSolved"],
        reverse=True
    )

    primary = languages[0]

    primary_name = primary["languageName"]

    primary_pct = round(
        primary["problemsSolved"] / total * 100,
        1
    )

    color_map = {
        "Python": "var(--py)",
        "Python3": "var(--py)",

        "Java": "var(--java)",

        "C++": "var(--cpp)",
        "Cpp": "var(--cpp)",

        "JavaScript": "var(--js)",
        "JS": "var(--js)",

        "Go": "var(--go)",

        "MySQL": "var(--mysql)",
        "SQL": "var(--mysql)",

        "C": "var(--c)"
    }

    bars_html = ""

    for lang in languages[:5]:

        name = lang["languageName"]

        pct = round(
            lang["problemsSolved"] / total * 100,
            1
        )

        color = color_map.get(
            name,
            "var(--accent)"
        )

        bars_html += f"""<div class="lang-bar-row"><span class="lang-bar-name" style="color:{color};width:48px;font-size:10px;">{name}</span> <div class="lang-bar-track"><div class="lang-bar-fill" style="width:{pct}%; background:{color};"></div></div> <span class="lang-bar-pct" style="color:{color};">{pct}% </span></div>"""

    primary_color = color_map.get(
        primary_name,
        "var(--accent)"
    )
    return st.markdown(
        f"""
            <div class="kpi-card">
            <div class="kpi-header">
                <h2 class="kpi-title">Most Used Language</h2>
                <div class="kpi-icon icon-blue">
                <svg viewBox="0 0 24 24">
                    <polyline points="16 18 22 12 16 6" />
                    <polyline points="8 6 2 12 8 18" />
                </svg>
                </div>
            </div>
            <div class="kpi-value-row">
                <div class="kpi-value" style="color:{primary_color};">{primary_name}</div>
                <span class="kpi-badge badge-positive"><span class="status-dot dot-blue"></span>Primary</span>
            </div>
            <p class="kpi-helper">{primary_pct}% of all submissions</p>
            <div style="margin-top:4px;display:flex;flex-direction:column;gap:6px;">{bars_html}</div>
            </div>
        """,
        unsafe_allow_html=True
    )

def leetcode_streak_metric(leetcode_data,show_kpi):
    if not show_kpi:
        return
    calendar_data = json.loads(
        leetcode_data["calendar"]["submissionCalendar"]
    )

    # Convert timestamps to dates
    submissions = {}

    for ts, count in calendar_data.items():
        date = datetime.fromtimestamp(int(ts)).date()
        submissions[date] = count

    if not submissions:
        return st.markdown("<div>No data available</div>",
                           unsafe_allow_html=True)

    # ---------- Current Streak ----------
    today = datetime.today().date()

    current_streak = 0
    day = today

    while submissions.get(day, 0) > 0:
        current_streak += 1
        day -= timedelta(days=1)

    # ---------- Best Streak ----------
    dates = sorted(submissions.keys())

    best_streak = 0
    streak = 0
    prev = None

    for d in dates:

        if submissions[d] == 0:
            streak = 0
            continue

        if prev and (d - prev).days == 1:
            streak += 1
        else:
            streak = 1

        best_streak = max(best_streak, streak)
        prev = d

    # ---------- Progress ----------
    progress_pct = (
        (current_streak / best_streak) * 100
        if best_streak else 0
    )

    progress_pct = min(progress_pct, 100)

    # ---------- Milestones ----------
    milestones = [7, 14, 30, 60, 100]

    milestone_html = ""

    for i, milestone in enumerate(milestones):

        status = (
            "done"
            if current_streak >= milestone
            else "next"
        )

        milestone_html += f"""<div class="milestone"> <div class="milestone-dot {status}"></div> <div class="milestone-num">{milestone}</div></div>"""

        if i < len(milestones) - 1:
            milestone_html += """
            <div class="milestone-line"></div>
            """
    return st.markdown(
        f"""
        <div class="kpi-card">
        <div class="kpi-header">
            <h2 class="kpi-title">Solving Streak</h2>
            <div class="kpi-icon icon-amber">
            <svg viewBox="0 0 24 24">
                <path
                d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z" />
            </svg>
            </div>
        </div>
        <div class="kpi-value-row">
            <div class="kpi-value">{current_streak} <span class="unit">days</span></div>
            <span class="kpi-badge badge-positive"><span class="status-dot dot-green"></span>Active</span>
        </div>
        <p class="kpi-helper">Consecutive days with a solve</p>
        
        <div class="progress-section">
            <div class="progress-header">
                <span class="progress-label">Progress to best streak</span>
                <span class="progress-pct">{current_streak} / {best_streak}</span>
                </div>
                <div class="progress-track">
                <div class="progress-fill" style="width:{progress_pct}%;"></div>
                </div>
                <div class="milestone-row">{milestone_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True)

def leetcode_submission_metric(leetcode_data,show_kpi):
    if not show_kpi:
        return
    calendar_data = json.loads(
        leetcode_data["calendar"]["submissionCalendar"]
    )

    # --- FIX: use UTC midnight timestamp, matching LeetCode's calendar keys ---
    today_timestamp = int(
        datetime.now(timezone.utc)
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .timestamp()
    )

    today_count = calendar_data.get(str(today_timestamp), 0)

    activity = sorted(
        [
            (int(ts), count)
            for ts, count in calendar_data.items()
        ],
        key=lambda x: x[0]
    )

    # Last 100 days
    last_100_days = activity[-100:]

    max_count = max(
        [count for _, count in last_100_days],
        default=1
    )
    if max_count == 0:
        max_count = 1  # avoid division issues if all zero

    total_submissions_100d = sum(count for _, count in last_100_days)

    heatmap_html = ""

    for _, count in last_100_days:
        if count == 0:
            level = "l0"
        elif count <= max_count * 0.25:
            level = "l1"
        elif count <= max_count * 0.50:
            level = "l2"
        elif count <= max_count * 0.75:
            level = "l3"
        else:
            level = "l4"

        heatmap_html += f'<div class="hm-cell {level}" title="{count} submissions"></div>'
    return st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <h2 class="kpi-title">Daily Submissions</h2>
                <div class="kpi-icon icon-mint">
                <svg viewBox="0 0 24 24">
                    <rect x="3" y="4" width="18" height="18" rx="2" />
                    <line x1="16" x2="16" y1="2" y2="6" />
                    <line x1="8" x2="8" y1="2" y2="6" />
                    <line x1="3" x2="21" y1="10" y2="10" />
                </svg>
                </div>
            </div>
            <div class="kpi-value-row">
                <div class="kpi-value">{today_count}</div>
                <span class="kpi-badge badge-positive"><span class="status-dot dot-green"></span>Active</span>
            </div>
            <p class="kpi-helper">Submissions in last 100 days</p>
            <div class="heatmap-grid">
                {heatmap_html}
            </div>
            <div class="hm-labels">
                <span class="hm-label">100d ago</span>
                <span class="hm-label">today</span>
            </div>
            <div class="hm-legend">
                <span class="hm-legend-label">Less</span>
                <div class="hm-legend-track">
                <div class="hm-legend-step l0"></div>
                <div class="hm-legend-step l1"></div>
                <div class="hm-legend-step l2"></div>
                <div class="hm-legend-step l3"></div>
                <div class="hm-legend-step l4"></div>
                </div>
                <span class="hm-legend-label">More</span>
            </div>
            </div>
        """,
        unsafe_allow_html=True
    )



def makeLineChart(df):

    # =====================================
    # EDGE CASES
    # =====================================

    if df.empty:

        return

    chart_df = df.copy()

    chart_df["date"] = pd.to_datetime(
        chart_df["date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    chart_df = chart_df.dropna(
        subset=["date"]
    )

    if chart_df.empty:

        return

    chart_df = chart_df.sort_values(
        by="date"
    )

    x_data = chart_df["date"].dt.strftime(
        "%d-%m-%Y"
    ).tolist()

    y_data = chart_df[
        "completion_percentage"
    ].fillna(0).tolist()

    # =====================================
    # ECHARTS OPTIONS
    # =====================================

    option = {

        "tooltip": {
            "trigger": "axis"
        },

        "grid": {
            "left": "5%",
            "right": "5%",
            "bottom": "10%",
            "top": "10%",
            "containLabel": True
        },

        "xAxis": {
            "type": "category",
            "data": x_data,
            "boundaryGap": False
        },

        "yAxis": {
            "type": "value",
            "min": 0,
            "max": 100
        },

        "series": [
            {
                "name": "Completion %",
                "type": "line",

                "data": y_data,

                "smooth": True,

                "symbol": "circle",

                "symbolSize": 8,

                "lineStyle": {
                    "width": 4,
                    "color": "#55856b"
                },

                "itemStyle": {
                    "color": "#55856b"
                },

                "areaStyle": {
                    "opacity": 0.15
                }
            }
        ]
    }
    return option