import shutil
import os

def createpython(sqlfile,dbname,tables):

    print "[INFO] Generating Python Files ..."

    # create the python directory where everything will go
    if not os.path.exists("./{0}/python".format(dbname)):
        os.makedirs("./{0}/python".format(dbname))
        os.makedirs("./{0}/python/models".format(dbname))

    # read in our python template that will be used to create our table
    # accessors
    with open("./templates/python/model.template","r") as f:
        base = f.read()
        f.close()

    # create our default config file with the correct database name in it
    config = ""
    fn = "./{0}/python/models/config.ini".format(dbname)
    with open(fn,"w") as f:
        config += "[sql2api]\n"
        config += "username=\n"
        config += "password=\n"
        config += "database={0}\n".format(dbname)
        config += "server=\n"
        f.write(config)
        f.close()
    print "[INFO] \t{0}".format(fn)

    # fill in our table accessor template with the correct data
    model_imports = "\n"
    for table in tables:
        table_name,columns = table;

        camel_table_name = "{0}{1}".format(table_name[0:1].upper(),table_name[1:])

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
        python = python.replace("<!camel_table_name!>",camel_table_name)
        python = python.replace("<!table_name!>",table_name)
        python = python.replace("<!csv_column_names!>",csv_column_names)
        python = python.replace("<!csv_no_primary_key_column_names!>",csv_no_primary_key_column_names)
        python = python.replace("<!csv_no_primary_key_column_names_sanitized!>",csv_no_primary_key_column_names_sanitized)
        python = python.replace("<!insert_value_string!>",insert_value_string)
        python = python.replace("<!column_name_primary_key!>",column_name_primary_key)
        python = python.replace("<!column_name_primary_key_sanitized!>",column_name_primary_key_sanitized)
        python = python.replace("<!update_value_string!>",update_value_string)

        fn = "./{0}/python/models/{1}.py".format(dbname,camel_table_name)
        with open(fn,"w") as f:
            f.write(python)
            f.close()
        print "[INFO] \t{0}".format(fn)
        
        model_imports += "import {0}\n".format(table_name)

    with open("./templates/python/__init__.template","r") as f:
        init = f.read()
        f.close()
    init = init.replace("<!model_imports!>",model_imports)
    fn = "./{0}/python/models/__init__.py".format(dbname)
    with open(fn,"w") as f:
        f.write(init)
        f.close()
    print "[INFO] \t{0}".format(fn)

    #shutil.copy2(sqlfile, "./{0}/python/models/definition.sql".format(dbname))

    return python

