# Python program to scrape website 
# and save quotes from website
import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.linkedin.com/in/aryash-shrivastava-487b3020a/"
try:
    r = requests.get(URL)
    r.raise_for_status()  # Raise an error for bad responses
except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

soup = BeautifulSoup(r.content, 'html.parser')  # Use the built-in HTML parser

quotes = []  # a list to store quotes

table = soup.find('div', attrs={'class': 'ph5'})
# Check if the table is found
print(table)