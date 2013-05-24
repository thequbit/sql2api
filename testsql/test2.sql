create database testdb2;

create table users ( userid int not null auto_incrementing primary key, username text not null, passwordhash text not null, displayname text not null);

create table facts (

factid int not null auto_increment primary key,
fact text not null,
userid int not null,
foreign key (userid) references users(userid)

)
;