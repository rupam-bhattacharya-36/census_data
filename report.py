import streamlit as st
import mysql.connector,credentials
import pandas as pd

db=mysql.connector.connect(**credentials.mysql_cred)
cursor=db.cursor()

cursor.execute(f"select district,population from censustable")

# Fetch the results
data = cursor.fetchall()
# Create a Pandas DataFrame
df = pd.DataFrame(data, columns=["District", "Population"])

# Display the data in Streamlit with a scrollbar
st.title("Census Data")
st.header("Population by State/UT")

# Use st.dataframe to display the DataFrame with a scrollbar
st.dataframe(df, height=400,width=400)

# How many literate males and females are there in each district?
cursor.execute(f"select district,Literate_Male,Literate_Female from censustable")
data2=cursor.fetchall()
df2=pd.DataFrame(data2,columns=["District","Literate_Male","Literate_Female"])
st.header("Literate Male/Female Population")
st.dataframe(df2,height=400,width=400)

query3=f'''select
case
  WHEN Workers is null or Male_Workers is null THEN NULL
  else ROUND(Male_Workers/Workers*100,2)
END as `Male_Workers(%)`,
case
  WHEN Workers is null or Female_Workers is null THEN NULL
  else ROUND(Female_Workers/Workers*100,2)
END as `Female_Workers(%)`
from censustable
'''
cursor.execute(query3)
data3=cursor.fetchall()
df3=pd.DataFrame(data3,columns=['Male_Worker(%)','Female_Worker(%)'])
st.header("% Male_Workers/Female_Workers")
st.dataframe(df3,height=400,width=400)

db.close()