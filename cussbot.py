import os
import logging
import configparser
import praw
import GLib
from cuss_scraper import Scraper
from Database import Database


class CussBotController:
    """
    Class for controlling CussBot startup.
    """

    def __init__(self):
        """
        Initializes required sections: configparser + Scraper()
        """

        # Reads config files
        self.config = configparser.RawConfigParser()
        # Scraper object used by CussBot
        self.scraper = Scraper()

    def bot_flow(self):
        """
        The bot's main logic.
        1. Checks config files for settings.
        2. Logs into PRAW.
        3. Runs the scraper.

        :return:
        """

        # Configures scraper settings
        scraper_settings = ScraperSetter(self.config)

        # Logs into Praw
        reddit = self.praw_login()

        # Starts the Scraper
        self.scraper.scraper_flow(scraper_settings, reddit)

    def praw_login(self):
        """
        Logs into PRAW, returns the PRAW object.

        :return:
        """

        # Read praw.ini config file for login info
        logger.info('Reading praw.ini file.')
        self.config.read('Config/praw.ini')

        # Assign login credentials using .ini file
        client_id = self.config['Praw Login']['client_id']
        client_secret = self.config['Praw Login']['client_secret']
        username = self.config['Praw Login']['username']
        password = self.config['Praw Login']['password']
        user_agent = self.config['Praw Login']['user_agent']

        # Reddit API Login
        logger.info("Attempting PRAW login.")
        r = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )

        logger.info("PRAW Login Successful.")

        return r


# Class manages the config directory and mandatory login file
class Configurator:
    """
    Class for creating Config directory and praw.ini file.
    """

    @staticmethod
    def create_empty_login(directory, file_name):
        """
        Creates empty praw.ini file with instructions.

        :param directory:
        :param file_name:
        """

        # New Config Parser
        config = configparser.RawConfigParser(allow_no_value=True)

        # Create Config Body
        config.add_section('Praw Login')
        config.set('Praw Login', '# Enter your Praw Login information below')
        config.set('Praw Login', 'client_id', '')
        config.set('Praw Login', 'client_secret', '')
        config.set('Praw Login', 'username', '')
        config.set('Praw Login', 'password', '')
        config.set('Praw Login', 'user_agent', '')

        # Creates path for Config File
        file_path = directory + '/' + file_name
        logger.info('Saving config file at ' + file_path)

        # Write Config File to created path
        with open(file_path, 'w') as configfile:
            config.write(configfile)

        logger.info("Successfully created empty Config file.")

    @staticmethod
    def config_init():
        """
        1. Assembles the config directory, then checks if this directory already exists. Creates directory if doesn't.
        2. Checks if praw.ini exists. Creates empty file if doesn't.
        """

        # Todo: Break this into two methods. 1) Check/create config directory.

        # Config Folder Info
        config_dir = 'Config'
        file_name = 'praw.ini'

        # Creates a path to include the new directory
        parent_dir = os.getcwd()
        config_path = os.path.join(parent_dir, config_dir)

        # Creates file path to check if file exists
        file_path = os.path.join(config_path, file_name)

        if os.path.exists(config_dir):
            logger.info(config_dir + ' directory found.')
            pass
        else:
            # Creates directory if doesn't exist
            logger.info(config_dir + ' directory missing. Creating Config directory.')
            GLib.create_dir(config_path)

        # Todo: 2) Break this into two methods. Check/create praw.ini file.
        if os.path.exists(file_path):
            logger.info('Praw Login File Found.')
        else:
            logger.info('Praw Login File Missing. Creating an empty Praw Login File.')
            Configurator.create_empty_login(config_dir, file_name)


class ScraperSetter:

    def __init__(self, config):
        """
        Reads the scraper.ini config file for scraper settings, then sets them.
        """

        # Attempts to read scraper.ini config
        try:
            config.read('Config/scraper.ini')
            self.subreddit = config['Comments']['subreddit']
            self.find_universal = config['Words']['universal']
            self.find_brit_aus = config['Words']['brit_aus']
            self.find_other = config['Words']['other']
            self.find_universal_derogatory = config['Words']['universal_derogatory']
            self.find_brit_aus_derogatory = config['Words']['brit_aus_derogatory']

        except KeyError:
            logger.exception("Failed to configure scraper due to KeyError.")
        except:
            logger.exception("Failed to configure scraper.")
            raise
        else:
            logger.info('Scraper configured successfully.')


# Logging setup
logging.basicConfig(filename='Logs/full_logs.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s : %(message)s')
# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Formatter and FileHandler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
file_handler = logging.FileHandler('Logs/cussbot.log')
file_handler.setFormatter(formatter)
# Adds FileHandler to Logger
logger.addHandler(file_handler)

if __name__ == "__main__":

    # Checks Config directory and praw login
    Configurator.config_init()

    # Creates and starts the database
    d = Database()
    d.start_database()

    # Create CussBotController object
    c = CussBotController()
    # Fires up the bot
    c.bot_flow()
