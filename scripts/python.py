import shutil
import os

def createpython(sqlfile,dbname,tables):

    print "[INFO] Generating Python Scripts ..."

    # create the python directory where everything will go
    if not os.path.exists("python"):
        os.makedirs("python")
        os.makedirs("./{0}/python/models".format(dbname))

    # read in our python template that will be used to create our table
    # accessors
    with open("./templates/python/model.template","r") as f:
        base = f.read()
        f.close()

    # create our default config file with the correct database name in it
    config = ""
    with open("./{0}/python/models/config.ini".format(dbname),"w") as f:
        config += "[sql2api]\n"
        config += "username=\n"
        config += "password=\n"
        config += "database={0}\n".format(dbname)
        config += "server=\n"
        f.write(config)
        f.close()

    # fill in our table accessor template with the correct data
    model_imports = "\n"
    for table in tables:
        table_name,columns = table;

        # set our base template
        python = base

        # generate python code to be intersted into the template
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
                column_name_primary_key_sanitized = "self.__sanitize({0})".format(cname)
                break

        update_value_string = ""
        for col in columns:
            cname,ctype,ciskey = col
            if ciskey == False:
                update_value_string += "{0} = %s,".format(cname)
        update_value_string = update_value_string[:-1]

 
        # replace all of the template variables with the generated python code
        python = python.replace("<!table_name!>",table_name)
        python = python.replace("<!csv_column_names!>",csv_column_names)
        python = python.replace("<!csv_no_primary_key_column_names!>",csv_no_primary_key_column_names)
        python = python.replace("<!csv_no_primary_key_column_names_sanitized!>",csv_no_primary_key_column_names_sanitized)
        python = python.replace("<!insert_value_string!>",insert_value_string)
        python = python.replace("<!column_name_primary_key!>",column_name_primary_key)
        python = python.replace("<!column_name_primary_key_sanitized!>",column_name_primary_key_sanitized)
        python = python.replace("<!update_value_string!>",update_value_string)

        with open("./python/models/{0}.py".format(table_name),"w") as f:
            f.write(python)
            f.close()
        
        model_imports += "import {0}\n".format(table_name)

    with open("./{0}/templates/python/__init__.template".format(dbname),"r") as f:
        init = f.read()
        f.close()
    init = init.replace("<!model_imports!>",model_imports)
    with open("./{0}/python/models/__init__.py".format(dbname),"w") as f:
        f.write(init)
        f.close()

    shutil.copy2(sqlfile, "./{0}/python/models/definition.sql".format(dbname))
    
    print "[INFO] Done."

    return python

