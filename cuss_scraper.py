import logging
import Comment
import words


class Scraper:

    # Simple test if bot is finding comments
    @staticmethod
    def praw_test(self, reddit, subreddit):

        logger.info('Praw Test Started.')

        # Subreddits | Subreddits go here
        s = reddit.subreddit(subreddit)

        # Keyphrase | Swear words go here in alphabetical order
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

        logger.info('Praw Test Complete.')

    def comment_finder(self, reddit, subreddit):

        # logger.info('comment_finder started.')
        #
        # s = reddit.subreddit(subreddit)
        pass


# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Formatter and FileHandler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
file_handler = logging.FileHandler('Logs/cussbot.log')
file_handler.setFormatter(formatter)
# Adds FileHandler to Logger
logger.addHandler(file_handler)
