"""
Reads in the raw CSV test data by importing the pandas and os libraries to appropriately 
find the files and parse them, before cleaning them when ran in the jupyter notebook menu, 
using a sqlite3 databse connection and the clean_file() function.
"""


import pandas as pd
import sqlite3
import os


folder_path = "TestResult"
files = os.listdir(folder_path)

f_mock = pd.read_csv(os.path.join(folder_path,files[0]))
f_t1 = pd.read_csv(os.path.join(folder_path,files[1]))
f_t2 = pd.read_csv(os.path.join(folder_path,files[2]))
f_t3 = pd.read_csv(os.path.join(folder_path,files[3]))
f_t4 = pd.read_csv(os.path.join(folder_path,files[4]))
survey = pd.read_csv(os.path.join(folder_path,files[5]))
sum_test = pd.read_csv(os.path.join(folder_path,files[6])) 
# reads in the CSV files using the file paths


def clean_file(df):
    
    """
    Cleans a DataFrame by sorting the values, removing duplicates, 
    unnecessary columns and adds the standardized grade. 
    
    Args:
        df (DataFrame): An uncleaned Pandas DataFrame.
        
    Returns:
        df (DataFrame): The cleaned version of the initial Pandas DataFrame.
    """
    
    if "Which of followings are true for you" not in df.columns:
        # condition to filter for the survey based DataFrame
        
        df = df.fillna(0)
        grade_col = [col for col in df.columns if "Grade" in col][0]
        
        df["original_order"] = df.index 
        # commits initial DataFrame order to memory
        
        df.sort_values(by=grade_col, ascending=False, inplace=True)
        df.drop_duplicates(subset='research id', keep='first', inplace=True)
        df.sort_values(by="original_order", inplace=True) 
        # retains initial order after duplicates are dropped
        
        df.drop(columns=["original_order", "State", "Time taken"], inplace=True)
        df[grade_col] = df[grade_col].replace("-", 0)
        df["standardized_grade"] = \
        round((pd.to_numeric(df[grade_col]) / int(grade_col.split("/")[1])) * 10000, 2) 
        # adds new grade column
    
    else:
        df = df.fillna(0)
    
    return df



    
if __name__ == "__main__":
    conn = sqlite3.connect("CWDatabase.db")
    clean_file(f_mock).to_sql("mock", conn, if_exists="replace", index=False)
    clean_file(f_t1).to_sql("ft1", conn, if_exists="replace", index=False)
    clean_file(f_t2).to_sql("ft2", conn, if_exists="replace", index=False)
    clean_file(f_t3).to_sql("ft3", conn, if_exists="replace", index=False)
    clean_file(f_t4).to_sql("ft4", conn, if_exists="replace", index=False)
    clean_file(survey).to_sql("survey", conn, if_exists="replace", index=False)
    clean_file(sum_test).to_sql("sumtest", conn, if_exists="replace", index=False) 
    # cleans the raw DataFrames when the file is ran in another module
    conn.commit()
    conn.close()