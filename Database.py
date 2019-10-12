import configparser
import logging
import sqlite3
import os
import words


class Database:

    def __init__(self):

        # Starts config parser to read words.ini
        self.config = configparser.RawConfigParser(allow_no_value=True)

        # Word lists
        self.universal = None
        self.universal_derogatory = None
        self.brit_aus = None
        self.brit_aus_derogatory = None
        self.other = None

    # Sets database directory
    @staticmethod
    def database_directory():
        """
        Assembles the database directory

        :return: db_directory
        :rtype: str
        """

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
        """
        Attempts to create a connection to the database.

        :param db_directory:
        :return: Connection object
        :rtype: object
        """

        conn = None

        # Attempt to create connection object, log exception if fails.
        try:
            conn = sqlite3.connect(db_directory)
            logger.info('Successfully created connection object.')
            return conn
        except:
            logger.exception('Failed to create connection object.')
            raise

        # Returns connection object
        return conn

    @staticmethod
    def close_conn(conn):
        """
        Attempts to close the connection to the database.

        :param conn:
        :return:
        """
        try:
            conn.close()
            logger.info('Successfully closed database connection.')
        except:
            logger.exception('Database connection failed to close.')
            raise

    @staticmethod
    def execute_sql_no_return(conn, query):
        """
        Executes the query. Returns nothing.

        :param conn:
        :param query:
        """

        # Executes sql query, doesn't return any values
        try:
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            logger.info(f'Successfully executed the query: \n{query}')
        except:
            logger.exception(f'Failed to execute the query: \n{query}')
            raise

    @staticmethod
    def execute_select(conn, query):
        """
        Executes select query.

        :param conn:
        :param query:
        :return: List of tuples.
        :rtype: List
        """

        try:
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            logger.info(f'Successfully executed the query: \n{query}')
        except:
            logger.exception(f'Failed to execute the query: \n{query}')
            raise

        rows = c.fetchall()
        return rows

    # Creates word table for the first time
    def create_word_tables(self, conn):
        """
        Executes queries to create word tables.

        :param conn:
        """

        sql_create_cusswords_table = """CREATE TABLE IF NOT EXISTS cusswords (
        id integer PRIMARY KEY,
        word text NOT NULL UNIQUE
        );"""

        sql_create_property_table = """CREATE TABLE IF NOT EXISTS property (
        word_id integer NOT NULL,
        property_name varchar(100) NOT NULL,
        property_value varchar(100) NOT NULL
        );"""

        sql_create_derivative_table = """CREATE TABLE IF NOT EXISTS derivatives (
        word_id integer NOT NULL,
        child_word varchar(100) NOT NULL UNIQUE
        );"""

        if conn is not None:
            # Create tables: cusswords, property, derivative
            self.execute_sql_no_return(conn, sql_create_cusswords_table)
            self.execute_sql_no_return(conn, sql_create_property_table)
            self.execute_sql_no_return(conn, sql_create_derivative_table)
        else:
            logger.info('Unable to create word tables as there is no connection.')

    def insert_list_into_db(self, conn, word_list):
        """
        Runs query which inserts words in word_list into cusswords table.

        :param conn:
        :param word_list:
        """

        if conn is not None:

            for l_word in word_list:

                sql_insert_into_cusswords = f"""
                INSERT INTO cusswords (word)
                VALUES(\'{l_word}\');
                """

                self. execute_sql_no_return(conn, sql_insert_into_cusswords)

    def word_list_insertion(self, conn):
        """
        Creates cusswords list by reading words.ini config file.

        :param conn:
        """

        self.config.read('Config/words.ini')

        # Splits strings from words.ini into usable lists
        self.universal = (self.config['Words']['universal']).split(', ')
        self.universal_derogatory = (self.config['Derogatory']['universal']).split(', ')
        self.brit_aus = (self.config['Words']['brit_aus']).split(', ')
        self.brit_aus_derogatory = (self.config['Derogatory']['brit_aus']).split(', ')
        self.other = (self.config['Words']['other']).split(', ')

        # Creates list of list
        cusswords_list = [
            self.universal,
            self.universal_derogatory,
            self.brit_aus,
            self.brit_aus_derogatory,
            self.other
            ]

        for word_list in cusswords_list:
            self.insert_list_into_db(conn, word_list)

    def property_insertion(self, conn):
        """
        Creates queries to insert the property of each word into the property table.

        :param conn:
        """

        select_all_from_cusswords = """
        SELECT * FROM cusswords 
        """

        rows = self.execute_select(conn, select_all_from_cusswords)

        for row in rows:
            word_id = row[0]
            word = row[1]
            print(word)

            word_properties = self.property_assigner(word)
            dialect = word_properties[0]
            derogatory = word_properties[1]

            insert_dialect_query = f"""
            INSERT INTO property (word_id, property_name, property_value)
            VALUES(\'{word_id}\', 'dialect', \'{dialect}\');
            """

            insert_derogatory_query = f"""
            INSERT INTO property (word_id, property_name, property_value)
            VALUES(\'{word_id}\', 'derogatory', \'{derogatory}\');
            """

            # Insert dialect property value into table
            self.execute_sql_no_return(conn, insert_dialect_query)

            # Insert derogatory property value into table
            self.execute_sql_no_return(conn, insert_derogatory_query)

    def property_assigner(self, word):
        """
        Assigns each word a property.

        :param word:
        :return: dialect and derogatory properties
        :rtype: tuple
        """

        # Sets dialect and derogatory values
        if word in self.universal:
            dialect = 'universal'
            derogatory = 'false'
        elif word in self.universal_derogatory:
            dialect = 'universal'
            derogatory = 'true'
        elif word in self.brit_aus:
            dialect = 'brit_aus'
            derogatory = 'false'
        elif word in self.brit_aus_derogatory:
            dialect = 'brit_aus'
            derogatory = 'true'
        elif word in self.other:
            dialect = 'other'
            derogatory = 'false'
        else:
            logger.info(f'The word {word} does not appear in any list.')

        return dialect, derogatory

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
        else:
            # Creates new database as cussbot.db does not exist
            logger.info('Database not found. Creating new database.')

            # Creates connection object. This also creates the database if doesn't exist.
            conn = self.create_connection(db_directory)
            # Create word tables
            self.create_word_tables(conn)
            # Insert all swearwords except derivatives into cusswords table
            self.word_list_insertion(conn)
            # Insert cussword properties into property table
            self.property_insertion(conn)
            # Close connection
            self.close_conn(conn)


"""
Logger is setup here.
"""

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Formatter and FileHandler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
file_handler = logging.FileHandler('Logs/database.log')
file_handler.setFormatter(formatter)
# Adds FileHandler to Logger
logger.addHandler(file_handler)

"""
Debugging Database.py
"""
if __name__ == "__main__":

    logger.info('Database.py is running as __main__.')
    # Create database object
    d = Database()
    # Starts the database
    d.start_database()
