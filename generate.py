import sys
import argparse
import re

def parse(sql):

    print "Parsing:\n\n{0}\n\n".format(sql)

    # make multiple spaces into single space
    re.sub(' +',' ',sql)

    statements = sql.split(";")

    tables = []

    for statement in statements:
        parts = statement.split(" ")

        if parts[0].lower() == "create" and len(parts) >= 2:
            
            if parts[1].lower() == "table" and len(parts) >= 3:
                
                tname = parts[2].split("(")[0].strip()
               
                print "{0}:".format(tname)
 
                columns = []
                
                cols = statement.split("(")[1].split(",")
                for col in cols:
                    col = col.replace(")","")
                    col = col.strip()

                    cname = col.split(" ")[0]
                    ctype = col.split(" ")[1]

                    if cname.lower() != "foreign":
                        print "\t{0} : {1}".format(cname,ctype)
                        columns.append((cname,ctype))

                tables.append((tname,columns))

                print ""

    return tables

def createpython(tables):

    pythontext = ""

    python += "import MySQLdb as mdb\nimport _mysql as mysql\n\n"

    for table in tables:

        (tname,columns) = table

        python += "def class {0}:\n\n".format(tname)

        python += "    def create(self,"

            for col in columns:

                python += "{0},".format(col)

            # remove last comma
            python = python[:-1]

        python += "):\n"

        python += "with self.__con:"

    return pythontext

def createphp(tables):

    php = ""

    return php

# application entry point
if __name__ == "__main__":
    
    print "Application starting ..."

    parser = argparse.ArgumentParser(description='Process inputs.')
    parser.add_argument('filename', type=str, help='input file name')

    args = parser.parse_args()

    with open(args.filename) as f:
        sql = f.read()

    sql = sql.replace("\r","").replace("\n","").replace("\t"," ")

    tables = parse(sql)

    print "Tables:\n\n{0}\n\n".format(tables)

    print "Creating Python DB Layer ..."

    python = createpython(tables)

    print "Python:\n\n{0}\n\n".format(python)

    print "... Done."

    print "Creating PHP5 JSON API Classes ..."

    php = createphp(tables)

    print "PHP:\n\n{0}\n\n".format(php)

    print "... Done."

    print "Application exiting ..."

