import sys
import argparse
import re
import os

def parse(sql):

    print "Parsing:\n\n{0}\n\n".format(sql)

    # make multiple spaces into single space
    re.sub(' +',' ',sql)

    statements = sql.split(";")

    tables = []

    for statement in statements:
        parts = statement.split(" ")

        if parts[0].lower() == "create" and len(parts) >= 2:
    
            if parts[1].lower() == "database" and len(parts) >= 3:

                dbname = parts[2].strip().replace(";","")

                print "Database Name: {0}".format(dbname)

        
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
                    
                    if "primary key" in col.lower():
                        cisprimarykey = True
                    else:
                        cisprimarykey = False

                    if cname.lower() != "foreign":
                        print "\t{0} : {1}".format(cname,ctype,cisprimarykey)
                        columns.append((cname,ctype,cisprimarykey))

                tables.append((tname,columns))

                print ""
    return (dbname,tables)

def createpython(dbname,tables):

    if not os.path.exists("python"):
        os.makedirs("python")

    for table in tables:

        with open("../templates/python.template") as f:
            python = f.read()

        (tablename,columns) = table;

        table_name = tablename

        csv_column_names = ""
        for col in columns:
            cname,ctype,ciskey = col
            csv_column_names += "{0},".format(cname)
        csv_column_names = csv_column_names[:-1] # remove last comma


        csv_no_primary_key_column_names = ""
        for col in columns:
            cname,ctype,ciskey = col
            if ciskey == False:
                csv_no_primary_key_column_names += "{0},".format(cname)
        csv_no_primary_key_column_names = csv_no_primary_key_column_names[:-1] # remove last comma

        insert_value_string = ""
        for col in columns:
            cname,ctype,ciskey = col
            if ciskey == False:
                insert_value_string += "%s,"
        insert_value_string = insert_value_string[:-1]

        column_name_primary_key = ""
        for col in columns:
            cname,ctype,ciskey = col
            if ciskey == True:
                column_name_primary_key = cname
                break

        update_value_string = ""
        for col in columns:
            cname,ctype,ciskey = col
            if ciskey == False:
                update_value_string += "{0} = %s,".format(cname)
        update_value_string = update_value_string[:-1]

        python = python.replace("<!table_name!>",table_name)
        python = python.replace("<!csv_column_names!>",csv_column_names)
        python = python.replace("<!csv_no_primary_key_column_names!>",csv_no_primary_key_column_names)
        python = python.replace("<!insert_value_string!>",insert_value_string)
        python = python.replace("<!column_name_primary_key!>",column_name_primary_key)
        python = python.replace("<!update_value_string!>",update_value_string)

        with open("./python/{0}.py".format(tablename),"w") as f:
            f.write(python)
            f.close()

        with open("./python/sqlcreds.txt","w") as f:
            f.write("host=\nusername=\npassword=\ndatabase={0}\n".format(dbname))
            f.close()

    return True

def createphp(tables):

    if not os.path.exists("php"):
        os.makedirs("php")

    for table in tables:

        with open("../templates/php.template") as f:
            php = f.read()
            f.close()

        php = php.replace();

    return php

# application entry point
if __name__ == "__main__":
    
    print "Application starting ..."

    parser = argparse.ArgumentParser(description='Process inputs.')
    parser.add_argument('sql_script', type=str, help='input sql script')

    args = parser.parse_args()

    with open(args.sql_script) as f:
        sql = f.read()

    sql = sql.replace("\r","").replace("\n","").replace("\t"," ")

    (dbname,tables) = parse(sql)

    # create a folder called the database name and change our working directory to it
    if not os.path.exists(dbname):
        os.makedirs(dbname)
    os.chdir(dbname)

    print "Tables:\n\n{0}\n\n".format(tables)

    print "Creating Python DB Layer ..."

    createpython(dbname,tables)

    print "Python:\n\n{0}\n\n".format(python)

    print "... Done."

    print "Creating PHP5 JSON API Classes ..."

    php = createphp(tables)

    print "PHP:\n\n{0}\n\n".format(php)

    print "... Done."

    os.chdir("..")

    print "Application exiting ..."

