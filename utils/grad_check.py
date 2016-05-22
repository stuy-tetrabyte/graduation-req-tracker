import database
import json
from database import DBManager
import Constants

reqs = json.loads(open('../data/reqs.json','r').read())['grad_requirements']
db_m = DBManager(Constants.PROJECT_DB_NAME, Constants.COURSES_TABLE_NAME)

def has_completed_track(passed_courses, track_reqs):
    """
    has_completed_track: checks if the list of passed courses completes the
    track requirements

    Args:
        passed_courses (list of tuples of ('code', 'mark')): a student's
            passed courses
	track_reqs (list of strings): list of required courses to complete a
            certain track
    
    Returns:
        a boolean value indicating if the list of passed courses completes the
        track requirements
    """

    relevent_courses_taken = []
    status = True

    for semester in track_reqs:
        fufilled = False

        for i in range(0, len(passed_courses)):
            if (passed_courses[i][0] in semester):
                passed_courses.pop(i)
                fufilled = True
                break

        status = status 
        
        if (not fufilled):
            return False

    return True

def requirements_met(OSIS):
    """
    requirements_met: returns a list containing dict objects of the various graduation requirements.

    Args:
        OSIS (string): 9 digit id of student to check
    Returns:
        List of dicts of grade requirements and completion status
        ex:
        [
            {
                "name": "Art Appreciation",
                "completed" : True,
                "courses_taken" : [<list of courses taken in this field>],
                "possible_tracks" : [
                    [<list of courses that will fufill this in 1 term>],
                    [<list of courses that will fufill this in 2 terms>],
                    ...
                ]
            },
            {
                "name": "Music Appreciation",
                "completed" : False,
                "courses_taken" : [<list of courses taken in this field>],
                "possible_tracks" : [
                    [<list of courses that will fufill this in 1 term>],
                    [<list of courses that will fufill this in 2 terms>],
                    ...
                ]
            },
            . . .
        ]
    """
    studnet_info = db_m.get_student_info(OSIS)
    ret = []

    for requirement in reqs:
        req_status = {'name': requirement['name'], 'completed': False}
        for option in requirement['options']:
            req_status['completed'] = req_status['completed'] or has_completed_track(studnet_info['passed_courses'], option['course-code'])
        ret.append(req_status)

    return ret

def check_grade_status(grade):
    """
    check_grade_status: checks the status of all the students in an entire grade

    Args:
        grade (int): the specified grade
    
    Returns:
        a list of student status dictionaries as specified above
    """
    student_info = db_m.get_grade_info(grade)
    ret = []

# TODO ASSIGN LOREN

    
if __name__ == '__main__':
    print requirements_met('701116515')
