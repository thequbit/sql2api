import MySQLdb as mdb
import _mysql as mysql
import re

class users:

    __settings = {}
    __con = False

    def __init__(self,configfile):
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

        # create connection
        self.__con = mdb.connect(host=self.__settings['host'], user=self.__settings['username'], passwd=self.__settings['password'], db=self.__settings['database'])

    def add(self,username,passwordhash,firstname,lastname,dob):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("INSERT INTO users(username,passwordhash,firstname,lastname,dob) VALUES(%s,%s,%s,%s,%s)",(username,passwordhash,firstname,lastname,dob))
            cur.close()

    def get(self,userid):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("SELECT * FROM users WHERE userid = %s",(userid))
            row = cur.fetchone()
            cur.close()

    def getall(self):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
            cur.close()

        _users = []
        for row in rows:
            _users.append(row)

        return _users

    def delete(self,userid):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("DELETE FROM users WHERE userid = %s",(userid))
            cur.close()

    def update(self,userid,username,passwordhash,firstname,lastname,dob):
        with self.__con:
            cur = self.__con.cursor()
            cur.execute("UPDATE users SET username = %s,passwordhash = %s,firstname = %s,lastname = %s,dob = %s WHERE userid = %s",(username,passwordhash,firstname,lastname,dob,userid))
            cur.close()




