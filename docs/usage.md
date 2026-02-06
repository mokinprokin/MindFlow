# 📖 User Guide

This document explains how to launch, interact with, and manage the MindFlow.

## 🎤 Voice Commands (Hands-Free Control)

The application uses OpenWakeWord for real-time activation. The engine listens for specific wake words to trigger UI windows.

| Wake Word     | Action                      | Target Feature        |
| ------------- | --------------------------- | --------------------- |
| "Alexa"       | Opens the Daily Planner     | voice_daily_service   |
| "Hey Jarvis"  | Opens 'Add New Word' Window | english_voice_service |

> **📝 Note**: Ensure your microphone is active. The engine runs as a background thread to avoid blocking the main UI.

## 🔔 Automated Notifications

The NotificationService runs in the background and triggers audio-visual alerts based on your schedule and the Spaced Repetition (SRS) algorithm.

### ✅ Task Reminders

- **⏰ Timing**: Triggered 15 minutes before a task's `time_from`.
- **🧠 Logic**: Only notifies for upcoming transitions.
- **🔊 Sound**: Plays `reminder.mp3`.

### 😴 Rest Notifications

- **⏰ Timing**: Based on the `rest_notification_min` setting in your config.
- **🧠 Logic**: Reminds you to take a break if you've been working continuously.
- **🔊 Sound**: Plays `rest.mp3`.

### 🇬🇧 English Repetition Quizzes

- **⏰ Timing**: Scheduled automatically throughout the day using a "chess-order" logic.
- **🧠 Logic**: Skips high-priority task slots to ensure you aren't interrupted during deep work.
- **🎯 Action**: Pop-up window appears for quick word review.

## 📅 Daily Workflow

### 🔄 Google Sheets Synchronization

On startup, the app automatically executes `daily_plan.setup_startup()`:

- Fetches tasks from your connected Google Sheet
- Compares them with the local `planner.db`
- Updates any changes to ensure the NotificationService has the latest data

### 🇬🇧 English Learning Cycle

1. **➕ Add**: Use "Marvin" to quickly save a new word you encountered
2. **💾 Sync**: Words are stored in the local SQLite database
3. **🔄 Review**: The system automatically picks 5 words (default) for your daily quiz based on the repetition algorithm

## ⌨️ Hotkeys & Manual Controls

If voice commands are not preferred, the application supports global hotkeys (configured in `src/features/notifications/utils.py`):

- **`\` (Backslash)**: Manually toggle the English Quiz window

### ⏱️ Debounce Logic

All triggers (voice or hotkey) have a 2.0s cooldown to prevent accidental double-activation.
