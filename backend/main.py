from typing import Union

from fastapi import FastAPI

app = FastAPI()

import scraper


@app.get("/analyze")
def analyze(devpost_url: str):
    # Step 1:
    # Fetch the data from the devpost_url

    project_links = scraper.get_project_gallery(devpost_url)

    # Step 2:
    # Fetch the data from the project links

    details = {}

    for project in project_links:

        # if we have proj

        project_details = scraper.get_project_details(project)
        details[project] = project_details

    # RETURN ANALYSIS?
    return details
