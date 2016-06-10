# core dependencies
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from functools import wraps
import sys, os
import pandas
import urllib, urllib2, json
sys.path.insert(0, './utils/')

# project imports
from database import DBManager
from Constants import *
from database_setup import delete_project_table, get_excel, load_excel_file
from tools import *

# security imports
from werkzeug import secure_filename

################################################################################
# Python Flask based server script for graduation requirement tracker          #
#                                                                              #
# Authors                                                                      #
#  Yicheng Wang                                                                #
#  Ariel Levy                                                                  #
#  Ethan Cheng                                                                 #
#  Loren Maggiore                                                              #
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
STUDENT_LOOKUP = app_dir + '/static/users_stuyedu.csv'
ALLOWED_EXTENSIONS = set(['xlsx', 'xls'])
CSV_EXTENSION = 'csv'
JSON_EXTENTION = 'json'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

print "Saving files to: ", app.config['UPLOAD_FOLDER']
print "Generating files in: ", app.config['DOWNLOAD_FOLDER']

db_m = DBManager(PROJECT_DB_NAME, COURSES_TABLE_NAME, STUDENT_TABLE_NAME)
list_of_students = []

# Load in list of administrators
ADMIN_FILE = open(app_dir + '/static/auth_users.csv', 'r')
ADMINS = [ str(s.strip('\"\n')) for s in ADMIN_FILE.readlines() if '@stuy.edu' in s ]
print ADMINS
ADMIN_FILE.close()

student_osis = {}
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

