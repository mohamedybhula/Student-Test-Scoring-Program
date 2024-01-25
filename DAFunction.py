"""
Contains raw functions imported and used by other modules. Also includes cleaned data
that has been manipulated to store different values in various variables used by functions.
The data is cleaned upon running 'CWPreprocessing.py' through an sqlite3 connection.
The functions utilize pandas and matplotlib to generate their output.
"""




import pandas as pd
import sqlite3
import matplotlib.pyplot as plt



conn = conn = sqlite3.connect("CWDatabase.db") 
# connecting to database to read in the test data as Pandas DataFrames

f_mock = pd.read_sql("SELECT * FROM mock", conn)
f_t1 = pd.read_sql("SELECT * FROM ft1", conn)
f_t2 = pd.read_sql("SELECT * FROM ft2", conn)
f_t3 = pd.read_sql("SELECT * FROM ft3", conn)
f_t4 = pd.read_sql("SELECT * FROM ft4", conn)
survey = pd.read_sql("SELECT [research id], [What level programming knowledge \
do you have?] FROM survey WHERE LOWER([What level programming knowledge do you \
have?]) LIKE '%beginner%'", conn) 
# selects only the rows where students prescribe themselves as a 'beginner' or lower

sum_test = pd.read_sql("SELECT * FROM sumtest", conn)

conn.close()








tests = [f_mock, f_t1, f_t2, f_t3, f_t4, sum_test]
test_names = ["Formulative Mock Test", "Formulative Test 1", "Formulative Test 2", 
              "Formulative Test 3", "Formulative Test 4", "Sum Test"]
test_names_dict = {"Formulative Mock Test": f_mock, "Formulative Test 1": f_t1, 
                   "Formulative Test 2": f_t2, "Formulative Test 3": f_t3, 
                   "Formulative Test 4": f_t4, "Sum Test": sum_test}

all_students = set()

for test in tests:
    if 'research id' in test.columns:
        all_students.update(test['research id'].unique())

all_students = list(all_students)  # creates a list of all the students id numbers, 
                                   # to help identify student numbers in later functions





def get_scores(id_num):
    """
    Returns the test scores of a given student based on their student id number.
    
    Args:
        id_num (int): The student id number.
        
    Returns:
        score_by_test (dict): A dictionary containing the test scores for the given student, 
                              using their standardized grade for each test.
    """
    
    scores = []
    for t in tests:
        filtered_data = t[t["research id"] == id_num]["standardized_grade"].values
        if len(filtered_data) > 0:
            scores.append(round(filtered_data[0], 2))  # adds the student's test grade to a list for each test
        else:
            scores.append(None)  # if the student did not take the test, a 'None' is added to the list
    
    score_by_test = {}
    
    for s, t in zip(scores, test_names):  # creates a dictionary of test scores using the list of scores and corresponding test names
        score_by_test[t] = s
    
    return score_by_test


def plot_scores(score_dict, id_num):
    """
    Plots a given student's scores as a bar chart.
    
    Args:
        score_dict (dict): A dictionary containing the student's scores for each test they completed.
        id_num (int): The id number of the student.
        
    Returns:
        A Matplotlib bar chart, where each test score for the student is shown by a different colour.
    """
    
    if id_num not in all_students or not isinstance(id_num, int):
        print("Not a valid Student Number")  
        # if the id is not in the list of student ids, the student must not exist
    
    else:
        score_dict_without_nones = {test: score for test, score in score_dict.items() if score is not None}
        colours = ["red", "blue", "green", "orange", "purple", "black"]
        plt.figure(figsize=(10, 6))
        bars = plt.bar(score_dict_without_nones.keys(), score_dict_without_nones.values(),
                       color=colours[:len(score_dict_without_nones)])
        plt.xlabel('Test Name')
        plt.ylabel('Standardized Score')
        plt.title(f'Test Scores for Student {id_num}')

        for bar, color in zip(bars, colours[:len(score_dict_without_nones)]):
            bar.set_color(color)

        plt.xticks(rotation=45)
        plt.tight_layout() 
        plt.show()

        
        

        
        
def get_performance(id_num, test_name):
    """
    Displays the grade and relative grade for each question that a given student completed for a given test.
    
    Args:
        id_num (int): The student's id number.
        test_name (str): The name of the test.
    
    Returns:
        df (DataFrame): A Pandas DataFrame.
    """
    
    if test_name not in test_names:
        print("Not a valid test. Please choose another test.")
        return None
    if id_num not in all_students:
        print("Student does not exist. Please choose another student")
        return None

    test_data = test_names_dict[test_name]
    question_cols = [col for col in test_data.columns if col.startswith('Q')]
    absolute_scores = []
    relative_scores = []
    
    for question in question_cols:
        test_data[question] = pd.to_numeric(test_data[question].replace('-', 0))
        student_data = test_data.loc[test_data["research id"] == id_num, question]
        
        if not student_data.empty:
            q_score = student_data.values[0]
            total_marks = int(question.split("/")[1]) 
            absolute_score = round((q_score / total_marks) * 10000, 2)
            absolute_scores.append(absolute_score)
            
            sdev = test_data[question].std()
            avg = test_data[question].mean()
            # uses the 'z-score' as a measure of how the student has performed relative to their peers
            z_score = (q_score - avg) / sdev 
            relative_scores.append(round(z_score, 2))
        else:
            print(f"No data found for student ID {id_num} in {test_name}.")
            return None

    df = pd.DataFrame({
        "Question": question_cols,
        "Absolute Score (/100)": absolute_scores,
        "Relative Score (Z-Score)": relative_scores
    })
    
    df["Question"] = df["Question"].\
    apply(lambda question_no: question_no[:4].replace(" ", "").replace("/", ""))
    # removing the original total score part for each question from the value in the 'Question' column
    
    return df






