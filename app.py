from flask import Flask, render_template, request
import sys
sys.path.insert(0, './utils/')
from database import DBManager
from Constants import *

################################################################################
# Python Flask based server script for graduation requirement tracker          #
#                                                                              #
# Authors                                                                      #
#  Yicheng Wang                                                                #
#  Ariel Levy                                                                  #
#                                                                              #
# Description                                                                  #
#  TODO                                                                        #
#                                                                              #
################################################################################

#{{{TODO LIST
#  TODO
#}}}
#{{{Dev Log
#  Project Created: 2016-05-13 19:32 - Yicheng W.
#}}}
#{{{ Preamble
app = Flask(__name__)
db_m = DBManager(PROJECT_DB_NAME, COURSES_TABLE_NAME, STUDENT_TABLE_NAME)
#}}}
#{{{ Pages
@app.route("/")
def home():
    """
    home: returns the home page
    
    Returns:
        the home page
    """
    return render_template("master.html")

@app.route('/login')
def login_page():
    """
    login_page: returns the login page

    Returns:
        the login page
    """
    return render_template("login.html")

@app.route('/login', methods = ['GET', 'POST'])
def login_check():
    """
    login_check: returns the check page for login
    
    Returns:
        the approporiate page
    """
    return ""

@app.route('/class')
def class_view():
    """
    class_view: returns the student data for all students
 
    Returns:
        the page with data of the specified graduating year
    """
    list_of_students = db_m.get_all_students_info()
    return render_template("class.html", students=list_of_students)

@app.route('/class', methods = ['GET', 'POST'])
def class_view_filtered(): # XXX Discuss server side v. client side
    """
    class_view_filtered: returns the filtered data for the specified graduation
    year, filters specified in the GET request, including:
        TODO

    Args:
        grade (get request argument): grade filter
    
    Returns:
        the page with the filtered dataset
    """
    grade = request.args.get('grade')
    print grade
    list_of_students = db_m.get_grade_info(grade)
    return render_template("class.html", students=list_of_students)

@app.route('/student/<OSIS>')
def student_view(OSIS):
    """
    student_view: returns the page for single-student data

    Args:
        OSIS (string): OSIS of student
    
    Returns:
        the page with the specified student's data
    """
    # TODO: get dictionary of student info, including:
    #   .osis - OSIS
    #   .lastn - last name
    #   .firstn - first name
    #   .grade - grade
    #   .offcl - official class
    student_info = {}
    if OSIS == "0":
        student_info["osis"] = "123456789"
        student_info["lastn"] = "Rachmaninoff"
        student_info["firstn"] = "Sergei Vasilievich"
        student_info["grade"] = "12"
        student_info["offcl"] = "7CC"
    # TODO: get a list of classes fulfilling grad requirements:
    #   0 - Art 
    #   1 - Music
    #   2 - Intro CS 
    #   3 - Drafting
    #   4 - Tech
    #   5 - Health
    list_of_courses = [""]*6
    if OSIS == "0":
        list_of_courses[0] = "ART APPRECIATION"
        list_of_courses[1] = "BEGINNING BAND"
        list_of_courses[2] = "INTRO COMP SCI 1 OF 2"
        list_of_courses[3] = "TECHNICAL GRAPHIC COMMUNICATIONS"
        list_of_courses[4] = "BEGINNING BAND, CONCERT BAND, SYMPHONIC BAND"
        list_of_courses[5] = "HEALTH"
    return render_template("student.html", profile=student_info, courses=list_of_courses)

@app.route('/data')
def manage_data():
    """
    manage_data: returns the page for data management

    Returns:
        the page with links to manage database
    """
    return render_template("data.html")

@app.route('/export/<int:grad_year>')
def export_db(grad_years):
    """
    export_db: export the database in xls form

    Args:
        grad_years (int): the specified graduation year
    
    Returns:
        an xls file for client to download
    """
    return ""
#}}}
#{{{ AJAX Calls
@app.route('/update_reqs', methods = ['GET', 'POST'])
def update_graduation_requirements():
    """
    update_graduation_requirements: AJAX call to server that updates the
    graduation requirements
    
    Returns:
        JSON status for success or failure
    """
    return ""

@app.route('/update_db/<int:grad_year>', methods = ['GET', 'POST'])
def update_db(grad_year):
    """
    update_db: AJAX call that updates the student info of a given graduating
    year in the database

    Args:
        grad_year (int): the specified graduation year
    
    Returns:
        JSON status for success or failure
    """
    return ""

@app.route('/update_student/<OSIS>', methods = ['GET', 'POST'])
def update_student(OSIS):
    """
    update_student: updates the information on a single student in the database

    Args:
        OSIS (string): the OSIS for the student
    
    Returns:
        JSON status for success or failure
    """
#}}}

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, debug = True)
