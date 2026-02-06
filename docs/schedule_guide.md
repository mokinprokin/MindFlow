# 📅 Daily Planning Best Practices

To get the most out of the MindFlow App, your daily schedule shouldn't just be a list of tasks—it should be a structured plan optimized for both productivity and language learning.

## 🤖 The AI-Powered Planning Workflow

We recommend using Gemini (or your preferred LLM) to draft your schedule. This ensures your day is balanced and formatted correctly for the app's sync engine.

### 📝 Step 1: Initialize Gemini

Open Gemini and provide the following System Prompt to set the context:

> **System Prompt**: "You are my expert Time Management Assistant. Your goal is to help me structure my day for maximum productivity and long-term growth. I will provide you with my main goals or a rough list of tasks, and you will organize them into a logical, high-efficiency schedule.
>
> **Output Requirements**:
>
> - Always provide the final plan in a Markdown table.
> - Use exactly these four columns: `time_from`, `time_to`, `task`, `priority`.
> - Use 24-hour format (HH:MM) for times.
> - Set priority as Low, Middle, or High based on the cognitive load required.
> - Ensure there is a 5–10 minute buffer between major tasks."

### 📥 Step 2: Feed Your Tasks

Describe your day to the AI: _"Today I need to finish the repository layer, have a meeting at 2 PM, and I want to spend time on my English quiz."_

### ✅ Step 3: Review the Output

The AI will generate a table. Ensure it looks like this:

| time_from | time_to | task                                        | priority |
| --------- | ------- | ------------------------------------------- | -------- |
| 07:00     | 08:15   | Morning Routine & Breakfast                 | Low      |
| 08:15     | 13:10   | Core Educational Session                    | High     |
| 13:10     | 13:45   | Mid-day Meal & Relaxation                   | Low      |
| 13:45     | 14:45   | Active English Acquisition                  | Middle   |
| 14:45     | 15:45   | Critical Project Development                | High     |
| 15:45     | 16:15   | Cognitive Recovery Break                    | Low      |
| 16:15     | 17:00   | Technical Documentation Update              | Middle   |
| 17:00     | 17:25   | Supplemental Nutrition                      | Low      |
| 17:25     | 17:50   | English Media Immersion & Physical Training | Middle   |

## 🎯 Priority System

The app's notification engine treats priorities differently. Use them strategically:

### 🔴 High Priority

- **Use for**: Deep work or meetings
- **App Behavior**: The English Quiz will **never** interrupt you during a High-priority task

### 🟡 Middle/Low Priority

- **Use for**: Routine tasks or breaks
- **App Behavior**: The system will use these slots to show you English quizzes or reminders, following the "chess-order" logic

## 💡 Pro-Tip: The "Buffer" Rule

Always leave at least one **Low** or **Middle** priority task between two **High** priority blocks. This gives the app's RepetitionService a "window" to show you your English words without breaking your focus during critical work.

## 🔗 Integrating with Google Sheets

Once you have your AI-generated table, follow these steps to sync it:

1. **📤 Export to Sheets**: Use Gemini's "Export to sheets" feature to automatically create your sheet in Google Sheets
2. **🔄 Sync**: Restart the app or wait for the next sync cycle. The NotificationService will automatically calculate your "chess-order" repetition schedule based on this new data
