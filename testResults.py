"""
Imports the functions necessary to visualise a student's test scores, given a student id from the 'DAFunction' module and test those functions. The functions here are also used for the functionality of the 'Get Test Results' button of 'menu.ipynb'.
"""

from DAFunction import get_scores, plot_scores

if __name__ == "__main__":
    plot_scores(get_scores(151), 151)
    plot_scores(get_scores(10), 10)
    plot_scores(get_scores(1000), 1000)
    plot_scores(get_scores("Not a number"), "Not a number")