import streamlit as st
import google.generativeai as genai


genai_API_KEY = st.secrets["genai_API"]

genai.configure(api_key=genai_API_KEY)
model = genai.GenerativeModel(model_name='gemini-pro')

def generate_analysis(prb_desc, feat_desc, targ_desc):
    prompt = f"""
    You are an expert business data analyst. You have been tasked to analyze data from the following context (details enclosed in tripple backticks):
    ```
    {prb_desc}
    ```
    For the above problem context, the 'target variable' so defined is described below (enclosed in single backticks): 
    `
    {targ_desc}
    `
    To analyze the above data, the following features are available to us (enclosed in double backticks):
    ``
    {feat_desc}
    ``

    For each feature, investigate:
    1. Can this feature be discarded, looking at the context? Does this feature look necessary? Why?
    2. What kinds of descriptive analysis, or exploratory data analysis may be useful to identify data in patterns or trends?
    3. If we want to do bivariate or multivariate analysis, specifically which other features should be studied along with this one? What kind of analysis can be done? Name each pair, and mention a list of techniques that can be done for bivariate analysis for each pair.


    Investigate which kinds of Descriptive or Exploratory Data Analysis Processes can be used to find insights on this data with respect to each feature. Also define a proper roadmap for this analysis.
    Answer step by step.
    """
    completion = model.generate_content(
        prompt,
        generation_config={
            'temperature': 0.4,
            'max_output_tokens': 2000
        }
    )

    return completion.text

@st.cache_data
def retr_ans(problem_description, feature_description, target_variable_description):
    return f"Data Summary:\n {generate_analysis(problem_description, feature_description, target_variable_description)}"

st.header("Online Analyst")

# Input for problem description
problem_description = st.text_area("Describe the problem you're trying to solve, do provide as much context (within humane limits) as possible.", placeholder="Also write the problem context, and why you are trying to solve that particular problem.")
# Input for features and their descriptions
feature_description = st.text_area("Describe the feature variables:", placeholder="Format:\nFeature1_name: Feature1 Description,\nFeature2_name: Feature2 Description\n(See: Help)", help="If possible, do include data regarding the types of variables (categorical or numerical), their spread, etc.")
# Input for target variable description
target_variable_description = st.text_area("Describe the target variable:")


if st.button('Say hello', help="Explain the details and click this button."):
    answer = retr_ans(problem_description, feature_description, target_variable_description)
    st.session_state['output'] = answer
    st.write(st.session_state.output)
    #st.write(answer)

