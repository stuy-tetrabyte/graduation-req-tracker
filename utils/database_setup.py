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
    strings. This replaces all spaces with _ and upper-cases all letters

    Params:
        datafile - A Pandas datafile

    Returns:
        A list of strings
    """
    return [ str(s).upper().replace(" ", "_") for s in datafile.columns ]

def is_table_set_up():
    """
    Returns True if this project's MySQL table is set up, False otherwise
    """
    query = "SELECT table_name FROM information_schema.tables WHERE table_schema='%s' and table_name='%s';"
    query = query % (Constants.PROJECT_DB_NAME, Constants.PROJECT_TABLE_NAME)
    retval = SQLConnector.execute(query)
    return retval != None and len(retval) == 1

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
    schema = (("%s VARCHAR(64), " * len(column_names))[:-2]) % tuple(column_names)
    query = query % (Constants.PROJECT_TABLE_NAME, schema)
    SQLConnector.execute(query)

def delete_project_table():
    """
    Deletes the table in MySQL that this project uses. Will do nothing if the
    table does not yet exist.
    """
    query = "DROP TABLE IF EXISTS %s;" % (Constants.PROJECT_TABLE_NAME,)
    SQLConnector.execute(query)

def reset_project_table():
    """
    Resets the table for this project by calling 'delete' and 'setup'
    """
    delete_project_table()
    df = get_excel("../sample_data/grad_req.xlsx")
    create_project_table(get_column_names(df))

def load_excel_file(datafile):
    """
    Takes a Pandas datafile and inserts the data into the project's MySQL table.
    If the project's table is not yet created, this function will call 'create'.
    """
    column_names = get_column_names(datafile)
    if not is_table_set_up():
        create_project_table(column_names)
    rows, cols = datafile.shape
    counter = 0
    print "Inserting %d rows with %d data fields each" % (rows, cols)
    for row in datafile.itertuples():
        if counter % 50 == 0:
            print "Progress: %d of %d" % (counter, rows)
        data = list(row._asdict().values())[1:]
        assert(len(data) == len(column_names))
        # Generate query
        query = "INSERT INTO %s (%s) VALUES (%s);"
        schema = (("%s , " * len(column_names))[:-2]) % tuple(column_names)
        values = (("'%s' , " * len(data))[:-2]) % tuple(( str(it) for it in data))
        query = query % (Constants.PROJECT_TABLE_NAME, schema, values)
        # print query
        SQLConnector.execute(query)
        counter += 1
    print "Done!"

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
            load_excel_file(get_excel(f))

if __name__ == "__main__":
    main()

