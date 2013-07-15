import MySQLdb as mdb
import _mysql as mysql
import re

class users:

    __settings = {}
    __con = False

    def __init__(self):
        configfile = "sqlcreds.txt"
        f = open(configfile)
        for line in f:
            # skip comment lines
            m = re.search('^\s*#', line)
            if m:
                continue

            # parse key=value lines
            m = re.search('^(\w+)\s*=\s*(\S.*)$', line)
            if m is None:
                continue

            self.__settings[m.group(1)] = m.group(2)
        f.close()

    def __connect():
        con = mdb.connect(host=self.__settings['host'], user=self.__settings['username'], passwd=self.__settings['password'], db=self.__settings['database'])
        return con

    def __sanitize(self,valuein):
        if type(valuein) == 'str':
            valueout = mysql.escape_string(valuein)
        else:
            valueout = valuein
        return valuein

    def add(self,username,passwordhash,firstname,lastname,dob):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO users(username,passwordhash,firstname,lastname,dob) VALUES(%s,%s,%s,%s,%s)",(self.__sanitize(username),self.__sanitize(passwordhash),self.__sanitize(firstname),self.__sanitize(lastname),self.__sanitize(dob)))
            cur.close()
            newid = cur.lastrowid
        con.close()
        return newid

    def get(self,userid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE userid = %s",(userid))
            row = cur.fetchone()
            cur.close()
        con.close()
        return row

    def getall(self):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
            cur.close()
        _users = []
        for row in rows:
            _users.append(row)
        con.close()
        return _users

    def delete(self,userid):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM users WHERE userid = %s",(userid))
            cur.close()
        con.close()

    def update(self,userid,username,passwordhash,firstname,lastname,dob):
        con = self.__connect()
        with con:
            cur = con.cursor()
            cur.execute("UPDATE users SET username = %s,passwordhash = %s,firstname = %s,lastname = %s,dob = %s WHERE userid = %s",(self.__sanitize(username),self.__sanitize(passwordhash),self.__sanitize(firstname),self.__sanitize(lastname),self.__sanitize(dob),self.__sanitize(userid)))
            cur.close()
        con.close()

##### Application Specific Functions #####

#    def myfunc():
#        con = self.__connect()
#        with con:
#            cur = son.cursor()
#            cur.execute("")
#            row = cur.fetchone()
#            cur.close()
#        con.close()
#        return row

