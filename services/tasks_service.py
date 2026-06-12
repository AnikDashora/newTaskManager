import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import datetime
import pandas as pd

# =====================================================
# GOOGLE AUTH
# =====================================================
@st.cache_data(ttl=200)
def fetch_tasks_data():

    task_columns = [
        "date",
        "task",
        "status"
    ]

    outcome_columns = [
        "date",
        "total_completed_task",
        "total_task",
        "completion_percentage"
    ]

    try:
        SCOPES = [
            "https://www.googleapis.com/auth/tasks"
        ]

        token_info = dict(st.secrets["token_data"])

        creds = Credentials(
            token=token_info["token"],
            refresh_token=token_info["refresh_token"],
            token_uri=token_info["token_uri"],
            client_id=token_info["client_id"],
            client_secret=token_info["client_secret"],
            scopes=token_info["scopes"]
        )

        if creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request
            creds.refresh(Request())

        tasks_service = build(
            "tasks",
            "v1",
            credentials=creds
        )

        task_data = []
        outcome_data = []

        tasklists = tasks_service.tasklists().list().execute()

        for tasklist in tasklists.get("items", []):

            list_name = tasklist["title"]

            try:
                formatted_date = datetime.strptime(
                    list_name,
                    "%d-%b-%Y"
                ).strftime("%d-%m-%Y")
            except:
                continue

            tasks = tasks_service.tasks().list(
                tasklist=tasklist["id"],
                showCompleted=True,
                showHidden=True
            ).execute()

            total_completed_task = 0
            total_task = 0

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

            completion_percentage = (
                round((total_completed_task / total_task) * 100, 2)
                if total_task > 0
                else 0
            )

            outcome_data.append([
                formatted_date,
                total_completed_task,
                total_task,
                completion_percentage
            ])

        task_df = pd.DataFrame(
            task_data,
            columns=task_columns
        )

        outcome_df = pd.DataFrame(
            outcome_data,
            columns=outcome_columns
        )

        if not task_df.empty:
            task_df["date"] = pd.to_datetime(
                task_df["date"],
                format="%d-%m-%Y"
            )
            task_df = task_df.sort_values("date")
            task_df["date"] = task_df["date"].dt.strftime("%d-%m-%Y")

        if not outcome_df.empty:
            outcome_df["date"] = pd.to_datetime(
                outcome_df["date"],
                format="%d-%m-%Y"
            )
            outcome_df = outcome_df.sort_values("date")
            outcome_df["date"] = outcome_df["date"].dt.strftime("%d-%m-%Y")

        return task_df, outcome_df

    except Exception as e:
        st.error(f"Failed to fetch Google Tasks data: {e}")

        task_df = pd.DataFrame(columns=task_columns)
        outcome_df = pd.DataFrame(columns=outcome_columns)

        return task_df, outcome_df