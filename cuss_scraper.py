import logging
from Comment import Comment


class Scraper:

    def __init__(self, settings, reddit):
        """
        Applies settings for scraper.

        :param settings:
        :param reddit:
        """

        # Sets reddit
        self.reddit = reddit
        self.subreddit = settings.subreddit

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
            settings.find_brit_aus_derogatory
        ]

        return scraper_settings

    def scraper_flow(self):
        # Adds words to self.scraper_words as per settings
        self.add_scraper_words()

    def add_scraper_words(self):
        """
        Checks each setting. Calls queries to append those words to list.
        """

        # universal
        if self.scraper_settings[0] == "True":
            # Query database for all words with universal dialect
            pass
        # brit_aus
        if self.scraper_settings[1] == "True":
            # Query database for all words with brit_aus dialect
            pass
        # other
        if self.scraper_settings[2] == "True:":
            # Query database for all words with other dialect
            pass
        # universal_derogatory
        if self.scraper_settings[3] == "True:":
            # Query database for all words with other universal dialect, and derogatory set to true
            pass
        # brit_aus_derogatory
        if self.scraper_settings[4] == "True:":
            # Query database for all words with other universal dialect, and derogatory set to true
            pass

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
