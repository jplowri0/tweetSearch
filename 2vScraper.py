import tweepy
from keys import *
import requests
import pandas as pd
import re 


#REF https://www.kirenz.com/post/2021-12-10-twitter-api-v2-tweepy-and-pandas-in-python/twitter-api-v2-tweepy-and-pandas-in-python/
# To do 
# Pagination
# ideas below: 
# https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9

#Authorisation to the twitter api 
client = tweepy.Client( bearer_token=bearer_token, 
                        consumer_key=consumer_key, 
                        consumer_secret=consumer_secret, 
                        access_token=access_token, 
                        access_token_secret=access_token_secret, 
                        return_type = requests.Response,
                        wait_on_rate_limit=True)


print("Twitter search results:")
print("This will search the past 7 days of Tweets")
# Replace with time period of your choice
start_time = '2022-04-14T00:00:00Z'
# Replace with time period of your choice
end_time = '2022-04-18T23:59:59Z'
#REF https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9

#Looping through the keyword csv
#REF https://stackoverflow.com/questions/5733419/how-to-iterate-over-the-file-in-python

#import the csv for the query. 
list_df = pd.read_csv("searchTerms.csv")

col1 = list_df["col1"]
col2 = list_df["col2"]
#print(col1(index=false))

#converting the columns in dataframe to a list. 
#REF https://stackoverflow.com/questions/22341271/get-list-from-pandas-dataframe-column-or-row
list1 = list_df['col1'].tolist()
list2 = list_df['col2'].tolist()


#Extacting a particular element from the list. 
#iterating through the list. 
#REF https://www.adamsmith.haus/python/answers/how-to-count-the-number-of-iterations-in-a-for-loop-in-python
for iteration, j in enumerate(list2):
    
    element2 = j

    if " " in element2:
        
        element2formatted = "\""+element2+"\""
    
    else:
        element2formatted = element2

  
    element1 = list1[iteration]
    query = element1+" "+element2formatted
    #print(query)
    
    # scrape twitter s
    #Uncomment the start time / end time if a specific time range is required. 
    tweets = client.search_recent_tweets(query=query, 
                                        tweet_fields=['author_id', 'created_at'],
                                        user_fields = ["name", "username", "location", "verified", "description"],
                                        #start_time=start_time,
                                        #end_time=end_time,
                                        max_results=10)


    # Save data as dictionary
    tweets_dict = tweets.json() 


    #try statement to handle the traceback error 
    #REF https://stackoverflow.com/questions/30834172/print-error-to-screen-but-continue-code-execution

    try:           
        # Extract "data" value from dictionary
        tweets_data = tweets_dict['data'] 
        
        # Transform to pandas Dataframe
        df = pd.json_normalize(tweets_data) 

        # save df
        #filename should be query plus date. 
        df.to_csv("scrapes/"+query+"_tweets.csv")
        print("[+] Hits for "+query+" recorded ")

        #the following if else statements are formatting the search query words for a URL. 
        if " " in element2:
            element2spaceFixed = element2.replace(" ", "%20")
            element2spaceFixed = element2spaceFixed.replace("\"", "")
        else:
            element2spaceFixed = element2

        if " " in element1:
            element1spaceFixed = element1.replace(" ", "%20")
            element1spaceFixed = element1spaceFixed.replace("\"", "")
        else:
            element1spaceFixed = element1

        print("link: https://twitter.com/search?q="+element1spaceFixed+"%20"+element2spaceFixed+"&src=typed_query&f=live")
        print("---------------------------------------------------------------")

    except Exception as exc: 
        nothing = 1+1 #running this line so as to not print anything during an exception. The code breaks if I leave nothing here. 
        print("[ ] Nothing for: "+query)
        print("---------------------------------------------------------------")

        #WANT TO REGEX THE LAST WORD IN THE QUERY. EXTRACT IT. 


