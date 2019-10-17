import logging
from Comment import Comment


class Scraper:

    def __init__(self):
        pass

    @staticmethod
    def scraper_flow(settings, reddit):

        # Apply settings to scraper_flow
        subreddit = settings.subreddit

        scraper_settings = [
            settings.find_universal,
            settings.find_brit_aus,
            settings.find_other,
            settings.find_universal_derogatory,
            settings.find_brit_aus_derogatory
        ]

        # Empty word list
        scraper_words = []

        logger.debug(f"""
Scraper started with the below settings: 
subreddit = {subreddit}
universal = {scraper_settings[0]}
brit_aus = {scraper_settings[1]}
other = {scraper_settings[2]}
universal_derogatory = {scraper_settings[3]}
brit_aus_derogatory = {scraper_settings[4]}
""")

        if scraper_settings[0] == "True":
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

    pass
