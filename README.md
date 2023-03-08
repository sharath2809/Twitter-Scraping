# Twitter-Scraping
Scraping twitter data using Python- snscrape and building streamlit web app where we can upload tweets into Mongodb database and download scraped tweets in CSV and Json formats
Basic workflow to be performed :
import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
# Connect to MongoDB
# Define function to scrape Twitter and store data in MongoDB
# Create empty list to store tweet dictionaries
# Iterate through each tweet using snscrape
# Store tweet data in dictionary
# Append tweet data to list
# Insert tweet data into MongoDB
# Create pandas dataframe from list of tweet dictionaries
# Define Streamlit app layout
# Define Streamlit button for scraping tweets
# Scrape tweets and display data in table
# Define Streamlit buttons for uploading and downloading data
In command prompt -streamlit run "file directory location in local folder\filename.py"
You should be able to run stream lit
