import os
import logging
import configparser
import praw
import words


# Class manages the config directory and mandatory login file
class Configurator:

    @staticmethod
    def create_dir(path):

        try:
            os.mkdir(path)
        except OSError as error:
            print('Creation of the directory %f failed.' % path)
            print(error)
        else:
            print('Successfully created the directory %s.' % path)

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

    @staticmethod
    def log_init():
        log_dir = 'Logs'
        pass


class CussFinder(object):

    def __init__(self, subreddit):

        # Praw session is set in praw_login()
        self.reddit = None
        self.subreddit = subreddit
        self.praw_login()
        self.comment_skimmer()

    def praw_login(self):

        # New Config Parser
        config = configparser.RawConfigParser()

        # Read praw.ini config file for login info
        logger.info('Reading praw.ini file.')
        config.read('Config/praw.ini')

        # Assign login credentials using .ini file
        client_id = config['Praw Login']['client_id']
        client_secret = config['Praw Login']['client_secret']
        username = config['Praw Login']['username']
        password = config['Praw Login']['password']
        user_agent = config['Praw Login']['user_agent']

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

    # Todo: Create new .py file for the comment skimmer
    def comment_skimmer(self):

        # Subreddits | Subreddits go here
        s = self.reddit.subreddit(self.subreddit)

        # Keyphrase | Swear words go here in alphabetical order
        # Todo: Add more swear words
        # Todo: Add conditional options depending on swear word origin
        keyphrase = words.brit_aus + words.brit_aus_derogatory + words.other + words.universal + words.universal_derogatory

        # Todo: Update log instead of printing to console
        # Look through comments in subreddit and print info to shell
        for comment in s.stream.comments():
            for cuss in keyphrase:
                if cuss in comment.body:
                    print(comment.body + '\n')
                    print(comment.author.name + ' said: ' + cuss + '\n')
                    print('https://www.reddit.com' + comment.permalink + '\n\n')


# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
file_handler = logging.FileHandler('Logs/CussBot.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# Checks Config directory and praw login
Configurator.config_init()

# logger = Logger()
sr = 'funny'
c = CussFinder(sr)
