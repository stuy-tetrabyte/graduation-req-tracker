from flask import Flask, render_template

################################################################################
# Python Flask based server script for graduation requirement tracker          #
#                                                                              #
# Authors                                                                      #
#  Yicheng Wang                                                                #
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
from flask import Flask

app = Flask(__name__)
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

@app.route('/class/<int:grad_year>')
def class_view(grad_year):
    """
    class_view: returns the student data for the specified graduation year

    Args:
        grad_year (int): the specified graduation year
    
    Returns:
        the page with data of the specified graduating year
    """
    # TODO: get list of students in a given grad year
    # each student entry should include OSIS, name, grad year
    list_of_students = []  
    return render_template("class.html", students=list_of_students)

@app.route('/class/<int:grad_year>', methods = ['GET', 'POST'])
def class_view_filtered(grad_year): # XXX Discuss server side v. client side
    """
    class_view_filtered: returns the filtered data for the specified graduation
    year, filters specified in the GET request, including:
        TODO

    Args:
        grad_year (int): the specified graduation year
    
    Returns:
        the page with the filtered dataset
    """
    # TODO: get list of students based on filters
    # each student entry should include OSIS, name, grad year
    list_of_students = []  
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
    return ""

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
