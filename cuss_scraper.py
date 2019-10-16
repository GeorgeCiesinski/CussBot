import logging
from Comment import Comment


class Scraper:

    def __init__(self):
        pass

    @staticmethod
    def scraper_flow(settings, reddit):

        # Todo: Below is only a test. Rewrite this into better code.
        # Todo: Use this to control various scrapers that search for different conditions
        subreddit = settings.subreddit
        universal = settings.find_universal
        brit_aus = settings.find_brit_aus
        other = settings.find_other
        universal_derogatory = settings.find_universal_derogatory
        brit_aus_derogatory = settings.find_brit_aus_derogatory

        scraper_settings = f"""
The scraper settings are: 
subreddit = {subreddit}
universal = {universal}
brit_aus = {brit_aus}
other = {other}
universal_derogatory = {universal_derogatory}
brit_aus_derogatory = {brit_aus_derogatory}
"""

        print(scraper_settings)

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
