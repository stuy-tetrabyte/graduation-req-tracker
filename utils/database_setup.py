import pandas
import argparse
import SQLConnector
import Constants
import sys
import json

def has_completed_track(passed_courses, track_reqs):
    """
    has_completed_track: checks if the list of passed courses completes the
    track requirements

    Args:
        passed_courses (list of strings): a student's
            passed courses
	track_reqs (list of strings): list of required courses to complete a
            certain track
    
    Returns:
        a boolean value indicating if the list of passed courses completes the
        track requirements
    """

    relevent_courses_passed = []
    status = True

    for semester in track_reqs:
        fufilled = False

        for i in range(0, len(passed_courses)):
            if (passed_courses[i] in semester):
                passed_courses.pop(i)
                fufilled = True
                break

        status = status 
        
        if (not fufilled):
            return False

    return True


def get_excel(filepath):
    """
    Returns a Pandas datafile that contains the contents of a Microsoft Excel
    Spreadsheet

    Params:
        filepath - A string containing the path to the file

    Returns:
        A Pandas datafile
    """
    return pandas.read_excel(filepath)

def get_column_names(datafile):
    """
    Returns a list containing the column names of a Pandas datafile as Python
    strings. This replaces all spaces with _ and upper-cases all letters

    Params:
        datafile - A Pandas datafile

    Returns:
        A list of strings
    """
    return [ str(s).strip().upper().replace(" ", "_") for s in datafile.columns ]

def is_table_set_up():
    """
    Returns True if this project's MySQL table is set up, False otherwise
    """
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema='%s' and table_name='%s';"
    retval = SQLConnector.execute(query % (Constants.PROJECT_DB_NAME, Constants.COURSES_TABLE_NAME,))
    courses_setup = retval != None and len(retval) == 1
    retval = SQLConnector.execute(query % (Constants.PROJECT_DB_NAME, Constants.STUDENT_TABLE_NAME))
    return courses_setup and (retval != None and len(retval) == 1)

def create_project_table(courses_column_names, student_column_names):
    """
    Sets up MySQL with a table with a set schema given a list of column_names.
    Does nothing if the table is already set up.

    Params:
        courses_column_names - A list of strings containing column names for the courses table
        student_column_names - A list of strings containing column names for the students table

    Returns:
        None
    """
    # Tons of format strings!
    query = "CREATE TABLE IF NOT EXISTS %s (%s);"
    schema = (("%s VARCHAR(64), " * len(courses_column_names))[:-2]) % tuple(courses_column_names)
    SQLConnector.execute(query % (Constants.COURSES_TABLE_NAME, schema))

    schema = (("%s VARCHAR(64), " * len(student_column_names))[:-2]) % tuple(student_column_names)
    SQLConnector.execute(query % (Constants.STUDENT_TABLE_NAME, schema))
    


def delete_project_table():
    """
    Deletes the table in MySQL that this project uses. Will do nothing if the
    table does not yet exist.
    """
    query = "DROP TABLE IF EXISTS %s;"
    SQLConnector.execute(query % (Constants.COURSES_TABLE_NAME,))
    SQLConnector.execute(query % (Constants.STUDENT_TABLE_NAME,))

def reset_project_table():
    """
    Resets the table for this project by calling 'delete' and 'setup'
    """
    delete_project_table()
    for i in range(0, Constants.TOTAL_REQ_COUNT):
        Constants.STUDENT_TABLE_COLUMNS.append("REQ%02d" % i) # grad reqs
    create_project_table(Constants.COURSES_TABLE_COLUMNS, Constants.STUDENT_TABLE_COLUMNS)

