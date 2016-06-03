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
