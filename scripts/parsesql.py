import re
import sys
import os

def parsesql(sql):

    sql = sql.replace("\t","");

    sql = sql.strip()

    # make multiple spaces into single space
    re.sub(' +',' ',sql)
    sql = sql.replace('\n','')

    #print "Parsing:\n\n{0}\n\n".format(sql)

    print "[INFO] Parsing SQL ..."

    statements = sql.split(";")

#    for statement in statements:
#        print "{0}\n".format(statement)


    #return ("",[])

    #print statements

    tables = []

    for statement in statements:
 
        if statement == "":
            continue

        #print "[INFO] Working on: '{0}'".format(statement)

        statement = statement.strip()

        statement = re.sub(' +',' ',statement)

        parts = statement.split(" ")

        if parts[0].lower() == "create" and len(parts) >= 2:

            #print "Found 'create' statement"

            if parts[1].lower() == "database" and len(parts) >= 3:
                dbname = parts[-1].strip().replace(";","")
                print "[INFO] Database Name: {0}".format(dbname)

            if parts[1].lower() == "table" and len(parts) >= 3:
                firstpart = statement.split('(')[0].strip()
                #print "firstpart: '{0}'".format(firstpart)
                tname = firstpart.split(" ")[-1].strip()
                meat = statement[statement.index("(")+1:]
                #print "[INFO] Table Name: {0}".format(tname)
                columns = []
                cols = meat.split(",")
                for col in cols:
                    col = col.strip()
                    if len(col) < 5:
                        continue;

                    cname = col.split(" ")[0]
                    ctype = col.split(" ")[1]

                    if "primary key" in col.lower():
                        cisprimarykey = True
                    else:
                        cisprimarykey = False

                    if cname.lower() != "foreign" and cname.lower() != "index":
                        columns.append((cname,ctype,cisprimarykey))

                print "[INFO] Found Table: `{0}` with {1} columns".format(tname,len(columns))

                tables.append((tname,columns))

    return (dbname,tables)

