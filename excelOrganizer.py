# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 16:40:46 2015

@author: Gaurav
"""

# Import modules
import pandas as pd
from collections import defaultdict

def getCol(df,colName):
# Isolate columns you want to compare and return with whitespace stripped
    i = 0
    col = df.get(colName)
    while type(col[i]) == type(col[0]):
        i+=1
    col = df.get(colName)[0:i]
    for i in range(len(col)):
        col[i] = col[i].rstrip()
    return col

def compareColumns(colA,colB):
# Perform comparison and record indices from each column with matches
    if len(colA) > len(colB):
        col1 = colA
        col2 = colB
    else:
        col2 = colA
        col1 = colB

    col1_flag = []
    col2_flag = []
    for i in range(len(col2)):
        for j in range(len(col1)):
            if col1[j] == col2[i]:
                col1_flag.append(j)
                col2_flag.append(i)
    return col1_flag, col2_flag

def dictFromDF(df,stringVal):
# Turn dictionary into a dataframe, relabel column, 
# turn list into strings, clean up to remove unnecessary information
    dictDF = defaultdict(list)
    for r in range(len(df)):
        vals = []
        for c in range(len(df.columns)):
            if df.ix[r,c] == stringVal:
                vals.append(cols[c])
        dictDF[r].append(vals)
    return dictDF

def compareDataFrames(dfA,dfB,columnName):
    colA = getCol(dfA,columnName)
    colB = getCol(dfB,columnName)
    colA_flag, colB_flag = compareColumns(colA,colB)
    dfA = dfA.ix[colA_flag,:]
    dfB = dfA.ix[colB_flag,:]
    dfA = dfA.reset_index(drop=True)
    dfB = dfB.reset_index(drop=True)
    dfC = pd.merge(dfA,dfB,on=columnName)
    return dfA, dfB, dfC

# Write data to Excel file
def dataframeToExcel(df_list):
    writer= pd.ExcelWriter('Aging_Data_Output.xlsx')
    for i in range(len(df_list)):
        df_list[i].to_excel(writer,sheet_name='df',index=False)
    writer.save()
    
# Read Excel Files
df1 = pd.read_excel('C:/Anaconda/Aging_Data_Table_1.xlsx', 'Sheet1', na_values=['N/A'])
df2 = pd.read_excel('C:/Anaconda/Aging_Data_Table_2.xlsx', 'Sheet1', na_values=['N/A'])

# Compare Data Frames
df1, df2, df3 = compareDataFrames(df1,df2,'Protein Group Description (Species: Homo Sapiens)')

# Get column labels as unicode values
cols = list(df2.columns.values)
GO = dictFromDF(df2,'X')
GO_df = pd.DataFrame.from_dict(GO,orient='index')
GO_df.columns = ['GO']
GO_df['GO'] = GO_df.GO.map(str)
GO_df['GO'] = GO_df['GO'].map(lambda x: x.replace("[u'","").replace("']","").replace("u'","").replace("'","").replace("[]",""))
GO_df.columns = ['Gene Ontologies (GO)']
# Concatenate df1 with new GO_df
df4 = pd.concat([df1,GO_df],axis=1,ignore_index=False)

dataframeToExcel([df1, df2, df3, df4])


"""
Possible Functions:
a. import Excel files as dataframes

b. change dataframe column to a set of strings and clean up unicode demarcation
def unicode_list_to_string(dataframe):
    ...
    return dict
 
c. count and save all dataframes?
   
d. save all dataframes to excel
def save_dataframes_to_excel(df_list,output_name):
    writer = pd.ExcelWriter(output_name)
    for i in range(len(df_list)):
        df_list[i].to_excel(writer,sheet_name='df4',index=False)


 
"""
"""
FUTURE IDEAS:
Cross-reference rat and monkey gene names to find similarities and merge
"""
"""
NOTES
Aging_Data_Table_1 has gene and fold-change info
Aging_Data_Table_2 has gene ontology
Task: create Aging_Data_Table_3 that combines the two
if col(C) of ADT1 matches col(A) of ADT2:
    append ADT2.cols(B:O) to ADT1.col(:)
    OR
    append ADT1.col(A,B,D) to ADT2.col(:)

# editing cells
# remove whitespace from right: a.rstrip()

# selecting cell from a column
In[1]: df.get('Primary Gene Name')[0].rstrip()
Out[51]: u'BCKDK'

# selecting an individal cell itself
# df1.loc[0] gives first row
# df1.loc[0][0] gives the cell at first column, first row
# .loc DISREGARDS LABELS so [r][c] is all data

# Indexing and selecting whole columns and rows
# df1.ix[row1:row2,col1:col2]

# Check types of data
# df1.dtypes will give types for each column

# Get list of column labels
# cols = df.columns.tolist()
# OR
# cols = list(df.columns.values)
# slice cols to change column order
# cols = cols[-1:] + cols[:-1] moves last column to first
# df = df[cols] will reorder based on new cols
# note that this will not update indices for df so df.ix unaffected

# Deleting a column
# def df['A'] or A = df.pop('A')

# Adding a column
# df['col'] = list works if len(list) fits pre-existing indices

# Change a value
# df.ix[row,column] = val
# df.ix[:,column] = val changes for all rows
# Flagging a column based on logic
# df['flag'] = df['A'] > 2
# can use to determine up vs. down-regulated proteins
"""