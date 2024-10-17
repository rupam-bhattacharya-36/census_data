import pandas as pd
import func
from pymongo import MongoClient
from bson.objectid import ObjectId
import mysql.connector,credentials,re
from io import StringIO


df = pd.read_excel("Census_2011.xlsx",sheet_name='census_2011 csv')
df.rename(columns={'State name': 'State/UT', 'District name': 'District','Male_Literate':'Literate_Male','Female_Literate':'Literate_Female','Rural_Households':'Households_Rural','Urban_Households':'Households_Urban','Age_Group_0_29':'Young_and_Adult','Age_Group_30_49':'Middle_Aged','Age_Group_50':'Senior_Citizen','Age not stated':'Age_Not_Stated'},inplace=True)
df['State/UT']=df['State/UT'].map(func.modify_statename).fillna(df['State/UT'])
df2 = pd.read_excel("Census_2011.xlsx",sheet_name="Telengana",header=None)
my_dict={key:"Telengana" for key in df2.iloc[:,0].values}
df['State/UT']=df['District'].map(my_dict).fillna(df['State/UT'])
nan_counts = df.isna().sum().to_frame(name='NaN Count').T
print(nan_counts.loc[:, 'Main_Workers':'Non_Workers'])
func.fill_missing_population(df)
nan_counts = df.isna().sum().to_frame(name='NaN Count').T
print(nan_counts.loc[:,'Main_Workers':'Non_Workers'])
func.fill_missing_age(df)
func.fill_missing_literates(df)
func.fill_missing_household(df)

mongo=credentials.mongo_cred
client=MongoClient(mongo["url"])
db=client[mongo["db"]]
documents=db[mongo["collection"]]
#collection.delete_many({})
# collection.insert_many(df.to_dict('records'))

# Find one document where no field has a null value
query = {"$and": [{field: {"$ne": None}} for field in documents.find_one().keys()]}
document = documents.find_one(query)
client.close()
def mapdict(string):
    string = re.sub(r"[/\- ]+|_{2,}", "_", string)
    if len(string)>50:
        return ''.join(word[0].upper() for word in string.split('_'))
    else:
        return string

mappedkeys={key:mapdict(key) for key in document.keys()}
table_str=StringIO()
table_str.write("object_id BINARY(12) PRIMARY KEY")
for k,v in mappedkeys.items():
    if isinstance(document[k],ObjectId):
        continue
    elif isinstance(document[k],int):
        sql_type="INT"
    elif isinstance(document[k],float):
        sql_type="FLOAT"
    elif isinstance(document[k],str):
        sql_type="VARCHAR(200)"
    else:
        sql_type="TEXT"
    table_str.write(f",{v} {sql_type}")
sql=f"CREATE TABLE IF NOT EXISTS CENSUS ({table_str.getvalue()})"

table_str.close()

mysqldb=mysql.connector.connect(**credentials.mysql_cred)

cursor=mysqldb.cursor()

cursor.execute(sql)

mysqldb.commit()

def insertype(element):
    if isinstance(element,ObjectId):
        return element.binary
    else:
        return element

insert_query=StringIO()
for d in documents:
    for v in d.values():
        insert_query.write(f"")
sql_query=f"INSERT INTO CENSUS VALUES({insert_query})"


cursor.close()
mysqldb.close()