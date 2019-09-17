import praw
import configparser

# Read praw.ini config file for login info
# Todo: Check if config file exists. Create if does not.
config = configparser.RawConfigParser()
config.read('Config/praw.ini')

client_id = config['Praw Login']['client_id']
client_secret = config['Praw Login']['client_secret']
username = config['Praw Login']['username']
password = config['Praw Login']['password']
user_agent = config['Praw Login']['user_agent']


# Reddit API Login
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

# Subreddits | Subreddits go here
subreddit = reddit.subreddit('funny')

# Keyphrase | Swear words go here in alphabetical order
keyphrase = ['asshole',
             'bastard',
             'bitch',
             'cunt',
             'fuck',
             'prick',
             'shit',
             'slut',
             'twat']

# Look through comments in subreddit and print info to shell
for comment in subreddit.stream.comments():
    for cuss in keyphrase:
        if cuss in comment.body:
            print(comment.body + '\n')
            print(comment.author.name + ' said: ' + cuss + '\n')
            print('https://www.reddit.com' + comment.permalink + '\n\n')

