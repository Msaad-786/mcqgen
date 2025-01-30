import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
import streamlit as st

logging.info("Streamlit App Started")

with open("response.json",'r') as file:
    response_json = json.loads(file)

st.title("MCQ's creater application with Langchains 🐦")

with st.form("user_input"):
    uploaded_file = st.file_uploader("Choose a file (pdf or t)")

    mcq_count = st.number_input("Enter the number of MCQ's to generate", min_value=3, max_value=50)

    subject = st.text_input("Enter the subject of the MCQ's", max_chars=20)

    tone = st.text_input("Enter the tone of the MCQ's", max_chars=20, placeholder="Simple")

    button = st.form_submit_button("Generate MCQ's")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(response_json)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error generating MCQ's")
            
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")
                if isinstance(response, dict):
                    quiz = response.get("quiz",None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in data table")

                else:
                    st.write(response)
            
