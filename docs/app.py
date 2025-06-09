import streamlit as st
import streamlit_survey as ss
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Streamlit Survey App ---

# 1. Set up the page and a single survey object
st.set_page_config(
    page_title="Streamlit-Survey & EDA Demo",
    page_icon="📊",
)
survey = ss.StreamlitSurvey("Unified Survey")

# --- APP LAYOUT ---

st.title("Streamlit-Survey & EDA Demo")

st.header("Part 1: Streamlit-Survey")
st.write("""
**Streamlit-Survey** is a Python package for incorporating surveys and structured feedback into [Streamlit](https://streamlit.io) apps.
This section demonstrates a unified survey form.
""")

# 2. Use st.form to group all inputs and have a single submit button
with st.form("unified_survey_form"):
    st.write("### User Background")

    # This question uses conditional logic to show/hide the next questions
    used_before = survey.radio(
        "Have you used Streamlit before?",
        options=["Yes", "No", "Not sure"],
        id="used_st_before",
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

    # 3. Add the form submit button
    submitted = st.form_submit_button("Submit Survey")

# 4. Show the results after the form is submitted
if submitted:
    st.success("Your responses have been recorded. Thank you!")
    st.write("### Survey Results:")
    st.json(survey.to_json())

st.write("---")

# --- Exploratory Data Analysis (EDA) ---

st.header("Part 2: Exploratory Data Analysis of Wellbeing")
st.write("This section performs an EDA on a wellbeing dataset.")

# --- 1. Load the Data ---
# IMPORTANT: This path is now relative.
# Create a folder named 'data' in your repository and place the CSV there.
csv_path = "data/wellbeing_surveys.csv"

try:
    df = pd.read_csv(csv_path)
    st.success("Dataset loaded successfully.")

    # --- 2. Initial Data Inspection (Displayed in an expander) ---
    with st.expander("Initial Data Inspection"):
        st.write("First 5 rows of the dataset:")
        st.dataframe(df.head())

        st.write("Dataset Information:")
        # To display info(), we capture its output
        import io

        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        st.write("Descriptive Statistics:")
        st.dataframe(df.describe())

        st.write("Checking for missing values:")
        st.dataframe(df.isnull().sum())

    # --- 3. Data Cleaning & Preparation ---
    df.columns = [col.lower() for col in df.columns]

    # --- 4. Univariate Analysis (Exploring Single Variables) ---
    st.subheader("Univariate Analysis")

    # Distribution of the target variable: Work/Life Balance Score
    st.write("#### Distribution of Work-Life Balance Score")
    fig1, ax1 = plt.subplots()
    sns.histplot(df['work_life_balance_score'], kde=True, bins=30, ax=ax1)
    ax1.set_title('Distribution of Work-Life Balance Score')
    st.pyplot(fig1)

    # How stressed are people on a daily basis?
    st.write("#### Distribution of Daily Stress Levels (0-5)")
    fig2, ax2 = plt.subplots()
    sns.countplot(x='daily_stress', data=df, ax=ax2)
    ax2.set_title('Distribution of Daily Stress Levels (0-5)')
    st.pyplot(fig2)

    # What about the age distribution?
    st.write("#### Age Distribution of Respondents")
    fig3, ax3 = plt.subplots()
    sns.countplot(
        x='age',
        data=df,
        order=['Less than 20', '21 to 35', '36 to 50', '51 or more'],
        ax=ax3
    )
    ax3.set_title('Age Distribution of Respondents')
    st.pyplot(fig3)

    # --- 5. Bivariate & Multivariate Analysis (Exploring Relationships) ---
    st.subheader("Bivariate & Multivariate Analysis")

    # Correlation heatmap
    st.write("#### Correlation Matrix of Numeric Variables")
    fig4, ax4 = plt.subplots(figsize=(14, 10))
    numeric_cols = df.select_dtypes(include=np.number)
    correlation_matrix = numeric_cols.corr()
    sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', ax=ax4)
    ax4.set_title('Correlation Matrix of Lifestyle and Wellbeing Variables')
    st.pyplot(fig4)

    # How does time for passion relate to the overall work-life balance score?
    st.write("#### Work-Life Balance Score vs. Time for Passion")
    fig5, ax5 = plt.subplots()
    sns.scatterplot(x='time_for_passion', y='work_life_balance_score', data=df, alpha=0.5, hue='gender', ax=ax5)
    ax5.set_title('Work-Life Balance Score vs. Time for Passion')
    st.pyplot(fig5)

    # How do sleep habits affect stress levels by age and gender?
    st.write("#### Daily Stress vs. Sleep Hours, Segmented by Age and Gender")
    g = sns.catplot(
        x='sleep_hours',
        y='daily_stress',
        hue='gender',
        col='age',
        data=df,
        kind='box',
        col_wrap=2,
        height=4,
        aspect=1.2,
        col_order=['Less than 20', '21 to 35', '36 to 50', '51 or more']
    )
    g.fig.suptitle('Daily Stress vs. Sleep Hours, by Age and Gender', y=1.03)
    st.pyplot(g)

    # --- EDA Summary ---
    with st.expander("Click to see EDA Summary"):
        st.write("""
        1.  **Work-Life Balance Score**: The distribution appears somewhat normal but might be slightly skewed. This is our primary metric for 'wellbeing'.
        2.  **Stress & Sleep**: There is a visible negative trend between sleep hours and stress levels. Generally, respondents who sleep more report lower levels of daily stress.
        3.  **Passion & Balance**: Spending more time on personal passions shows a positive correlation with a higher work-life balance score.
        4.  **Social Connections**: There's a positive trend indicating that individuals with a larger social network tend to report a higher number of personal achievements.
        5.  **Correlations**: The heatmap revealed several interesting correlations. For example, 'achievement' and 'supporting_others' have a positive correlation.
        """)


except FileNotFoundError:
    st.error(f"File not found at `{csv_path}`. Please make sure the file is in a `data` folder in your repository.")
except Exception as e:
    st.error(f"An error occurred during the EDA: {e}")
