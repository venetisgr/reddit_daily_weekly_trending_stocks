# Daily and Weekly top trending Stocks based on Reddit comments


## Description

The goal of this program is to provide the ability to the users to find the top trending daily and weekly stocks in reddit. In order to achieve this various subreddits are "examined". There are various "filtering" methods implemented in the code in order for the user to keep the "result" he wants and can also add his own. Also the user can chooce to keep the top N(user input) daily and weekly stocks. These top stocks are saved in a useful dataframe format in order for the user to leverage them in other applications. Lastly all the comments and dates associated with the daily and weekly trending stocks can be saved in a csv in order to be further used by other programs.

## Getting Started
###API Key
It is necessary in order to use this program to request API keys from reddit in order to use their API

### Dependencies
The following libraries are needed:

* praw
* time
* pandas 
* matplotlib
* squarify
* nltk
* emoji
* en_core_web_sm
* datetime 
* json
* numpy 
* time

## Help

Though not so much an issue, but based on how "strict" filtering is there might be not enough comments in order to find the actual weekly and daily trending stocks

## Acknowledgments

* [Inspired by his work and the data.py was his creation](https://github.com/asad70/reddit-sentiment-analysis)

