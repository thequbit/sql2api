import shutil
import os

def createphp(dbname,tables):

    print "[INFO] Generating PHP Classes ..."

    php = ""

    if not os.path.exists("php"):
        os.makedirs("php")

    apifile = open("./php/getall.php","w")
    apifile.write('<?\n\n\trequire_once("DatabaseTool.class.php");\n\n\t$from = $_GET["from"];\n\n\tswitch($from)\n\t{\n\t\tdefault:\n\t\t\techo "{}";\n\t\t\tbreak;\n\n')

    for table in tables:

        with open("../templates/php/php.template") as f:
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

        try:
            shutil.copy2("../templates/php/tocopy/*", "./php")
        except:
            continue

    apifile.write("\t}\n\n?>")

    return php

