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
                    'courses': [
                        [<term 1 courses>],
                        [<term 2 courses>],
                        ...
                        [<term n courses>]
                    ]
                }
        """

        q = 'SELECT FIRSTNAME, LASTNAME, COURSE, MARK, GRADE, YEAR FROM %s WHERE STUDENTID = %s ORDER BY YEAR ASC' % (self.course_table, OSIS)
        res = self.conn.execute(q)

        if (len(res) == 0):
            return None

        year = int(res[0][-1])
        course_list = []
        current_term = []

        for item in res:
            if int(item[-1]) != year:
                course_list.append(current_term)
                current_term = []

            current_term.append((item[2], int(item[3])))

        student = {
            "name": "%s %s" % (res[0][0], res[0][1]),
            "OSIS": OSIS,
            "grade": int(res[0][4]),
            'courses': course_list
        }

        return student

if __name__ == '__main__':
    db_m = DBManager(Constants.PROJECT_DB_NAME, Constants.PROJECT_TABLE_NAME)
    print db_m.get_student('701111577')

