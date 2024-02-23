import streamlit as st
import pandas as pd
import numpy as np
import requests
import json

st.set_page_config(page_title="AI Support NLP", page_icon="🧊", layout="wide", initial_sidebar_state="expanded")

# Define a function to process the input
def process_input(input_data):

    output = {
        "message": "Inference output from Sagemaker endpoint has been generated successfully.",
        "status_code": "200",
        "prediction": "{\"result\": [{\"score\": [0.8907358646392822], \"Request details\": \"Request Box integration\", \"task\": \"TASK3913534\"}, {\"score\": [0.8584097027778625], \"Request details\": \"Box Integration for 1000-700\", \"task\": \"TASK3963163\"}, {\"score\": [0.8571497201919556], \"Request details\": \"Enable Box Integration 734-4243\", \"task\": \"TASK3329964\"}, {\"score\": [0.8514263033866882], \"Request details\": \"Support in coordinating data connections (see spreadsheet attached)\", \"task\": \"TASK4647484\"}, {\"score\": [0.8499947190284729], \"Request details\": \"TEST SUPPORT\", \"task\": \"TASK4653588\"}, {\"score\": [0.8482497334480286], \"Request details\": \"CMR Workspace for this environment\", \"task\": \"TASK4334342\"}, {\"score\": [0.8454003930091858], \"Request details\": \"NOVELTY data access through AI Bench\", \"task\": \"TASK3690497\"}, {\"score\": [0.8452848792076111], \"Request details\": \"Studio setup in the ppt environment.\", \"task\": \"TASK3867694\"}, {\"score\": [0.8442512154579163], \"Request details\": \"configuration of a ZPA segment for using RStudio\", \"task\": \"TASK4570570\"}, {\"score\": [0.8438296914100647], \"Request details\": \"Request for stack upgrade.\", \"task\": \"TASK4390248\"}]}"
    }
    return output

# Define a function to handle row clicks
def show_details(task_id):
    # Store the clicked task_id in the session state
    st.session_state['selected_task_id'] = task_id
    

# Create a Streamlit app
def main():

    
    st.title('AI Support - SNOW NLP')  # Add a title

    # Initialize session state
    if 'selected_task_id' not in st.session_state:
        st.session_state['selected_task_id'] = None
    if 'df_predictions' not in st.session_state:
        st.session_state['df_predictions'] = pd.DataFrame(columns=['Score', 'Description', 'Task ID'])
    

    # Create two columns for the layout
    col1, col2 = st.columns([1, 1])

    # Display the DataFrame in the first column
    with col1:
        input_data = st.text_area("Enter the description", height=100)  # Create a text area for user input

        # Add a button to trigger the computation
        if st.button('Submit'):
            # Use the input in a function and get the result
            output_data = process_input(input_data)

            # Display the result
            #st.write('Output:', output_data)

            # Extract the prediction value
            prediction = output_data['prediction']

            # Parse the JSON string into a Python object
            prediction_data = json.loads(prediction)

            # Extract the 'result' list, which contains the predictions
            result = prediction_data['result']

            # Convert results into a pandas DataFrame
            df_predictions= pd.DataFrame(result)
            # Rename the column headings
            df_predictions.columns = ['Score','Description', 'Task ID']
            
            # If 'score' is a list with a single item, we can convert it to a simple float for better display in the table
            df_predictions['Score'] = df_predictions['Score'].apply(lambda x: x[0])

            # Store the DataFrame in the session state
            st.session_state['df_predictions'] = df_predictions

        #st.write("Output Table:")
        # Use a button for each Task ID to make it clickable
        for index, row in st.session_state['df_predictions'].iterrows():
            if st.button(f"{row['Task ID']} : {row['Description']}"):
                show_details(row['Task ID'])

                # Optionally, add a button to clear the selection
        #if st.button('Clear Selection'):
            #st.session_state['selected_task_id'] = None

                    

    # Display the respective score in the second column
    with col2:
        if st.session_state.selected_task_id:
            # Get the score for the clicked task ID
            selected_row = st.session_state['df_predictions'][st.session_state['df_predictions']['Task ID'] == st.session_state.selected_task_id]
            #selected_row_df = pd.DataFrame(selected_row)
            selected_row_tb = selected_row.transpose()
            html_t = selected_row_tb.to_html(header=False)
            st.write(html_t, unsafe_allow_html=True)
            #transposed_row_str = selected_row_tb.astype(str)

            #st.table(selected_row_tb.astype(str))
            #if not selected_row.empty:
            #    score = selected_row.iloc[0]['Score']
            #    st.write(f"Details for Task ID: {st.session_state.selected_task_id}")
            #    st.write(f"Confidence Score: {score}")
            #    st.write(selected_row.iloc[0]['Description'])






    # Apply custom CSS styling within Streamlit using st.markdown
    st.markdown("""
    <style>
    table.dataframe {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1rem;
    }
    table.dataframe th {
        border: 1px solid #dddddd;
        padding: 8px;
        text-align: center; /* Center-align text in th and td */
    }
    table.dataframe td {
        border: 1px solid #dddddd;
        padding: 8px;
        text-align: center; /* Left-align text in th and td */
    }
    table.dataframe th {
        background-color: #055296;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display the HTML in Streamlit
    #st.write(html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()

