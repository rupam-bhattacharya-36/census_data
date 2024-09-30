import pandas as pd
import func
from pymongo import MongoClient
from bson.objectid import ObjectId
import mysql.connector,credentials

df = pd.read_excel("Census_2011.xlsx",sheet_name='census_2011 csv')
df.rename(columns={'State name': 'State/UT', 'District name': 'District','Male_Literate':'Literate_Male','Female_Literate':'Literate_Female','Rural_Households':'Households_Rural','Urban_Households':'Households_Urban','Age_Group_0_29':'Young_and_Adult','Age_Group_30_49':'Middle_Aged','Age_Group_50':'Senior_Citizen','Age not stated':'Age_Not_Stated'},inplace=True)
df['State/UT']=df['State/UT'].map(func.modify_statename).fillna(df['State/UT'])
df2 = pd.read_excel("Census_2011.xlsx",sheet_name="Telengana",header=None)
my_dict={key:"Telengana" for key in df2.iloc[:,0].values}
df['State/UT']=df['District'].map(my_dict).fillna(df['State/UT'])
func.fill_missing_population(df)
func.fill_missing_age(df)
func.fill_missing_literates(df)
func.fill_missing_household(df)

print(df.columns.values)
mongo=credentials.mongo_cred
client=MongoClient(mongo["url"])
db=client[mongo["db"]]
collection=db[mongo["collection"]]
data_dict=df.to_dict('records')
#collection.delete_many({})
collection.insert_many(data_dict)
document=collection.find_one()
client.close()
schema_columns = list(document.keys())

sql=credentials.mysql_cred
mysqldb = mysql.connector.connect(**sql)
cursor=mysqldb.cursor()
cursor.execute("create table Rupamtable( id INT PRIMARY KEY,name VARCHAR(100),salary INT)")
cursor.execute("use table Rupamtable")
cursor.execute("insert into Rupamtable values((1,'Rupam',3000),(2,'Sayan',20000))")
mysqldb.close()