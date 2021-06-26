import requests
from bs4 import BeautifulSoup
import re



def get_minute_links(soup):
  minute_links = soup.find_all('a', class_="btn-meeting-minutes")
  return ["https:%s" % link['href'] for link in minute_links]

#Given a search term and a text, return true if the term with word boundaries
#at the both ends exists within the text.
def find_string(search_string, text):
    return bool(re.search(r"\b" + re.escape(search_string) + r"\b", text))


# Check the minutes of each meeting for presence of a search term
# If found, print out the meeting information, the term found, and
# a url to the meeting page.
def search_meetings(minutes):
    matches = []
    for link in minutes:
        request = requests.get(link)
        soup = BeautifulSoup(request.content, 'lxml')
        content = soup.find(id='publicationContent')
        issue = soup.find("h2")


        for term in searchterms:
            if(find_string(term, content.text)):
                if(issue is not None):
                    matches.append([issue.text, term, link])
                else:
                    matches.append(["Not Available", term, link])
    return(matches)

def main():
    search_parl_sessions = [[43, 1], [42, 1], [41, 2], [41, 1]]
    # Get the index page
    for parl, session in search_parl_sessions:
        url = "https://www.parl.ca/Committees/en/REGS/Meetings?parl=" + str(parl) + "&session=" + str(session)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')
        meeting_matches = []

        #Get the Minutes pages
        minutes = get_minute_links(soup)

        #Find meetings wiith minutes that contain the search term
        meeting_matches = search_meetings(minutes)

        #Print out details for matches
        for match in meeting_matches:
            print("Parliament:", parl, "Session:", session, " - ",match[0], "[", match[1], "]", match[2])


if __name__ == "__main__":
    # Read in the search terms from file, one search term per line.
    with open('searchterms.txt') as f:
        searchterms = f.read().splitlines()
    main()
