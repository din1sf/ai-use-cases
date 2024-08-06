import pandas as pd
import streamlit as st
from openai import OpenAI

# make sure OPENAI_API_KEY is set as environment variable
client = OpenAI()

st.title('Usecase 1')
uploaded_file = st.file_uploader("Choose a XLS file",type="xlsx")
if uploaded_file is not None:
    # load uploaded XLS file into a dataframe (only the first sheet)
    testcases_df = pd.read_excel(uploaded_file,sheet_name="Test_Case_Upload_Template_CPT")

    st.write(testcases_df)

    # copy few columns from the dataframe
    df = pd.DataFrame()
    df['Folder'] = testcases_df['Folder'].fillna(method='ffill')
    df['Test Package'] = testcases_df['Test Package'].fillna(method='ffill')
    df['Test Case Name *'] = testcases_df['Test Case Name *'].fillna(method='ffill')
    df['Test Case Description'] = testcases_df['Test Case Description'].fillna(method='ffill')

    # drop duplicates rows to reduce the size of the dataframe
    df = df.drop_duplicates()

    # generate csv string from dataframe
    csv = df.to_csv(index=False)
    print(csv)

    # system message for the model
    system_message = """
    You are a helpful assistant. You are able to identify the folder, test package, test case name and test case description based on a given criteria.
    As a input you will have a csv table with columns: Folder, Test Package, Test Case Name and Test Case Description.
    Your taks is based on the given criteria to identify the all Test Package data and output it in json format.
    Input will be provided in the following format:

    CVS data:
    {csv}

    Criteria:
    {criteria}
    """

    user_prompt = st.text_area('Prompt', value='Write a prompt here', height=200)

    # generate user message for the model - combine csv string and user prompt
    user_message = """
    CSV data:\n
    {csv}

    Criteria:\n
    {criteria}
    """.format(csv=csv, criteria=user_prompt)

    if st.button('Generate', key='generate_prompt'):
        with st.expander('Generate prompt'):
            st.text_area('Generated System Message', value=system_message, height=200)
            st.text_area('Generated Prompt Message', value=user_message, height=200)

        with st.spinner('Processing...'):
            # call the model with the generated messages
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"{system_message}",
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": f"{user_message}"},
                        ],
                    }
                ],
            )

            # get the result from the model
            result = response.choices[0].message.content
            print(result)
            st.info(result)