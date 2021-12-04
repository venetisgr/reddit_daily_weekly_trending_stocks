import praw
from data import *
import time
import pandas as pd
import matplotlib.pyplot as plt
import squarify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import emoji    # removes emojis
import re   # removes links
import en_core_web_sm
import string
from datetime import datetime
import json
import numpy as np
import nltk
nltk.downloader.download('vader_lexicon')
nltk.downloader.download('wordnet')
import time

reddit = praw.Reddit(user_agent="dva_project",
                         client_id="RgcFSOeVO0D-wlwsCCU5tg",
                         client_secret="TuoLrWmihYoAYSPaShN2K4HpcRewtA",
                         username="dva_test",
                         password="team_NOT_cool_2021")

#####get daily and weekly trends
def data_extractor_daily_and_week(reddit,no_posts):
    '''extracts daily and weekly mentioned tickers
    Parameter: reddt: reddit obj
               no_posts: number of posts that will be searched #200 and 500 are ok
    Return:   check the return section for more information
    
    '''


    ##################################
    #Initialization
    subs = ['wallstreetbets',"stocks","stock_picks","spacs","pennystocks","finance","financialindependence","options","investing","forex","stockmarket","Shortsqueeze" ]     # sub-reddit to search

    
    # post will be considered if it satisfies the following requirements
    #upvotes = [0,0.3,0.5,0.7]
    #ups = [0,20,200,500]
    upvotes = [0]
    ups = [0]
    
    ################################### 
    #Return Items
    from collections import defaultdict
    
    #weekly
    titles = {} #a dict that contains all the titles for the given subreddit and filtering combination
    #titles = {"wsb":{(0,0):[],(0,20):[]}} #key1 subreddit #key2 filtering combination, value a list that contains the titles
    #tiles[sub]=defaultdict(list)
    
    tickers = defaultdict(lambda: defaultdict(int)) #remove two # to use it
    # a dict that contains all the ticks, for the given post filtering combinations, the value is the no appearances
    #ticks = {(0,0):{"TSLA":#count, "APPL":#count }, (0,20):{"TSLA":#count, "APPL":#count }}
    #key1 filtering combination #key2 stock , value is the #count of the tick
    
    tick_comments = defaultdict(lambda: defaultdict(list))
    #similar structure as the tickers but the value is the actual comments that correspond to that tick
    tick_dates = defaultdict(lambda: defaultdict(list))
    #similar strucutre as the tickers but the value is the date the comment was made
    
    
    #daily
    titles_d = {} #a dict that contains all the titles for the given subreddit and filtering combination
    #titles = {"wsb":{(0,0):[],(0,20):[]}} #key1 subreddit #key2 filtering combination, value a list that contains the titles
    #tiles[sub]=defaultdict(list)
    
    tickers_d = defaultdict(lambda: defaultdict(int)) #remove two # to use it
    # a dict that contains all the ticks, for the given post filtering combinations, the value is the no appearances
    #ticks = {(0,0):{"TSLA":#count, "APPL":#count }, (0,20):{"TSLA":#count, "APPL":#count }}
    #key1 filtering combination #key2 stock , value is the #count of the tick
    
    tick_comments_d = defaultdict(lambda: defaultdict(list))
    #similar structure as the tickers but the value is the actual comments that correspond to that tick
    tick_dates_d = defaultdict(lambda: defaultdict(list))
    #similar strucutre as the tickers but the value is the date the comment was made
    
    
    
    
    ###########################################################################
    for sub in subs:
        start = time.time() #time it took for on subreddit comment extraction
        print(sub)
        
        #### subreddit selection
        subreddit = reddit.subreddit(sub) #select the subreddit
        #titles[sub]=defaultdict(list)
        
        
        ###### itterate through the posts

        hot_posts = subreddit.hot( limit=no_posts)
        for post in hot_posts:
            try:
                flair = post.link_flair_text #flair tags, they explain
                author = post.author.name   #post author
                post_text = post.selftext   #actual post (text)
                
            except:
                pass
            #post info has issue skip
            #i can use continue to bypass the for itteration
              
            
            
            post.comment_sort = 'hot'   #keep the most "hot" comments
            comments = post.comments #comments of that post
            
            #get more comments
            try:
                post.comments.replace_more(limit=5)   #might not be possible to replace that many
            except:
                try:
                    post.comments.replace_more(limit=3)   #might not be possible to replace that many
                except:
                    try:
                        post.comments.replace_more(limit=1)   #might not be possible to replace that many
                    except:
                        pass
            
             
            
            #itterate through various filtering methods
            #upvotes = [0,0.3,0.50.7]
            #ups = [0,20,200,500]
                
            for upv in upvotes:
                for up in ups:
                    #keep posts that satisfy the min requirements bellow
                    if post.upvote_ratio >= upv and post.ups > up: 
                                                                              
                        #comment extraction 
                        
                        for comment in comments:
                            
                            try: #deleted comment, skip
                                auth = comment.author.name #if deleted this would give an error
                            except:
                                continue #skip comment if it is deleted
                                
                            time_creation = (time.time()- comment.created_utc)/60/60/24
                            
                            #weekly and daily after middle of function
                            if float(time_creation)<=7 : 
                                split = comment.body.split(" ") #split comment to words
                                for word in split:
                                    word = word.replace("$", "") 

                                    #stocks tickers are capitals and less or equal than 5 letters
                                    #we also check if the tick is inside the stock lists "us"
                                    if word.isupper() and len(word) <= 5 and word not in blacklist and word in us:

                                        tickers[(upv,up)][word] = tickers[(upv,up)][word] + 1 #no appearances for the given tick

                                        #further filter by date #could be done in the dataframe?
                                        tick_comments[(upv,up)][word].append(comment.body) 
                                        #comment related to that tick
                                        tick_dates[(upv,up)][word].append(datetime.fromtimestamp(comment.created_utc))
                                        #date the comment was posted
                                        
                                        #daily  
                                        if float(time_creation)<=1:
                                            
                                            tickers_d[(upv,up)][word] = tickers_d[(upv,up)][word] + 1 #no appearances for the given tick

                                            #further filter by date #could be done in the dataframe?
                                            tick_comments_d[(upv,up)][word].append(comment.body) 
                                            #comment related to that tick
                                            tick_dates_d[(upv,up)][word].append(datetime.fromtimestamp(comment.created_utc))
                                            #date the comment was posted
                                        
                            
                                        
                                        

        end = time.time()
        print("time",(end - start)/60)
        
        
                
    return tick_comments, tick_dates, tickers, tickers_d, tick_comments_d, tick_dates_d            


