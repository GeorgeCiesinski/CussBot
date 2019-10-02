import logging
import sqlite3
import os
import words


class Database:

    db_directory = None

    @staticmethod
    def check_table():
        # Sqlite3 Folder Info
        db_dir = 'Sqlite3'
        file_name = 'cussbot.db'

        # Creates a path to include the new directory
        parent_dir = os.getcwd()
        db_path = os.path.join(parent_dir, db_dir)
        Database.db_directory = os.path.join(db_dir, file_name)

    @staticmethod
    def create_database():
        # Todo: Modify this to check if db exists or not, and to update logger correctly.
        c = sqlite3.connect('Sqlite3/cussbot.db')
        logger.info('Database successfully created.')
        c.close()
        logger.info('Database successfully closed.')

    @staticmethod
    def create_table():
        c = sqlite3.connect('Sqlite3/cussbot.db')
        c.execute("""
        create table cusswords
        (
          id integer primary key autoincrement,
          word varchar(100) 
        );
        """)
        c.close()
        logger.info('cusswords table created.')

    @staticmethod
    def insert_values():
        universal = words.universal
        c = sqlite3.connect('Sqlite3/cussbot.db')
        for u in universal:
            c.execute("Insert into cusswords (word) values (?)", u)
            logger.info('Inserted the word ' + u + ' into database.')
        c.commit()
        c.close()


# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Formatter and FileHandler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
file_handler = logging.FileHandler('Logs/database.log')
file_handler.setFormatter(formatter)
# Adds FileHandler to Logger
logger.addHandler(file_handler)

# Debugging Database.py
if __name__ == "__main__":
    Database.create_database()
    Database.create_table()
    Database.insert_values()
