#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np

import streamlit as st
from streamlit_chat import message
import streamlit.components.v1 as components

from IPython.display import display, HTML
from ansi2html import Ansi2HTMLConverter
conv = Ansi2HTMLConverter()



st.header("🎈Chat with B2B Survey Data")

with st.sidebar:
    st.header(":green[New Features in Version 5.0!!!]")
    st.markdown("* :green[New UI design for easier use.]")
    st.markdown("* :green[Added capability to search internet if content out of scope of provided dataset.]")
    st.markdown("* :green[Added parsing errors handling to decrease question failure rate.]")
    st.markdown("* :green[Continue enhance reply accuray.]")
    st.markdown("")
    st.subheader("Features in version 4.0")
    st.markdown("* Enhanced data retrieval module to get better accuracy and passing rate.")
    st.markdown("* Added capability to ask data structure question.")
    st.markdown("* Added capability to reply with some simple style charts.")
    st.markdown("")
    st.markdown("For example, you can ask:")
    st.markdown(":blue[_I want to specifically analyze data from EMEA's SMB segment._]")
    st.markdown(":blue[_What customer mainly complain about when their NPS score lower than 5._]")
    st.markdown(":blue[_What's the data structure looks like?_]")
    st.markdown(":blue[_Draw a bar chart to show segments, and their count_]")
    st.markdown("")
    st.markdown("----")
    st.markdown("The current memory windows is set to 3, so recent 3 conversation will be impact on the content generation, but not earlier than that")
    st.markdown("")
    st.markdown("Click 'clear conversation' whenever you feel like to get a fresh start")


def draw_pic(response): 
    if not response:
        return
    response_dict = eval(response)

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("items", inplace=True)
        st.bar_chart(df)  

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("items", inplace=True)
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)
            
# initiate session state variables
if "docs" not in st.session_state:
    st.session_state["docs"] = []
if "messages" not in st.session_state:
    st.session_state.messages = []
app = Chatwithdataset()
with open("data/thoughts.log", "r+") as f:
    f.truncate(0)

clear_button = st.button("Clear Conversation", key="clear")
if clear_button:
    st.session_state.messages = []
    st.session_state['docs'] = []
    app = Chatwithdataset()
    with open("data/thoughts.log", "w") as f:
        f.truncate(0)
    memory = init_memory()


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = app.run(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)
        draw_pic(app.res_graph)
    
    st.session_state.messages.append({"role": "assistant", "content": response})


    if st.session_state['docs']:
        docs_df = pd.DataFrame([doc.metadata for doc in st.session_state["docs"]]) 
        del docs_df['source'], docs_df['row']
    else:
        docs_df = pd.DataFrame()
    st.markdown(f"Citation Data (Size = {len(docs_df)})")
    st.dataframe(docs_df, height=250)
    st.session_state['docs'] = []