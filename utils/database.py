import database_setup

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



