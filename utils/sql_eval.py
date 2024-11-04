import sqlite3
import logging

def sql_eval(command: str):
    with sqlite3.connect("temporals.db") as connection:
        cursor = connection.cursor()
        connection.execute("PRAGMA foreign_keys = ON;")
        try:
            cursor.execute(command)
            if command.startswith('SELECT'):
                results = cursor.fetchall()
                return results
            else:
                connection.commit()
                return 'Complete'
        except Exception as e:
            logging.error(e)
            return e
