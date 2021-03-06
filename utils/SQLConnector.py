import mysql.connector
import Constants

class Connection:
    """
    Class to help simplify the execution of SQL queries using MySQL Connector
    """
    def __init__(self, db_name):
        """
        Sets up the MySQL connection and cursor variable
        """
        self.conn = mysql.connector.connect(user='tetrabyte', password='test', database=db_name)
        self.cursor = self.conn.cursor(buffered=True)

    def execute(self, *args):
        """
        Executes a query and returns all resulting rows if available
        """
        self.cursor.execute(*args)
        retval = None
        if self.cursor.rowcount > 0:
            try:
                retval = self.cursor.fetchall()
            except:
                retval = None
        self.conn.commit()
        return retval

    def __del__(self):
        """
        Destroys the internal variables of this class
        """
        self.conn.close()
        del self.cursor
        del self.conn

def execute(*args):
    """
    Executes a single SQL command
    """
    c = Connection(Constants.PROJECT_DB_NAME)
    retval = c.execute(*args)
    return retval

