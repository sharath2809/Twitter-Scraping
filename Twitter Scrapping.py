

import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["tweets"]

# Define function to scrape Twitter and store data in MongoDB
def scrape_tweets(keyword, since, until, num_tweets):
    # Create empty list to store tweet dictionaries
    tweet_list = []

    # Iterate through each tweet using snscrape
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword} since:{since} until:{until} lang:en").get_items()):
        if i >= num_tweets:
            break

        # Store tweet data in dictionary
        tweet_dict = {}
        tweet_dict["date"] = tweet.date.strftime("%Y-%m-%d %H:%M:%S")
        tweet_dict["id"] = tweet.id
        tweet_dict["url"] = tweet.url
        tweet_dict["content"] = tweet.content
        tweet_dict["user"] = tweet.username
        tweet_dict["reply_count"] = tweet.replyCount
        tweet_dict["retweet_count"] = tweet.retweetCount
        tweet_dict["language"] = tweet.lang
        tweet_dict["source"] = tweet.sourceLabel
        tweet_dict["like_count"] = tweet.likeCount

        # Append tweet data to list
        tweet_list.append(tweet_dict)

        # Insert tweet data into MongoDB
        result = collection.insert_one(tweet_dict)
        print(f"Inserted tweet with ID {result.inserted_id}.")

    print("Finished inserting tweets into MongoDB.")

    # Create pandas dataframe from list of tweet dictionaries
    df = pd.DataFrame(tweet_list, columns=["date", "id", "url", "content", "user", "reply_count", "retweet_count", "language", "source", "like_count"])

    return df

# Define Streamlit app layout
st.title("Twitter Scraper")
st.write("Enter keyword or hashtag, select date range, and specify number of tweets to scrape.")
keyword = st.text_input("Keyword/Hashtag")
since = st.date_input("Start Date")
until = st.date_input("End Date")
num_tweets = st.slider("Number of Tweets", min_value=10, max_value=1000, value=50)

# Define Streamlit button for scraping tweets
if st.button("Scrape Tweets"):
    if keyword:
        # Scrape tweets and display data in table
        df = scrape_tweets(keyword, since, until, num_tweets)
        st.write(df)

        # Define Streamlit buttons for uploading and downloading data
        if st.button("Upload to MongoDB"):
            for _, row in df.iterrows():
                tweet_dict = dict(row)
                result = collection.insert_one(tweet_dict)
                print(f"Inserted tweet with ID {result.inserted_id}.")
            st.write("Data uploaded to MongoDB.")

        if st.button("Download as CSV"):
            csv = df.to_csv(index=False)
            st.download_button(label="Download CSV", data=csv, file_name="tweets.csv", mime="text/csv")

        if st.button("Download as JSON"):
            json = df.to_json(orient="records")
            st.download_button(label="Download JSON", data=json, file_name="tweets.json", mime="application/json")