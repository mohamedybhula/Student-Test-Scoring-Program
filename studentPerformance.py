"""
Imports the functions necessary to show a student's raw and relative 
scores for a given a student id and given test, from the 'DAFunction' 
module and test those functions. The functions here are also used for the 
functionality of the 'Get Student's Performance' button of 'menu.ipynb'.
"""

from DAFunction import get_performance
    

if __name__ == "__main__":
    print(f"{get_performance(117, 'Formulative Test 2')} \n\n\n")
    print(f"{get_performance(151, 'Formulative Test 1')} \n\n\n")
    print(f"{get_performance(1500, 'Formulative Mock Test')} \n\n\n")
    print(f"{get_performance(26, 'Non-Existent Test')} \n\n\n")
    print(f"{get_performance(-5, 'Formulative Test 3')} \n\n\n")