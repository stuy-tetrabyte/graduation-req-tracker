import database_setup
import Constants
from SQLConnector import Connection

assert(database_setup.is_table_set_up())

# TODO: Create the stubs for database files
# Assignee: Loren



def get_student(OSIS):
    """
        get_student: returns a dictionary of the student with the given osis and all of the courses they've taken

        Args: 
                OSIS (string): 9 digit id of the student in quesiton
        Returns:
                Dict with student info and courses 
                ex : {
                        name: "Student Name",
                        OSIS: "123456789",
                        term_1 : [ABC21, etc],
                        term_2 : [ABC21, etc],
                        term_3 : [ABC21, etc],
                        etc
                }
    """

    c = Connection(Constants.PROJECT_DB_NAME)
    res = c.execute('SELECT FIRSTNAME, LASTNAME, COURSE, GRADE, YEAR FROM %s WHERE STUDENTID = %s ORDER BY YEAR DESC' % (Constants.PROJECT_TABLE_NAME, OSIS))
    student = {
        name: "%s %s" % (res[0][0], res[0][1])
    }
    print res

if __name__ == '__main__':
    get_student('701111528')

