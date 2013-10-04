import distutils.core
import os

def createphp(dbname,tables):

    print "[INFO] Generating PHP Files ..."

    php = ""

    if not os.path.exists("./{0}/php".format(dbname)):
        os.makedirs("./{0}/php".format(dbname))

    apifn = "./{0}/php/getall.php".format(dbname)
    apifile = open(apifn,"w")
    apifile.write(
"""
<?\n
\trequire_once("DatabaseTool.class.php");

\t$from = $_GET["from"];

\tswitch($from)
\t{

\t\tdefault:
\t\t\techo "{}";
\t\t\tbreak;

"""
                 )

    basephp = ""
    with open("./templates/php/php.template") as f:
        basephp = f.read()
        f.close()

    for table in tables:

        php = basephp

        (table_name,columns) = table;

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

        update_value_string = ""
        for col in columns:
            cname,ctype,ciskey = col
            if ciskey == False:
                update_value_string += "{0} = ?,".format(cname)
        update_value_string = update_value_string[:-1] # remove last comma

        update_s_string = ""
        for col in columns:
            cname,ctype,ciskey = col
            update_s_string += "s"

        php = php.replace("<!table_name!>",table_name)
        php = php.replace("<!camel_table_name!>",camel_table_name)
        php = php.replace("<!csv_no_primary_key_column_names!>",csv_no_primary_key_column_names)
        php = php.replace("<!phpafied_column_names!>",phpafied_column_names)
        php = php.replace("<!insert_value_string!>",insert_value_string)
        php = php.replace("<!insert_s_string!>",insert_s_string)
        php = php.replace("<!array_contents!>",array_contents)
        php = php.replace("<!column_name_primary_key!>",column_name_primary_key)
        php = php.replace("<!update_value_string!>",update_value_string)
        php = php.replace("<!update_s_string!>",update_s_string)

        apifile.write(
"""
\t\tcase \"{0}\":
\t\t\trequire_once(\"{1}Manager.class.php\");
\t\t\t$mgr = new {1}Manager();
""".format(table_name,camel_table_name)
                     )

        apifile.write(
"""
\t\t\techo json_encode($mgr->getall());

\t\t\tbreak;
"""                  );

        fn = "./{0}/php/{1}Manager.class.php".format(dbname,camel_table_name)
        with open(fn,"w") as f:
            f.write(php)
            f.close()
        print "[INFO] \t{0}".format(fn)

    fn = "./{0}/php/sqlcredentials.php".format(dbname)
    with open(fn,"w") as f:
        f.write("<?php\n")
        f.write("\tdefine('MYSQL_HOST','');\n")
        f.write("\tdefine('MYSQL_USER','');\n")
        f.write("\tdefine('MYSQL_PASS','');\n")
        f.write("\tdefine('MYSQL_DATABASE','{0}');\n".format(dbname))
        f.write("?>\n")
        f.close()
    print "[INFO] \t{0}".format(fn)
        #try:
        #shutil.copy2("./templates/php/tocopy/*", "./{0}/php/".format(dbname))
        #except:
        #    pass 

    distutils.dir_util.copy_tree("./templates/php/tocopy/", "./{0}/php/".format(dbname))

    apifile.write("\t}\n\n?>")

    apifile.close()
    print "[INFO] \t{0}".format(apifn)

    return php

