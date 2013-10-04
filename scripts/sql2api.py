import sys
import os

from parsesql import parsesql
from php import createphp
from python import createpython

def main(argv):

    if len(argv) != 2:
        print "\nUsage:\n\tpython sql2api.py <file.sql>\n\n"
        return

    filename = argv[1]

    # open the sql script
    with open(filename) as f:
        sql = f.read()

    # some pre-processing
    sql = sql.replace("\r","").replace("\n","").replace("\t"," ")
    
    # parse the SQL into the database name and all of the table names/types/keys
    (dbname,tables) = parsesql(sql)

    # create a folder called the database name and change our working directory to it
    if not os.path.exists(dbname):
        os.makedirs(dbname)
    #os.chdir(dbname)


    #
    # generate output scripts
    #

    # generate python classes to interface to the DB
    python = createpython(filename,dbname,tables)

    # generate php classes to interface to the DB
    php = createphp(dbname,tables)


    # return us to the original calling directory
    os.chdir("..")

    print "\nApplication exiting ...\n"

if __name__ == '__main__': sys.exit(main(sys.argv))
