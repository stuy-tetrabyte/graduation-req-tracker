import database_setup
from Constants import *
from SQLConnector import Connection
from datetime import date
import os, json

assert(database_setup.is_table_set_up())

class DBManager:
    """
    Class to manage the student/courses database
    """

    def __init__(self, db_name, course_table_name, student_table_name):
        self.conn = Connection(db_name)
        self.course_table = course_table_name
        self.student_table = student_table_name
        script_path = os.path.realpath(__file__)
        script_loc = os.path.dirname(script_path)
        self.reqs = json.loads(open(script_loc + '/../data/reqs.json', 'r').read())['grad_requirements']

    def get_student_courses(self, OSIS):
        """
        get_student_courses: returns a list of the students' courses

        Args:
            OSIS (string): student ID in question

        Returns:
            returns a list of information regarding all the courses a student
            took
        """
        q = "SELECT * FROM %s WHERE STUDENTID = '%s';"
        q = q % (self.student_table, OSIS)
        data = self.conn.execute(q)
        if data:
            return data
        else:
            return []

    def get_student_info(self, OSIS):
        """
        get_student_info: returns a dictionary of the student with the given osis and all of the courses they've taken

        Args:
            OSIS (string): 9 digit id of the student in quesiton

        Returns:
            Dict with student information in the following format:
            {
                "osis": "123456789",
                "lastn": "Rachmaninoff",
                "firstn": "Sergei Vasilievich",
                "grade": "12",
                "offcl": "7CC",
                "req_status": [list of status codes as specified in
                py, the index of
                which corresponding to the requirement specified in
                data/reqs.json (note that the database was also generated in
                this order)]
            }
        """
        query = "SELECT * FROM %s WHERE STUDENTID='%s';"
        query = query % (self.student_table, OSIS)
        query_res = self.conn.execute(query)
        if not query_res: # if query_res == None
            return None
        data = [ str(elem) for elem in query_res[0] ]
        return {
            "osis": data[0],
            "lastn": data[1],
            "firstn": data[2],
            "grade": data[3],
            "offcl": data[4],
            "req_status": [ int(n) for n in data[5:] ]
        }

    def get_grade_info(self, grade):
        """
        get_grade_info: return a list of all the student's information within a
        certain grade

        Args:
            grade (int): the specified grade who's information one is querying

        Returns:
            a list of dictionaries of all the informations of all the students
            within the specified grade, in the same format as the return type
            for get_student_info
        """
        grade_query = "SELECT * FROM %s WHERE GRADE=%d;"
        grade_query = grade_query % (self.student_table, grade)
        studentlist = self.conn.execute(grade_query)
        if not studentlist: # if studentlist == None
            return None
        dict_list = []
        for student in studentlist:
            data = [ str(elem) for elem in student ]
            dict_list.append({
                "osis": data[0],
                "lastn": data[1],
                "firstn": data[2],
                "grade": data[3],
                "offcl": data[4],
                "req_status": [ int(n) for n in data[5:] ]
            })
        return dict_list

    def get_all_students_info(self):
        """
        get_all_students_info: returns a list of all the students' informations

        Args:
            None

        Returns:
            a list of dictionaries of student information as specified by the
            documentation of the get_student_info
        """
        dict_list = []
        for i in range(4):
            info = self.get_grade_info(i + 9)
            if info: # if info != None
                dict_list += info
        return dict_list

    def get_req_course_track(self, OSIS, req_num):
        """
        get_req_course_track: returns course suggestions for student to meet req

        Args:
            OSIS (string) : studentID
            req_num (int) : req to check (nums in constants.py)

        Returns:
        """
        student_courses = get_student_courses(OSIS)
        req_tracks = json.loads(open('../data/reqs.json', 'r').read())['grad_requirements'][req_num]["options"]
        track_progress = [] 
        #check if already started on any tracks
        for track in req_tracks:
            for semester in track:
                for course in semester:
                    if (course in student_courses): #also check if passed
                        track_progress.append(track)
        #then check if none started, or one completed
        #if none suggest all
        #if done suggest ?
        #if progress, suggest the rest of current track(s)

    def get_next_term_course_suggestions(self, OSIS):
        """
        get_next_term_course_suggestions: returns the courses one can take next
        term to fufill graduation requirements

        Args:
            OSIS (string): studentID of student in question

        Returns:
            a nested list of course codes, at the top level, each index
            correspondes to a graduation requirement as specified in
            data/reqs.json. Within each index, it should contain an empty list if
            the requirement has already been fufilled, or a list of tracks to
            fufill the requirement (this is subject to change, may not be the best
            idea) (may also require more than a couple of helper functions)

            Example
            [
                [["UAS11"], ["UDS11Q8", "UDS11Q8", ...], ...], # music
                [], # art
                ...
            ]
        """
        pass

    def get_all_students_failed_req(self, req_num):
        """
        get_all_students_failed_req: returns a list of student
        informations for everyone who has failed a class

        Args:
            req_num (int) : index of requirement checking against (in reqs.json)

        Returns:
            a list of student information as specified by the documentation of
            get_student_info except with the extra key "failed_courses" which
            correspondes to a list of (course_code, mark) tuples of all the
            courses a student has failed
        """
        all_students = self.get_all_students_info()
        students = [ student for student in all_students if student["req_status"][req_num] == HAS_FAILED ]
        return students

    def get_all_students_fufilled_req(self, req_num):
        """
        get_all_students_fufilled_req: gets a list of student information for
        everyone who has fufilled a requirement
    
        Args:
            req_num (type): TODO
        
        Returns:
            a list of student ifnromation as specified by the documentation of
            get_student_info for all the students who have fufilled a
            requirement
        """
        all_students = self.get_all_students_info()
        students = [ student for student in all_students if student['req_status'][req_num] == COMPLETED ]
        return students

    def get_all_students_need_req(self, req_num):
        """
        get_all_students_need_req: gets a list of student information for
        everyone who still needs to fufill a requirement
    
        Args:
            req_num (type): TODO
        
        Returns:
            a list of student information as specified by the doc. of
            get_student_info for all the students who still need to fufill the
            specified requirement either by failing a req. class or not
            taking the req class yet
        """
        all_students = self.get_all_students_info()
        students = [ student for student in all_students
                if student['req_status'][req_num] != COMPLETED ]
        return students

    def get_all_can_graduate(self):
        """
        get_all_can_graduate: gets a list of all students who have fufilled all
        graduation requirements
    
        Args:
            None
        
        Returns:
            a list of student info as specified by the doc. of
            get_student_info for all the students who can graduate (fufilled
            all requirements)
        """
        condition = ""
        for i in range(TOTAL_REQ_COUNT):
            condition += "REQ%02d = '%d' AND " % (i, COMPLETED)
        condition = condition[:-5]
        q = "SELECT STUDENTID FROM %s WHERE %s" % (self.student_table, condition)
        res = self.conn.execute(q)
        if res:
            return [self.get_student_info(osis) for (osis,) in res]
        else: # nobody can graduate :(
            return []

    def get_relevent_courses(self, osis, req_number):
        """
        get_relevent_courses: gets all the courses a student has taken that is
        relevent to a specific requirement
    
        Args:
            osis (string): the studentid of the student in question
            req_number (int): requirement number
        
        Returns:
            a nested list where each index is a list of all the courses a
            student has taken with respect to a specific requirement number,
            each course is stored as a tuple of ('code', 'name', 'mark')
        """
        options = self.reqs[req_number]['options']
        relevent_courses = set()
        for option in options:
            for courses in option['course-code']:
                relevent_courses = relevent_courses.union(set(courses))
        relevent_courses = str(tuple(relevent_courses))
        q = "SELECT COURSE, COURSE_TITLE, MARK FROM %s WHERE STUDENTID = %s\
                AND COURSE IN (%s)" % (self.course_table, osis, relevent_courses)
        r = self.conn.execute(q)
        if (r):
            return r
        else:
            return []

if __name__ == '__main__':
    db_m = DBManager(PROJECT_DB_NAME, COURSES_TABLE_NAME,
            STUDENT_TABLE_NAME)
    print "Test get_students_info: 701113960"
    print db_m.get_student_info('701113960'), "\n"
    print "Test get_grade_info: 12"
    print db_m.get_grade_info(12), "\n"
    print "Test get_all_students_info:"
    print db_m.get_all_students_info(), "\n"
    print "Test get_all_students_failed_req: Drafting"
    print db_m.get_all_students_failed_req(3), "\n"
    print "Test get_all_students_fufilled_req: Art"
    print db_m.get_all_students_fufilled_req(1), '\n'
    print "Test get_all_students_need_req: 10-Tech"
    print db_m.get_all_students_need_req(5), '\n'
    print "Test get_all_can_graduate:"
    print db_m.get_all_can_graduate(), '\n'

