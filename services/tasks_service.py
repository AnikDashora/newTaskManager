import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime
import pandas as pd

# =====================================================
# GOOGLE AUTH
# =====================================================

def fetch_tasks_data():

    SCOPES = [
        "https://www.googleapis.com/auth/tasks"
    ]

    # =====================================================
    # LOAD TOKEN FROM STREAMLIT SECRETS
    # =====================================================

    token_info = dict(st.secrets["token_data"])

    creds = Credentials(
        token=token_info["token"],
        refresh_token=token_info["refresh_token"],
        token_uri=token_info["token_uri"],
        client_id=token_info["client_id"],
        client_secret=token_info["client_secret"],
        scopes=token_info["scopes"]
    )

    # =====================================================
    # REFRESH TOKEN IF EXPIRED
    # =====================================================

    if creds.expired and creds.refresh_token:

        from google.auth.transport.requests import Request

        creds.refresh(Request())

    # =====================================================
    # BUILD GOOGLE TASKS API
    # =====================================================

    tasks_service = build(
        "tasks",
        "v1",
        credentials=creds
    )

    # =====================================================
    # STORAGE
    # =====================================================

    task_data = []

    outcome_data = []

    # =====================================================
    # FETCH TASK LISTS
    # =====================================================

    tasklists = tasks_service.tasklists().list().execute()

    # =====================================================
    # LOOP THROUGH TASK LISTS
    # =====================================================

    for tasklist in tasklists.get("items", []):

        list_name = tasklist["title"]

        try:

            formatted_date = datetime.strptime(
                list_name,
                "%d-%b-%Y"
            ).strftime("%d-%m-%Y")

        except:

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

            if google_status == "completed":

                status = "completed"

                total_completed_task += 1

            else:

                status = "pending"

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

                (total_completed_task / total_task) * 100,

                2
            )

        else:

            completion_percentage = 0

        # =================================================
        # OUTCOME DATA
        # =====================================================

        outcome_data.append([

            formatted_date,

            total_completed_task,

            total_task,

            completion_percentage
        ])

    # =====================================================
    # CREATE DATAFRAMES
    # =====================================================

    task_df = pd.DataFrame(

        task_data,

        columns=[

            "date",
            "task",
            "status"
        ]
    )

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
    # SORT DATA BY DATE
    # =====================================================

    task_df["date"] = pd.to_datetime(
        task_df["date"],
        format="%d-%m-%Y"
    )

    outcome_df["date"] = pd.to_datetime(
        outcome_df["date"],
        format="%d-%m-%Y"
    )

    task_df = task_df.sort_values(
        by="date"
    )

    outcome_df = outcome_df.sort_values(
        by="date"
    )

    # =====================================================
    # CONVERT DATE BACK TO STRING
    # =====================================================

    task_df["date"] = task_df["date"].dt.strftime(
        "%d-%m-%Y"
    )

    outcome_df["date"] = outcome_df["date"].dt.strftime(
        "%d-%m-%Y"
    )

    return task_df, outcome_df