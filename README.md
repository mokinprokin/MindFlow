# MindFlow App

A comprehensive productivity application that integrates with Google Sheets for daily planning, features voice-activated controls, and includes an English learning module with interactive quizzes and vocabulary management.

## Overview

This application helps users manage their daily tasks by syncing with Google Sheets, allowing voice-based interaction for hands-free operation, and provides an integrated English learning experience that ties into daily tasks for better memorization.

## Documentation

The project includes comprehensive documentation to help you understand and use the application:

- **[📁 Project Structure](docs/project_structure.md)** - Detailed overview of the codebase organization and architecture
- **[🚀 Installation Guide](docs/instalation.md)** - Step-by-step setup instructions for Google Cloud APIs and local environment
- **[📖 User Guide](docs/usage.md)** - IMPORTANT! How to use voice commands, notifications, and daily workflow
- **[📅 Schedule Guide](docs/schedule_guide.md)** - IMPORTANT! Best practices for daily planning with AI assistance

## Key Features

### Daily Planner

- **Google Sheets Integration**: Automatically fetches and syncs daily plans from the most recently created Google Spreadsheet.
- **Local Storage**: Downloads and stores tasks locally in a SQLite database for offline access.
- **Voice Activation**: Call up the daily planner interface using voice commands at any time.
- **Task Management**: View, track, and manage daily tasks with a clean, intuitive UI built with Flet.

### Voice Control

- **Wake Word Detection**: Uses OpenWakeWord and Vosk for reliable voice recognition.
- **Custom Commands**: Supports multiple wake words like "Alexa" for specific actions.
- **Background Services**: Runs continuously in the background for instant responsiveness.

### English Learning Module

- **Task-Integrated Quizzes**: Displays English vocabulary quizzes based on current daily tasks to enhance learning through context.
- **Vocabulary Management**: Add new words to your vocabulary database by saying "Marvin" to open the word addition interface.
- **Repetition System**: Implements spaced repetition for better word retention.
- **Interactive UI**: Dedicated screens for quiz taking, word management, and learning progress.

### Additional Features

- **Notifications**: Background notification system for task reminders.
- **Sound Effects**: Audio feedback for various actions.
- **Auto-Start Services**: Automatically launches required background processes on startup.
- **Database Migrations**: Uses Alembic for database schema management.

## Prerequisites

- Python 3.8 or higher
- Google Cloud Project with Sheets API enabled
- OAuth 2.0 credentials for Google API access

## Usage

### Daily Planner

- The app automatically syncs with your latest Google Sheet on startup.
- Say "Alexa" to open the daily planner interface.
- View and manage your tasks through the Flet-based UI.

### English Learning

- Quizzes appear automatically based on your daily tasks.
- Say "hey_jarvis" to add new words to your vocabulary.
- Access the English learning section through the main interface.

### Voice Commands

- "Alexa": Opens the daily planner
- "Hey_jarvis": Opens the word addition interface

## Libraries and Dependencies

### Core Dependencies

- **Flet**: Modern UI framework for Python desktop applications
- **aiogoogle**: Asynchronous Google API client
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **Alembic**: Database migration tool

### Voice and Audio

- **Vosk**: Offline speech recognition
- **OpenWakeWord**: Wake word detection
- **PyAudio**: Audio I/O library
- **sounddevice/soundfile**: Audio processing

### Utilities

- **Pydantic**: Data validation and settings management
- **APScheduler**: Task scheduling
- **aiofiles**: Asynchronous file operations
- **colorama**: Colored terminal output

### Machine Learning

- **scikit-learn**: Machine learning algorithms (used in repetition system)
- **scipy**: Scientific computing
- **numpy**: Numerical computing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if available)
5. Submit a pull request

## Support

For issues or questions, please open an issue on the GitHub repository.
