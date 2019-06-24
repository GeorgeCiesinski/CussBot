# CussBot

CussBot is a Reddit bot project I have created to search through Reddit comments for various swear words. Upon finding such a comment, the bot will check if the user has been evaluated before, and will reply to their comment to let them know what percentage of their words are swear words, and how they compare to the average.

## Procedure

Upon finding a swear word, the user's comment history is evaluated to determine what percentage of all of their words used are swear words. Once this is done, the bot stores the username and the percentage of their words which are swear words in the database. 

The bot then replies to the comment with the number of swear words in their comment, the swear word they used, and how they compare to the Reddit average. 

## Usage

The bot will only evaluate users once, unless specifically invoked to re-evaluate them at a later date. 

## Contributing

At this time, contributions are not being accepted since this project is intended to improve my abilities with both Git and Python.