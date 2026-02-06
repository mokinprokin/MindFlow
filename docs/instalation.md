# 🚀 Installation & Setup Guide

This guide will walk you through setting up the MindFlow, from configuring Google Cloud APIs to launching the application on your local machine.

## ☁️ Google Cloud Platform (GCP) Configuration

The application requires access to the Google Sheets API and Google Drive API to synchronize your planner tasks.

### 📋 Step-by-Step API Setup

1. **🌐 Go to Google Cloud Console**: [https://console.cloud.google.com](https://console.cloud.google.com)

2. **📁 Create a New Project**: Click the project dropdown in the top left and select "New Project". Give it a name like `MindFlow-Planner`.

3. **🔧 Enable the APIs**:
   - Navigate to **APIs & Services > Library**
   - Search for "Google Sheets API" and click **Enable**
   - Search for "Google Drive API" and click **Enable**

4. **🔐 Configure OAuth Consent Screen**:
   - Go to **APIs & Services > OAuth consent screen**
   - Select **External** (unless you have a Workspace organization)
   - Fill in the required App Information (App name, support email)
   - Add the following scopes:
     - `https://www.googleapis.com/auth/spreadsheets`
     - `https://www.googleapis.com/auth/drive.metadata.readonly`

5. **🔑 Create Credentials**:
   - Go to **APIs & Services > Credentials**
   - Click **Create Credentials > OAuth client ID**
   - Select **Desktop App** as the application type
   - Once created, you will receive your **Client ID** and **Client Secret**. Copy these for your `.env` file.

## 💻 Local Environment Setup

Open your terminal or command prompt in the project root directory.

### 🐍 Create and Activate Virtual Environment

We recommend using a virtual environment to manage dependencies:

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 📦 Install Dependencies

Use pip to install the required libraries:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration (.env)

Create a file named `.env` in the project root and populate it with the following variables. Replace `your_google_client_id` and `your_google_client_secret` with the credentials obtained in Step 1.

```env
# Database
DB_PATH=./src/data/planner.db

# Sync Settings
SYNC_START_HOUR=9
SYNC_END_HOUR=18
SYNC_CHECK_INTERVAL=300

# UI Colors
PRIMARY_COLOR=#007bff
SECONDARY_COLOR=#6c757d
ACCENT_COLOR=#28a745
TEXT_COLOR=#000000
TEXT_SECONDARY=#666666
CHECKBOX_COLOR=#007bff

# Google API Credentials
CLIENT_ID=your_google_client_id
CLIENT_SECRET=your_google_client_secret
TOKEN_URI=https://oauth2.googleapis.com/token
SCOPES=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.metadata.readonly"]
```

## ▶️ Running the Application

Once your environment is set up and your `.env` file is ready, you can launch the application.

### 🚀 Start the Application

Run the main entry point as a module:

```bash
python -m src.main
```

### 🔄 What happens next?

- **🌐 Browser Auth**: On the first run, a browser window will open asking you to authorize the application via Google
- **🗄️ Initialization**: The app will create `src/data/planner.db` if it doesn't exist
- **🔄 Sync**: Tasks will be fetched from your Google Sheets
- **🎤 Background Services**: Voice engines and Notification services will start automatically

> **💡 Tip**: If the voice engine fails to start, ensure your microphone is connected and permissions are granted.
