import database_setup
import Constants
from SQLConnector import Connection
from datetime import date

assert(database_setup.is_table_set_up())

# TODO: Create the stubs for database files
# Assignee: Loren

class DBManager:
    """
    Class to manage the student/courses database
    """

    def __init__(self, db_name, course_table_name, student_table_name):
        self.conn = Connection(db_name)
        self.course_table = course_table_name
        self.student_table = student_table_name


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
                "req_status": [list of booleans, the index of
                which corresponding to the requirement specified in
                data/reqs.json (note that the database was also generated in
                this order)]
            }
        """
        query = "SELECT * FROM %s WHERE STUDENTID='%s';"
        query = query % (self.student_table, OSIS)
        data = [ str(elem) for elem in self.conn.execute(query)[0] ]
        return {
            "osis": data[0],
            "lastn": data[1],
            "firstn": data[2],
            "grade": data[3],
            "offcl": data[4],
            "req_status": [ True if req == "True" else False for req in data[5:] ]
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
        pass

    def get_all_students_info(self):
        """
        get_all_students_info: returns a list of all the students' informations

        Args:
            None

        Returns:
            a list of dictionaries of student information as specified by the
            documentation of the get_student_info
        """
        pass

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

    def get_all_students_who_have_failed(self):
        """
        get_all_students_who_have_failed: returns a list of student
        informations for everyone who has failed a class

        Args:
            self (type): TODO

        Returns:
            a list of student information as specified by the documentation of
            get_student_info except with the extra key "failed_courses" which
            correspondes to a list of (course_code, mark) tuples of all the
            courses a student has failed
        """
        pass

if __name__ == '__main__':
    db_m = DBManager(Constants.PROJECT_DB_NAME, Constants.COURSES_TABLE_NAME,
            Constants.STUDENT_TABLE_NAME)
    #print db_m.get_student_info('701116533')
    print db_m.get_student_info('701116533')
    #print db_m.get_grade_info(9)

