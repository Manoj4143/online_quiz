# 1. Project Title
**Online Quiz System**

---

## 2. Introduction
The **Online Quiz System** is a robust, Python-based Command Line Interface (CLI) application that integrates with a MySQL database. It provides an interactive platform where users can participate in a trivia-style quiz, submit their answers, and immediately receive feedback on their performance. The system securely stores questions, options, and correct answers in a relational database, making it easily extensible. It also features a leaderboard that ranks players based on their scores and completion percentages.

---

## 3. Scope of the Project
The scope of this project encompasses:
- A dynamic quiz-taking interface directly accessible from the terminal.
- An automated database setup script (`setup_admin.py`) for initializing tables and populating sample data.
- Secure database configurations to handle users and permissions.
- Tracking of individual user performances and saving their scores to the database.
- A global leaderboard displaying the top 10 players sorted by highest percentage and score.

---

## 4. Problem Statement
Traditional paper-based quizzes and static digital forms lack real-time interactivity and automated scoring capabilities. Furthermore, managing the questions and dynamically tracking top scores across multiple users can be cumbersome. There is a need for a lightweight, interactive quiz platform that automates the evaluation process, securely stores data using a relational database (MySQL), and motivates users through competitive leaderboards.

---

## 5. Objectives
- **Automated Evaluation:** Compare user inputs against correct answers retrieved from the database in real-time.
- **Database Integration:** Seamlessly integrate with MySQL to manage data (Questions, Options, Answers, Scores).
- **Leaderboard Generation:** Create a ranking system to display the top scores achieved by players.
- **Easy Deployment:** Provide an automated script to establish the required database schema, grant user permissions, and populate initial data without manual SQL execution.

---

## 6. Requirement Analysis

### Functional Requirements
- **System Setup:** The system must automatically create the database (`online_quiz_system`) and related tables.
- **Take Quiz:** Users must be able to input their name, read questions, and select an option (1-4).
- **Score Calculation:** The system must validate the user's choice and increment the score if correct.
- **Score Persistence:** The user's final score and percentage must be saved to the database.
- **View Leaderboard:** The system must retrieve and display the top 10 scores from the database.

### Non-Functional Requirements
- **Usability:** The CLI must be intuitive with clear error handling for invalid inputs (e.g., entering letters instead of numbers).
- **Performance:** Database queries must execute quickly to provide a seamless user experience.
- **Maintainability:** Code should be modularized (e.g., separating configuration, database setup, and quiz logic).
- **Data Integrity:** The database must use constraints (e.g., Primary Keys, Foreign Keys, `ON DELETE CASCADE`) to maintain referential integrity.

### Hardware & Software Requirements
- **Hardware:** A standard PC/Laptop (Minimum 2GB RAM, 1GHz Processor).
- **Software:** 
  - Operating System: Windows, macOS, or Linux.
  - Runtime: Python 3.x
  - Database: MySQL Server (running locally or remotely).
  - Dependencies: `mysql-connector-python` library.

---

## 7. System Design

### Modules
1. **Database Setup Module (`setup_admin.py`):** Handles root database connection, creates schemas, handles user privileges, and parses `index.sql` to insert dummy data.
2. **Configuration Module (`config.py`):** Stores environment and database connection variables securely.
3. **Quiz Engine Module (`index.py`):** The core application logic. It handles the user interface, fetching questions, validating answers, calculating scores, and displaying the leaderboard.

### Tier Architecture
The system follows a **2-Tier Client-Server Architecture**:
1. **Client/Application Tier:** The Python CLI scripts (`index.py`) acting as the application logic layer where user interaction and data processing occur.
2. **Data Tier:** The MySQL Server containing the `online_quiz_system` database which serves as the persistent storage layer.

---

## 8. Database Design
The relational database `online_quiz_system` consists of the following tables:

1. **Questions**
   - `QuestionID` (INT, Primary Key, Auto Increment)
   - `QuestionText` (VARCHAR)
2. **Options**
   - `OptionID` (INT, Primary Key)
   - `QuestionID` (INT, Foreign Key referencing `Questions`)
   - `OptionText` (VARCHAR)
3. **Answers**
   - `AnswerID` (INT, Primary Key, Auto Increment)
   - `QuestionID` (INT, Foreign Key referencing `Questions`, UNIQUE)
   - `CorrectOptionID` (INT, Foreign Key referencing `Options`)
4. **user_scores**
   - `ScoreID` (INT, Primary Key, Auto Increment)
   - `player_name` (VARCHAR)
   - `score` (INT)
   - `total_questions` (INT)
   - `percentage` (DECIMAL)
   - `quiz_date` (TIMESTAMP)

---

## 9. SQL Queries

### Data Insertion (DML)
```sql
-- Inserting Questions
INSERT INTO Questions (QuestionID, QuestionText) VALUES (1, 'What is the chemical symbol for Gold?');

-- Inserting Options
INSERT INTO Options (OptionID, QuestionID, OptionText) VALUES (1, 1, 'Ag'), (2, 1, 'Au');

-- Inserting Answers
INSERT INTO Answers (QuestionID, CorrectOptionID) VALUES (1, 2);

-- Saving User Score
INSERT INTO user_scores (player_name, score, total_questions, percentage) 
VALUES ('John Doe', 8, 10, 80.00);
```

### Data Retrieval (SELECT Queries)
```sql
-- Fetch all questions
SELECT QuestionID FROM Questions ORDER BY QuestionID;

-- Fetch question text by ID
SELECT QuestionText FROM Questions WHERE QuestionID = 1;

-- Fetch options for a specific question
SELECT OptionID, OptionText FROM Options WHERE QuestionID = 1 ORDER BY OptionID;
```

### Score Calculation Query
```sql
-- Retrieve the correct option for validation
SELECT CorrectOptionID FROM Answers WHERE QuestionID = 1;
```

### Leaderboard / Ranking Query
```sql
-- Retrieve top 10 players sorted by percentage and score
SELECT player_name, score, total_questions, percentage, quiz_date 
FROM user_scores 
ORDER BY percentage DESC, score DESC 
LIMIT 10;
```

### Update and Delete Queries
```sql
-- Deleting data during setup to ensure a clean state
DELETE FROM Answers;
DELETE FROM Options;
DELETE FROM Questions;
```
*(Note: Foreign key constraints `ON DELETE CASCADE` ensure that deleting a question also removes its associated options and answers).*

---

## 10. Conclusion
The **Online Quiz System** successfully demonstrates the integration of a Python-based interactive application with a MySQL relational database. By implementing a normalized database schema and modular Python scripts, the project ensures data integrity, rapid data retrieval, and easy setup. The system meets all functional and non-functional requirements, providing users with a seamless quiz-taking experience and an engaging leaderboard system.
