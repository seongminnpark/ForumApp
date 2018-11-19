drop database if exists test1;
create database test1;
use test1;

drop table if exists admins;
create table IF NOT EXISTS admins (
	aid int(10) NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    _password varchar(255) NOT NULL,
    _email varchar(255) NOT NULL unique,
    primary key (aid)
    );


drop table if exists users;
create table IF NOT EXISTS users (
	uid int(10) NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    _password varchar(255) NOT NULL,
    _email varchar(255) NOT NULL unique,
    primary key (uid)
    );
    

drop table if exists topics;
create table IF NOT EXISTS topics (
    tid int(10) NOT NULL AUTO_INCREMENT,
    topic varchar(255) NOT NULL unique,
    _description varchar(255),
    parent_id int(10),
    primary key (tid)
    );
    
drop table if exists posts;
create table IF NOT EXISTS posts (
	pid int(10) NOT NULL AUTO_INCREMENT, 
    uid int(10) NOT NULL,
    tid int(10) NOT NULL,
    title  varchar(255) NOT NULL,
    content varchar(255) NOT NULL,
    post_time timestamp default now(),
    primary key (pid),
    foreign key (uid) references users(uid),
    foreign key (tid) references topics(tid)
    );
    
drop table if exists comments;
create table IF NOT EXISTS comments (
	cid int(10) NOT NULL AUTO_INCREMENT, 
    uid int(10) NOT NULL,
    pid int(10) NOT NULL,
    father_id int(10),
    content varchar(255) NOT NULL,
    post_time datetime NOT NULL,
    primary key (cid),
    foreign key (uid) references users(uid),
    foreign key (pid) references posts(pid) ON DELETE CASCADE,
    foreign key (father_id) references comments(cid) ON DELETE CASCADE
    );

drop table if exists bans;
create table IF NOT EXISTS bans (
    bid int(10) NOT NULL AUTO_INCREMENT, 
	uid int(10) NOT NULL unique,
    post_time datetime NOT NULL,
    aid int(10) NOT NULL,
    content varchar(255) NOT NULL,
    primary key (bid),
    foreign key (uid) references users(uid),
	foreign key (aid) references admins(aid)
    );

drop table if exists likes;
create table IF NOT EXISTS likes (
	lid int(10) NOT NULL auto_increment,
	uid int(10) NOT NULL,
    pid int(10) NOT NULL,
	post_time datetime NOT NULL,
    primary key (lid),
    unique(uid, pid),
    foreign key (pid) references posts(pid) ON DELETE CASCADE,
    foreign key (uid) references users(uid)
    );

drop table if exists reports;
create table IF NOT EXISTS reports (
	rid int(10) NOT NULL AUTO_INCREMENT,
	reporter int(10) NOT NULL,
    reported int (10) NOT NULL,
    pid int(10) ,
	cid int(10) , 
	post_time datetime NOT NULL,
    primary key (rid),
    foreign key (reporter) references users(uid),
    foreign key (reported) references users(uid),
    foreign key (pid) references posts(pid) ON DELETE CASCADE,
	foreign key (cid) references comments(cid) ON DELETE CASCADE
    );
 
