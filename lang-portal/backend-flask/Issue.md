During the initial testing while still in development, I encountered the following problem:

{
  "id": 2
}
(base) san@DESKTOP-TU96UUS:~/lang-portal/gunoi$ 
(base) san@DESKTOP-TU96UUS:~/lang-portal/gunoi$ curl -X POST -H "Content-Type: application/json" -d '{"review_items": [{"word_id": 1, "correct": true}, {"word_id": 2, "correct": false}]}' "http://127.0.0.1:5000/api/study-sessions/1/review"
{
  "error": "ON CONFLICT clause does not match any PRIMARY KEY or UNIQUE constraint"
}

The error "ON CONFLICT clause does not match any PRIMARY KEY or UNIQUE constraint" indicates a problem with the SQL query in the record_review_results function within routes/study_sessions.py

INSERT INTO word_reviews (word_id, correct_count, wrong_count)
VALUES (?, ?, ?)
ON CONFLICT(word_id) DO UPDATE SET
correct_count = correct_count + ?,
wrong_count = wrong_count + ?

This query attempts to use an ON CONFLICT clause (also known as an "UPSERT") to either insert a new row into the word_reviews table or, if a row with the same word_id already exists, update the correct_count and wrong_count columns. The error message means that the word_reviews table does not have a primary key or unique constraint on the word_id column. Without this constraint, SQLite doesn't know how to handle the conflict.

Looking at the provided database.png, we can confirm that the word_reviews table should have word_id as its primary key. 

Solution:

CREATE TABLE IF NOT EXISTS word_reviews (
  word_id INTEGER PRIMARY KEY,
  correct_count INTEGER DEFAULT 0,
  wrong_count INTEGER DEFAULT 0,
  last_reviewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (word_id) REFERENCES words(id)
);

