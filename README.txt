================================================================================
ONLINE QUIZ APPLICATION - MySQL Edition
================================================================================

PROJECT OVERVIEW
================================================================================
This is a Python-based quiz application that runs interactive quizzes using 
a MySQL database. Users answer multiple-choice questions and get instant 
feedback with a final score.

FILES & WHAT THEY DO
================================================================================

1. config.py
   - Stores MySQL database connection details (host, username, password, etc)
   - Acts as a configuration file for the entire project

2. index.py
   - Main quiz application
   - Connects to MySQL, fetches questions, displays them to user
   - Compares user answers to correct answers in database
   - Shows score at the end

3. index.sql
   - Database schema (structure) definition
   - Creates 3 tables: Questions, Options, Answers
   - Includes sample quiz questions with multiple-choice options
   - Can be imported directly into MySQL

4. setup_admin.py
   - Setup script to initialize the database
   - Creates database and tables automatically
   - Requires MySQL root/admin credentials

5. SETUP.md
   - Detailed setup instructions (Windows/Linux/Mac)

CODE FLOW (How It Works)
================================================================================
1. index.py connects to MySQL using credentials from config.py
2. Fetches all quiz questions from the Questions table
3. For each question, displays it and its options (from Options table)
4. Gets user input
5. Checks answer against CorrectOptionID in Answers table
6. Shows ✅ if correct, ❌ with correct answer if wrong
7. Displays final score and percentage

INSTALLATION
================================================================================

Step 1: Install Requirements
   pip install mysql-connector-python

Step 2: Start MySQL Server
   Windows: net start MySQL80
   Or use Services app (Win+R → services.msc)

Step 3: Update config.py
   Edit config.py and set your MySQL credentials:
   - user: your MySQL username (default: root)
   - password: your MySQL password
   - host: localhost (default)

Step 4: Initialize Database
   python setup_admin.py
   (Enter your MySQL root username and password when prompted)

Step 5: Run the Quiz
   python index.py

TROUBLESHOOTING
================================================================================
- "Cannot connect to MySQL": Make sure MySQL service is running
- "Access denied": Check username/password in config.py
- "No questions found": Run setup_admin.py first to initialize database

================================================================================
