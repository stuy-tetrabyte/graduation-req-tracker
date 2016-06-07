# core dependencies
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from functools import wraps
import sys, os
import pandas
sys.path.insert(0, './utils/')

# project imports
from database import DBManager
from Constants import *
from database_setup import delete_project_table, get_excel, load_excel_file

# security imports
from werkzeug import secure_filename

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
app_path = os.path.realpath(__file__)
app_dir = os.path.dirname(app_path)

UPLOAD_FOLDER = app_dir + '/uploaded_files/'
DOWNLOAD_FOLDER = app_dir + '/downloadables/'
ALLOWED_EXTENSIONS = set(['xlsx', 'xls'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

print "Saving files to: ", app.config['UPLOAD_FOLDER']
print "Generating files in: ", app.config['DOWNLOAD_FOLDER']

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
    grades = []
    req_statuses = [[], [], [], [], [], [], []]
    
    get_req_args = request.args

    if not get_req_args:
        return render_template('class.html', students = db_m.get_all_students_info())

    for grade in range(9, 13):
        if get_req_args.get( 'grade-' + str( grade ) ) == 'on':
            grades.append(str( grade ))

    for req in range(0, 7):
        if get_req_args.get( str( req ) + '-fulfilled' ) == 'on':
            req_statuses[req].append(0)
        if get_req_args.get( str( req ) + '-missing' ) == 'on':
            req_statuses[req].append(1)
        if get_req_args.get( str( req ) + '-failed' ) == 'on':
            req_statuses[req].append(2)

    list_of_students = [student_info for student_info
                            in db_m.get_students_such_that(req_statuses)
                            if student_info['grade'] in grades]

    export_student_list(list_of_students)

    return render_template("class.html", students=list_of_students, boxes = dict( get_req_args ))

@app.route('/student', methods = ['GET'])
@app.route('/student/', methods = ['GET'])
def student_search():
    return redirect(url_for('student_view', OSIS = request.args.get('osis')))

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
    next_term_suggestions = [""] * 7
    if not student_info:
        return render_template("student_not_found.html", osis=OSIS)
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
                if entry[2] == 'F' or entry[2] == 'NC' or entry[2] == 'NS' or int(entry[2]) < 65:
                    if entry[0] + " (FAILED)" in courses:
                        courses[entry[0] + " (FAILED)"] += 1
                    else:
                        courses[entry[0] + " (FAILED)"] = 1
                elif entry[0] in courses:
                    courses[entry[0]] += 1
                else:
                    courses[entry[0]] = 1

            def format_output(d):
                output = []
                for key in d:
                    output.append("%s (%d)" % (key, d[key]))
                return ", ".join(output)

            list_of_courses[i] = "None" if courses == {} else format_output(courses)

            need_to_take = db_m.get_req_course_track(OSIS, i)[1]
            for j in need_to_take:
                if j == []: # fufilled
                    next_term_suggestions[i] = "Fufilled"

            if next_term_suggestions[i] == "":
                suggestions = ""
                for j in need_to_take:
                    for k in j[0]:
                        suggestions += str( k ) + ', '

                suggestions = suggestions[:-2]

                next_term_suggestions[i] = suggestions

    return render_template("student.html", profile=student_info,
            courses=list_of_courses, suggestions = next_term_suggestions)

@app.route('/data')
@app.route('/data/')
# @login_required
def manage_data():
    """
    manage_data: returns the page for data management

    Returns:
        the page with links to manage database
    """
    return render_template("data.html")

def allowed_filename(filename):
    """
    Utility function to verify a file extension

    Returns:
        True if the filename is that of an Excel file
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=["GET", "POST"])
@app.route('/upload/', methods=["GET", "POST"])
# @login_required
def upload():
    """
    upload: takes a .xls or .xlsx file and models the database.
    #TODO: (enhancement) allow the user to undo, or revert to previous versions
    #TODO: (enhancement) load the file into the database asynchronously and
    display a progress bar.

    Returns:
        The upload page (regardless of whether not you are uploading or not
    """
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_filename(f.filename):
            secure_name = secure_filename(f.filename)
            path_to_uploaded = os.path.join(app.config['UPLOAD_FOLDER'], secure_name)
            print "Saving file to: ", path_to_uploaded
            f.save(os.path.join(path_to_uploaded))
            print "Deleting database to clean state..."
            delete_project_table()
            print "Loading database..."
            load_excel_file(get_excel(path_to_uploaded))
            print "Removing file to save storage..."
            os.remove(path_to_uploaded)
        else:
            print "File extension not allowed!", str(f)

        return redirect(url_for("class_view"))
    else:
        return render_template("upload.html")

# @app.route('/export_filtered', methods = ['POST'])
# @app.route('/export_filtered/', methods = ['POST'])
def export_student_list(student_list):
    """
    Generates an excel file given a student_list (formated the same way as
    list_of_students from the class view route.

    Args:
        student_list: a list of dictionaries of student data
            [
                {
                    'offcl': 'nan',
                    'firstn': 'nan',
                    'grade': '9',
                    'lastn': 'nan',
                    'osis': '701111441',
                    'req_status': [1, 1, 1, 1, 1, 1, 1]
                },
                ...
            ]

    Returns:
        An Excel file for the user to download
    """
    data = []
    for student in student_list:
        row = {
                "OSIS" : student['osis'],
                "OFF. CLASS" : student['offcl'],
                "GRADE" : student['grade'],
                "LAST NAME" : student['lastn'],
                "FIRST NAME" : student['firstn']
        }
        data.append(row)
    df = pandas.DataFrame(data)
    print df

    filename = "filtered.xlsx" # TODO: Make the filename the filter options
    if allowed_filename(filename):
        secure_name = secure_filename(filename)
        path_to_filtered = os.path.join(app.config['DOWNLOAD_FOLDER'], secure_name)
        df.to_excel(path_to_filtered, index=False)
        # return send_from_directory(directory=app.config['DOWNLOAD_FOLDER'],
        #        filename=secure_name)
    else:
        return None


#}}}
#{{{ AJAX Calls
@app.route('/update_reqs', methods = ['GET', 'POST'])
@app.route('/update_reqs/', methods = ['GET', 'POST'])
def update_graduation_requirements():
    """
    update_graduation_requirements: AJAX call to server that updates the
    graduation requirements

    Returns:
        JSON status for success or failure
    """
    return ""

@app.route('/update_db/<int:grad_year>', methods = ['GET', 'POST'])
@app.route('/update_db/<int:grad_year>/', methods = ['GET', 'POST'])
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
@app.route('/update_student/<OSIS>/', methods = ['GET', 'POST'])
def update_student(OSIS):
    """
    update_student: updates the information on a single student in the database

    Args:
        OSIS (string): the OSIS for the student

    Returns:
        JSON status for success or failure
    """
    return ""
#}}}

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8000, debug = True)

