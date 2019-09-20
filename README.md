# CussBot

Cussbot looks on Reddit for comments with swear words in them. It analyzes the comment
and additional comments made by the user for swearing statistics and saves this information 
to a database. This information is anonymous as per below. 

# Anonymous Data

The only information stored permanently are the username to prevent duplicate analysis, 
and the resulting statistics. Comments are not stored as this would be redundant.

## Procedure

1. Bot scans Subreddits which are specified earlier during the day. 
2. Finds comments with swear words. 
3. Analyzes comment statistics for use in later optional steps.
4. Analyzes user's comment history. **See Analysis for more information**
5. Replies to the user with any outstanding statistics.

Optional step 1. **Needs expansion:** Bot calculates which comment has the highest percentage of swearwords and the largest number
of swearwords. 

Optional Step 2. Bot replies to this comment declaring it the daily winner.

## Comment Analysis

Cussbot scans the user's comment history 

The bot scans for:

- Number of words
- Number of swear words
- Swear word diversity
- Swear words used (stores only one instance per comment as this will be used to 
calculate the most used swear words in order.)
- Subreddit the comment was found
- Any additional relevant data **Needs expansion.**

## Usage

The bot will only evaluate users once, unless specifically invoked by the user to 
re-evaluate them at a later date. The bot will also list instructions below in case
of error. The user can reply to the bot which will read the comment to see if any
error has been made. 

## Contributing

At this time, contributions are not being accepted since this project is intended 
to improve my abilities with both Git and Python. 