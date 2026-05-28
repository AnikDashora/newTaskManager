import math

from matplotlib.pyplot import bar
import streamlit as st
import os
import sys
import random
import pandas as pd
from streamlit_echarts import st_echarts
from datetime import datetime, timedelta, date


def completion_trend_metric(df):
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["week"] = df["date"].dt.strftime("%Y-%U")
    # Group by week and calculate average completion percentage
    weekly_data = (
        df.groupby("week")["completion_percentage"]
        .mean()
        .reset_index()
    )

    # Get current week average
    current_week_avg = weekly_data.iloc[-1]["completion_percentage"]

    # Get previous week average
    previous_week_avg = weekly_data.iloc[-2]["completion_percentage"]

    # Find percentage change
    percent_change = int(round(
        (
            (current_week_avg - previous_week_avg)
            / previous_week_avg
        ) * 100,
        2
    ))

    last_8_days = (
        df.sort_values("date")
        .tail(8)
    )

    values = last_8_days["completion_percentage"].tolist()

    # Normalize values to SVG height
    svg_width = 200
    svg_height = 50

    min_val = min(values)
    max_val = max(values)

    # Avoid division by zero
    if max_val == min_val:
        max_val += 1

    points = []

    for i, value in enumerate(values):

        # X position
        x = (i / (len(values) - 1)) * svg_width

        # Y position (invert because SVG origin is top-left)
        y = svg_height - (
            ((value - min_val) / (max_val - min_val))
            * svg_height
        )

        points.append(f"{x},{y}")

    polyline_points = " ".join(points)

    # Area fill polygon
    polygon_points = (
        f"0,{svg_height} "
        + polyline_points
        + f" {svg_width},{svg_height}"
    )

    # =========================
    # UI COLORS
    # =========================

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

def average_completion_metric(df):
    average_completion = round(
        df["completion_percentage"].mean(),
        2
    )

    remaining = 100 - average_completion

    # -----------------------------
    # DONUT CHART LOGIC
    # -----------------------------

    radius = 24

    circumference = 2 * math.pi * radius

    # Completed stroke
    completed_stroke = (
        average_completion / 100
    ) * circumference

    # Remaining stroke
    remaining_stroke = circumference - completed_stroke

    # Dynamic dasharray
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

def total_progress_metric(df):
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

def monthly_rate_metric(df):
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
                                stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />
                            {''.join(circle_text)}
                            {''.join(month_name)}
                        </svg>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

def active_days_metric(df):

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
                    <div class="activity-bars" aria-label="Activity heatmap: {active_days} active days">
                        {''.join(bar_html)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

def weekly_rate_metric(df):

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
                    <svg viewBox="0 0 200 64" height="64" aria-label="Weekly completion: Mon 70% to Sun 82%">
                        <line x1="0" y1="52" x2="200" y2="52" stroke="#ddd" stroke-width="0.8" />
                        {''.join(bars_html)}
                        {''.join(labels_html)}
                    </svg>
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )

def productivity_streak_metric(df, expected_percentage_streak):
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

    streak_start_index = 0

    # Loop backwards
    for i in range(len(df) - 1, -1, -1):

        completion = df.loc[i, "completion_percentage"]

        # Break streak
        if completion < expected_percentage_streak:

            streak_start_index = i + 1
            break

    # -----------------------------
    # STREAK DATAFRAME
    # -----------------------------

    streak_df = df.iloc[streak_start_index:]

    # Total streak days
    streak_days = len(streak_df)

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
                    <div class="activity-bars" aria-label="Daily productivity scores over 14 days" style="margin-top:22px;">{''.join(bars_html)}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

def needs_attendtion_metric(df):

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
                                stroke="#c96868" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" />
                            {''.join(circle_html)}
                            {''.join(label_html)}
                        </svg>
                    </div>
                </div>
                    """,
                    unsafe_allow_html=True
                )

def todays_progress_metric(df):
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