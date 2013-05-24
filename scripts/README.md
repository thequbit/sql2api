./scripts
---------

Below is a list of the scripts that are included with the tool.  If you want to just simply create a standard output based on input SQL, then you want to use the sql2api.py script.


	sql2api.py - entry point to the sql2api tool.  This takes in SQL and spits out a number of classes that assist in database communications.

	parsesql.py - takes in sql and returns a database name and table information

	php.py - takes in database name and table info, and spits out php classes that can be used to interface with the database.  standard CRUD functions exist.  It also spits out an example json API script.

	python.py - takes in database name and table info, and spits out python classes that can be used to interface with the database.  standard CRUD functions exist.


If you find any issues with any of the above scripts, please open an issue within the GitHub interface.  Enjoy!

