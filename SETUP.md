# MySQL Quiz Application Setup Guide

## Prerequisites
You need MySQL Server installed on your system. If you don't have it, download and install it first:
- **Windows**: Download from https://dev.mysql.com/downloads/mysql/
- **Alternative**: Use MySQL via Docker, XAMPP, or WAMP

## Setup Steps

### Step 1: Verify MySQL is Running
On Windows, start the MySQL service:
```powershell
net start MySQL80
```
Or use Services app: Press `Win+R`, type `services.msc`, find MySQL and start it.

### Step 2: Update Database Credentials (if needed)
Edit `config.py` and update your MySQL credentials:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           # Your MySQL username
    'password': '',           # Your MySQL password
    'database': 'online_quiz_db',
    'port': 3306
}
```

### Step 3: Initialize the Database
Run the setup script to create the database and tables:
```powershell
python setup.py
```

This will:
- Create the `online_quiz_db` database
- Create all necessary tables (Questions, Options, Answers)
- Insert sample quiz questions

### Step 4: Run the Quiz Application
```powershell
python index.py
```

## Alternative: Manual Setup with MySQL CLI

If you prefer to set up manually using MySQL command line:

```bash
mysql -u root -p
# Enter your password

# Then run the SQL commands from index.sql
```

Or import the SQL file directly:
```bash
mysql -u root -p < index.sql
```

## Troubleshooting

### Error: "Cannot connect to MySQL server"
- Make sure MySQL service is running
- On Windows: `net start MySQL80`
- Check that localhost:3306 is accessible

### Error: "Access denied"
- Verify your username/password in `config.py`
- Default MySQL user is usually 'root' with no password
- If you set a password during MySQL installation, update `config.py`

### Error: "Database already exists"
- This is fine! The setup script handles this automatically
- It will reuse the existing database and reset the sample data

## Project Files

- `index.py` - Main quiz application (uses MySQL)
- `index.sql` - SQL schema and sample data
- `setup.py` - Database initialization script
- `config.py` - Database connection configuration

## Features

✅ MySQL database backend  
✅ Multiple quiz questions  
✅ Score tracking  
✅ Automatic database setup  
✅ Easy configuration  

Enjoy your quiz!
