# Online Quiz System

## Introduction
The `Online Quiz System` is a Python-based command-line quiz application that uses MySQL to store questions, answer options, and user scores. This project demonstrates a simple quiz workflow with database setup, question loading, score tracking, and a leaderboard feature.

## Project Overview
This repository is designed to help users quickly set up a quiz environment and interact with it through a console interface.

The project includes:
- Database schema creation and initialization
- Question and answer loading from a SQL file
- Quiz execution with real-time answer validation
- Score persistence and leaderboard display

## Files and Purpose

- `setup_admin.py`
  - Creates the MySQL database `online_quiz_system`
  - Defines the tables: `Questions`, `Options`, `Answers`
  - Grants permissions to the standard quiz user `manu`
  - Loads sample quiz data from `index.sql`
  - Writes the database connection details into `config.py`

- `config.py`
  - Stores the MySQL connection configuration used by `index.py`
  - Contains host, user, password, database, and port settings

- `index.py`
  - Provides the main quiz interface
  - Allows users to take the quiz or view the leaderboard
  - Retrieves questions, options, and answers from MySQL
  - Saves quiz results into a `user_scores` table for leaderboard display

- `index.sql`
  - Contains sample quiz data for the database
  - Inserts the questions, options, and correct answers used by the quiz

## Highlights

- Uses a MySQL database for persistent storage
- Supports quiz data initialization from a SQL file
- Includes a simple leaderboard mechanism
- Handles admin setup and permissions automatically
- Provides user-friendly prompts and feedback

## Database

- Database: MySQL
- Database name: `online_quiz_system`
- Main tables:
  - `Questions`
  - `Options`
  - `Answers`
  - `user_scores` (created automatically in `index.py` for leaderboard storage)

## Setup and Usage

1. Ensure MySQL is installed and running on your machine.
2. Run the admin setup script:
   ```bash
   python setup_admin.py
   ```
3. After setup completes, start the quiz app:
   ```bash
   python index.py
   ```
4. Choose:
   - `1` to take the quiz
   - `2` to view the leaderboard
   - `3` to exit

## Notes

- `setup_admin.py` uses root/admin credentials only for initial database creation.
- The default application user is `manu`, and credentials are written to `config.py`.
- If you update quiz data manually, rerun `setup_admin.py` to reload `index.sql`.

## Recommendation

For production use, update `config.py` to secure the database password and consider adding a separate environment-based configuration system.
