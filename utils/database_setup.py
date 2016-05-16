import pandas
import argparse
import SQLConnector
import Constants

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

def is_table_set_up():
    """
    Returns True if this project's MySQL table is set up, False otherwise
    """
    retval = SQLConnector.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='test' and table_name='mytable';")
    retval = [ str(s) for s in retval ]
    return len(retval) == 1

def create_project_table(column_names):
    """
    Sets up MySQL with a table with a set schema given a list of column_names.
    Does nothing if the table is already set up.

    Params:
        column_names - A list of strings containing column names

    Returns:
        None
    """
    # Tons of format strings!
    query = "CREATE TABLE IF NOT EXISTS %s (%s);"
    # Sanitize the column names
    column_names = [ s.replace(" ", "_") for s in column_names ]
    schema = (("%s VARCHAR(64), " * len(column_names))[:-2]) % tuple(column_names)
    query = query % (Constants.PROJECT_TABLE_NAME, schema)
    SQLConnector.execute(query)

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

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--create",
        help="Creates the table",
        action="store_true"
    )

    parser.add_argument(
        "-d",
        "--delete",
        help="Deletes the table",
        action="store_true"
    )

    parser.add_argument(
        "-r",
        "--reset",
        help="Resets the table",
        action="store_true"
    )

    parser.add_argument(
        "-l",
        "--load",
        help="Load an Excel spreadsheet into the MySQL table",
        action="append"
    )

    parser.add_argument(
        "-t",
        "--test",
        help="Prints True if the table is set up, False otherwise",
        action="store_true"
    )

    args = parser.parse_args()

    if args.create:
        df = get_excel("../sample_data/grad_req.xlsx")
        create_project_table(get_column_names(df))
    elif args.delete:
        delete_project_table()
    elif args.reset:
        reset_project_table()

    if args.test:
        print(is_table_set_up())

    if args.load == None:
        return
    else:
        for f in args.load:
            load_excel_file(f)

if __name__ == "__main__":
    main()

