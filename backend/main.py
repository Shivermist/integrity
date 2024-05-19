from dataclasses import dataclass
import re
import streamlit as st

import scraper


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

        with st.spinner("Comparing to related projects..."):
            links_to_fetch = scraper.get_related(link, project_details["team_members"])

            compare_bar = st.progress(0, text="Comparing projects...")
            content_to_compare = []
            for i, link in enumerate(links_to_fetch):
                fetched = scraper.get_project_details(link)

                to_compare = fetched["description"] + fetched["full_description"]
                if "How we built it" in to_compare:
                    idx = to_compare.find("How we built it")
                    to_compare = to_compare[:idx]
                content_to_compare.append(to_compare)

                compare_bar.progress((i + 1) / len(links_to_fetch) * 2)

            source_description = (
                project_details["description"] + project_details["full_description"]
            )
            if "How we built it" in source_description:
                idx = source_description.find("How we built it")
                source_description = source_description[:idx]

            for i, content in enumerate(content_to_compare):

                comp = scraper.compare(
                    source_description,
                    content,
                )
        # st.write(project_details, content_to_compare)
        # st.write(e)
