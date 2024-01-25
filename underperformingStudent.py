"""
Imports the functions necessary to showthe underperforming students 
from the 'DAFunction' module and test those functions. The functions 
here are also used for the functionality of the 'Find Underperforming 
Students' button of 'menu.ipynb'.
"""

from DAFunction import is_underperforming, display_underperforming

if __name__ == "__main__":
    print(display_underperforming(is_underperforming()))