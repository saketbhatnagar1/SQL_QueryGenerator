#CREATING STREAMLIT APP

from dotenv import load_dotenv

load_dotenv()#Load enviorments

import streamlit as st
import os
import sqlite3

import google.generativeai as genai

#COnfig the api key::

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Create a function to load google gemini model adn provide query as response::
#NLP->SQL Query::
def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')#CALLING GEMINI PRO MODEL
    response = model.generate_content([prompt[0],question])
    return response.text



#Creating a function to retreive query from sql database:
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows


#Defining the prompt::

prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

#StreamLIT app:
st.set_page_config(page_title="Retrieve any sql query")
st.header("APP TO RETRIVE SQL DATA")

question = st.text_input("Input ",key="Input")

submit = st.button("the Question's Answer:")



if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    data = read_sql_query(response,"student.db")
    st.subheader("Query is  :")
    for row in data:
        print(row)
        st.header(row)

        
