import os
import praw
import configparser
import words


class CussFinder(object):

    def __init__(self, subreddit):
        # Praw session is set in praw_login()
        self.reddit = None
        self.subreddit = subreddit
        self.praw_login()
        self.comment_skimmer()

    def create_dir(self, folder):
        directory = folder
        parent_dir = os.getcwd()
        print(parent_dir)
        path = os.path.join(parent_dir, directory)

        try:
            os.mkdir(path)
        except OSError as error:
            print('Creation of the directory %f failed.' % path)
            print(error)
        else:
            print('Successfully created the directory %s.' % path)

    def config_init(self):

        folder = 'Config'
        if os.path.exists(folder):
            print(folder, 'directory found.')
            pass
        else:
            # Creates directory if doesn't exist
            print(folder, 'directory missing. Creating Config directory.')
            self.create_dir(folder)

    def praw_login(self):

        # Read praw.ini config file for login info
        # Todo: Check if config file exists. Create if does not
        self.config_init()
        config = configparser.RawConfigParser()
        config.read('Config/praw.ini')

        # Assign login credentials using .ini file
        client_id = config['Praw Login']['client_id']
        client_secret = config['Praw Login']['client_secret']
        username = config['Praw Login']['username']
        password = config['Praw Login']['password']
        user_agent = config['Praw Login']['user_agent']

        # Reddit API Login
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )

        print("PRAW Login Successful.")

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


sr = 'funny'
c = CussFinder(sr)
