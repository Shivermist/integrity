# scraper.py
# basic functions to scrabe devpost data
from bs4 import BeautifulSoup
import requests

baseURL = "https://deltahacks-x.devpost.com/"

# checking first page
desiredStartPage = "project-gallery"
page = requests.get(baseURL + desiredStartPage)
curPage = page
projects = []
soup = BeautifulSoup(page.content, "html.parser")
projects += soup.find_all(
    "a", class_=["block-wrapper", "link.fade", "link-to-software"]
)
curPage = soup.find("a", rel=["next"])

# checking subsequent pages

while curPage != None:
    page = requests.get(baseURL + curPage["href"])
    soup = BeautifulSoup(page.content, "html.parser")
    projects += soup.find_all(
        "a", class_=["block-wrapper", "link.fade", "link-to-software"]
    )
    curPage = soup.find("a", rel=["next"])

# getting all project links

projectLinks = []
for link in projects:
    projectLinks.append(link["href"])
print(projectLinks)
print(len(projectLinks))
allTeams = []

# go through each project found
for link in projectLinks:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    # get project title
    title = soup.find(id="app-title")
    print(title.text)

    # get project description
    description = soup.find("p", class_="large")
    print(description.text)

    # get all project description
    fullInformation = soup.find(id="app-details-left")
    # ul tags is class=cp-tag
    if fullInformation is not None:
        innerDivs = fullInformation.find_all("div")

        for div in innerDivs[1:]:
            print(div.text)

    # get github url (if it exists)
    softwareURLS = fullInformation.find(
        "ul", attrs={"data-role": True}, class_="no-bullet"
    )
    # find URLS containing github
    if softwareURLS is not None:
        for url in softwareURLS.find_all("a"):
            if "https://github.com" in url["href"]:
                github = url["href"]
        print(github)

    # get all team members
    teamMembers = soup.find_all("li", class_="software-team-member")
    members = []
    for member in teamMembers:
        memberLink = member.find("a", class_="user-profile-link")
        if memberLink is not None:
            members.append(memberLink["href"])
    print(members)

    # add to all teams list
    allTeams.append(members)

print(allTeams)
# go through all of their projects and do checks


# # teams
# hackerURL = "https://devpost.com/kennyzhao-code"

def getProjectsFromHacker(hackerURL):
    # checking first page
    # desiredStartPage = "project-gallery"
    page = requests.get(hackerURL)
    # curPage = page
    # projects = []
    soup = BeautifulSoup(page.content, "html.parser")
    projects = soup.find_all(
        "a", class_=["block-wrapper-link", "fade", "link-to-software"]
    )
    # curPage = soup.find("a", rel=["next"])

    # prints the projects in a list
    projectLinks = []
    for link in projects:
        projectLinks.append(link["href"])
    print(projectLinks)
    print(len(projectLinks))
    # allTeams = []

    projectRepos = []

    for link in projectLinks:
        page = requests.get(link)
        soup = BeautifulSoup(page.content, "html.parser")

        # # get project title
        # title = soup.find(id="app-title")
        # print(title.text)

        # # get project description
        # description = soup.find("p", class_="large")
        # print(description.text)

        # get all project description
        fullInformation = soup.find(id="app-details-left")
        # ul tags is class=cp-tag
        # if fullInformation is not None:
        #     innerDivs = fullInformation.find_all("div")

            # for div in innerDivs[1:]:
            #     print(div.text)

        # get github url (if it exists)
        softwareURLS = fullInformation.find(
            "ul", attrs={"data-role": True}, class_="no-bullet"
        )
        # find URLS containing github
        if softwareURLS is not None:
            for url in softwareURLS.find_all("a"):
                if "https://github.com" in url["href"]:
                    github = url["href"]
                    projectRepos.append(github)

        
    print(projectRepos)

for team in allTeams:
    print(team)
    for member in team:
        print(member)
        getProjectsFromHacker(member)
