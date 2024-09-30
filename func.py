import pandas as pd
def modify_statename(s):
    return ' '.join(word if word.lower()!='and' else 'and' for word in s.title().split())

def fill_missing_population(df:pd.DataFrame):
    mask_population = (df['Population'].isna() & (df[['Male','Female']].isna().sum(axis=1)==0))
    df.loc[mask_population,'Population']=df.loc[mask_population,'Male'] + df.loc[mask_population,'Female']
    mask_age = (df['Population'].isna() & (df[['Young_and_Adult','Middle_Aged','Senior_Citizen','Age_Not_Stated']].isna().sum(axis=1)==0))
    df.loc[mask_age,'Population'] = df.loc[mask_age,'Young_and_Adult']+df.loc[mask_age,'Middle_Aged']+df.loc[mask_age,'Senior_Citizen']+df.loc[mask_age,'Age_Not_Stated']
    df['Male']=df['Male'].fillna(df['Population']-df['Female'])
    df['Female']=df['Female'].fillna(df['Population']-df['Male'])

def fill_missing_age(df: pd.DataFrame):
    pop_notna = df['Population'].notna()
    age_columns = ['Young_and_Adult', 'Middle_Aged', 'Senior_Citizen', 'Age_Not_Stated']

    for col in age_columns:
        mask_other_ages_notna = df[age_columns].drop(col, axis=1).notna().all(axis=1)
        mask = pop_notna & df[col].isna() & mask_other_ages_notna 
        df.loc[mask, col] = df.loc[mask, 'Population'] - df.loc[mask, age_columns].drop(col, axis=1).sum(axis=1)

def fill_missing_literates(df:pd.DataFrame):
    fill_total_lit = (df['Literate'].isna() & (df[['Literate_Male','Literate_Female']].notna().all(axis=1)))
    df.loc[fill_total_lit,'Literate']=df.loc[fill_total_lit,'Literate_Male']+df.loc[fill_total_lit,'Literate_Female']
    mask=df['Literate'].notna()
    df['Literate_Male']=df['Literate_Male'].fillna(df.loc[mask,'Population']-df.loc[mask,'Literate_Female'])
    df['Literate_Female']=df['Literate_Female'].fillna(df.loc[mask,'Population']-df.loc[mask,'Literate_Male'])



def fill_missing_household(df:pd.DataFrame):
    mask=df['Households'].isna()
    fill_total_household=(mask & df[['Households_Rural','Households_Urban']].notna().all(axis=1))
    df['Households']=df['Households'].fillna(df.loc[fill_total_household,'Households_Rural']+df.loc[fill_total_household,'Households_Urban'])
    mask=df['Households'].notna()
    df['Households_Rural']=df['Households_Rural'].fillna(df.loc[mask,'Households']-df.loc[mask,'Households_Urban'])
    df['Households_Urban']=df['Households_Urban'].fillna(df.loc[mask,'Households']-df.loc[mask,'Households_Rural'])
