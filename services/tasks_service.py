import os
import streamlit as st
import pandas as pd

from datetime import datetime

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# =====================================================
# FETCH TASK DATA
# =====================================================

def fetch_tasks_data():

    # =================================================
    # GOOGLE SCOPES
    # =================================================

    SCOPES = [
        "https://www.googleapis.com/auth/tasks.readonly"
    ]

    # =================================================
    # LOAD TOKEN
    # =================================================

    creds = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )

    # =================================================
    # BUILD TASKS API
    # =================================================

    tasks_service = build(
        "tasks",
        "v1",
        credentials=creds
    )

    # =================================================
    # STORAGE
    # =================================================

    task_data = []

    outcome_data = []

    # =================================================
    # FETCH TASK LISTS
    # =================================================

    tasklists = tasks_service.tasklists().list().execute()

    # =================================================
    # LOOP THROUGH TASK LISTS
    # =================================================

    for tasklist in tasklists.get("items", []):

        list_name = tasklist["title"]

        # -------------------------------------------------
        # ONLY ALLOW DATE FORMAT LISTS
        # Example:
        # 28-May-2026
        # -------------------------------------------------

        try:

            formatted_date = datetime.strptime(
                list_name,
                "%d-%b-%Y"
            ).strftime("%d-%m-%Y")

        except:

            # Skip default Google lists
            continue

        # =================================================
        # FETCH TASKS
        # =================================================

        tasks = tasks_service.tasks().list(
            tasklist=tasklist["id"],
            showCompleted=True,
            showHidden=True
        ).execute()

        total_completed_task = 0

        total_task = 0

        # =================================================
        # LOOP THROUGH TASKS
        # =================================================

        for task in tasks.get("items", []):

            total_task += 1

            task_title = task.get(
                "title",
                "Untitled"
            )

            google_status = task.get(
                "status",
                "needsAction"
            )

            # ---------------------------------------------
            # STATUS CONVERSION
            # ---------------------------------------------

            if google_status == "completed":

                status = "completed"

                total_completed_task += 1

            else:

                status = "pending"

            # ---------------------------------------------
            # TASK DATA
            # ---------------------------------------------

            task_data.append([

                formatted_date,
                task_title,
                status
            ])

        # =================================================
        # COMPLETION PERCENTAGE
        # =================================================

        if total_task > 0:

            completion_percentage = round(

                (
                    total_completed_task
                    / total_task
                ) * 100,

                2
            )

        else:

            completion_percentage = 0

        # =================================================
        # OUTCOME DATA
        # =================================================

        outcome_data.append([

            formatted_date,

            total_completed_task,

            total_task,

            completion_percentage
        ])

    # =====================================================
    # CREATE TASK DATAFRAME
    # =====================================================

    task_df = pd.DataFrame(

        task_data,

        columns=[

            "date",
            "task",
            "status"
        ]
    )

    # =====================================================
    # CREATE OUTCOME DATAFRAME
    # =====================================================

    outcome_df = pd.DataFrame(

        outcome_data,

        columns=[

            "date",
            "total_completed_task",
            "total_task",
            "completion_percentage"
        ]
    )

    # =====================================================
    # HANDLE EMPTY DATAFRAMES
    # =====================================================

    if task_df.empty:

        task_df = pd.DataFrame(
            columns=[
                "date",
                "task",
                "status"
            ]
        )

    if outcome_df.empty:

        outcome_df = pd.DataFrame(
            columns=[
                "date",
                "total_completed_task",
                "total_task",
                "completion_percentage"
            ]
        )

    # =====================================================
    # SORT TASK DATAFRAME
    # =====================================================

    if not task_df.empty:

        task_df["date"] = pd.to_datetime(
            task_df["date"],
            format="%d-%m-%Y",
            errors="coerce"
        )

        task_df = task_df.sort_values(
            by="date"
        )

        task_df["date"] = task_df[
            "date"
        ].dt.strftime("%d-%m-%Y")

    # =====================================================
    # SORT OUTCOME DATAFRAME
    # =====================================================

    if not outcome_df.empty:

        outcome_df["date"] = pd.to_datetime(
            outcome_df["date"],
            format="%d-%m-%Y",
            errors="coerce"
        )

        outcome_df = outcome_df.sort_values(
            by="date"
        )

        outcome_df["date"] = outcome_df[
            "date"
        ].dt.strftime("%d-%m-%Y")

    # =====================================================
    # RETURN DATA
    # =====================================================

    return task_df, outcome_df