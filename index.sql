-- ====================================================
-- MYSQL QUIZ DATABASE SCHEMA
-- ====================================================
-- Run this script in MySQL Workbench or mysql CLI:
-- mysql -u root -p < index.sql
-- ====================================================

-- Create the database
CREATE DATABASE IF NOT EXISTS online_quiz_db;
USE online_quiz_db;

-- ====================================================
-- 1. DATABASE SCHEMA (The Structure)
-- ====================================================

-- Table to store the quiz questions
CREATE TABLE Questions (
    QuestionID INT PRIMARY KEY AUTO_INCREMENT,
    QuestionText VARCHAR(500) NOT NULL
);

-- Table to store the multiple-choice options for each question
CREATE TABLE Options (
    OptionID INT PRIMARY KEY AUTO_INCREMENT,
    QuestionID INT NOT NULL,
    OptionText VARCHAR(255) NOT NULL,
    FOREIGN KEY (QuestionID) REFERENCES Questions(QuestionID) ON DELETE CASCADE
);

-- Table to store the correct answer for each question
CREATE TABLE Answers (
    AnswerID INT PRIMARY KEY AUTO_INCREMENT,
    QuestionID INT NOT NULL,
    CorrectOptionID INT NOT NULL,
    FOREIGN KEY (QuestionID) REFERENCES Questions(QuestionID) ON DELETE CASCADE,
    FOREIGN KEY (CorrectOptionID) REFERENCES Options(OptionID) ON DELETE CASCADE
);

-- ====================================================
-- 2. SEED DATA (Populating the Quiz)
-- ====================================================

-- Insert Question 1
INSERT INTO Questions (QuestionText)
VALUES ('What is the capital of France?');

-- Insert the 4 options for Question 1
INSERT INTO Options (QuestionID, OptionText)
VALUES 
    (1, 'Paris'), 
    (1, 'London'), 
    (1, 'Berlin'), 
    (1, 'Madrid');

-- Set the correct answer for Question 1 (OptionID 1: Paris)
INSERT INTO Answers (QuestionID, CorrectOptionID)
VALUES (1, 1); 

-- Insert Question 2
INSERT INTO Questions (QuestionText)
VALUES ('What is the largest planet in our solar system?');

-- Insert the 4 options for Question 2
INSERT INTO Options (QuestionID, OptionText)
VALUES 
    (2, 'Jupiter'), 
    (2, 'Saturn'), 
    (2, 'Neptune'), 
    (2, 'Venus');

-- Set the correct answer for Question 2 (OptionID 5: Jupiter)
INSERT INTO Answers (QuestionID, CorrectOptionID)
VALUES (2, 5);

-- Insert Question 3
INSERT INTO Questions (QuestionText)
VALUES ('What is the smallest country in the world?');

INSERT INTO Options (QuestionID, OptionText)
VALUES 
    (3, 'Vatican City'), 
    (3, 'Monaco'), 
    (3, 'Liechtenstein'), 
    (3, 'San Marino');

INSERT INTO Answers (QuestionID, CorrectOptionID)
VALUES (3, 9);

-- Insert Question 4
INSERT INTO Questions (QuestionText)
VALUES ('Who wrote Romeo and Juliet?');

INSERT INTO Options (QuestionID, OptionText)
VALUES 
    (4, 'William Shakespeare'), 
    (4, 'Jane Austen'), 
    (4, 'Charles Dickens'), 
    (4, 'Mark Twain');

INSERT INTO Answers (QuestionID, CorrectOptionID)
VALUES (4, 13);

-- Insert Question 5
INSERT INTO Questions (QuestionText)
VALUES ('What is the chemical symbol for Gold?');

INSERT INTO Options (QuestionID, OptionText)
VALUES 
    (5, 'Go'), 
    (5, 'Gd'), 
    (5, 'Au'), 
    (5, 'Ag');

INSERT INTO Answers (QuestionID, CorrectOptionID)
VALUES (5, 17);

-- Insert Question 6
INSERT INTO Questions (QuestionText)
VALUES ('In what year did the Titanic sink?');

INSERT INTO Options (QuestionID, OptionText)
VALUES 
    (6, '1910'), 
    (6, '1912'), 
    (6, '1915'), 
    (6, '1920');

INSERT INTO Answers (QuestionID, CorrectOptionID)
VALUES (6, 22);

-- Insert Question 7
INSERT INTO Questions (QuestionText)
VALUES ('What is the capital of Japan?');

INSERT INTO Options (QuestionID, OptionText)
VALUES 
    (7, 'Osaka'), 
    (7, 'Tokyo'), 
    (7, 'Kyoto'), 
    (7, 'Hiroshima');

INSERT INTO Answers (QuestionID, CorrectOptionID)
VALUES (7, 26);

-- Insert Question 8
INSERT INTO Questions (QuestionText)
VALUES ('How many sides does a hexagon have?');

INSERT INTO Options (QuestionID, OptionText)
VALUES 
    (8, '4'), 
    (8, '5'), 
    (8, '6'), 
    (8, '8');

INSERT INTO Answers (QuestionID, CorrectOptionID)
VALUES (8, 30);

-- Insert Question 9
INSERT INTO Questions (QuestionText)
VALUES ('What is the largest ocean on Earth?');

INSERT INTO Options (QuestionID, OptionText)
VALUES 
    (9, 'Atlantic Ocean'), 
    (9, 'Indian Ocean'), 
    (9, 'Pacific Ocean'), 
    (9, 'Arctic Ocean');

INSERT INTO Answers (QuestionID, CorrectOptionID)
VALUES (9, 34);

-- Insert Question 10
INSERT INTO Questions (QuestionText)
VALUES ('Who painted the Mona Lisa?');

INSERT INTO Options (QuestionID, OptionText)
VALUES 
    (10, 'Michelangelo'), 
    (10, 'Leonardo da Vinci'), 
    (10, 'Raphael'), 
    (10, 'Donatello');

INSERT INTO Answers (QuestionID, CorrectOptionID)
VALUES (10, 38);

-- ====================================================
-- 3. VERIFICATION QUERIES
-- ====================================================

-- QUERY A: Fetch all questions with their options
SELECT 
    q.QuestionID, 
    q.QuestionText AS 'Question', 
    o.OptionID AS 'Option Number', 
    o.OptionText AS 'Choice'
FROM Questions q
JOIN Options o ON q.QuestionID = o.QuestionID
ORDER BY q.QuestionID, o.OptionID;

-- QUERY B: Fetch question with correct answer
SELECT 
    q.QuestionID,
    q.QuestionText,
    a.CorrectOptionID,
    o.OptionText AS CorrectAnswer
FROM Questions q
JOIN Answers a ON q.QuestionID = a.QuestionID
JOIN Options o ON a.CorrectOptionID = o.OptionID
ORDER BY q.QuestionID;