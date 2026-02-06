# 📁 Project Structure Documentation

This document provides a detailed overview of the codebase structure for the MindFlow.

## 📂 Root Level Files

- **alembic.ini** 📄: Configuration file for Alembic database migration tool.
- **requirements.txt** 📄: List of Python dependencies required for the project.
- **README.md** 📄: Main documentation file with installation, usage, and feature descriptions.

## 📂 `src/` Directory

The main source code directory containing all application logic.

### 🔧 Core Files

- **config.py** 📄: Application configuration using Pydantic settings. Handles environment variables for database, sync settings, UI colors, and Google API credentials.
- **main.py** 📄: Entry point of the application. Initializes the database and starts background services.

### 📊 `data/` Directory

- **planner.db** 🗄️: SQLite database file storing tasks, words, and application state.
- **sync_state.json** 📄: JSON file tracking synchronization state with Google Sheets.

### 🗄️ `db/` Directory

Database-related modules.

- **database.py** 📄: Database initialization and connection management using SQLAlchemy with async support.
- **db_manager.py** 📄: Database manager class for handling connections and operations.
- **dependencies.py** 📄: Dependency injection utilities for database sessions.
- **repositories/** 📁: Repository pattern implementation.
  - **base_mapper.py** 📄: Base mapper class for database operations.
  - **base.py** 📄: Base repository class with common CRUD operations.

### ⚙️ `features/` Directory

Feature-based organization of application modules.

#### 🇬🇧 `english/` Directory

English learning functionality.

- **model.py** 📄: SQLAlchemy models for words and related entities.
- **repository.py** 📄: Repository for word-related database operations.
- **schemas.py** 📄: Pydantic schemas for word data validation.
- **services/** 📁: Business logic for English features.
  - **repetition.py** 📄: Spaced repetition algorithm implementation.
  - **word_show.py** 📄: Service for displaying words in quizzes.
  - **word_write.py** 📄: Service for adding new words to vocabulary.

#### 🌐 `google/` Directory

Google API integrations.

- **schemas/** 📁: Data models for Google services.
  - **google_sheets.py** 📄: Schema for Google Sheets data.
  - **token.py** 📄: Schema for OAuth tokens.
- **services/** 📁: Google API service implementations.
  - **google_sheets.py** 📄: Service for interacting with Google Sheets API.
  - **token.py** 📄: OAuth token management and refresh logic.

#### 🔔 `notifications/` Directory

Notification system.

- **service.py** 📄: Background notification service for task reminders.

#### ⏰ `scheduler/` Directory

Task scheduling functionality.

- **service.py** 📄: APScheduler-based task scheduling service.

#### 🖥️ `screens/` Directory

UI screens and components organized by feature.

##### 🇬🇧 `english_home/` Directory

English learning home screen.

- **english_home.py** 📄: Main screen class for English learning interface.
- **view.py** 📄: UI view components for the English home screen.
- **services/** 📁: Screen-specific services.
  - **manager.py** 📄: Screen management logic.
  - **window.py** 📄: Window management for the English screen.

##### ❓ `english_quiz/` Directory

English quiz functionality.

- **quiz_home.py** 📄: Main quiz screen implementation.
- **view.py** 📄: Quiz UI components.
- **utils.py** 📄: Utility functions for quiz logic.
- **services/** 📁: Quiz-specific services.
  - **manager.py** 📄: Quiz management and scoring.
  - **window.py** 📄: Quiz window handling.

##### 🏠 `home/` Directory

Main application home screen (daily planner).

- **constants.py** 📄: UI constants and styling.
- **home.py** 📄: Main home screen class.
- **view.py** 📄: Home screen UI components.
- **components/** 📁: Reusable UI components.
  - **components.py** 📄: General UI components.
  - **reload.py** 📄: Reload functionality components.
  - **task_item.py** 📄: Individual task item component.
- **services/** 📁: Home screen services.
  - **manager.py** 📄: Home screen management.
  - **tasks_list.py** 📄: Task list handling.
  - **window.py** 📄: Home window management.

#### 🔊 `sound/` Directory

Audio functionality.

- **service.py** 📄: Sound playback service.
- **sounds/** 📁: Audio files for various UI events.
  - **click.mp3** 🎵: Click sound effect.
  - **close.mp3** 🎵: Window close sound.
  - **open_english.mp3** 🎵: English section open sound.
  - **open.mp3** 🎵: General open sound.
  - **reminder.mp3** 🎵: Notification reminder sound.
  - **rest.mp3** 🎵: Rest/break sound.

#### ✅ `tasks/` Directory

Task management functionality.

- **model.py** 📄: Task SQLAlchemy model.
- **repository.py** 📄: Task repository for database operations.
- **schemas.py** 📄: Task data validation schemas.
- **service.py** 📄: Task business logic service.
- **utils.py** 📄: Task-related utility functions.

#### 🎤 `voice/` Directory

Voice recognition and wake word detection.

- **engine.py** 📄: Main voice engine using OpenWakeWord and Vosk.
- **models/** 📁: Pre-trained voice models.
  - **marvin_v2.onnx** 🤖: Wake word model for "Marvin".
  - **ok_neo.onnx** 🤖: Wake word model for "OK Neo".

### 🔄 `migrations/` Directory

Database migration files managed by Alembic.

- **env.py** 📄: Alembic environment configuration.
- **README** 📄: Alembic migration instructions.
- **script.py.mako** 📄: Migration script template.
- **versions/** 📁: Individual migration files for database schema changes.

### 📜 `scripts/` Directory

Utility scripts and background services.

- **autostart.py** 📄: Script for setting up auto-start services.
- **fetch_tasks.py** 📄: Script for fetching tasks from Google Sheets.
- **notifications_background.py** 📄: Background notification service script.
- **utils.py** 📄: General utility functions.
- **voice_background_daily.py** 📄: Background voice service for daily planner.
- **voice_background_english.py** 📄: Background voice service for English features.
- **other/** 📁: Platform-specific scripts for running services.
  - Batch files and VBS scripts for Windows service management.

## 🏗️ Architecture Principles

### 🧩 Modular Design

The codebase follows a modular architecture with clear separation of concerns:

- **Features** 📦: Grouped by functionality (english, google, tasks, etc.)
- **Screens** 🖥️: UI components organized by screen/feature
- **Services** ⚙️: Business logic separated from UI
- **Repositories** 📚: Data access layer abstraction

### ⚡ Asynchronous Programming

Extensive use of async/await patterns for:

- Database operations (aiosqlite)
- API calls (aiogoogle)
- UI updates (Flet async support)

### 🔗 Dependency Injection

Database sessions and other dependencies are injected through the dependency injection system in `db/dependencies.py`.

### 📚 Repository Pattern

All database operations go through repository classes for better testability and separation of concerns.

### ⚙️ Service Layer

Business logic is encapsulated in service classes, keeping controllers thin and focused on orchestration.

## 🔄 Data Flow

1. **🚀 Initialization**: `main.py` initializes database and starts background services.
2. **🔄 Sync**: `fetch_tasks.py` periodically syncs with Google Sheets.
3. **🎤 Voice Input**: Voice engine listens for wake words and triggers appropriate actions.
4. **🖱️ UI Interaction**: Flet-based screens handle user interactions and display data.
5. **💾 Data Persistence**: All changes are persisted through repository layer to SQLite database.

This structure ensures maintainability, scalability, and clear separation of concerns throughout the application.
