import os
import logging
import configparser
import praw
from cuss_scraper import Scraper


# Class manages the config directory and mandatory login file
class Configurator:

    @staticmethod
    def create_dir(path):

        try:
            os.mkdir(path)
        except OSError as error:
            logger.exception('Creation of the directory %f failed.' % path)
        else:
            logger.info('Successfully created the directory %s.' % path)

    @staticmethod
    def create_empty_login(directory, file_name):
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

        logger.info("Created empty Config file.")

    @staticmethod
    def config_init():

        # Config Folder Info
        config_dir = 'Config'
        file_name = 'praw.ini'

        # Creates a path to include the new directory
        parent_dir = os.getcwd()
        config_path = os.path.join(parent_dir, config_dir)
        file_path = os.path.join(config_path, file_name)

        if os.path.exists(config_dir):
            logger.info(config_dir + ' directory found.')
            pass
        else:
            # Creates directory if doesn't exist
            logger.info(config_dir + ' directory missing. Creating Config directory.')
            Configurator.create_dir(config_path)

        if os.path.exists(file_path):
            logger.info('Praw Login File Found.')
        else:
            logger.info('Praw Login File Missing. Creating an empty Praw Login File.')
            Configurator.create_empty_login(config_dir, file_name)


class CussBotController:

    def __init__(self):

        # Praw session is set in praw_login()
        self.reddit = None
        # Subreddit configured in scraper.ini
        self.subreddit = None
        # Reads config files
        self.config = configparser.RawConfigParser()
        # Scraper object used by CussBot
        self.s = Scraper()

    def bot_flow(self):
        # Configures scraper settings
        self.configure_scraper()
        # Logs into Praw
        self.praw_login()
        # Todo: Simple praw test, replace with meaningful methods
        self.test_scraper()

    def praw_login(self):

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
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )

        logger.info("PRAW Login Successful.")

    def configure_scraper(self):
        self.config.read('Config/scraper.ini')
        self.subreddit = self.config['Comments']['subreddit']
        logger.info('Scraper configured successfully.')

    def test_scraper(self):
        Scraper.praw_test(self.s, self.reddit, self.subreddit)


# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Formatter and FileHandler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
file_handler = logging.FileHandler('Logs/CussBot.log')
file_handler.setFormatter(formatter)
# Adds FileHandler to Logger
logger.addHandler(file_handler)

# Checks Config directory and praw login
Configurator.config_init()

# Create CussBotController object
c = CussBotController()
# Fires up the bot
c.bot_flow()
