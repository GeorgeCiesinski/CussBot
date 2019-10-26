import logging
from Comment import Comment
from Database import Database


class Scraper:

    def __init__(self, settings, reddit, database):
        """
        Applies settings for scraper.

        :param settings:
        :param reddit:
        """

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

    @staticmethod
    def setup_scraper(settings):
        """
        Creates list of scraping settings.

        :param settings:
        :return: list of settings
        :rtype: list
        """

        scraper_settings = [
            settings.find_universal,
            settings.find_brit_aus,
            settings.find_other,
            settings.find_universal_derogatory,
            settings.find_brit_aus_derogatory,
            settings.find_derivatives
        ]

        return scraper_settings

    def scraper_flow(self):
        # Adds words to self.scraper_words as per settings
        self.determine_set_words()

    def determine_set_words(self):
        """
        Determines words set in scraper_settings, calls method to add words to self.scraper_words
        """

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
            logger.info("Appending derivatives to scraper_words.")
            Database.append_derivatives(self.database, self.scraper_words)

    def add_scraper_words(self, dialect, derogatory):
        """
        Adds words specified by determine_set_words()

        :param dialect:
        :param derogatory:
        """
        self.scraper_words = Database.append_scraper_words(self.database, self.scraper_words, dialect, derogatory)
        logger.info(f'Scraper has appended dialect: \'{dialect}\', derogatory: \'{derogatory}\'')

    # Simple test if bot is finding comments
    @staticmethod
    def praw_test(reddit, subreddit):

        logger.info('Praw Test Started.')

        # Subreddits | Subreddits go here
        s = reddit.subreddit(subreddit)

        """
        Test goes here
        """

        for comment in s.stream.comments():
            c = Comment(comment)
            print(c.body)

        """
        Test complete
        """

        logger.info('Praw Test Complete.')


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
