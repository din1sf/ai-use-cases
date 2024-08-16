import pandas as pd
import streamlit as st
from openai import OpenAI
import re
import json
import os

os.environ["OPENAI_API_KEY"] = "put-key-here" 
os.environ["OPENAI_BASE_URL"] = "https://ews-emea.api.bosch.com/knowledge/insight-and-analytics/llms/d/v1" 

client = OpenAI(default_headers={"api-key": os.getenv("OPENAI_API_KEY")})
model = "meta-llama/Meta-Llama-3.1-8B-Instruct"  

def step1(testcases_df):
    st.subheader('Step 1: ')
    # copy few columns from the dataframe
    df = pd.DataFrame()
    df['Folder'] = testcases_df['Folder'].ffill()
    df['Test Package'] = testcases_df['Test Package'].ffill()
    df['Test Case Name *'] = testcases_df['Test Case Name *'].ffill()
    df['Test Case Description'] = testcases_df['Test Case Description'].ffill()

    # drop duplicates rows to reduce the size of the dataframe
    df = df.drop_duplicates()

    # generate csv string from dataframe
    csv = df.to_csv(index=False)
    # print(csv)

    # system message for the model
    system_message = """
    You are a helpful assistant. You are able to identify the folder, test package, test case name and test case description based on a given criteria.
    As a input you will have a csv table with columns: Folder, Test Package, Test Case Name and Test Case Description.
    Your taks is based on the given criteria to identify the all Test Package data and output it in json format.
    If output is not found, you should output a empty json array.
    Input will be provided in the following format:

    CVS data:
    {csv}

    Criteria:
    {criteria}
    """

    user_prompt = st.text_area('Prompt', value='Help me with Test data for the Put-away into high racks for the Warehouse/Plant 3551 ', height=200)

    st.write('After the User’s Input, the tool should identify the test package, test case and corresponding test steps from the database (based on the contextual understanding).')
 

    # generate user message for the model - combine csv string and user prompt
    user_message = """
    CSV data:\n
    {csv}

    Criteria:\n
    {criteria}
    """.format(csv=csv, criteria=user_prompt)

    if st.button('Step1', key='generate_prompt'):
        with st.expander('Prompt'):
            st.markdown('### System message')
            st.text_area('Prompt', value=system_message, height=200)
            st.markdown('### User message')
            st.text_area('Prompt', value=user_message, height=200)

        with st.spinner('Processing...'):
            # call the model with the generated messages
            response = client.chat.completions.create(
                model=model,
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

            # result = """
            #     Here is the JSON representation of the identified data:

            #     ```json
            #     {
            #     "Folder": "CT-UD",
            #     "Test Package": "HCDD_IT1_I2D_PRD_02 PTW High rack",
            #     "Test Case Name": "BP_IT_CPT_P2F_CO01_Create Production order manually",
            #     "Test Case Description": "This test case is about creating new production order"
            #     }
            #     ```
            # """     

            print(result)

            # json_content = result
            match = re.search(r'```(\w+)\n(.*?)```', result, re.DOTALL)
            if match:
                json_content = match.group(2)
            else:
                json_content = None
               
                
            with st.expander('Output'):
                st.markdown('### Output from the model:')
                st.info(result)

            # create json from content
            testpackage_df = pd.DataFrame()

            if not json_content:
                st.error('No JSON content found')
                return None, None
            
            found_tc_json = json.loads(json_content)
            # st.write(found_tc_json)
            if not found_tc_json:
                st.error('No test package found')
                return None, None
            
            # is json array or object
            if isinstance(found_tc_json, dict):
                found_tc_json = [found_tc_json]

            for item in found_tc_json:
                tc = item['Test Case Name']
                if (tc):
                    matched_df = testcases_df[testcases_df['Test Case Name *'] == tc]
                    testpackage_df = pd.concat([testpackage_df, matched_df])
                    

            return found_tc_json, testpackage_df
        
    return None, None


st.title('Usecase 1')

st.subheader('Data Source:')
st.write('The data source is a XLS file containin testcases information')

uploaded_file = st.file_uploader("Choose a XLS file",type="xlsx")
if uploaded_file is not None:
    # load uploaded XLS file into a dataframe (only the first sheet)
    testcases_df = pd.read_excel(uploaded_file,sheet_name="Test_Case_Upload_Template_CPT")

    with st.expander('Loaded data'):
        st.write(testcases_df)

    # STEP 1
    matched_json, matched_tc_df = step1(testcases_df)
    st.markdown('### Matched Test cases:')
    st.write(matched_tc_df)

    # STEP2
    if matched_tc_df is not None:
        st.markdown('### Step 2: ')
        st.write('It should read all steps involved and perform the search for test data elements. Eg. Production order')

        # sort by Test Case Name and Step Number
        matched_tc_df = matched_tc_df.sort_values(by=['Test Case Name *', 'Step Number'])
        
        # iterate over the matched test cases and Step Number
        for index, row in matched_tc_df.iterrows():
            with (st.container(border=True)):
                st.write('Test Package: ', row['Test Package'])
                st.write('Name: ', row['Test Case Name *'])
                st.write('Step Number: ', row['Step Number'])
                st.write('Description: ', row['Step Test Instruction'])


        