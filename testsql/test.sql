create database if exists testdb;

create table if exists users(
userid int not null auto_incremenet primary key,
username text not null,
passwordhash text not null,
firstname text not null,
lastname text not null,
dob datetime not null
);
