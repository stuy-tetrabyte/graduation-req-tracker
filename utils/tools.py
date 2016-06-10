from json import loads
import csv
import Constants as c
import pandas as pd

def check_json(file_path):
    """
    check_json: checks if an uploaded json file is valid for the purpose of this
    project

    Args:
        file_path (string): relative path to JSON file
    
    Returns:
        True or False as to if an uploaded file is valid
    """
    try:
        reqs = loads(open(file_path, 'r').read())
    except ValueError, e:
        print "Failed on loads"
        return False

    # check if is giant JSON containing "grad_requirements"
    if "grad_requirements" not in reqs:
        print "grad_requirements not present"
        return False

    if len(reqs['grad_requirements']) != c.TOTAL_REQ_COUNT:
        return False

    for req in reqs["grad_requirements"]:
        if "name" not in req:
            print "name not in req"
            return False

        if "options" not in req:
            print "options not in req"
            return False

        for option in req["options"]:
            if "track-name" not in option:
                print "track-name not in option"
                return False

            if "course-code" not in option:
                print "course-code not in option"
                return False

            for course_code_list in option['course-code']:
                if not isinstance(course_code_list, list):
                    print "coursecode not nested list"
                    return False
                
                for course in course_code_list:
                    if not isinstance(course, unicode) and not isinstance(course, str):
                        print type(course)
                        print "elements of coursecode are not strings"
                        return False

    return True

def check_student_csv(path):
    """
    check_student_csv: returns if the file specified at the location is a
    valid student csv file

    Args:
        path (string): relative path to csv file
    
    Returns:
        True or False depending on if specified file is a valid csv
    """
    try:
        reader = csv.reader(open(path, 'rb'))
    except IOError:
        return False

    for i, rows in enumerate(reader):
        if i == 0:
            if "OSIS" in rows and "EMAIL" in rows:
                return True
        return False

def check_admin_csv(path):
    """
    check_admin_csv: returns if thefile specified at the location is a valid
    admin csv file

    Args:
        path (string): path to file
    
    Returns:
        True or False depending if specified file is a valid admin csv
    """
    try:
        reader = csv.reader(open(path, 'rb'))
    except IOError:
        print "IOError"
        return False

    for i, rows in enumerate(reader):
        if len(rows) != 1:
            print rows
            return False
        
        sides = rows[0].strip().split('@')

        if len(sides) != 2 or sides[1] != 'stuy.edu':
            print sides
            return False

    return True

def check_transcript_excel(path):
    """
    check_transcript_excel: checks if the file at the specified path is a
    valid transcript excel file

    Args:
        path (string): path to file
    
    Returns:
        True or False as to if the file is valid
    """
    try:
        df = pd.read_excel(path)
    except LookupError:
        return False

    col_names = [str(s).strip().upper().replace(" ", "_")
                    for s in df.columns]

    return col_names == ["STUDENTID", "LASTNAME", 'FIRSTNAME', 'GRADE', 'OFFCLASS', 'SCHOOL', 'YEAR', 'TERM', 'COURSE', 'COURSE_TITLE', 'INSTRUCTIONAL_LEVEL', 'MARK', 'CREDITS']
