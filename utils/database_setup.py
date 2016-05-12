import pandas
import argparse

def get_excel(filepath):
    """
    Returns a Pandas datafile that contains the contents of a Microsoft Excel
    Spreadsheet

    Params:
        filepath - A string containing the path to the file

    Returns:
        A Pandas datafile
    """
    return pandas.read_excel(filepath)

def get_column_names(datafile):
    """
    Returns a list containing the column names of a Pandas datafile as Python
    strings

    Params:
        datafile - A Pandas datafile

    Returns:
        A list of strings
    """
    return [ str(s) for s in datafile.columns ]

def check_if_mysql_installed():
    """
    Verifies if MySQL is installed on the current system. Will throw an
    error if MySQL fails to run
    """
    pass

def is_table_set_up():
    """
    Returns True if this project's MySQL table is set up, False otherwise
    """
    pass

def create_project_table(column_names):
    """
    Sets up MySQL with a table with a set schema given a list of column_names.
    Does nothing if the table is already set up.

    Params:
        column_names - A list of strings containing column names

    Returns:
        None
    """
    pass

def delete_project_table():
    """
    Deletes the table in MySQL that this project uses. Will do nothing if the
    table does not yet exist.
    """
    pass

def reset_project_table():
    """
    Resets the table for this project by calling 'delete' and 'setup'
    """
    delete_project_table()
    create_project_table()

def load_excel_file(datafile):
    """
    Takes a Pandas datafile and inserts the data into the project's MySQL table.
    If the project's table is not yet created, this function will call 'create'.
    """
    if not is_table_set_up():
        create_project_table()
    # TODO: Fill in this part

