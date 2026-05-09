import mysql.connector
from mysql.connector import Error
import getpass

def admin_setup():
    """Setup using root/admin credentials to create database and grant permissions"""
    
    print("=" * 50)
    print("MySQL Admin Setup")
    print("=" * 50)
    print("\nThis requires MySQL root (admin) access.\n")
    
    # Get root credentials from user
    root_user = input("MySQL Root Username [root]: ").strip() or "root"
    root_password = getpass.getpass("MySQL Root Password: ")
    host = input("MySQL Host [localhost]: ").strip() or "localhost"
    port = input("MySQL Port [3306]: ").strip() or "3306"
    
    try:
        port = int(port)
    except ValueError:
        port = 3306
    
    print("\nConnecting as admin...")
    
    try:
        # Connect as root/admin
        conn = mysql.connector.connect(
            host=host,
            user=root_user,
            password=root_password,
            port=port
        )
        cursor = conn.cursor()
        print("✅ Connected as admin!")
        
        # Create database
        print("\nCreating database...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS online_quiz_db")
        print("✅ Database 'online_quiz_db' created!")
        
        # Use the database
        cursor.execute("USE online_quiz_db")
        
        # Create tables
        print("Creating tables...")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Questions (
                QuestionID INT PRIMARY KEY AUTO_INCREMENT,
                QuestionText VARCHAR(500) NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Options (
                OptionID INT PRIMARY KEY AUTO_INCREMENT,
                QuestionID INT NOT NULL,
                OptionText VARCHAR(255) NOT NULL,
                FOREIGN KEY (QuestionID) REFERENCES Questions(QuestionID) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Answers (
                AnswerID INT PRIMARY KEY AUTO_INCREMENT,
                QuestionID INT NOT NULL,
                CorrectOptionID INT NOT NULL,
                FOREIGN KEY (QuestionID) REFERENCES Questions(QuestionID) ON DELETE CASCADE,
                FOREIGN KEY (CorrectOptionID) REFERENCES Options(OptionID) ON DELETE CASCADE
            )
        """)
        print("✅ Tables created!")
        
        # Grant permissions to manu user
        print("\nGranting permissions to 'manu' user...")
        cursor.execute("GRANT ALL PRIVILEGES ON online_quiz_db.* TO 'manu'@'%'")
        cursor.execute("FLUSH PRIVILEGES")
        print("✅ Permissions granted to 'manu' user!")
        
        # Clear existing data and insert sample data
        print("Inserting sample data...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE Answers")
        cursor.execute("TRUNCATE TABLE Options")
        cursor.execute("TRUNCATE TABLE Questions")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # Insert all 10 questions with options
        questions_data = [
            {
                "text": "What is the capital of France?",
                "options": ["Paris", "London", "Berlin", "Madrid"],
                "correct": 0  # Index 0 = Paris
            },
            {
                "text": "What is the largest planet in our solar system?",
                "options": ["Jupiter", "Saturn", "Neptune", "Venus"],
                "correct": 0  # Index 0 = Jupiter
            },
            {
                "text": "What is the smallest country in the world?",
                "options": ["Vatican City", "Monaco", "Liechtenstein", "San Marino"],
                "correct": 0  # Index 0 = Vatican City
            },
            {
                "text": "Who wrote Romeo and Juliet?",
                "options": ["William Shakespeare", "Jane Austen", "Charles Dickens", "Mark Twain"],
                "correct": 0  # Index 0 = William Shakespeare
            },
            {
                "text": "What is the chemical symbol for Gold?",
                "options": ["Go", "Gd", "Au", "Ag"],
                "correct": 2  # Index 2 = Au
            },
            {
                "text": "In what year did the Titanic sink?",
                "options": ["1910", "1912", "1915", "1920"],
                "correct": 1  # Index 1 = 1912
            },
            {
                "text": "What is the capital of Japan?",
                "options": ["Osaka", "Tokyo", "Kyoto", "Hiroshima"],
                "correct": 1  # Index 1 = Tokyo
            },
            {
                "text": "How many sides does a hexagon have?",
                "options": ["4", "5", "6", "8"],
                "correct": 2  # Index 2 = 6
            },
            {
                "text": "What is the largest ocean on Earth?",
                "options": ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean", "Arctic Ocean"],
                "correct": 2  # Index 2 = Pacific Ocean
            },
            {
                "text": "Who painted the Mona Lisa?",
                "options": ["Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello"],
                "correct": 1  # Index 1 = Leonardo da Vinci
            }
        ]
        
        # Insert questions, options, and answers
        option_id = 1
        for q_id, question in enumerate(questions_data, 1):
            cursor.execute("INSERT INTO Questions (QuestionText) VALUES (%s)", (question["text"],))
            
            correct_option_id = None
            for opt_idx, option_text in enumerate(question["options"]):
                cursor.execute("INSERT INTO Options (QuestionID, OptionText) VALUES (%s, %s)", 
                              (q_id, option_text))
                
                if opt_idx == question["correct"]:
                    correct_option_id = option_id
                
                option_id += 1
            
            cursor.execute("INSERT INTO Answers (QuestionID, CorrectOptionID) VALUES (%s, %s)", 
                          (q_id, correct_option_id))
        
        conn.commit()
        print("✅ Sample data inserted!")
        
        # Update config.py with manu credentials
        print("\nUpdating config.py...")
        with open('config.py', 'w') as f:
            f.write(f"""# MySQL Database Configuration
DB_CONFIG = {{
    'host': '{host}',
    'user': 'manu',
    'password': 'Manojkumar#098',
    'database': 'online_quiz_db',
    'port': {port}
}}
""")
        print("✅ Configuration saved!")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 50)
        print("✅ Database setup complete!")
        print("=" * 50)
        print("\nYou can now run: python index.py")
        
    except Error as err:
        if err.errno == 2003:
            print("❌ Error: Cannot connect to MySQL server.")
            print("   Make sure MySQL is running!")
        elif err.errno == 1045:
            print("❌ Error: Access denied.")
            print("   Check the root username and password.")
        else:
            print(f"❌ Database Error: {err}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    admin_setup()