def load_excel_file(datafile):
    """
    Takes a Pandas datafile and inserts the data into the project's MySQL table.
    If the project's table is not yet created, this function will call 'create'.

    The column names are specified within Constants.COURSES_TABLE_COLUMNS and
    Constants.STUDENT_TABLE_COLUMNS

    If they are not present in the datafile, a KeyError will be raised
    """
    column_names = get_column_names(datafile) # loads file
    
    # check if COURSES_TABLE_COLUMNS are completed contained in the column names
    for name in Constants.COURSES_TABLE_COLUMNS:
        if name not in column_names:
            raise KeyError("%s is not present in the provided datafile" % name)
            sys.exit(1)

    # check if STUDENT_TABLE_COLUMNS are completely contained in the column names
    for name in Constants.STUDENT_TABLE_COLUMNS:
        if name not in column_names:
            raise KeyError("%s is not present in the provided datafile" % name)
            sys.exit(1)

    for i in range(0, Constants.TOTAL_REQ_COUNT):
        Constants.STUDENT_TABLE_COLUMNS.append("REQ%02d" % i) # grad reqs

    if not is_table_set_up():
        create_project_table(Constants.COURSES_TABLE_COLUMNS, Constants.STUDENT_TABLE_COLUMNS)

    rows, cols = datafile.shape
    counter = 0
    print "Populating %s" % Constants.COURSES_TABLE_NAME
    print "Inserting %d rows with %d data fields each" % (rows, cols)

    student_data = {} # dictionary used to temporarily store data for students datatabe

    for row in datafile.itertuples():
        if counter % 100 == 0:
            print "Progress: %d of %d" % (counter, rows)

        data = list(row._asdict().values())[1:]
        #assert(len(data) == len(column_names))

        # FIXME THIS IS BAD BUT IDK HOW TO MAKE IT BETTER - YICHENG
        # Works for now tho
        if str(data[0]) not in student_data.keys():
            student_data[str(data[0])] = [data[1], data[2], data[3], data[4]]

        data = [data[0], data[5], data[6], data[7], data[8], data[9], data[11], data[12]]

        # Generate query
        query = "INSERT INTO %s (%s) VALUES (%s);"
        schema = (("%s , " * len(Constants.COURSES_TABLE_COLUMNS))[:-2]) % tuple(Constants.COURSES_TABLE_COLUMNS)
        values = (("'%s' , " * len(data))[:-2]) % tuple(( str(it).upper() for it in data))

        query = query % (Constants.COURSES_TABLE_NAME, schema, values)
        # print query
        SQLConnector.execute(query)
        counter += 1

    print "Done!"
    print "Begin analysis... Populating %s" % Constants.STUDENT_TABLE_NAME

    reqs = json.loads(open('../data/reqs.json', 'r').read())['grad_requirements']

    query = "SELECT DISTINCT STUDENTID FROM %s;" % (Constants.COURSES_TABLE_NAME)

    res = SQLConnector.execute(query)

    print "Inserting %d students" % (len(res))

    counter = 0

    for (osis, ) in res:

        if counter % 100 == 0:
            print "Progress: %d of %d" % (counter, len(res))

        query = "SELECT COURSE FROM %s WHERE STUDENTID = %s AND \
            ((MARK >= 65 AND MARK REGEXP '^[0-9]+$') OR MARK='P' OR MARK='C' OR \
            MARK='CR');" % (Constants.COURSES_TABLE_NAME, osis)

        r = SQLConnector.execute(query)
        if r:
            courses_passed = [course for (course,) in r]
        else:
            courses_passed = []

        req_status = []

        for requirement in reqs:
            status = False
            for option in requirement['options']:
                status = status or has_completed_track(courses_passed, option['course-code'])
                if status:
                    break
            req_status.append(str(status))

        query = "INSERT INTO %s (%s) VALUES (%s);"
        schema = (("%s, " * len(Constants.STUDENT_TABLE_COLUMNS))[:-2]) % tuple(Constants.STUDENT_TABLE_COLUMNS)
        values = (("'%s', " * len(Constants.STUDENT_TABLE_COLUMNS))[:-2]) % tuple([osis] + student_data[str(osis)] + req_status)
        query = query % (Constants.STUDENT_TABLE_NAME, schema, values)

        r = SQLConnector.execute(query)

        counter += 1


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--create",
        help="Creates the table",
        action="store_true"
    )

    parser.add_argument(
        "-d",
        "--delete",
        help="Deletes the table",
        action="store_true"
    )

    parser.add_argument(
        "-r",
        "--reset",
        help="Resets the table",
        action="store_true"
    )

    parser.add_argument(
        "-l",
        "--load",
        help="Load an Excel spreadsheet into the MySQL table",
        action="append"
    )

    parser.add_argument(
        "-t",
        "--test",
        help="Prints True if the table is set up, False otherwise",
        action="store_true"
    )

    args = parser.parse_args()

    if args.create:
        create_project_table(Constants.COURSES_TABLE_COLUMNS, Constants.STUDENT_TABLE_COLUMNS)
    elif args.delete:
        delete_project_table()
    elif args.reset:
        reset_project_table()

    if args.test:
        print(is_table_set_up())

    if args.load == None:
        return
    else:
        for f in args.load:
            load_excel_file(get_excel(f))

if __name__ == "__main__":
    main()

