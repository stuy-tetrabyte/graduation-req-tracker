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

    def __init__(self, db_name, course_table_name):
        self.conn = Connection(db_name)
        self.course_table = course_table_name


    def get_student(self, OSIS):
        """
        get_student: returns a dictionary of the student with the given osis and all of the courses they've taken

        Args: 
            OSIS (string): 9 digit id of the student in quesiton
        Returns:
            Dict with student info and courses 
            ex : {
                    'name': "Student Name",
                    'OSIS': "123456789",
                    'grade': 12,
                    'passed_courses' : [<list of passed courses>],
                    'failed_courses' : [<list of failed courses>]
                }

            the courses are stored as tuples of (<course code>, <mark received>)
        """

        q = 'SELECT FIRSTNAME, LASTNAME, GRADE FROM %s WHERE STUDENTID = %s' % (self.course_table, OSIS)
        res = self.conn.execute(q)

        if (len(res) == 0):
            return None

        student_info = {
            'name': res[0][0] + ' ' + res[0][1],
            'OSIS': OSIS,
            'grade': res[0][2]
        }

        q = 'SELECT COURSE, MARK, TERM, YEAR FROM %s WHERE STUDENTID = %s AND MARK >= 65 ORDER BY YEAR, TERM ASC' % (self.course_table, OSIS)
        res = self.conn.execute(q)
        passed_courses = []
        if (res):
           for item in res:
                passed_courses.append((item[0], item[1]))


        q = 'SELECT COURSE, MARK, TERM, YEAR FROM %s WHERE STUDENTID = %s AND MARK < 65 ORDER BY YEAR, TERM ASC' % (self.course_table, OSIS)
        res = self.conn.execute(q)

        failed_courses = []
        if (res):
           for item in res:
               failed_courses.append((item[0], item[1]))

        student_info['passed_courses'] = passed_courses
        student_info['failed_courses'] = failed_courses

        return student_info

if __name__ == '__main__':
    db_m = DBManager(Constants.PROJECT_DB_NAME, Constants.PROJECT_TABLE_NAME)
    print db_m.get_student('701116533')

