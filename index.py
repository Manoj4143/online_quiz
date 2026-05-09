import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

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
        cursor = conn.cursor()
    except Error as err:
        if err.errno == 2003:
            print("❌ Error: Cannot connect to MySQL server.")
            print("Make sure MySQL is running and the database is set up.")
            print("Run 'python setup.py' first to initialize the database.")
        elif err.errno == 1045:
            print("❌ Error: Access denied. Check your username/password in config.py")
        else:
            print(f"❌ Connection Error: {err}")
        return

    # 2. Display welcome and fetch available questions
    print("Welcome to the SQL-Powered Quiz (MySQL Edition)!\n")
    
    try:
        cursor.execute("SELECT QuestionID FROM Questions ORDER BY QuestionID")
        questions = cursor.fetchall()
        
        if not questions:
            print("❌ No questions found. Run 'python setup.py' to initialize the database.")
            conn.close()
            return
        
        score = 0
        total = len(questions)
        
        # 3. Loop through each question
        for question_tuple in questions:
            question_id = question_tuple[0]
            
            # Fetch the question
            cursor.execute("SELECT QuestionText FROM Questions WHERE QuestionID = %s", (question_id,))
            question_text = cursor.fetchone()[0]
            print(f"\nQuestion {question_id}: {question_text}")
            
            # Fetch the options
            cursor.execute("SELECT OptionID, OptionText FROM Options WHERE QuestionID = %s", (question_id,))
            options = cursor.fetchall()
            for opt in options:
                print(f"[{opt[0]}] {opt[1]}")
            
            # 4. Get User Input
            try:
                user_choice = int(input("Enter the number of your choice: "))
                
                # 5. Verify using SQL CASE logic
                cursor.execute("""
                    SELECT CASE 
                        WHEN CorrectOptionID = %s THEN 1 
                        ELSE 0 
                    END AS IsCorrect
                    FROM Answers 
                    WHERE QuestionID = %s
                """, (user_choice, question_id))
                
                result = cursor.fetchone()
                if result[0] == 1:
                    print("✅ Correct!")
                    score += 1
                else:
                    # Fetch the correct answer for feedback
                    cursor.execute("""
                        SELECT o.OptionText 
                        FROM Answers a
                        JOIN Options o ON a.CorrectOptionID = o.OptionID
                        WHERE a.QuestionID = %s
                    """, (question_id,))
                    correct_answer = cursor.fetchone()[0]
                    print(f"❌ Wrong! The correct answer is: {correct_answer}")
                    
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # 6. Display final score
        print(f"\n{'='*40}")
        print(f"Quiz Complete! Your Score: {score}/{total}")
        print(f"Percentage: {(score/total)*100:.1f}%")
        print(f"{'='*40}")
        
    except Error as err:
        print(f"❌ Database Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_quiz()