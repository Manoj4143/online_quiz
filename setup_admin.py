import mysql.connector
from mysql.connector import Error
import getpass

def read_sql_file(filename):
    """Read and parse SQL file, executing statements in the correct order"""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        # Split by semicolon and clean up
        statements = []
        for statement in content.split(';'):
            statement = statement.strip()
            # Remove SQL comments
            lines = [line.split('--')[0].strip() for line in statement.split('\n')]
            statement = ' '.join(line for line in lines if line)
            if statement:
                statements.append(statement)
        
        # Sort statements to ensure proper execution order:
        # 1. INSERT INTO Questions first
        # 2. INSERT INTO Options second
        # 3. INSERT INTO Answers last
        questions_insert = []
        options_insert = []
        answers_insert = []
        
        for stmt in statements:
            upper_stmt = stmt.upper()
            if 'INSERT INTO' in upper_stmt:
                if 'QUESTIONS' in upper_stmt:
                    questions_insert.append(stmt)
                elif 'OPTIONS' in upper_stmt:
                    options_insert.append(stmt)
                elif 'ANSWERS' in upper_stmt:
                    answers_insert.append(stmt)
        
        result = questions_insert + options_insert + answers_insert
        return result if result else None
    except FileNotFoundError:
        print(f"❌ Error: {filename} not found!")
        return None

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
        cursor.execute("CREATE DATABASE IF NOT EXISTS online_quiz_system")
        print("✅ Database 'online_quiz_system' created!")
        
        # Use the database
        cursor.execute("USE online_quiz_system")
        
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
                OptionID INT PRIMARY KEY,
                QuestionID INT NOT NULL,
                OptionText VARCHAR(255) NOT NULL,
                FOREIGN KEY (QuestionID) REFERENCES Questions(QuestionID) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Answers (
                AnswerID INT PRIMARY KEY AUTO_INCREMENT,
                QuestionID INT NOT NULL UNIQUE,
                CorrectOptionID INT NOT NULL,
                FOREIGN KEY (QuestionID) REFERENCES Questions(QuestionID) ON DELETE CASCADE,
                FOREIGN KEY (CorrectOptionID) REFERENCES Options(OptionID) ON DELETE CASCADE
            )
        """)
        print("✅ Tables created!")
        
        # Grant permissions to manu user
        print("\nGranting permissions to 'manu' user...")
        cursor.execute("GRANT ALL PRIVILEGES ON online_quiz_system.* TO 'manu'@'%'")
        cursor.execute("FLUSH PRIVILEGES")
        print("✅ Permissions granted to 'manu' user!")
        
        # Load and execute SQL from index.sql
        print("\nLoading questions from index.sql...")
        sql_statements = read_sql_file('index.sql')
        
        if sql_statements:
            # Clear existing data first with foreign keys disabled
            print("Clearing existing data...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            try:
                cursor.execute("DELETE FROM Answers")
                cursor.execute("DELETE FROM Options")
                cursor.execute("DELETE FROM Questions")
            except Error:
                pass  # Tables might not exist yet
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            # Execute each SQL statement from index.sql
            print("Inserting data from index.sql...")
            for statement in sql_statements:
                try:
                    cursor.execute(statement)
                    conn.commit()  # Commit each statement individually
                except Error as e:
                    print(f"⚠️  Warning: {e}")
                    conn.rollback()  # Rollback failed statement
            
            print("✅ Sample data from index.sql inserted!")
        else:
            print("❌ Failed to load index.sql")
        
        # Update config.py with manu credentials
        print("\nUpdating config.py...")
        with open('config.py', 'w') as f:
            f.write(f"""# MySQL Database Configuration
DB_CONFIG = {{
    'host': '{host}',
    'user': 'manu',
    'password': 'Manojkumar#098',
    'database': 'online_quiz_system',
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