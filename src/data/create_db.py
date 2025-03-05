"""
Code from COMP0035
Contains functions to create the paralympics database without data.
"""
import sqlite3

from paralympics import add_data


def create_db(cursor, connection):
    """Create the paralympics database structure and add the data.

    Parameters
    ----------
    connection: sqlite connection object
    cursor: sqlite cursor object
    """

    # Define the tables and relationships using SQL statements
    disability_sql = '''CREATE TABLE disability (
                            disability_id INTEGER PRIMARY KEY,
                            category TEXT NOT NULL)'''

    country_sql = '''CREATE TABLE country (
                    code TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    region TEXT,
                    sub_region TEXT,
                    member_type TEXT,
                    notes TEXT
                    )'''

    host_sql = '''CREATE TABLE host (
                    host_id INTEGER PRIMARY KEY,
                    country_code TEXT NOT NULL,
                    host TEXT NOT NULL,
                    FOREIGN KEY (country_code) REFERENCES country(code) ON DELETE CASCADE ON UPDATE CASCADE)'''

    event_sql = '''CREATE TABLE event (
                    event_id INTEGER PRIMARY KEY,
                    type INTEGER NOT NULL,
                    year INTEGER NOT NULL,
                    start TEXT,
                    end TEXT,
                    countries INTEGER,
                    events INTEGER,
                    sports INTEGER,
                    highlights TEXT,
                    url TEXT,
                    latitude TEXT,
                    longitude TEXT
                )'''

    disability_event_sql = '''CREATE TABLE disability_event (
                            disability_id INTEGER,
                            event_id INTEGER,
                            PRIMARY KEY (disability_id, event_id),
                            FOREIGN KEY (disability_id) REFERENCES disability(disability_id) ON DELETE CASCADE ON UPDATE CASCADE,
                            FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE)'''

    host_event_sql = '''CREATE TABLE host_event (
                            host_id TEXT NOT NULL,
                            event_id INTEGER NOT NULL,
                            PRIMARY KEY (host_id, event_id),
                            FOREIGN KEY (host_id) REFERENCES host(host_id) ON DELETE CASCADE ON UPDATE CASCADE,
                            FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE
                    )'''

    participants_sql = '''CREATE TABLE participants (
                    participant_id INTEGER PRIMARY KEY,
                    participants_m INTEGER,
                    participants_f INTEGER,
                    participants INTEGER,
                    event_id INTEGER,
                    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE

                )'''

    medal_result_sql = '''CREATE TABLE medal_result (
                            result_id INTEGER PRIMARY KEY,
                            event_id INTEGER,
                            country_code TEXT,
                            rank INTEGER,
                            gold INTEGER,
                            silver INTEGER,
                            bronze INTEGER,
                            total INTEGER,
                            FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE,
                            FOREIGN KEY (country_code) REFERENCES country(code) ON DELETE CASCADE ON UPDATE CASCADE)
                        '''

    question_sql = '''CREATE TABLE question (
                        question_id INTEGER PRIMARY KEY,
                        question TEXT NOT NULL,
                        event_id INTEGER,
                        FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE
                        )'''

    quiz_sql = '''CREATE TABLE quiz (
                    quiz_id INTEGER PRIMARY KEY,
                    quiz_name TEXT NOT NULL,
                    close_date TEXT
                )'''

    answer_choice_sql = '''CREATE TABLE answer_choice (
                                ac_id INTEGER PRIMARY KEY,
                                question_id INTEGER NOT NULL,
                                choice_text TEXT NOT NULL,
                                choice_value INTEGER,
                                is_correct INTEGER,
                                FOREIGN KEY (question_id) REFERENCES question(question_id) ON DELETE CASCADE ON UPDATE CASCADE
                        )'''

    quiz_question_sql = '''CREATE TABLE quiz_question (
                    question_id INTEGER,
                    quiz_id INTEGER,
                    PRIMARY KEY(question_id, quiz_id),
                    FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id) ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY (question_id) REFERENCES question(question_id) ON DELETE CASCADE ON UPDATE CASCADE
                    )'''

    student_response_sql = '''CREATE TABLE student_response (
                            response_id INTEGER PRIMARY KEY,
                            student_email TEXT NOT NULL,
                            score INTEGER NOT NULL,
                            quiz_id INTEGER NOT NULL,
                            FOREIGN KEY (quiz_id) REFERENCES quiz(quiz_id) ON DELETE CASCADE ON UPDATE CASCADE
                        )'''

    try:
        # Drop each table if they already exist
        cursor.execute('DROP TABLE IF EXISTS host_event;')
        cursor.execute('DROP TABLE IF EXISTS disability_event;')
        cursor.execute('DROP TABLE IF EXISTS participants;')
        cursor.execute('DROP TABLE IF EXISTS medal_result;')
        cursor.execute('DROP TABLE IF EXISTS event;')
        cursor.execute('DROP TABLE IF EXISTS host;')
        cursor.execute('DROP TABLE IF EXISTS country;')
        cursor.execute('DROP TABLE IF EXISTS disability;')
        cursor.execute('DROP TABLE IF EXISTS answer_choice;')
        cursor.execute('DROP TABLE IF EXISTS quiz_question;')
        cursor.execute('DROP TABLE IF EXISTS student_response;')
        cursor.execute('DROP TABLE IF EXISTS question;')
        cursor.execute('DROP TABLE IF EXISTS quiz;')

        # Create the tables
        cursor.execute(country_sql)
        cursor.execute(host_sql)
        cursor.execute(event_sql)
        cursor.execute(participants_sql)
        cursor.execute(disability_sql)
        cursor.execute(host_event_sql)
        cursor.execute(disability_event_sql)
        cursor.execute(question_sql)
        cursor.execute(quiz_sql)
        cursor.execute(answer_choice_sql)
        cursor.execute(quiz_question_sql)
        cursor.execute(student_response_sql)
        cursor.execute(medal_result_sql)

        # Commit the changes
        connection.commit()

        # Call the function to add the data
        add_data.add_all_data(cursor, connection)

    except sqlite3.Error as e:
        print(f'An error occurred creating the database. Error: {e}')
        if connection:
            connection.rollback()
