#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import re

searchParlSessions = [[43, 1], [42, 1], [41, 2], [41, 1]]

# Read in the search terms from file, one search term per line.
with open('searchterms.txt') as f:
    searchterms = f.read().splitlines()


# notices = []
# evidence = []
minutes = []

def getMinuteLinks(soup):
    minutelinks = soup.find_all('a', class_="btn-meeting-minutes")
    for a in minutelinks:
        minutes.append("https:" + a['href'])
    return minutes


#Given a search term and a text, return true if the term with word boundaries
#at the both ends exists within the text.
def find_string(searchString, text):
    if re.search(r"\b" + re.escape(searchString) + r"\b", text):
        return True
    return False

# Check the minutes of each meeting for presence of a search term
# If found, print out the meeting information, the term found, and
# a url to the meeting page.


def searchMeetings(minutes):
    matches = []
    for link in minutes:
        request = requests.get(link)
        soup = BeautifulSoup(request.content, 'lxml')
        content = soup.find(id='publicationContent')
        issue = soup.find("h2")

        for term in searchterms:
            if(find_string(term, content.text)):
                matches.append([issue.text, term, link])
    return(matches)

def main():
    # Get the index page
    for parl, session in searchParlSessions:
        url = "https://www.parl.ca/Committees/en/REGS/Meetings?parl=" + str(parl) + "&session=" + str(session)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')

        #Get the Minutes pages
        minutes = getMinuteLinks(soup)
        #Print out details for matches
        for match in searchMeetings(minutes):
            print("Parliament: ", parl, "Session: ", session, " ",match[0], "[", match[1], "]", match[2])


if __name__ == "__main__":
    main()
