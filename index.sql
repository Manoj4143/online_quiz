-- 1. INSERT QUESTIONS
INSERT INTO Questions (QuestionID, QuestionText) VALUES
(1, 'What is the chemical symbol for Gold?'),
(2, 'Which planet is known as the Red Planet?'),
(3, 'Who painted the Mona Lisa?'),
(4, 'What is the largest mammal in the world?'),
(5, 'In what year did the Titanic sink?'),
(6, 'What is the capital city of Japan?'),
(7, 'Which element has the atomic number 1?'),
(8, 'What does "HTTP" stand for in website addresses?'),
(9, 'Which country gifted the Statue of Liberty to the USA?'),
(10, 'How many bones are in the adult human body?');

-- 2. INSERT OPTIONS
-- Note: OptionIDs are unique. 4 options per question.
INSERT INTO Options (OptionID, QuestionID, OptionText) VALUES
(1, 1, 'Ag'), (2, 1, 'Au'), (3, 1, 'Gd'), (4, 1, 'Fe'),
(5, 2, 'Venus'), (6, 2, 'Mars'), (7, 2, 'Jupiter'), (8, 2, 'Saturn'),
(9, 3, 'Van Gogh'), (10, 3, 'Picasso'), (11, 3, 'Da Vinci'), (12, 3, 'Dalí'),
(13, 4, 'Elephant'), (14, 4, 'Blue Whale'), (15, 4, 'Great White Shark'), (16, 4, 'Giraffe'),
(17, 5, '1912'), (18, 5, '1905'), (19, 5, '1920'), (20, 5, '1898'),
(21, 6, 'Seoul'), (22, 6, 'Beijing'), (23, 6, 'Bangkok'), (24, 6, 'Tokyo'),
(25, 7, 'Helium'), (26, 7, 'Oxygen'), (27, 7, 'Hydrogen'), (28, 7, 'Carbon'),
(29, 8, 'HyperText Transfer Protocol'), (30, 8, 'High Transfer Text Process'), (31, 8, 'Hyperlink Total Text Protocol'), (32, 8, 'Hard Text Transfer Protocol'),
(33, 9, 'United Kingdom'), (34, 9, 'France'), (35, 9, 'Germany'), (36, 9, 'Canada'),
(37, 10, '186'), (38, 10, '206'), (39, 10, '256'), (40, 10, '306');

-- 3. INSERT ANSWERS
-- Maps the Question to the specific OptionID that is correct
INSERT INTO Answers (QuestionID, CorrectOptionID) VALUES
(1, 2),   -- Au
(2, 6),   -- Mars
(3, 11),  -- Da Vinci
(4, 14),  -- Blue Whale
(5, 17),  -- 1912
(6, 24),  -- Tokyo
(7, 27),  -- Hydrogen
(8, 29),  -- HyperText Transfer Protocol
(9, 34),  -- France
(10, 38); -- 206