def find_top_n_stocks(stock_count,n,min_no_com):
    '''
    Input: 
    stock_count: dictionary that has the name of the stock as key and the number of appearances for that stock is the key
    n: number of stock with the highest count that will be selected
    min_no_com: minimum number of comments/mentions needed in order to include that stock #20 for daily #100 weekly 
    
    Output 
    ret: a list that contains the n most mentioned stocks
    '''
    sorted_dict = dict(sorted(stock_count.items(), key=lambda item: item[1], reverse=True))
    ret = []
    for stck in sorted_dict.keys():
        if sorted_dict[stck]>=min_no_com:
            ret.append(stck)
    return ret[:n]


def df_top_trenders(daily_ticks,weekly_ticks,save):
    #save: represents whether u want the df to be saved as a csv too (True or False)
    #returns a dataframe that contains the daily and weekly trenders
    d = {"daily_trenders":daily_ticks,"weekly_trenders":weekly_ticks}
    df = pd.DataFrame(d)
    if save==True:
        df.to_csv("daily_weekly_trending_stocks.csv", index=False)        
    return df
        
def execute1():    
    
    tick_comments, tick_dates, tickers, tickers_d, tick_comments_d, tick_dates_d  = data_extractor_daily_and_week(reddit,500)

    daily_ticks = find_top_n_stocks(tickers_d[(0,0)],15,20)
    print(f"Daily ticks: {daily_ticks}")
    weekly_ticks = find_top_n_stocks(tickers[(0,0)],15,50)
    print(f"Weekly ticks: {weekly_ticks}")

    df_top_trenders(daily_ticks,weekly_ticks,True)