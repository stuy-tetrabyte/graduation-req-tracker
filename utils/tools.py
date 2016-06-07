from json import loads

def check_json(file_path):
    """
    check_json: checks if an uploaded json file is valid for the purpose of this
    project

    Args:
        file_path (string): relative path to JSON file
    
    Returns:
        True or False as to if an uploaded file is valid
    """
    reqs = loads(open(file_path, 'r').read())

    # check if is giant JSON containing "grad_requirements"
    if "grad_requirements" not in reqs:
        return False

    for req in reqs["grad_requirements"]:
        if "name" not in req:
            return False

        if "options" not in req:
            return False

        for option in req["options"]:
            if "course-code" not in option:
                return False

            for course_code_list in option['course-code']:
                if not isinstance(course_code_list, list):
                    return False
                
                for course in course_code_list:
                    if not isinstance(course, str):
                        return False

    return True
