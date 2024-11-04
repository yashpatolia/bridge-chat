import sqlite3
import logging

def sql_eval(command: str):
    with sqlite3.connect("temporals.db") as connection:
        cursor = connection.cursor()
        connection.execute("PRAGMA foreign_keys = ON;")
        try:
            cursor.execute(command)
            logging.info(f'[DB] {command}')
            if command.startswith('select'):
                results = cursor.fetchall()
                return results
            else:
                connection.commit()
                return 'Complete'
        except Exception as e:
            logging.error(e)
            return e
