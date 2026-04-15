import sqlite3

def setup_full_database():
    con = sqlite3.connect('user_data.db')
    cur = con.cursor()

    # This will store every quiz attempt my users will have
    cur.execute('''
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        topic VARCHAR(255) NOT NULL,
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES userdata(id)
    )
    ''')
    # This will keep the results of each persons quiz and hopefully will be displayed as part of the dashboard and leaderboard
    cur.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        user_answer TEXT,
        correct INTEGER,
        FOREIGN KEY(quiz_id) REFERENCES quizzes(id),
        FOREIGN KEY(question_id) REFERENCES questions(id)
    )
    ''')
    # Important part of the NEA showing the user their strongest and weakest areas
    cur.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        topic VARCHAR(255) NOT NULL,
        score INTEGER NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES userdata(id)
    )
    ''')
    con.commit()
    con.close()
if __name__ == "__main__":
    setup_full_database()
    print("Database and tables created.")
