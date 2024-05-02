DROP DATABASE IF EXISTS user_db0;
DROP DATABASE IF EXISTS user_db1;
DROP DATABASE IF EXISTS user_db2;

DROP DATABASE IF EXISTS book_db0;
DROP DATABASE IF EXISTS book_db1;
DROP DATABASE IF EXISTS book_db2;

create database book_db0;
use book_db0;

DROP TABLE IF EXISTS book;

create table book(
book_id int primary key, 
isbn LONGTEXT,
author LONGTEXT, 
title LONGTEXT, 
publisher LONGTEXT, 
publication_year int, 
subjects LONGTEXT);

insert into book
SELECT * 
FROM total.Books
WHERE (MOD(book_id,3) = 0);


create database book_db1;
use book_db1;

DROP TABLE IF EXISTS book;

create table book(
book_id int primary key, 
isbn LONGTEXT,
author LONGTEXT, 
title LONGTEXT, 
publisher LONGTEXT, 
publication_year int, 
subjects LONGTEXT);

insert into book 
SELECT * 
FROM total.Books
WHERE (MOD(book_id,3) = 1);

create database book_db2;
use book_db2;

DROP TABLE IF EXISTS book;

create table book(
book_id int primary key, 
isbn LONGTEXT,
author LONGTEXT, 
title LONGTEXT, 
publisher LONGTEXT, 
publication_year int, 
subjects LONGTEXT);

insert into book 
SELECT * 
FROM total.Books
WHERE (MOD(book_id,3) = 2);

create database user_db0;
use user_db0;

DROP TABLE IF EXISTS users, favorite;

CREATE TABLE users (
    user_id int NOT NULL,
    PRIMARY KEY (user_id),
    user_name varchar(255) NOT NULL,
    birthday DATE,
    email varchar(255) NOT NULL,
    password varchar(255) NOT NULL
);

insert into users 
SELECT * 
FROM total.Users
WHERE (MOD(user_id,3) = 0);

CREATE TABLE favorite (    
  user_id INT NOT NULL,    
    book_id INT NOT NULL,    
    PRIMARY KEY (user_id, book_id),    
    FOREIGN KEY (user_id) REFERENCES user_db0.users(user_id)-- ,    
--  FOREIGN KEY (book_id) REFERENCES book_db0.book(book_id)
    );

insert into favorite 
SELECT F.* 
FROM total.Favorite as F, users
WHERE F.user_id = users.user_id;
		


create database user_db1;
use user_db1;

DROP TABLE IF EXISTS users, favorite;

CREATE TABLE users (
    user_id int NOT NULL,
		PRIMARY KEY (user_id),
    user_name varchar(255) NOT NULL,
    birthday DATE,
    email varchar(255) NOT NULL,
    password varchar(255) NOT NULL
);

insert into users 
SELECT * 
FROM total.Users
WHERE (MOD(user_id,3) = 1);

CREATE TABLE favorite (    
  user_id INT NOT NULL,    
    book_id INT NOT NULL,    
    PRIMARY KEY (user_id, book_id),    
    FOREIGN KEY (user_id) REFERENCES user_db1.users(user_id)-- ,    
--  FOREIGN KEY (book_id) REFERENCES book_db1.book(book_id)
    );
		
insert into favorite 
SELECT F.* 
FROM total.Favorite as F, users
WHERE F.user_id = users.user_id;
    
create database user_db2;
use user_db2;

DROP TABLE IF EXISTS users, favorite;

CREATE TABLE users (
    user_id int NOT NULL,
		PRIMARY KEY (user_id),
    user_name varchar(255) NOT NULL,
    birthday DATE,
    email varchar(255) NOT NULL,
    password varchar(255) NOT NULL
);

insert into users 
SELECT * 
FROM total.Users
WHERE (MOD(user_id,3) = 2);

CREATE TABLE favorite (    
  user_id INT NOT NULL,    
    book_id INT NOT NULL,    
    PRIMARY KEY (user_id, book_id),    
    FOREIGN KEY (user_id) REFERENCES user_db2.users(user_id)-- ,    
--  FOREIGN KEY (book_id) REFERENCES book_db2.book(book_id)
    );
		
insert into favorite 
SELECT F.* 
FROM total.Favorite as F, users
WHERE F.user_id = users.user_id;
		