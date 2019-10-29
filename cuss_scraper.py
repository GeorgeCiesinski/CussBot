import logging
from Comment import Comment
from Database import Database
import configparser


class Scraper:

    def __init__(self, settings, reddit, database):
        """
        Applies settings for scraper.

        :param settings:
        :param reddit:
        """

        # Sets up config
        self.config = configparser.RawConfigParser()

        # Sets reddit
        self.reddit = reddit
        self.subreddit = settings.subreddit

        # Sets up database
        self.database = database

        # Sets up the scraper
        self.scraper_settings = self.setup_scraper(settings)

        # Creates empty word list
        self.scraper_words = []

        logger.debug(f"""
        Scraper started with the below settings: 
        subreddit = {self.subreddit}
        universal = {self.scraper_settings[0]}
        brit_aus = {self.scraper_settings[1]}
        other = {self.scraper_settings[2]}
        universal_derogatory = {self.scraper_settings[3]}
        brit_aus_derogatory = {self.scraper_settings[4]}
        derivatives = {self.scraper_settings[5]}
        """)

        # Starts scraper logic
        self.scraper_flow()

    def run_check(self):
        """
        Reads the scraper.ini config file to see if it should run the next cycle.

        :return:
        """

        config = self.config

        try:
            config.read('Config/scraper.ini')
            run = config['Scraper Flow']['run']
            logger.debug('Successfully read scraper.ini [Scraper Flow][Run].')
        except:
            logger.exception("Failed to read scraper.ini.")
            raise

        logger.debug(f'scraper.ini [Scraper Flow][Run] set to {run}')
        return run

    @staticmethod
    def setup_scraper(settings):
        """
        Creates list of scraping settings.

        :param settings:
        :return: list of settings
        :rtype: list
        """

        try:
            scraper_settings = [
                settings.find_universal,
                settings.find_brit_aus,
                settings.find_other,
                settings.find_universal_derogatory,
                settings.find_brit_aus_derogatory,
                settings.find_derivatives
            ]
            logger.debug('scraper_settings applied successfully.')
        except:
            logger.exception('setup_scraper failed to apply scraper_settings.')
            raise

        return scraper_settings

    def scraper_flow(self):

        logger.info('Starting scraper_flow.')

        # Adds words to self.scraper_words as per settings
        self.determine_set_words()

        # Begins scraping subreddit
        self.subreddit_scraper(self.reddit, self.subreddit)

    def determine_set_words(self):
        """
        Determines words set in scraper_settings, calls method to add words to self.scraper_words
        """

        logger.info('Starting determine_set_words.')

        # universal
        if self.scraper_settings[0] == "True":
            # Query database for all words with universal dialect but not derogatory
            dialect = 'universal'
            derogatory = 'false'
            self.add_scraper_words(dialect, derogatory)
        # brit_aus
        if self.scraper_settings[1] == "True":
            # Query database for all words with brit_aus dialect but not derogatory
            dialect = 'brit_aus'
            derogatory = 'false'
            self.add_scraper_words(dialect, derogatory)
        # other
        if self.scraper_settings[2] == "True":
            # Query database for all words with other dialect
            dialect = 'other'
            derogatory = 'false'
            self.add_scraper_words(dialect, derogatory)
        # universal_derogatory
        if self.scraper_settings[3] == "True":
            # Query database for all words with other universal dialect, and derogatory set to true
            dialect = 'universal'
            derogatory = 'true'
            self.add_scraper_words(dialect, derogatory)
        # brit_aus_derogatory
        if self.scraper_settings[4] == "True":
            # Query database for all words with other universal dialect, and derogatory set to true
            dialect = 'brit_aus'
            derogatory = 'true'
            self.add_scraper_words(dialect, derogatory)
        if self.scraper_settings[5] == "True":
            logger.info('Appending derivatives to scraper_words.')
            Database.append_derivatives(self.database, self.scraper_words)

        logger.info('determine_set_words successfully generated scraper_words list.')

    def add_scraper_words(self, dialect, derogatory):
        """
        Adds words specified by determine_set_words()

        :param dialect:
        :param derogatory:
        """
        self.scraper_words = Database.append_scraper_words(self.database, self.scraper_words, dialect, derogatory)
        logger.info(f'Scraper has appended dialect: \'{dialect}\', derogatory: \'{derogatory}\'')

    # Simple test if bot is finding comments
    def subreddit_scraper(self, reddit, subreddit):
        """
        Loads comment stream from subreddit and checks each comment for words matching scraper_words list.

        :param reddit:
        :param subreddit:
        """

        logger.info(f'Scraping /r/{subreddit} for the specified words below:\n {self.scraper_words}')

        # Subreddits | Subreddits go here
        s = reddit.subreddit(subreddit)

        # Sets run variable to start comment scraping
        run = self.run_check()

        # For each comment: for each word in scraper_words, check if the word is present in the comment body
        while run == 'true':
            for comment in s.stream.comments():
                run = self.run_check()
                for word in self.scraper_words:
                    if word in comment.body:
                        c = Comment(comment)
                        self.comment_analyzer(c)

        logger.info(f'Finished scraping /r/{subreddit}.')

    def comment_analyzer(self, comment):
        """
        Analyzer gets comment.
        - Counts total number of words
        - Counts total number of swear words
        - Creates a list (or dict) of each swear word
        - Increases the count of each swear word until all words are counted

        - Stores comment id, author, subreddit, and above statistics

        :param comment:
        """

        print(comment.id)


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
    # Todo: Create debugger test
    pass
