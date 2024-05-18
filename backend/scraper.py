# scraper.py
# basic functions to scrabe devpost data


from bs4 import BeautifulSoup
import requests

baseURL = "https://deltahacks-x.devpost.com/"
projectGal = baseURL + "project-gallery"

page = requests.get(projectGal)

# print(page.text)

soup = BeautifulSoup(page.content, "html.parser")

# go to id = submission-gallery

# mainContainer = soup.find(id="container")
# find main section
# mainSection = mainContainer.find(id="main")
# innerSection = mainContainer.find("section", class_=["large-9", "pull-3", "columns"])
# innerSection2 = mainContainer.find("section", {"role": "main"})
submissionGallery = soup.find(id="submission-gallery")

# projs = soup.find_all("a", {"class": "block-wrapper-link fade link-to-software"})
projects = soup.find_all("a", class_=["block-wrapper", "link.fade", "link-to-software"])

# print(submissionGallery.prettify())
projectLinks = []

for link in projects:
    print(link["href"])
    projectLinks.append(link["href"])

# find all pages
# check if next page clickable
nextPage = submissionGallery.find("a", rel=["next"])

while nextPage is not None:
    nextPage = baseURL + nextPage["href"]
    print(nextPage)
    # load next page
    page = requests.get(nextPage)
    soup = BeautifulSoup(page.content, "html.parser")
    submissionGallery = soup.find(id="submission-gallery")
    # find all project links
    projects = soup.find_all(
        "a", class_=["block-wrapper", "link.fade", "link-to-software"]
    )
    for link in projects:
        # print(link["href"])
        projectLinks.append(link["href"])
    nextPage = submissionGallery.find("a", rel=["next"])

print(projectLinks)
print(len(projectLinks))
