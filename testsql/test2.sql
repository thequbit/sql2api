create database if not exists testdb2;

create table if not exists users ( userid int not null auto_increment primary key, username text not null, passwordhash text not null, displayname text not null);

create table if not exists facts (

factid int not null auto_increment primary key,
fact text not null,
userid int not null,
foreign key (userid) references users(userid)

)
;

create table if not exists hits( hitid int not null auto_increment primary key, ipaddress text not null, hitdt datetime not null);
