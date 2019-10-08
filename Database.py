import logging
import sqlite3
import os
import words


class Database:

    # Sets database directory
    @staticmethod
    def database_directory():
        # Sqlite3 Folder Info
        db_dir = 'Sqlite3'
        # Name of the database file. Needs to be stored in the Sqlite3 Folder.
        file_name = 'cussbot.db'

        # Creates a path for the Database
        db_directory = os.path.join(db_dir, file_name)
        logger.info(f'Successfully joined {db_dir} and {file_name} into {db_directory}')
        return db_directory

    @staticmethod
    def create_connection(db_directory):

        conn = None

        # Attempt to create connection object, log exception if fails.
        try:
            conn = sqlite3.connect(db_directory)
            return conn
        except:
            logger.exception('Failed to create connection object.')
            raise

        # Returns connection object
        return conn

    # Creates word table for the first time
    @staticmethod
    def create_word_tables(conn):
        # Connection object
        c = conn

    def start_database(self):
        
        """
        This method always needs to be run first.
        - Creates db if doesn't exist
        - Creates tables in db if they do not exist
        """

        # Sets database directory
        db_directory = self.database_directory()

        # Checks if database exists
        if os.path.exists(db_directory):
            logger.info('Database has been found at ' + db_directory + '.')
            # Creates connection object.
            conn = self.create_connection(db_directory)
        else:
            logger.info('Database not found. Creating new database.')
            # Creates connection object. This also creates the database if doesn't exist.
            conn = self.create_connection(db_directory)
            logger.info('Database successfully created.')


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

    # Create database object
    d = Database()
    # Starts the database
    d.start_database()
