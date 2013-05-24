sql2api
=======

A tool that will take in sql, and spit out python and php code for quick API generation.

This tool takes in SQL scripts and spits out (currently) python classes and php classes to help streamline the generation of simple to use web API's.  The steps between getting database data out of the database and onto the web via simple JSON API's can sometimes be challenging, and time consuming.  This tool's objective is to simplify that process.

	Usage:
	> python generate.py <file.sql>

The tool pulls template files from the ./templates directory and uses them to generate the output scripts.  Modifying those templates will allow you to quickly, and simply add 'base line' functionality to your API system.

Example: a stupidly simple blog database (entries and comments).

First, we create our sql that creates our database and tables within it:

	create database myblog;

	create table entries(
	entryid int not null auto_increment primary key,
	entrytext text not null,
	entrydt datetime not null
	);

	create table comments(
	commentid int not null auto_increment primary key,
	commenttext text not null,
	entryid int not null,
	foreign key (entryid) references entries(entryid)
	);
	
Now that we have defined our database structure, we can pass it into sql2api's generate.py script, and it will generate some python classes so we can interface to the database, as well as some php code that will serv up json's of the data within the database.

$ python generate.py myblog.sql
Application starting ...

[INFO] Parsing SQL ...
[INFO] Database Name: myblog
[INFO] Found Table: entries
[INFO] Found Table: comments
[INFO] Generating Python Classes ...
[INFO] Generating PHP Classes ...

Application exiting ...

$

The script generated the following files:

	./myblog/php/CommentManger.class.php
	./myblog/php/DatabaseTool.class.php
	./myblog/php/EntriesManager.class.php
	./myblog/php/getall.php
	./myblog/php/sqlcredentials.php
	./myblog/python/comments.py
	./myblog/python/entries.py
	./myblog/python/sqlcreds.txt

These files are generated using the nomenclatures within the SQL that were passed into the script.  All naming conventions are carried through across all generated files.

NOTE: you *must* edit sqlcredentials.php and sqlcreds.txt to add your specific SQL credentials.  (todo: I will add grant keyword parsing to parse() function within generate.py at some point)


PHP
---
The php files that are generated are very easy to use, and are class based.  Let's look at the CommentManager.class.php file, five functions were auto generated:

	class CommentsManager
	{
		function add($commenttext,$entryid);
		function get($commentid);
		function getall();
		function del($commentid);
		function update(); // not implemented at this time
	}
	
These functions within the Comments Manager class can be called as such:

	// include the comments manager class
	require_once("CommentsManager.class.php");
	
	// get the entry id from the URL
	$entryid = $_GET['entryid'];
	
	// add the comment to the blog entry
	$mgr = new CommentsManager();
	$mgr->add("This blog is awesome!",$entryid);
	
	// report success
	echo "Succes!";
	
Python
------
The python files that are generated are intended to be used with additional python scripts that are generating data or pulling in data from other places.  They can also be used with python web frame works such as DJango or Flask.

Looking at the comments.py file, this is what is created:

	class comments:

		def __init__(self,configfile):
		def add(self,commenttext,entryid):
		def get(self,commentid):
		def getall(self):
		def delete(self,commentid):
		def update(self,commentid,commenttext,entryid):

This class can be used very simply as follows:

	from comments import comments

	def add_comment(entryid):
		c = comments('sqlcreds.txt')
		comments.add("This blog is awesome!",entryid)
		return True

If you would like additional languages/templates supported please let me know, or pull request your own!