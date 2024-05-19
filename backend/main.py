# from typing import List

# from fastapi import FastAPI
# from sentence_transformers import SentenceTransformer
# import numpy as np

# app = FastAPI()

# import scraper

# # model = SentenceTransformer(
# #     "sentence-transformers/all-mpnet-base-v2"
# # )  # this one is shit

# # model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2") # this one is better

# model = SentenceTransformer("Alibaba-NLP/gte-large-en-v1.5", trust_remote_code=True)


# def get_related(project_link, team_members):
#     """
#     returns all projects done by the team members of this project
#     """

#     links = []

#     for member in team_members:
#         links.extend(scraper.get_hacker_projects(member))

#     links = set(links)
#     links.remove(project_link)
#     return list(links)


# def compare(src, targets):
#     embeddings = model.encode([src, *targets])

#     a = embeddings[0]
#     b = embeddings[1:]

#     cos_sim = np.dot(a, b.T) / (np.linalg.norm(a) * np.linalg.norm(b))

#     return cos_sim.tolist()


# @app.get("/analyze")
# def analyze(devpost_url: str):
#     # Step 1:
#     # Fetch the data from the devpost_url

#     project_links = scraper.get_project_gallery(devpost_url)

#     # Step 2:
#     # Fetch the data from the project links

#     details = {}

#     for project in project_links:

#         # if we have proj

#         project_details = scraper.get_project_details(project)
#         details[project] = project_details

#         links_to_fetch = get_related(project, project_details["team_members"])

#         content_to_compare: List[str] = []
#         for link in links_to_fetch:
#             fetched = scraper.get_project_details(link)

#             to_compare = fetched["description"] + fetched["full_description"]
#             if "How we built it" in to_compare:
#                 idx = to_compare.find("How we built it")
#                 to_compare = to_compare[:idx]
#             content_to_compare.append(to_compare)

#         # run comparison check

#         source_description = (
#             project_details["description"] + project_details["full_description"]
#         )
#         if "How we built it" in source_description:
#             idx = source_description.find("How we built it")
#             source_description = source_description[:idx]

#         e = compare(
#             source_description,
#             content_to_compare,
#         )
#         print(project_details, content_to_compare)
#         print(e)
#         exit(1)

#     # For each team member, gather details on all their previous projects

#     # RETURN ANALYSIS?
#     return details
