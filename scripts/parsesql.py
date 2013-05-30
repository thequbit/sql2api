import re
import sys
import os

def parsesql(sql):

    sql = sql.replace("\t","");

    sql = sql.strip()

    # make multiple spaces into single space
    re.sub(' +',' ',sql)

    #print "Parsing:\n\n{0}\n\n".format(sql)

    print "[INFO] Parsing SQL ..."

    statements = sql.split(";")

#    for statement in statements:
#        print "{0}\n".format(statement)


    #return ("",[])

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
                meat = statement[statement.index("(")+1:]
#                print "\tMeat: {0}".format(meat)
                columns = []

                cols = meat.split(",")

                for col in cols:
                    col = col.strip()
                    if len(col) < 5:
                        continue;
#                    print "\tColumn Raw: {0}".format(col)

                    cname = col.split(" ")[0]
                    ctype = col.split(" ")[1]

#                    print "\tColumn: `{0}` of type `{1}`".format(cname,ctype)

                    if "primary key" in col.lower():
                        cisprimarykey = True
                    else:
                        cisprimarykey = False

                    if cname.lower() != "foreign":
                        #print "\t{0} : {1}".format(cname,ctype,cisprimarykey)
                        columns.append((cname,ctype,cisprimarykey))

                print "[INFO] Found Table: `{0}` with {1} columns".format(tname,len(columns))

                tables.append((tname,columns))

    return (dbname,tables)

