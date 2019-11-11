# CussBot

Cussbot looks on Reddit for comments with swear words in them. It stores subreddit
and user statistics for later analysis. See Comment Analysis section for further 
details.

# Data collection

Complete comments are not stored as this would take up a large amount of data in the
database. This bot stores the comment id to prevent duplication, and statistical data
about the comment body. 

# Purpose

The purpose of this bot is frankly to improve my Python knowledge. I learned how to 
write Python, but I wanted to do a solo project to learn the entire process of creating 
a project from scratch. I don't intend to sell the data. The end result will be the 
analysis of different subreddits on reddit for their swearword usage. Once I have 
sufficiently analyzed enough subreddits, I will be plotting the data and will publish 
it to Reddit. 

# Known flaws

There are tons of known flaws. I have only used SQL in a professional environment during
my coop term many years ago, and am consequently relearning it from scratch. The SQL in
this project is rife with issues that probably open it to SQL injection attacks as well as
unintentional SQL injection from regular usage. I plan to tackle this later on as the bot
becomes more functional. There are probably many other flaws I haven't found yet in the
program, but I'm using the experience I gain from this project to make better projects
which are less vulnerable in the future.

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

## Database

CussBot uses the SQLite3 database. The cussbot.db database file is stored in the Sqlite3
folder. If it doesn't exist, Database.py creates it during the first startup.

### ++ Tables ++

#### Words (3 tables)

##### cussword

Purpose: Stores unique cusswords.

| id (Primary Key)| word  |
| --------------- | ----- |
| 1               | shit  |
| 2               | arse  |
| 3               | fuck  |

##### property

Purpose: Stores properties for the words in cussword.

| word_id | property_name | property_value |
| ------- | ------------- | -------------- |
| 2       | derogatory    | false          |
| 2       | dialect       | british        |

##### derivative

Purpose: Stores derivatives of words in cussword.

| word_id | child_word   |
| ------- | ------------ |
| 3       | fucker       |
| 3       | motherfucker | 

#### Reddit Comment Data

##### comment

Purpose: Stores comment "reddit data".

| id (Primary Key) | comment_id | user_name | Subreddit |
|------------------|------------|-----------|-----------|
| 1                | example    |example    |example    |
| 2                | example    |example    |example    |

##### word_count

Purpose: Stores unique cusswords used in comment, and each word's count.
Note: word_id is the id from cussword.

| id         | word_id    | count     |
|------------|------------|-----------|
| 1          | example    |example    |
| 2          | example    |example    |

##### percentage

Purpose: Stores the count of cusswords, normal words, and the ratio of the two.

| id         | cuss_amount | user_name | Subreddit |
|------------|-------------|-----------|-----------|
| 1          | example    |example    |example    |
| 2          | example    |example    |example    |



##### subreddit

| id               | 

# Contributing

At this time, contributions are not being accepted since this project is intended 
to improve my abilities with both Git and Python. 


# Special Thanks

This project is dedicated to my grandma who passed away at the age of 92 while I was
building this. 