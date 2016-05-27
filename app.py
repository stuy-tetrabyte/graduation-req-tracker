from flask import Flask, render_template, request, session
from functools import wraps
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
#  Ethan Cheng                                                                 #
#                                                                              #
# Description                                                                  #
#  TODO                                                                        #
#                                                                              #
################################################################################

#{{{ Preamble
app = Flask(__name__)
db_m = DBManager(PROJECT_DB_NAME, COURSES_TABLE_NAME, STUDENT_TABLE_NAME)
#}}}
#{{{ Decorator Functions
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session or not session['logged_in']:
            session.clear()
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def redirect_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return redirect(url_for("class_view"))
        return f(*args, **kwargs)
    return decorated_function
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

@app.route('/login', methods=["GET", "POST"])
@app.route('/login/', methods=["GET", "POST"])
@redirect_if_logged_in
def login():
    """
    login_page: returns the login page

    Returns:
        the login page
    """
    return render_template("login.html")

@app.route('/class', methods = ['GET'])
@app.route('/class/', methods = ['GET'])
# @login_required
def class_view():
    """
    class_view: returns the student data for all students

    This applies filters specified by the GET request, including:
        - grade
        - TODO: ADD MORE

    Returns:
        the page with data of the specified graduating year
    """
    list_of_students = []
    grade = request.args.get('grade')
    if grade:
        list_of_students = db_m.get_grade_info(grade)
    else:
        list_of_students = db_m.get_all_students_info()
    return render_template("class.html", students=list_of_students)

@app.route('/student/<OSIS>')
@app.route('/student/<OSIS>/')
# @login_required
def student_view(OSIS=0):
    """
    student_view: returns the page for single-student data. By default, if
    failed, will return the page with fake data.

    Args:
        OSIS (string): OSIS of student

    Returns:
        the page with the specified student's data
    """

    student_info = db_m.get_student_info(OSIS)
    list_of_courses = [""] * 7
    if not student_info:
        # Default data for testing
        student_info = {
            "osis" : "123456789",
            "lastn" : "Rachmaninoff",
            "firstn" : "Sergei Vasilievich",
            "grade" : "12",
            "offcl" : "7CC"
        }
        list_of_courses = [
            "ART APPRECIATION",
            "BEGINNING BAND",
            "INTRO COMP SCI 1 OF 2",
            "TECHNICAL GRAPHIC COMMUNICATIONS",
            "BEGINNING BAND, CONCERT BAND, SYMPHONIC BAND",
            "HEALTH"
        ]
    else:
        for i in range(len(list_of_courses)):
            data = db_m.get_relevant_courses(OSIS, i)
            courses = {}
            for entry in data:
                if entry[1] in courses:
                    courses[entry[1]] += 1
                else:
                    courses[entry[1]] = 1

            def format_output(d):
                output = []
                for key in d:
                    output.append("%s (%d)" % (key, d[key]))
                return ", ".join(output)

            list_of_courses[i] = "None" if courses == {} else format_output(courses)

    return render_template("student.html", profile=student_info, courses=list_of_courses)

@app.route('/data')
# @login_required
def manage_data():
    """
    manage_data: returns the page for data management

    Returns:
        the page with links to manage database
    """
    return render_template("data.html")

@app.route('/export/<int:grad_year>')
# @login_required
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
