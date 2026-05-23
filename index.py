import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from datetime import datetime

def run_quiz():
    # 1. Connect to MySQL database
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            port=DB_CONFIG['port']
        )
        cursor = conn.cursor(dictionary=True)
    except Error as err:
        if err.errno == 2003:
            print("❌ Error: Cannot connect to MySQL server.")
            print("Make sure MySQL is running and the database is set up.")
            print("Run 'python setup_admin.py' first to initialize the database.")
        elif err.errno == 1045:
            print("❌ Error: Access denied. Check your username/password in config.py")
        else:
            print(f"❌ Connection Error: {err}")
        return

    # 2. Display welcome and fetch available questions
    print("\n" + "="*50)
    print("Welcome to the SQL-Powered Quiz!")
    print("="*50 + "\n")
    
    try:
        cursor.execute("SELECT QuestionID FROM Questions ORDER BY QuestionID")
        questions = cursor.fetchall()
        
        if not questions:
            print("❌ No questions found. Run 'python setup_admin.py' to initialize the database.")
            conn.close()
            return
        
        # Get player name
        player_name = input("Enter your name to start: ").strip()
        if not player_name:
            player_name = "Anonymous"
        
        score = 0
        total = len(questions)
        
        print(f"\n{player_name}, answer {total} questions! Good luck! 🎯\n")
        
        # 3. Loop through each question
        for idx, question in enumerate(questions, 1):
            question_id = question['QuestionID']
            
            # Fetch the question
            cursor.execute("SELECT QuestionText FROM Questions WHERE QuestionID = %s", (question_id,))
            question_data = cursor.fetchone()
            question_text = question_data['QuestionText']
            print(f"\n[Question {idx}/{total}] {question_text}")
            
            # Fetch the options
            cursor.execute("SELECT OptionID, OptionText FROM Options WHERE QuestionID = %s ORDER BY OptionID", (question_id,))
            options = cursor.fetchall()
            
            # Display options with 1-4 numbering for user input
            for i, opt in enumerate(options, 1):
                print(f"  [{i}] {opt['OptionText']}")
            
            # 4. Get User Input
            while True:
                try:
                    user_choice = input("\nEnter your choice (1-4): ").strip()
                    user_choice_num = int(user_choice)
                    
                    if user_choice_num < 1 or user_choice_num > len(options):
                        print("❌ Invalid choice. Please enter 1-4.")
                        continue
                    
                    # Map user input (1-4) to actual OptionID
                    user_choice = options[user_choice_num - 1]['OptionID']
                    break
                except ValueError:
                    print("❌ Please enter a valid number.")
            
            # 5. Verify answer using SQL
            cursor.execute("""
                SELECT CorrectOptionID FROM Answers WHERE QuestionID = %s
            """, (question_id,))
            
            result = cursor.fetchone()
            correct_option_id = result['CorrectOptionID']
            
            if user_choice == correct_option_id:
                print("✅ Correct!")
                score += 1
            else:
                cursor.execute("SELECT OptionText FROM Options WHERE OptionID = %s", (correct_option_id,))
                correct_answer = cursor.fetchone()
                print(f"❌ Wrong! The correct answer was: {correct_answer['OptionText']}")
        
        # 6. Display final score and save to database
        print(f"\n{'='*50}")
        print(f"Quiz Complete, {player_name}!")
        print(f"Your Final Score: {score}/{total}")
        print(f"Percentage: {(score/total)*100:.1f}%")
        print(f"{'='*50}\n")
        
        # Save score to database (optional - create table if needed)
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_scores (
                    ScoreID INT PRIMARY KEY AUTO_INCREMENT,
                    player_name VARCHAR(100) NOT NULL,
                    score INT NOT NULL,
                    total_questions INT NOT NULL,
                    percentage DECIMAL(5, 2),
                    quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            percentage = (score/total)*100
            cursor.execute("""
                INSERT INTO user_scores (player_name, score, total_questions, percentage) 
                VALUES (%s, %s, %s, %s)
            """, (player_name, score, total, percentage))
            conn.commit()
            print("✅ Your score has been saved to the leaderboard!\n")
        except Error as e:
            print(f"⚠️  Could not save score: {e}\n")
        
    except Error as err:
        print(f"❌ Database Error: {err}")
    finally:
        cursor.close()
        conn.close()

def view_leaderboard():
    """Display top scores from the leaderboard"""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            port=DB_CONFIG['port']
        )
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT player_name, score, total_questions, percentage, quiz_date 
            FROM user_scores 
            ORDER BY percentage DESC, score DESC 
            LIMIT 10
        """)
        
        scores = cursor.fetchall()
        
        if scores:
            print("\n" + "="*60)
            print("🏆 TOP 10 LEADERBOARD 🏆")
            print("="*60)
            for rank, row in enumerate(scores, 1):
                print(f"{rank}. {row['player_name']} - {row['score']}/{row['total_questions']} ({row['percentage']:.1f}%)")
            print("="*60 + "\n")
        else:
            print("❌ No scores yet. Take the quiz first!")
        
        cursor.close()
        conn.close()
    except Error as err:
        print(f"❌ Error viewing leaderboard: {err}")

if __name__ == "__main__":
    while True:
        print("\n1. Take Quiz")
        print("2. View Leaderboard")
        print("3. Exit")
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            run_quiz()
        elif choice == "2":
            view_leaderboard()
        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid option. Please try again.")
