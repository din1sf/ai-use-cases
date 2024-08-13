import pandas as pd
import streamlit as st
import re
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate


st.subheader('Data Source:')
st.write('The data source is a XLS file containin testcases information')

uploaded_file = st.file_uploader("Choose a XLS file",type="xlsx")
if uploaded_file is not None:
    # load uploaded XLS file into a dataframe (only the first sheet)
    testcases_df = pd.read_excel(uploaded_file,sheet_name="Test_Case_Upload_Template_CPT")

    st.subheader('Step 1: ')
    # copy few columns from the dataframe
    df = pd.DataFrame()
    df['Folder'] = testcases_df['Folder'].ffill()
    df['Test Package'] = testcases_df['Test Package'].ffill()
    df['Test Case Name *'] = testcases_df['Test Case Name *'].ffill()
    df['Test Case Description'] = testcases_df['Test Case Description'].ffill()

    # drop duplicates rows to reduce the size of the dataframe
    df = df.drop_duplicates()

    st.write(df)

    csv = df.to_csv(index=False)

    if st.button('Step1', key='generate_prompt'):
        with st.spinner('Processing...'):
            # Define the criteria
            criteria = "Put-away into high racks for the Warehouse/Plant 3551"

            # Create a prompt template
            template = """
            You are a helpful assistant. You are able to identify the folder, test package, test case name and test case description based on a given criteria.
            As a input you will have a csv table with columns: Folder, Test Package, Test Case Name and Test Case Description.
            Your taks is based on the given criteria to identify the all Test Package data and output it in json format.
            Please list only tescase names wich match the criteria or user query.
            If output is not found, you should output a empty json array.
            Input will be provided in the following format:

            CVS data:
            {csv}

            Criteria:
            {criteria}
            """

            st.text_area('Prompt', value=template, height=200)


            # Initialize the Ollama Llama 3.1 model
            llm = Ollama(model="llama3.1")


            prompt_template = PromptTemplate.from_template(template)
            message = prompt_template.format(csv=csv, criteria=criteria)

            print(message)

            result = llm.invoke(message)

            # Print the result
            st.write(result)