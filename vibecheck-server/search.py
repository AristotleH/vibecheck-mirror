import requests
import praw #reddit api wrapper
import tweepy
import string
import nltk
import re
import vars
import sys
import os

from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

blocked = {'RT', '@', 'https','*', '>', '<' , '[', ']','"','%','i','|','way','t','http','post','s','’'} #common things we should filter
#google auth
GOOGLE_API_KEY = vars.GOOGLE_KEY #pls don't query more than 25 times a day thnx
SEARCH = "014749590020630390210:k5gghnyn2pt" #https://cse.google.com/cse/setup/basic?cx=014749590020630390210:k5gghnyn2pt

#twitter auth
consumer_key = vars.TWITTER_CONSUMER_KEY
consumer_secret = vars.TWITTER_SECRET_KEY

access_token = vars.ACCESS_TOKEN
access_token_secret = vars.ACCESS_TOKEN_SECRET




analyser = SentimentIntensityAnalyzer()
num_datum = 0
sentiment_sum = 0


def interpret_compound_score(score):
    if score >= 0.05:
        return "positive"
    if score <= -.05:
        return "negative"
    return "neutral"

def search_google(query):
    reddit_urls = [] #populated by search
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH}&q={query}"
    data = requests.get(url).json()
    results = data['items']
    for result in results:
        if "reddit" in result['link']:
            reddit_urls.append(result['link'])
    return reddit_urls

def word_count(strings): #returns a list of tuples [word,freq] O(n) = nlog(n)
    words = {}
    multiwords = {}
    stops = stopwords.words('english')
    for s in strings:
        s = s.strip(string.punctuation).lower()
        toked = nltk.word_tokenize(s)
        toked = nltk.pos_tag(toked)
        for word in toked:
            if len(word[0]) < 3 or len(word[0]) > 20:
                continue
            if (word[1] == 'NN' or word[1] == 'NNP' or word[1] == 'ADJ') and word[0] not in blocked: #noun, adjective
                if word[0] in words:
                    words[word[0]] += 1
                    if words[word[0]] > 5:
                        multiwords[word[0]] = words[word[0]]
                else:
                    words[word[0]] = 1

    return multiwords
def parse_subreddit(r,reddit_comments,post,hot_flag=True): #query hot instead of top

    lim = 5 #how many posts to return
    match = re.search('\/r\/(.*?)\/', post) #only name of subreddit
    subr = match.group(1)
    sub = r.subreddit(subr).top('week',limit=3)
    #sub = r.subreddit(subr).hot(limit=lim) if hot_flag else r.subreddit(subr).top(limit=lim)
    for post in sub:
        if len(reddit_comments) >= 1000: 
                break
        reddit_comments.append(post.selftext)
        post.comment_sort = 'best'
        comments = post.comments
        for comment in comments:
                if isinstance(comment,praw.models.MoreComments):
                        break
                        #comments = comment.comments()
                else:
                    reddit_comments.append(comment.body)


def search_reddit(posts):
    reddit_comments = [] #populated by search_reddit
    r = praw.Reddit(client_id=vars.REDDIT_CLIENT_ID, client_secret=vars.REDDIT_CLIENT_SECRET, user_agent="vibecheck" )
    if posts: #nonempty
        for post in posts:
            if len(reddit_comments) >= 1000: 
                break
            try:
                postP = r.submission(url=post)
            except:
                try:
                   parse_subreddit(r,reddit_comments,post)
                except:
                   continue
                continue
            postP.comment_sort = 'best'
            reddit_comments.append(postP.selftext)
            comments = postP.comments
            for comment in comments:
                if isinstance(comment,praw.models.MoreComments):
                        break
                        #comments = comment.comments()
                else:
                    reddit_comments.append(comment.body)
    return reddit_comments


def search_twitter(keyword):

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

  maxTweets = 1000
  tweetsPerQuery = 100
  tweetCount = 0

  sinceId = None

  twitter_comments = []

  max_id = -1

  while tweetCount < maxTweets:
      if(max_id <= 0):
          if(not sinceId):
              tweets = api.search(q=keyword, count=tweetsPerQuery)
          else:
              tweets = api.search(q=keyword, count=tweetsPerQuery, since_id=sinceId)
      else:
          if(not sinceId):
              tweets = api.search(q=keyword, count=tweetsPerQuery, max_id=str(max_id - 1))
          else:
              tweets = api.search(q=keyword, count=tweetsPerQuery, max_id=str(max_id - 1), since_id=sinceId)
      if(not tweets):
          break
      for tweet in tweets:
          twitter_comments.append(tweet.text)
          #print(tweet.text + '\n') for testing purposes
      tweetCount += len(tweets)
      max_id = tweets[-1].id

  '''
  public_tweets = api.search(keyword,count=100)

  for tweet in public_tweets:
    tweety = tweet.text
    #print(tweety + '\n') test output
    twitter_comments.append(tweety)
  '''

def analyze_text(texts):
    global num_datum, sentiment_sum
    num_datum += len(texts)
    for text in texts:
        compound_sentiment = analyser.polarity_scores(text).get('compound')
        if compound_sentiment > .5 or compound_sentiment < -.5: 
            compound_sentiment  *= 2
            num_datum += 1
       # print("Tweet: ", text, "\nCompund sentiment: ", compound_sentiment, " - ",
               # interpret_compound_score(compound_sentiment), "\n")
        
        sentiment_sum += compound_sentiment






'''
analyze_text(twitter_comments)
mean_sentiment = sentiment_sum / num_datum
'''
#print("Mean Sentiment:", mean_sentiment, " - ", interpret_compound_score(mean_sentiment))