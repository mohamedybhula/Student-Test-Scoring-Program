"""
Imports the functions necessary to show the hardworking students, from the 
'DAFunction' module and test those functions. The functions here are also used for the 
functionality of the 'Find Hardworking Students' button of 'menu.ipynb'.
"""

from DAFunction import find_hardworking

if __name__ == "__main__":
    df = find_hardworking()
    print(df)