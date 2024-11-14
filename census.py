import pandas as pd
import func
from pymongo import MongoClient
import mysql.connector,credentials,re


df = pd.read_excel("Census_2011.xlsx",sheet_name='census_2011 csv')
df.rename(columns={'State name': 'State_UT', 'District name': 'District','Male_Literate':'Literate_Male','Female_Literate':'Literate_Female','Rural_Households':'Households_Rural','Urban_Households':'Households_Urban','Age_Group_0_29':'Young_and_Adult','Age_Group_30_49':'Middle_Aged','Age_Group_50':'Senior_Citizen','Age not stated':'Age_Not_Stated'},inplace=True)
df['State_UT']=df['State_UT'].map(func.modify_statename).fillna(df['State_UT'])
df2 = pd.read_excel("Census_2011.xlsx",sheet_name="Telengana",header=None)
my_dict={key:"Telengana" for key in df2.iloc[:,0].values}
df['State_UT']=df['District'].map(my_dict).fillna(df['State_UT'])

# data cleaning and transformation
func.fill_missing_population(df)

# dictionary of original column names and refined names removing whitespace and extra _
mapped_cols={col:re.sub(r'(_+\s+|\s+_+|\s+|_+)',r'_',col).strip('_') for col in df.columns}
df.rename(columns=mapped_cols,inplace=True)

# dictionary of the column names whose length>50 where key:columnname value:shorthand form
mapped_cols={col:''.join(word[0].lower() for word in col.split('_')) for col in df.columns if len(col)>50}


# connecting with mongodb to upload dataframe
mongo=credentials.mongo_cred
client_server_connection=MongoClient(mongo["url"])
db=client_server_connection[mongo["db"]]
collection_documents=db[mongo["collection"]]
collection_documents.delete_many({})
collection_documents.insert_many(df.to_dict(orient='records'))


# connecting with mysql database
mysqldb=mysql.connector.connect(**credentials.mysql_cred)
mysqlcursor=mysqldb.cursor()

# this part is for creating a new table in the database which requires names of column with datatype
# mysql_columns is a generator object iterable where each iteration yields "column_name datatype"
mysql_columns=func.mysqlcolumns(df,mapped_cols)
mysqlcursor.execute(f"create table if not exists censustable (object_id BINARY(12) PRIMARY KEY,{','.join(i for i in mysql_columns)})")
mysqldb.commit()

# # inserting data from mongodb to mysql
collection_records=collection_documents.find()
for doc in collection_records:
    id=doc.pop('_id').binary
    query=f"insert into censustable values(%s,{','.join('%s' for i in range(len(doc)))})"
    mysqlcursor.execute(query,[id]+[doc[key] for key in doc])
    mysqldb.commit()

client_server_connection.close()




mysqlcursor.close()
mysqldb.close()
