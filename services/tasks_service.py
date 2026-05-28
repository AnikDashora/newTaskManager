import os
import streamlit as st
import pandas as pd

from datetime import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# =====================================================
# GOOGLE AUTH
# =====================================================

def fetch_tasks_data():

    SCOPES = [
        "https://www.googleapis.com/auth/tasks.readonly"
    ]

    # =================================================
    # GOOGLE CLIENT CONFIG FROM STREAMLIT SECRETS
    # =================================================

    client_config = {

        "installed": {

            "client_id":
            st.secrets["google"]["client_id"],

            "project_id":
            st.secrets["google"]["project_id"],

            "auth_uri":
            st.secrets["google"]["auth_uri"],

            "token_uri":
            st.secrets["google"]["token_uri"],

            "auth_provider_x509_cert_url":
            st.secrets["google"][
                "auth_provider_x509_cert_url"
            ],

            "client_secret":
            st.secrets["google"]["client_secret"],

            "redirect_uris":
            st.secrets["google"]["redirect_uris"]
        }
    }

    creds = None

    # =================================================
    # LOAD TOKEN
    # =================================================

    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # =================================================
    # LOGIN
    # =================================================

    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_config(
            client_config,
            SCOPES
        )

        # ---------------------------------------------
        # STREAMLIT CLOUD FRIENDLY
        # ---------------------------------------------

        creds = flow.run_console()

        with open("token.json", "w") as token:

            token.write(creds.to_json())

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

        # ---------------------------------------------
        # ONLY DATE FORMAT LISTS
        # Example:
        # 28-May-2026
        # ---------------------------------------------

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
        # LOOP TASKS
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
            # STATUS
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
    # SORT DATE
    # =====================================================

    if not task_df.empty:

        task_df["date"] = pd.to_datetime(
            task_df["date"],
            format="%d-%m-%Y"
        )

        task_df = task_df.sort_values(
            by="date"
        )

        task_df["date"] = task_df[
            "date"
        ].dt.strftime("%d-%m-%Y")

    if not outcome_df.empty:

        outcome_df["date"] = pd.to_datetime(
            outcome_df["date"],
            format="%d-%m-%Y"
        )

        outcome_df = outcome_df.sort_values(
            by="date"
        )

        outcome_df["date"] = outcome_df[
            "date"
        ].dt.strftime("%d-%m-%Y")

    return task_df, outcome_df