import sys
import argparse
import re
import os
import shutil

def parse(sql):

    sql = sql.replace("\t","");

    sql = sql.strip()

    # make multiple spaces into single space
    re.sub(' +',' ',sql)

    #print "Parsing:\n\n{0}\n\n".format(sql)

    print "[INFO] Parsing SQL ..."

    statements = sql.split(";")

    #print statements

    tables = []

    for statement in statements:
        
        statement = statement.strip()

        parts = statement.split(" ")

        if parts[0].lower() == "create" and len(parts) >= 2:
    
            if parts[1].lower() == "database" and len(parts) >= 3:

                dbname = parts[2].strip().replace(";","")

                print "[INFO] Database Name: {0}".format(dbname)

        
            if parts[1].lower() == "table" and len(parts) >= 3:
                
                tname = parts[2].split("(")[0].strip()
               
                print "[INFO] Found Table: {0}".format(tname)
 
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
                        #print "\t{0} : {1}".format(cname,ctype,cisprimarykey)
                        columns.append((cname,ctype,cisprimarykey))

                tables.append((tname,columns))

    return (dbname,tables)

def createpython(dbname,tables):

    print "[INFO] Generating Python Classes ..."

    python = ""

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

    return python

def createphp(dbname,tables):

    print "[INFO] Generating PHP Classes ..."

    php = ""

    if not os.path.exists("php"):
        os.makedirs("php")

    apifile = open("./php/getall.php","w")
    apifile.write('<?\n\n\trequire_once("DatabaseTool.class.php");\n\n\t$from = $_GET["from"];\n\n\tswitch($from)\n\t{\n\t\tdefault:\n\t\t\techo "{}";\n\t\t\tbreak;\n\n')

    for table in tables:

        with open("../templates/php.template") as f:
            php = f.read()
            f.close()

        (tablename,columns) = table;

        table_name = tablename

        camel_table_name = "{0}{1}".format(table_name[0:1].upper(),table_name[1:])

        phpafied_column_names = ""
        for col in columns:
            cname,ctype,ciskey = col
            if ciskey == False:
                phpafied_column_names += "${0},".format(cname)
        phpafied_column_names = phpafied_column_names[:-1]

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
                insert_value_string += "?,"
        insert_value_string = insert_value_string[:-1] # remove last comma

        insert_s_string = ""
        for col in columns:
            cname,ctype,ciskey = col
            if ciskey == False:
                insert_s_string += "s"

        array_contents = ""
        for col in columns:
            cname,ctype,ciskey = col
            array_contents += "'{0}' => $row['{0}'],".format(cname)
        array_contents = array_contents[:-1] # remove last comma

        column_name_primary_key = ""
        for col in columns:
            cname,ctype,ciskey = col
            if ciskey == True:
                column_name_primary_key = cname
                break
        
        php = php.replace("<!table_name!>",table_name)
        php = php.replace("<!camel_table_name!>",camel_table_name)
        php = php.replace("<!csv_no_primary_key_column_names!>",csv_no_primary_key_column_names)
        php = php.replace("<!phpafied_column_names!>",phpafied_column_names)
        php = php.replace("<!insert_value_string!>",insert_value_string)
        php = php.replace("<!insert_s_string!>",insert_s_string)
        php = php.replace("<!array_contents!>",array_contents)
        php = php.replace("<!column_name_primary_key!>",column_name_primary_key)

        apifile.write("\t\tcase \"{0}\":\n\t\t\trequire_once(\"{1}Manager.class.php\");\n\t\t\t$mgr = new {1}Manager();\n".format(table_name,camel_table_name))
        apifile.write("\t\t\techo json_encode($mgr->getall());\n\t\t\tbreak;\n\n");

        with open("./php/{0}Manager.class.php".format(camel_table_name),"w") as f:
            f.write(php)
            f.close()

        with open("./php/sqlcredentials.php","w") as f:
            f.write("<?php\n")
            f.write("\tdefine('MYSQL_HOST','');\n")
            f.write("\tdefine('MYSQL_USER','');\n")
            f.write("\tdefine('MYSQL_PASS','');\n")
            f.write("\tdefine('MYSQL_DATABASE','{0}');\n".format(dbname))
            f.write("?>\n")
            f.close()

        shutil.copy2("../templates/DatabaseTool.class.php", "./php")

    apifile.write("\t}\n\n?>")

    return php

# application entry point
if __name__ == "__main__":
    
    print "Application starting ...\n"

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

    python = createpython(dbname,tables)

    php = createphp(dbname,tables)

    os.chdir("..")

    print "\nApplication exiting ...\n"
