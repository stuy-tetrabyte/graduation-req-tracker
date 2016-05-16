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
        self.conn = mysql.connector.connect(user='root', password='test', database=db_name)
        self.cursor = self.conn.cursor(buffered=True)

    def execute(self, *args):
        """
        Executes a query and returns all resulting rows if available
        """
        self.cursor.execute(*args)
        retval = None
        if self.cursor.rowcount > 0:
            retval = self.cursor.fetchall()
        self.conn.commit()
        return retval

    def destroy(self):
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
    c.destroy()
    return retval

