import os
from datetime import datetime
import pandas as pd
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# =====================================================
# GOOGLE AUTH
# =====================================================
def fetch_tasks_data():
    SCOPES = [
        "https://www.googleapis.com/auth/tasks"
    ]

    creds = None

    # -----------------------------------------------------
    # LOAD EXISTING TOKEN
    # -----------------------------------------------------

    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # -----------------------------------------------------
    # LOGIN IF TOKEN MISSING
    # -----------------------------------------------------

    if not creds or not creds.valid:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:

            token.write(creds.to_json())

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

                (total_completed_task / total_task) * 100,

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

    # =====================================================
    # DISPLAY
    # =====================================================

    # print("\n================ TASK DATA =================\n")

    # print(task_df)

    # print("\n================ OUTCOME DATA =================\n")

    # print(outcome_df)

    # =====================================================
    # OPTIONAL CSV EXPORT
    # =====================================================

    # task_df.to_csv(
    #     "task_data.csv",
    #     index=False
    # )

    # outcome_df.to_csv(
    #     "outcome_data.csv",
    #     index=False
    # )

    # print("\nCSV files exported successfully ✅")