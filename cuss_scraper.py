import logging
import Comment


class Scraper:

    # Simple test if bot is finding comments
    @staticmethod
    def praw_test(self, reddit, subreddit):

        logger.info('Praw Test Started.')

        # Subreddits | Subreddits go here
        s = reddit.subreddit(subreddit)

        """
        Test goes here
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