def is_underperforming():
    """
    Finds a list of students whose relative test scores are negative on average,
    so are underperforming relative to their peers.
    
    Args:
        None
    
    Returns:
        underperforming (dict): A dictionary of student ids and their mean z-scores
                                for students who underpeformed and completed at least 4 tests.
    """
    
    underperforming = {}
    
    for student in all_students:
        num_completed = 0  # tracks the number of tests the student completed
        z_scores = []
        
        for test in tests:
            student_data = test[test["research id"] == student]
            
            if not student_data.empty:
                student_grade = student_data["standardized_grade"].values[0]
                sdev = test["standardized_grade"].std()
                avg = test["standardized_grade"].mean()
                z_score = round((student_grade - avg) / sdev, 2)
                z_scores.append(z_score)
                num_completed += 1
            else:
                continue
        
        if (sum(z_scores) / len(z_scores)) < 0 and num_completed > 3:
            # includes the student if their mean z-score is negative
            underperforming[student] = round(sum(z_scores) / len(z_scores), 2)
    
    return underperforming


def display_underperforming(students):
    """
    Displays the test scores of the students who underperformed.
    
    Args:
        students (dict): A list of student ids as integers and their mean z-scores
                         across all tests as integers.
        
    Returns:
        underperforming_df (DataFrame): A Pandas DataFrame showing all of the test scores for each student.
    """
    
    grade_dict = {
        "Student ID": [],
        "Formulative Mock Test": [],
        "Formulative Test 1": [],
        "Formulative Test 2": [],
        "Formulative Test 3": [],
        "Formulative Test 4": [],
        "Sum Test": [],
        "Mean Z-Score": []
    }  # dictionary used to create the final DataFrame
    
    for student in students:
        for test in test_names:
            all_data = test_names_dict[test]  
            # uses the global variables to find all of the different test DataFrames
            
            student_data = all_data[all_data["research id"] == student]
            
            if not student_data.empty:
                student_grade = student_data["standardized_grade"].values[0]
                grade_dict[test].append(student_grade)  
                # adds the student grade to the appropriate dictionary item
            
            else:
                grade_dict[test].append(None)
        
        grade_dict["Student ID"].append(student)
        grade_dict["Mean Z-Score"].append(students[student])
    
    underperforming_df = pd.DataFrame(grade_dict)
    formulative_test_cols = \
    [col for col in underperforming_df.columns if col.startswith("Formulative")]
    underperforming_df["Lowest Grade"] = underperforming_df[formulative_test_cols].min(axis=1)
    # includes the student's lowest grade across the formulative tests they completed
    underperforming_df = underperforming_df.sort_values(by="Sum Test", ascending=True).reset_index(drop=True)
    
    return underperforming_df






def find_hardworking(beginners=survey["research id"].values):
    """
    Displays the students who are 'hardworking', as they have described themselves
    as 'beginners' but scored over 60 on the sum test.
    
    Args:
        beginners (DataFrame): The 'survey' table from the data base as Pandas DataFrame,
                               filtered to only beginners.
        
    Returns:
        hardworking_df (DataFrame): A Pandas DataFrame showing which students are
                                    hardworking based on the criteria.
    """
    
    beginner_students_over_60 = []
    over_60 = sum_test[sum_test["standardized_grade"] > 60]
    
    for val in over_60["research id"].values:
        if val in beginners:
            beginner_students_over_60.append(val)  # creates a list of student ids who are beginners and scored over 60
    
    beginner_responses = []
    beginner_over_60_grades = []
    
    for student in beginner_students_over_60:
        response = survey[survey["research id"] == student]\
        ["What level programming knowledge do you have?"].values[0]
        grade = sum_test[sum_test["research id"] == student]\
        ["standardized_grade"].values[0]
        beginner_responses.append(response)
        beginner_over_60_grades.append(grade)  # finds the students survey responses and sum test scores
        
    hardworking_df = pd.DataFrame({
        "Student ID": beginner_students_over_60,
        "Sum Test Score": beginner_over_60_grades,
        "Survey Response": beginner_responses
    })
    
    return hardworking_df
