"""Cussbot
https://www.reddit.com/user/cussbot

username: cussbot
password: SeBzxr*we%&xBHQcf%8NfBmjzg6vYwhS

client_id: nrE5x4yJ_LUo9Q
client_secret: m8ItmlnLRlJ6GVVS1KD5tWsvhsQ
"""

import praw

# Reddit API Login
reddit = praw.Reddit(client_id = 'nrE5x4yJ_LUo9Q',
                     client_secret = 'm8ItmlnLRlJ6GVVS1KD5tWsvhsQ',
                     username = 'cussbot',
                     password = 'SeBzxr*we%&xBHQcf%8NfBmjzg6vYwhS',
                     user_agent = 'cussbot by /u/th1nker')

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

