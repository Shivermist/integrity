# scraper.py
# basic functions to scrabe devpost data


from bs4 import BeautifulSoup
import requests

baseURL = "https://deltahacks-x.devpost.com/"
projectGal = baseURL + "project-gallery"


def get_project_gallery(base_url):
    """Fetches links to all projects from the project gallery.

    Args:
        base_url: The base URL of the website.

    Returns:
        A list of strings containing URLs to all projects on the website.
    """

    project_links = []
    desired_start_page = "project-gallery"
    page = requests.get(base_url + desired_start_page)
    current_page = page

    while current_page is not None:
        soup = BeautifulSoup(page.content, "html.parser")

        # Extract project links from current page
        projects = soup.find_all(
            "a", class_=["block-wrapper", "link.fade", "link-to-software"]
        )
        for project in projects:
            project_links.append(project["href"])

        # Find the link to the next page (if it exists)
        current_page = soup.find("a", rel=["next"])

        # Fetch the next page
        if current_page:
            page = requests.get(base_url + current_page["href"])

    return project_links


def get_project_details(link):
    """
    This function scrapes project details from a given website.

    Args:
        link (str): The URL of the project webpage.

    Returns:
        dict: A dictionary containing the extracted project details. Keys include:
            title (str): Project title
            description (str): Project description (short)
            full_description (str): Full project description (might include multiple sections)
            github_url (str): URL to the project's Github repository (if found)
            team_members (list): List of URLs to team members' profiles (if found)
    """

    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    project_details = {}

    # Get title
    title = soup.find(id="app-title")
    if title:
        project_details["title"] = title.text.strip()

    # Get short description
    description = soup.find("p", class_="large")
    if description:
        project_details["description"] = description.text.strip()

    # Get full description (might include multiple sections)
    fullInformation = soup.find(id="app-details-left")
    if fullInformation:
        innerDivs = fullInformation.find_all("div")
        full_description = ""
        for div in innerDivs:
            full_description += div.get_text(" ").strip() + "\n"
        project_details["full_description"] = full_description

    # Get Github URL
    softwareURLS = fullInformation.find(
        "ul", attrs={"data-role": True}, class_="no-bullet"
    )
    if softwareURLS:
        for url in softwareURLS.find_all("a"):
            if "https://github.com" in url["href"]:
                project_details["github_url"] = url["href"]
                break  # Stop after finding the first Github URL

    # Get team members
    teamMembers = soup.find_all("li", class_="software-team-member")
    members = []
    for member in teamMembers:
        memberLink = member.find("a", class_="user-profile-link")
        if memberLink:
            members.append(memberLink["href"])
    project_details["team_members"] = members

    return project_details


def get_hacker_projects(hacker_link):
    """
    Scrapes and returns a list of projects a hacker has worked on.

    Args:
        hacker_link (str): The URL of the hacker's profile page.

    Returns:
        list: A list of links to projects the hacker has worked on.
    """

    # TODO: Implement this function
