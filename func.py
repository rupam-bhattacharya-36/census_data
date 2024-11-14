import pandas as pd
def modify_statename(s):
    # convert all state names to title format with 'and' if present in lowercase example Jammu and Kashmir
    return ' '.join(word if word.lower()!='and' else 'and' for word in s.title().split())

def fill_missing_population(df:pd.DataFrame):
    # filling missing population values by male+female where male and female has values
    mask_population = (df['Population'].isna()) & ((df[['Male','Female']].isna().sum(axis=1)==0))
    df.loc[mask_population,'Population']=df.loc[mask_population,'Male'] + df.loc[mask_population,'Female']

    # filling missing population values by age groups where all age groups has values
    mask_age = (df['Population'].isna()) & (df.loc[:,'Young_and_Adult':'Age_Not_Stated'].isna().sum(axis=1)==0)
    df.loc[mask_age,'Population'] = df.loc[mask_age,'Young_and_Adult':'Age_Not_Stated'].sum(axis=1)

    # filling missing population values by workers number as every person falls under 3 category of workers
    mask=(df['Population'].isna()) & (df[['Main_Workers','Marginal_Workers','Non_Workers']].isna().sum(axis=1)==0)
    df.loc[mask,'Population']=df.loc[mask,'Main_Workers':'Non_Workers'].sum(axis=1)

    # filling missing population values by religion data as every person will fall under a certain religion.
    mask=(df['Population'].isna()) & (df.loc[:,'Hindus':'Religion_Not_Stated'].isna().sum(axis=1)==0)
    df.loc[mask,'Population']=df.loc[mask,'Hindus':'Religion_Not_Stated'].sum(axis=1)

    # all population fields are filled, now filling missing male fields
    mask=df['Male'].isna()
    df.loc[mask,'Male']=df.loc[mask,'Population']-df.loc[mask,'Female']

    # filling missing female fields
    mask=df['Female'].isna()
    df.loc[mask,'Female']=df.loc[mask,'Population']-df.loc[mask,'Male']

    # all the fields in population, male, female are filled. now filling rest of the fileds where population can be used

    # filling missing age groups
    # creating a common sum of all agegroups for future use
    agesumdf=df.loc[:,'Young_and_Adult':'Age_Not_Stated'].sum(axis=1)
    # filling Young_and_Adult agegroup
    mask=(df['Young_and_Adult'].isna()) & (df.loc[:,'Middle_Aged':'Age_Not_Stated'].isna().sum(axis=1)==0)
    df.loc[mask,'Young_and_Adult'] = df.loc[mask,'Population'] - agesumdf[mask]
    mask=(df['Middle_Aged'].isna())&(df.loc[:,['Young_and_Adult','Senior_Citizen','Age_Not_Stated']].isna().sum(axis=1)==0)
    df.loc[mask,'Middle_Aged'] = df.loc[mask,'Population'] - agesumdf[mask]
    mask=df['Senior_Citizen'].isna()&df.loc[:,['Young_and_Adult','Middle_Aged','Age_Not_Stated']].isna().sum(axis=1)==0
    df.loc[mask,'Senior_Citizen'] = df.loc[mask,'Population'] - agesumdf[mask]
    mask=(df['Age_Not_Stated'].isna()) & (df.loc[:,'Young_and_Adult':'Senior_Citizen'].isna().sum(axis=1)==0)
    df.loc[mask,'Age_Not_Stated'] = df.loc[mask,'Population'] - agesumdf[mask]

    # fill missing religions
    religiondf=df.loc[:,'Hindus':'Religion_Not_Stated'].sum(axis=1)
    mask=(df['Hindus'].isna()) & (df.loc[:,list(df.loc[:,'Hindus':'Religion_Not_Stated'].drop('Hindus',axis=1).columns)].isna().sum(axis=1)==0)
    df.loc[mask,'Hindus']=df.loc[mask,'Population']-religiondf[mask]
    mask=(df['Muslims'].isna()) & (df.loc[:,list(df.loc[:,'Hindus':'Religion_Not_Stated'].drop('Muslims',axis=1).columns)].isna().sum(axis=1)==0)
    df.loc[mask,'Muslims']=df.loc[mask,'Population']-religiondf[mask]
    mask=(df['Christians'].isna()) & (df.loc[:,list(df.loc[:,'Hindus':'Religion_Not_Stated'].drop('Christians',axis=1).columns)].isna().sum(axis=1)==0)
    df.loc[mask,'Christians']=df.loc[mask,'Population']-religiondf[mask]
    mask=(df['Sikhs'].isna()) & (df.loc[:,list(df.loc[:,'Hindus':'Religion_Not_Stated'].drop('Sikhs',axis=1).columns)].isna().sum(axis=1)==0)
    df.loc[mask,'Sikhs']=df.loc[mask,'Population']-religiondf[mask]
    mask=(df['Buddhists'].isna()) & (df.loc[:,list(df.loc[:,'Hindus':'Religion_Not_Stated'].drop('Buddhists',axis=1).columns)].isna().sum(axis=1)==0)
    df.loc[mask,'Buddhists']=df.loc[mask,'Population']-religiondf[mask]
    mask=(df['Jains'].isna()) & (df.loc[:,list(df.loc[:,'Hindus':'Religion_Not_Stated'].drop('Jains',axis=1).columns)].isna().sum(axis=1)==0)
    df.loc[mask,'Jains']=df.loc[mask,'Population']-religiondf[mask]
    mask=(df['Others_Religions'].isna()) & (df.loc[:,list(df.loc[:,'Hindus':'Religion_Not_Stated'].drop('Others_Religions',axis=1).columns)].isna().sum(axis=1)==0)
    df.loc[mask,'Others_Religions']=df.loc[mask,'Population']-religiondf[mask]
    mask=(df['Religion_Not_Stated'].isna()) & (df.loc[:,list(df.loc[:,'Hindus':'Religion_Not_Stated'].drop('Religion_Not_Stated',axis=1).columns)].isna().sum(axis=1)==0)
    df.loc[mask,'Religion_Not_Stated']=df.loc[mask,'Population']-religiondf[mask]

    # fill missing workers
    mask=(df['Main_Workers'].isna()) & (df[['Marginal_Workers','Non_Workers']].isna().sum(axis=1)==0)
    df.loc[mask,'Main_Workers']=df.loc[mask,'Population']-df.loc[mask,'Marginal_Workers':'Non_Workers'].sum(axis=1)
    mask=(df['Marginal_Workers'].isna()) & (df[['Main_Workers','Non_Workers']].isna().sum(axis=1)==0)
    df.loc[mask,'Marginal_Workers']=df.loc[mask,'Population']-df.loc[mask,['Main_Workers','Non_Workers']].sum(axis=1)
    mask=(df['Non_Workers'].isna()) & (df[['Main_Workers','Marginal_Workers']].isna().sum(axis=1)==0)
    df.loc[mask,'Non_Workers']=df.loc[mask,'Population']-df.loc[mask,['Main_Workers','Marginal_Workers']].sum(axis=1)

    # fill missing male workers female workers
    mask=(df['Workers'].isna()) & (df.loc[:,['Male_Workers','Female_Workers']].isna().sum(axis=1)==0)
    df.loc[mask,'Workers']=df.loc[mask,['Male_Workers','Female_Workers']].sum(axis=1)
    mask=(df['Male_Workers'].isna()) & (df.loc[:,['Workers','Female_Workers']].isna().sum(axis=1)==0)
    df.loc[mask,'Male_Workers']=df.loc[mask,'Workers']-df.loc[mask,'Female_Workers']
    mask=(df['Female_Workers'].isna()) & (df.loc[:,['Workers','Male_Workers']].isna().sum(axis=1)==0)
    df.loc[mask,'Female_Workers']=df.loc[mask,'Workers']-df.loc[mask,'Male_Workers']

    # fill missing literates
    mask= (df['Literate'].isna()) & (df[['Literate_Male','Literate_Female']].isna().sum(axis=1)==0)
    df.loc[mask,'Literate']=df.loc[mask,['Literate_Male','Literate_Female']].sum(axis=1)
    # fill missing male literates
    mask=(df[['Literate','Literate_Female']].isna().sum(axis=1)==0)&(df['Literate_Male'].isna())
    df.loc[mask,'Literate_Male']=df.loc[mask,'Literate']-df.loc[mask,'Literate_Female']
    # fill missing female literates
    mask=(df[['Literate','Literate_Male']].isna().sum(axis=1)==0)&(df['Literate_Female'].isna())
    df.loc[mask,'Literate_Female']=df.loc[mask,'Literate']-df.loc[mask,'Literate_Male']

    # fill households, households_rural, households_urban
    mask=(df['Households'].isna())&(df[['Households_Rural','Households_Urban']].isna().sum(axis=1)==0)
    df.loc[mask,'Households']=df.loc[mask,['Households_Rural','Households_Urban']].sum(axis=1)
    mask=(df[['Households','Households_Rural']].isna().sum(axis=1)==0)&(df['Households_Urban'].isna())
    df.loc[mask,'Households_Urban']=df.loc[mask,'Households']-df.loc[mask,'Households_Rural']
    mask=(df[['Households','Households_Urban']].isna().sum(axis=1)==0)&(df['Households_Rural'].isna())
    df.loc[mask,'Households_Rural']=df.loc[mask,'Households']-df.loc[mask,'Households_Urban']


def mysqlcolumns(df:pd.DataFrame,mapped_cols:dict):
    mapper={'int64':'INT','float64':'FLOAT','object':'VARCHAR(50)'}
    columns=(f"{col} {mapper[str(df[col].dtype)]}" if len(col)<=50 else f"{mapped_cols[col]} {mapper[str(df[col].dtype)]}" for col in df.columns)
    return columns


