from dataclasses import dataclass
import re
import streamlit as st

import scraper

from model import fs

compare = fs()
compare.load("optimized_cot.json")

from functools import cache


@cache
def compare_projects(project_1, project_2):
    return compare(project_1=project_1, project_2=project_2).answer.lower() == "yes"


def get_related(project_link, team_members):
    """
    returns all projects done by the team members of this project
    """

    links = []

    for member in team_members:
        links.extend(scraper.get_hacker_projects(member))

    links = set(links)
    links.remove(project_link)
    return list(links)


st.image("./integrity_logo.svg")
st.write("### Find suspicious projects on your hackathon!")


form = st.form(key="url form")
url = form.text_input("Devpost URL:")
form.form_submit_button("Analyze")

st.divider()

regex = r".*.devpost\.com/$"
if url and not (re.match(regex, url)):
    st.error("Invalid URL, please enter a valid Devpost URL")

elif url:
    with st.spinner("Getting Hackathon Details..."):
        project_links, header = scraper.get_project_gallery(url)

    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    st.image(header)
    st.write("## Projects")

    for i, link in enumerate(project_links[:5]):
        with st.spinner(f"Fetching project {link}..."):
            project_details = scraper.get_project_details(link)

        st.write(f"### [{project_details['title']}]({link})")
        st.write(project_details["description"])

        my_bar.progress((i + 1) / len(project_links))

        show_all_good = True
        if "github_url" in project_details.keys():
            with st.spinner("Checking GitHub..."):
                github_url = project_details["github_url"]

                num_commits, num_contributors, first_commit, last_commit = (
                    scraper.get_github_details(github_url)
                )

                if num_commits < 4:
                    st.error(
                        f"Less than 4 commits in the repository ({num_commits} commits)",
                        icon="🚨",
                    )
                    show_all_good = False

                if num_contributors > 4:
                    st.error(
                        f"More than 4 contributors in the repository ({num_contributors} contributors)",
                        icon="🚨",
                    )
                    show_all_good = False

                if (last_commit - first_commit).seconds > 129600:  # 36 hours
                    st.error(
                        f"Some commits are more than 36 hours apart. Be sure to check this isn't an existing project.",
                        icon="🚨",
                    )
                    show_all_good = False

        if False:
            with st.spinner("Comparing to related projects..."):
                links_to_fetch = get_related(link, project_details["team_members"])

                compare_bar = st.progress(0, text="Comparing projects...")
                compare_bar_total = len(links_to_fetch)

                content_to_compare = []
                for i, link in enumerate(links_to_fetch):
                    fetched = scraper.get_project_details(link)

                    to_compare = fetched["description"] + fetched["full_description"]
                    if "How we built it" in to_compare:
                        idx = to_compare.find("How we built it")
                        to_compare = to_compare[:idx]
                    content_to_compare.append(to_compare)

                    compare_bar_total = len(links_to_fetch) + len(content_to_compare)

                    compare_bar.progress((i + 1) / compare_bar_total)

                source_description = (
                    project_details["description"] + project_details["full_description"]
                )
                if "How we built it" in source_description:
                    idx = source_description.find("How we built it")
                    source_description = source_description[:idx]

                issues = False
                for i, content in enumerate(content_to_compare):
                    res = compare_projects(source_description, content)

                    if res:
                        if not issues:
                            st.error("Similar Previous Project Detected", icon="🚨")
                        issues = True
                        show_all_good = False

                        st.write(f"Similar to previous project [{links_to_fetch[i]}]")

                    compare_bar.progress(min(1.0, 0.5 + (i + 1) / compare_bar_total))

                compare_bar.empty()

        if show_all_good:
            st.success("No issues detected", icon="✅")
