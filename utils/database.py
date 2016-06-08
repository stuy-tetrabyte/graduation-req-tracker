import database_setup
from Constants import *
from SQLConnector import Connection
from datetime import date
import os, json

assert(database_setup.is_table_set_up())

global use_and

class DBManager:
    """
    Class to manage the student/courses database
    """

    def __init__(self, db_name, course_table_name, student_table_name):
        global use_and
        use_and = True
        self.conn = Connection(db_name)
        self.course_table = course_table_name
        self.student_table = student_table_name
        script_path = os.path.realpath(__file__)
        script_loc = os.path.dirname(script_path)
        self.reqs = json.loads(open(script_loc + '/../static/reqs.json', 'r').read())['grad_requirements']

    

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
            a tuple of length 2 where the first is metadata and the second is
            data. The metadata contains the names of the tracks, and the data is
            in the format of nested lists where the first list
            represents the courses already taken while the second list includes
            list suggestions for future courses. Inside each list, each
            corresponding index represents a list of course codes. which the
            student has taken (will need to take)

            Sample format:
            (
                [ # metadata
                    "name of track 1",
                    "name of track 2",
                    ...
                ],
                [ # courses passed
                    [<courses passed in track 1],
                    [<courses passed in track 2],
                    . . .
                ],
                [ # courses need to take in the future
                    [
                        [<next sem courses for track 1>],
                        [<2 next sem courses for track 1>],
                        . . .
                    ],
                    [
                        [<next sem courses for track 2>],
                        [<2 next sem courses for track 2>],
                        . . .
                    ],
                    . . .
                ]
            )
        """
        student_courses = [course for (course, name, mark)
                            in self.get_relevant_courses(OSIS, req_num)
                            if mark == 'P'
                                or mark == 'C'
                                or mark == 'CR'
                                or mark in ['A', 'B', 'C', 'D']
                                or int(mark) >= 65] # . . . passing filter

        req_tracks = self.reqs[req_num]['options']
        # according to client we want to show all options, not just the track
        # the current student is on (which is already covered by
        # 'get_relevant_courses')

        tracks = []
        passed_courses = []
        need_to_take = []

        for option in req_tracks:
            tracks.append(option['track-name'])
            student_courses_copy = student_courses[:] # make a copy
            taken = []
            still_need = []

            for semester in option['course-code']: # each semester
                need = True
                for i in range(0, len(student_courses_copy)):
                    if student_courses_copy[i] in semester:
                        taken.append(student_courses_copy.pop(i))
                        need = False
                        break # semester is fufilled if student has taken a
                              # class
                if need:
                    still_need.append(semester)

            passed_courses.append(taken)
            need_to_take.append(still_need)

        return [tracks, passed_courses, need_to_take]

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

    def get_students_such_that(self, req_status):
        """
        get_students_such_that: gets a list of all students with some set of
        graduation requirements
    
        Args:
            req_status (list): a list of specified requirement statuses in the
            following format:
            [
                [<desired status for req0, OR statement>],
                [<desired status for req1, OR statement>],
                ...
            ]

            Ex:
            [
                [0, 1],
                [0],
                [2],
                [0,1,2]
            ]
            means get all students that:
                completed or has not completed REQ0,
                completed REQ1,
                failed REQ2,
                completed, has not completed, or failed REQ3
        
        Returns:
            a list of studnet info as specified by the doc. of get_student_info
            for all the students with the specified requirement statuses
        """
        global use_and
        assert(len(req_status) == TOTAL_REQ_COUNT)

        req_cond_and = "REQ%02d IN (%s) AND "
        req_cond_or = "REQ%02d IN (%s) OR "
        q = "SELECT STUDENTID FROM %s WHERE " % (self.student_table)

        for i in range(0, TOTAL_REQ_COUNT):
            if (use_and):
                q += req_cond_and % (i, str(req_status[i])[1:-1])
            else:
                q += req_cond_or % (i, str(req_status[i])[1:-1])

        q = q[:-4] + ';' # remove the final AND

        r = self.conn.execute(q)

        if r:
            return [self.get_student_info(osis) for (osis,) in r]
        else:
            return []


    def get_relevant_courses(self, osis, req_number):
        """
        get_relevant_courses: gets all the courses a student has taken that is
        relevant to a specific requirement

        Args:
            osis (string): the studentid of the student in question
            req_number (int): requirement number

        Returns:
            a nested list where each index is a list of all the courses a
            student has taken with respect to a specific requirement number,
            each course is stored as a tuple of ('code', 'name', 'mark')
        """
        options = self.reqs[req_number]['options']
        relevant_courses = set()
        for option in options:
            for courses in option['course-code']:
                relevant_courses = relevant_courses.union(set(courses))
        relevant_courses = str([str(code) for code in relevant_courses])[1:-1]
        q = "SELECT COURSE, COURSE_TITLE, MARK FROM %s WHERE STUDENTID = '%s'\
                AND COURSE IN (%s)" % (self.course_table, osis, relevant_courses)
        r = self.conn.execute(q)
        if (r):
            return r
        else:
            return []

    def change_db_logic(self,change_to):
        """
        toggle db logic between 'AND' and 'OR'
        Args:
        change_to : string - should be either "and" or "or" and sets the db logic
        """
        global use_and
        if (change_to == 'and'):
            use_and = True
        else:
            #must be or
            use_and = False

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
    print "Test get_relevant_courses: 701113960 and MUSIC"
    print db_m.get_relevant_courses('701113960', 0), '\n'
    print "Test get_req_course_track: 701113960 and MUSIC"
    print db_m.get_req_course_track('701113960', 0), '\n'
    print "Test get_students_such_that:"
    print db_m.get_students_such_that([[0,1,2], [0,1,2], [0,1,2], [0,1,2],
        [0,1,2], [0,1,2], [0,1,2]])
