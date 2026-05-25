# 📊 Google Productivity Dashboard

A professional Streamlit dashboard that integrates with **Google Tasks API** and **Google Calendar API** to manage tasks, monitor productivity, and visualize daily schedules in real-time.

Built using:
- Python
- Streamlit
- Google OAuth 2.0
- Google Tasks API
- Google Calendar API

---

# 🚀 Features

## ✅ Google Tasks Integration
- View pending tasks
- View completed tasks
- Mark tasks as completed
- Create new tasks
- Create new task lists
- Organize tasks by task list

---

## 📅 Google Calendar Integration
- Fetch upcoming calendar events
- Daily schedule overview
- Event visualization

---

## 📈 Productivity Dashboard
- Task analytics
- Completion tracking
- Productivity metrics
- Real-time updates

---

# 🧠 Project Architecture

```text
google-productivity-dashboard/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── credentials.json
├── token.json
│
├── config/
│   └── settings.py
│
├── auth/
│   └── google_auth.py
│
├── services/
│   ├── calendar_service.py
│   └── tasks_service.py
│
├── components/
│   ├── task_cards.py
│   ├── calendar_view.py
│   └── metrics.py
│
├── utils/
│   ├── helpers.py
│   └── date_utils.py
│
├── data/
│   └── cache/
│
├── assets/
│   ├── styles.css
│   └── logo.png
│
└── view/
    ├── dashboard.py
    ├── analytics.py
    └── settings.py
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/google-productivity-dashboard.git

cd google-productivity-dashboard
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Google API Setup

---

## Step 1: Create Google Cloud Project

Go to:

https://console.cloud.google.com/

Create a new project.

---

## Step 2: Enable APIs

Enable:
- Google Tasks API
- Google Calendar API

---

## Step 3: Configure OAuth Consent Screen

- User Type → External
- Add test users
- Add required scopes

Required scopes:

```python
https://www.googleapis.com/auth/tasks
https://www.googleapis.com/auth/calendar.readonly
```

---

## Step 4: Create OAuth Credentials

Create:
```text
OAuth Client ID
```

Application Type:
```text
Desktop App
```

Download credentials JSON file.

Rename it:

```text
credentials.json
```

Move it to project root folder.

---

# ▶️ Running The App

```bash
streamlit run app.py
```

---

# 🔑 First Login

When app starts:
- Google login popup opens
- Login with your Gmail
- Allow permissions

After successful login:
```text
token.json
```
is automatically generated.

---

# 📦 requirements.txt

```txt
streamlit
google-auth-oauthlib
google-api-python-client
pandas
plotly
```

---

# 🧠 Authentication Flow

```text
User Login
    ↓
Google OAuth
    ↓
Access Token Generated
    ↓
token.json Saved
    ↓
Google APIs Accessible
```

---

# 📂 Core Modules

---

## 🔐 auth/

Handles:
- OAuth authentication
- Token generation
- Token refresh

---

## ⚡ services/

Handles:
- Google API communication
- Task CRUD operations
- Calendar operations

---

## 🧩 components/

Reusable UI components:
- Task cards
- Calendar widgets
- KPI metrics

---

## 🛠 utils/

Utility/helper functions:
- Date formatting
- Task sorting
- Data cleanup

---

## 👀 view/

Contains:
- Dashboard screens
- Analytics screens
- App views

---

# 🚀 Current Features

| Feature | Status |
|---|---|
| Google Login | ✅ |
| Fetch Tasks | ✅ |
| Completed Tasks | ✅ |
| Create Tasks | ✅ |
| Create Task Lists | ✅ |
| Complete Tasks | ✅ |
| Calendar Events | ✅ |
| Productivity Analytics | 🚧 |
| AI Insights | 🚧 |

---

# 📈 Future Improvements

## Planned Features

- Productivity charts
- Streak tracking
- AI productivity assistant
- Smart scheduling
- Notification system
- Dark mode
- CSV/PDF exports
- Deployment pipeline

---

# 🔥 Example Dashboard Flow

```text
Google Tasks API
        ↓
Services Layer
        ↓
Caching Layer
        ↓
Components
        ↓
Dashboard UI
```

---

# 🧠 Caching Strategy

The project supports caching for:
- Task analytics
- Calendar events
- Charts
- API optimization

Example:

```python
@st.cache_data(ttl=60)
def load_tasks():
    pass
```

---

# 🚨 Security Notes

## DO NOT upload:

```text
credentials.json
token.json
```

to GitHub.

These files contain private credentials.

---

# ✅ .gitignore

```gitignore
token.json
credentials.json
__pycache__/
.env
```

---

# 🐳 Deployment Ideas

Can be deployed on:
- Streamlit Cloud
- Render
- Railway
- AWS
- Azure

---

# 👨‍💻 Tech Stack

| Technology | Usage |
|---|---|
| Python | Backend |
| Streamlit | Frontend |
| Google OAuth | Authentication |
| Google Tasks API | Task Management |
| Google Calendar API | Scheduling |
| Pandas | Analytics |
| Plotly | Visualization |

---

# 📸 Screenshots

Add screenshots here later.

Example:

```markdown
![Dashboard Screenshot](assets/dashboard.png)
```

---

# 🤝 Contributing

Contributions are welcome.

Steps:
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push branch
5. Open Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 🌟 Author

Developed by Anik Dashora 🚀

```