import shutil
import os

def createpython(dbname,tables):

    print "[INFO] Generating Python Classes ..."

    python = ""

    if not os.path.exists("python"):
        os.makedirs("python")

    for table in tables:

        with open("../templates/python/python.template") as f:
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

        csv_no_primary_key_column_names_sanitized = ""
        for col in columns:
            cname,ctype,ciskey = col
            if ciskey == False:
                csv_no_primary_key_column_names_sanitized += "self.__sanitize({0}),".format(cname)
        csv_no_primary_key_column_names_sanitized = csv_no_primary_key_column_names_sanitized[:-1] # remove last comma

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
   
        column_name_primary_key_sanitized = ""
        for col in columns:
            cname,ctype,ciskey = col
            if ciskey == True:
                column_name_primary_key_sanitized = "self.__sanitize({0}".format(cname)
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
        python = python.replace("<!csv_no_primary_key_column_names_sanitized!>",csv_no_primary_key_column_names_sanitized)
        python = python.replace("<!insert_value_string!>",insert_value_string)
        python = python.replace("<!column_name_primary_key!>",column_name_primary_key)
        python = python.replace("<!column_name_primary_key_sanitized!>",column_name_primary_key_sanitized)
        python = python.replace("<!update_value_string!>",update_value_string)

        #with open("../templates/python/python.search.template") as f:
        #    search_functions = f.read()
        #
        #if 'latitude' in [x[0] for x in columns] and 'longitude' in [x[0] for x in columns]:
        #    search_function
        #
        #python = python.replace("<!search_functions!)>",search_functions)

        with open("./python/{0}.py".format(tablename),"w") as f:
            f.write(python)
            f.close()

        with open("./python/sqlcreds.txt","w") as f:
            f.write("host=\nusername=\npassword=\ndatabase={0}\n".format(dbname))
            f.close()

        try:
            shutil.copy2("../templates/python/tocopy/*", "./python") 
        except:
            continue

    return python

