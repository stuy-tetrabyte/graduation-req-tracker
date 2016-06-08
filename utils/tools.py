from json import loads
import Constants as c

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
