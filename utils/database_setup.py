import pandas

def load_excel(filepath):
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

def set_up_mysql_schema():
    """
    Sets up MySQL with a table with a set schema
    """
    pass

