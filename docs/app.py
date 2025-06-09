import streamlit as st
import streamlit_survey as ss

# 1. Set up the page and a single survey object
st.set_page_config(
    page_title="Streamlit-Survey Single-Page Demo",
    page_icon="🧘",
)
survey = ss.StreamlitSurvey("Unified Survey")

# --- APP LAYOUT ---

"""
# Streamlit-Survey Demo

**Streamlit-Survey** is a Python package for incorporating surveys and structured feedback into [Streamlit](https://streamlit.io) apps.

## Installation

Streamlit-Survey can be installed from PyPI:
```
pip install streamlit-survey
```


## Unified Survey Example
This form combines elements from across the original multi-page demo into a single, cohesive survey.
"""

# 2. Use st.form to group all inputs and have a single submit button
with st.form("unified_survey_form"):
    st.write("### User Background")

    # This question uses conditional logic to show/hide the next questions
    used_before = survey.radio(
        "Have you used Streamlit before?",
        options=["Yes", "No", "Not sure"],
        id="used_st_before",  # Use a unique ID for each question
        horizontal=True
    )

    if used_before == "Yes":
        survey.select_slider(
            "How often do you use Streamlit?",
            options=["Daily", "Weekly", "Monthly", "Rarely"],
            id="st_frequency",
        )
    elif used_before == "No":
        used_other = survey.radio(
            "Have you used other dashboarding tools?",
            options=["Yes", "No"],
            id="used_other_tools",
            horizontal=True
        )
        if used_other == "Yes":
            survey.multiselect(
                "Which other tools have you used?",
                options=["Dash", "Voila", "Panel", "Bokeh", "Plotly", "Other"],
                id="other_tools_list",
            )

    st.write("---")
    st.write("### General Feedback")

    # Example components from the 'Survey Components' page
    survey.text_area(
        "What are your general comments or feedback?",
        id="general_feedback"
    )

    survey.radio(
        "How would you rate this demo?",
        options=["😞", "🙁", "😐", "🙂", "😀"],
        id="demo_rating",
        horizontal=True
    )

    st.write("---")
    st.write("### Additional Component Examples")

    # Components added from 1_🗃️_Survey_Components.py
    survey.selectbox("Which option do you prefer? (Select Box)", options=["Option 1", "Option 2", "Option 3"], id="selectbox_demo")
    survey.checkbox("I acknowledge the terms and conditions (Checkbox)", id="checkbox_demo")
    survey.dateinput("Please select a date (Date Input)", id="date_input_demo")
    survey.timeinput("Please select a time (Time Input)", id="time_input_demo")
    survey.text_input("Enter a short text (Text Input)", id="text_input_demo")
    survey.number_input("Enter a number between 0 and 100 (Number Input)", min_value=0, max_value=100, value=50, id="number_input_demo")
    survey.slider("Select a value on the slider", min_value=0, max_value=100, value=50, id="slider_demo")


    # 3. Add the form submit button
    submitted = st.form_submit_button("Submit Survey")

# 4. Show the results after the form is submitted
if submitted:
    st.success("Your responses have been recorded. Thank you!")
    st.write("### Survey Results:")

    # Use survey.to_json() to get the collected data
    st.json(survey.to_json())

"""
---
## Features

Survey components are similar to Streamlit inputs, but they have additional features that make them suitable for surveys:

- Questions and responses are automatically saved.
- Component states and previous responses are automatically restored and displayed based on survey data.
- Survey can be saved to and loaded from JSON files.
- Custom survey components can be created for more complex input UI and functionality.
"""
