drop table if exists todos;

create table entries( id integer primary key autoincrement, title text not null, text text not null);
create table todos( id integer primary key autoincrement, title text not null, done integer not null);