def redirect_if_student(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session['logged_in'] and not session['admin']:
            return redirect(url_for("student_view", OSIS=0))
        return f(*args, **kwargs)
    return decorated_function
#}}}
#{{{ Tools
def load_student_osis_dict():
    """
    load_student_osis_dict: loads a csv file at static/users_stuyedu.csv into
    the student_osis dictionary

    Returns:
        True upon success, False otherwise
    """
    global student_osis
    student_osis = {}

    try:
        reader = csv.reader(open(STUDENT_LOOKUP, 'rb'))
    except IOError:
        return False

    for i, rows in enumerate(reader):
        if i == 0:
            val_index = rows.index("OSIS")
            key_index = rows.index("EMAIL")
            continue

        k = rows[key_index]
        v = rows[val_index]

        student_osis[k] = v

    return True

def get_osis(email):
    """
    get_osis: returns the osis number based on an email supplied, return None
    otherwise

    Args:
        email (type): TODO

    Returns:
        osis string of the student
    """
    global student_osis
    if email in student_osis:
        return student_osis[email]
    else:
        return None

def allowed_filename(filename):
    """
    Utility function to verify a file extension

    Returns:
        True if the filename is that of an Excel file
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#}}}
#{{{ Pages
@app.route("/")
def home():
    """
    home: returns the home page

    Returns:
        the home page
    """
    return redirect(url_for("login"))

@app.route("/about")
@app.route("/about/")
@login_required
def about():
    """
    about: returns the about page

    Returns:
        the about page
    """
    return render_template("about.html")

@app.route('/login', methods=["GET", "POST"])
@app.route('/login/', methods=["GET", "POST"])
@redirect_if_logged_in
def login():
    """
    login_page: returns the login page

    Returns:
        the login page
    """
    token = request.args.get("t1")
    access = request.args.get("t2")
    if token is None or access is None:
        return render_template("login.html")
    else:
        # Query Google Token Authenticator
        URL = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="
        api_call = urllib2.urlopen(URL + token)
        data = json.loads(api_call.read())
        print data
        if str(data['email_verified']) == 'true' and str(data['email']).endswith("@stuy.edu"):
            session['logged_in'] = True
            session['token'] = access
            if str(data['email']) in ADMINS:
                session['admin'] = True
            else:
                session['admin'] = False
                session['email'] = str(data['email'])
            print session
            return redirect(url_for('class_view'))
        else:
            session.clear()
            print "FAILED LOGIN"
            return render_template("login.html")

@app.route('/logout')
@app.route('/logout/')
def logout():
    try:
        URL = 'https://accounts.google.com/o/oauth2/revoke?token='
        api_call = urllib2.urlopen(URL + session['token'])
        if api_call.getcode() != 200:
            print "Token Revoking Failed with user: " + str(session)
    except:
        print "Token Revoking Failed with user: " + str(session)
    session.clear()
    print "Should be {}: " + str(session)
    return redirect(url_for('login'))

@app.route('/class', methods = ['GET'])
@app.route('/class/', methods = ['GET'])
@login_required
@redirect_if_student
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

    global list_of_students

    if not get_req_args:
        list_of_students = db_m.get_all_students_info()
        return render_template('class.html', students = db_m.get_all_students_info())

    logic = get_req_args.get( 'logic' )
    print type( logic )
    db_m.change_db_logic(logic)
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

    # export_student_list(list_of_students)

    return render_template("class.html", students=list_of_students, boxes = dict( get_req_args ))

@app.route('/student', methods = ['GET'])
@app.route('/student/', methods = ['GET'])
@login_required
@redirect_if_student
def student_search():
    return redirect(url_for('student_view', OSIS = request.args.get('osis')))

@app.route('/student/<OSIS>')
@app.route('/student/<OSIS>/')
@login_required
def student_view(OSIS=0):
    """
    student_view: returns the page for single-student data. By default, if
    failed, will return the page with fake data.

    Args:
        OSIS (string): OSIS of student

    Returns:
        the page with the specified student's data
    """

    if not session['admin'] and session['email']:
        OSIS = get_osis(session['email'])

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

            data = db_m.get_req_course_track(OSIS, i)
            track_names = data[0]
            taken = [len(courses) for courses in data[1]]
            need_to_take = data[2]

            for j in range(len( taken )):
                if taken[j] != 0:
                    track_names[j] += " (Started)"

            for j in need_to_take:
                if j == []: # fufilled
                    next_term_suggestions[i] = "Fufilled"

            if next_term_suggestions[i] == "":
                next_term_suggestions[i] = []
                for j in range(len(track_names)):
                    next_term_suggestions[i].append((track_names[j],
                        need_to_take[j][0]))

    return render_template("student.html", profile=student_info,
            courses=list_of_courses, suggestions = next_term_suggestions)

@app.route('/data')
@app.route('/data/')
@login_required
@redirect_if_student
def manage_data():
    """
    manage_data: returns the page for data management

    Returns:
        the page with links to manage database
    """
    return render_template("data.html")

@app.route('/upload', methods=["GET", "POST"])
@app.route('/upload/', methods=["GET", "POST"])
@login_required
@redirect_if_student
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
            return render_template('upload.html', redir = 'upload', err = "File extension not allowed! " + f.filename);

        return redirect(url_for("class_view"))
    else:
        return render_template("upload.html", redir = 'upload')

@app.route('/update_reqs', methods = ['GET', 'POST'])
@app.route('/update_reqs/', methods = ['GET', 'POST'])
@login_required
@redirect_if_student
def update_graduation_requirements():
    """
    update_graduation_requirements: takes a .json file and sanitizes/checks it
    and updates the backend JSON file

    Returns:
        The upload page, or a finished page
    """
    if request.method == 'POST':
        f = request.files['file']
        if f:
            secure_name = secure_filename(f.filename)
            path_to_uploaded = os.path.join(app.config['UPLOAD_FOLDER'],
                    secure_name)
            print "Saving file to: ", path_to_uploaded
            f.save(os.path.join(path_to_uploaded))
            if check_json(path_to_uploaded):
                os.rename(path_to_uploaded, app_dir + '/static/reqs.json')
                db_m.reqs = json.loads(open(app_dir + '/static/reqs.json').read())['grad_requirements']
                return redirect(url_for("class_view"))
            else:
                return render_template('upload.html', redir = 'update_reqs', err = "Invalid JSON file!")

    else:
        return render_template('upload.html', redir = 'update_reqs')

@app.route('/update_students', methods = ['GET', 'POST'])
@app.route('/update_students/', methods = ['GET', 'POST'])
@login_required
@redirect_if_student
def update_student_osis():
    """
    update_student_osis: updates the current csv file based on an uploaded csv
    file

    Returns:
        The upload page, or the finished page
    """
    if request.method == 'POST':
        f = request.files['file']
        if f and '.' in f.filename and f.filename.rsplit('.', 1)[1] == CSV_EXTENSION:
            secure_name = secure_filename(f.filename)
            path_to_uploaded = os.path.join(app.config['UPLOAD_FOLDER'],
                    secure_name)
            print "Saving file to: ", path_to_uploaded
            f.save(os.path.join(path_to_uploaded))
            if check_student_csv(path_to_uploaded):
                os.rename(path_to_uploaded, app_dir + '/static/users_stuyedu.csv')
                load_student_osis_dict()
                return redirect(url_for("class_view"))
            else:
                return render_template('upload.html', redir =
                        'update_students', err =
                        'Invalid CSV file!')
        else:
            return render_template('upload.html', redir =
                    'update_students', err =
                    'Invalid CSV file!')

    else:
        return render_template('upload.html', redir = 'update_students')

@app.route('/update_admins', methods = ['GET', 'POST'])
@app.route('/update_admins/', methods = ['GET', 'POST'])
@login_required
@redirect_if_student
def update_admin_list():
    """
    update_admin_list: updates the list of admins based on an uploaded csv

    Returns:
        The class view page, or the finished page
    """
    if request.method == 'POST':
        f = request.files['file']
        if f and '.' in f.filename and f.filename.rsplit('.', 1)[1] == CSV_EXTENSION:
            secure_name = secure_filename(f.filename)
            path_to_uploaded = os.path.join(app.config['UPLOAD_FOLDER'],
                    secure_name)
            print "Saving file to: ", path_to_uploaded
            f.save(os.path.join(path_to_uploaded))
            if check_admin_csv(path_to_uploaded):
                os.rename(path_to_uploaded, app_dir + '/static/auth_users.csv')
                ADMIN_FILE = open(app_dir + '/static/auth_users.csv', 'r')
                global ADMINS
                ADMINS = [ str(s.strip('\"\n')) for s in ADMIN_FILE.readlines() if '@stuy.edu' in s ]
                ADMIN_FILE.close()
                return redirect(url_for("class_view"))
            else:
                return render_template('upload.html', redir =
                        'update_admins', err =
                        'Invalid CSV file!')
        else:
            return render_template('upload.html', redir = 'update_admins', err =
                        'Invalid CSV file!')

    else:
        return render_template('upload.html', redir = 'update_admins')

@app.route('/export_filtered')
@app.route('/export_filtered/')
@login_required
@redirect_if_student
def export_student_list():
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
    global list_of_students
    data = []
    for student in list_of_students:
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
        if os.path.isfile(path_to_filtered):
            os.remove(path_to_filtered)
        df.to_excel(path_to_filtered, index=False)
        return send_from_directory(directory=app.config['DOWNLOAD_FOLDER'],
               filename=secure_name, as_attachment=True,
               attachment_filename=secure_name)
    else:
        return None


#}}}

if __name__ == "__main__":
    if not load_student_osis_dict():
        print "LOADING STUDENTS FAILED"
    app.secret_key = "Ryuu-ga, Wa-ga-te-ki-wo, Ku-ra-u. #genji"
    app.run(host = "0.0.0.0", port = 8000, debug = True)

