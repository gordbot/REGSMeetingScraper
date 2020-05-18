#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup

parliament = "42"
session = "1"

# Read in the search terms from file, one search term per line
with open('searchterms.txt') as f:
    searchterms = f.read().splitlines()

# Get the index page
url = "https://www.parl.ca/Committees/en/REGS/Meetings?parl=" + parliament + "&session=" + session
page = requests.get(url)

soup = BeautifulSoup(page.content, 'lxml')

#notices = []
#evidence = []
minutes = []

# Links to Notice of Meeting
#noticelinks = soup.find_all('a', class_="btn-meeting-notice")
#for a in noticelinks:
#    notices.append("https:" + a['href'])

# Links to Meeting Evidence
#evidencelinks = soup.find_all('a', class_="btn-meeting-evidence")
#for a in evidencelinks:
#    evidence.append("https:" + a['href'])

# Lnks to Meeting Minutes
def getMinuteLinks(soup):
	minutelinks = soup.find_all('a', class_="btn-meeting-minutes")
	for a in minutelinks:
		minutes.append("https:" + a['href'])
	return minutes

# Check the minutes of each meeting for presence of a search term
# If found, print out the meeting information, the term found, and
# a url to the meeting page
def searchMeetings(minutes):
	matches = []
	for link in minutes:
		request = requests.get(link)
		soup = BeautifulSoup(request.content, 'lxml')
		content = soup.find(id='publicationContent')

		issue = soup.find("h2")

		for term in searchterms:
			if term in content.text:
				matches.append([issue.text, term, link])
	return(matches)

def main():
	minutes = getMinuteLinks(soup)
	for match in searchMeetings(minutes):
		print(match)


if __name__ == "__main__":
    main()
