drop database if exists test1;
create database test1;
use test1;

drop table if exists `user`;
create table IF NOT EXISTS `user` (
	user_id int(10) NOT NULL AUTO_INCREMENT,
    email varchar(255) NOT NULL unique,
    password_hash varchar(255) NOT NULL,
    token varchar(255) NOT NULL,
    is_admin int(1) NOT NULL,
    primary key (user_id)
);
    
-- drop table if exists `user_role`;
-- create table IF NOT EXISTS `user_role` (
-- 	role_id int(10) NOT NULL AUTO_INCREMENT,
--     role_name varchar(255) NOT NULL unique,
--     primary key (role_id)
-- );

-- drop table if exists `user_is_role`;
-- create table IF NOT EXISTS `user_is_role` (
--     user_id int(10) NOT NULL unique,
--     role_id int(10) NOT NULL,
--     primary key (user_id),
--     foreign key (user_id) references `user`(user_id),
--     foreign key (role_id) references `user_role`(role_id)
-- );

drop table if exists `category`;
create table IF NOT EXISTS `category` (
    category_id int(10) NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL unique,
    primary key (category_id)
);
    
drop table if exists `post`;
create table IF NOT EXISTS `post` (
	post_id int(10) NOT NULL AUTO_INCREMENT, 
    poster_id int(10) NOT NULL,
    category_id int(10) NOT NULL,
    title  varchar(255) NOT NULL,
    content text NOT NULL,
    post_time datetime default now(),
    primary key (post_id),
    foreign key (poster_id) references `user`(user_id),
    foreign key (category_id) references `category`(category_id)
);
    
drop table if exists `comment`;
create table IF NOT EXISTS `comment` (
	comment_id int(10) NOT NULL AUTO_INCREMENT, 
    commenter_id int(10) NOT NULL,
    post_id int(10) NOT NULL,
    content text NOT NULL,
    post_time datetime NOT NULL,
    primary key (comment_id),
    foreign key (commenter_id) references `user`(user_id),
    foreign key (post_id) references `post`(post_id) ON DELETE CASCADE
);

drop table if exists `likes`;
create table IF NOT EXISTS `likes` (
	likes_id int(10) NOT NULL auto_increment,
	user_id int(10) NOT NULL,
    post_id int(10) NOT NULL,
	like_time datetime NOT NULL,
    primary key (likes_id),
    unique(user_id, post_id),
    foreign key (post_id) references post(post_id) ON DELETE CASCADE,
    foreign key (user_id) references user(user_id)
);

drop table if exists `ban`;
create table IF NOT EXISTS `ban` (
    ban_id int(10) NOT NULL AUTO_INCREMENT, 
	banned_id int(10) NOT NULL unique,
    banner_id int(10) NOT NULL,
    ban_time datetime NOT NULL,
    primary key (ban_id),
    foreign key (banned_id) references `user`(user_id),
	foreign key (banner_id) references `user`(user_id)
);

drop table if exists `report`;
create table IF NOT EXISTS `report` (
	report_id int(10) NOT NULL AUTO_INCREMENT,
	reporter_id int(10) NOT NULL,
    post_id int(10) ,
	reoport_time datetime NOT NULL,
    comment TEXT,
    primary key (report_id),
    foreign key (reporter_id) references `user`(user_id),
    foreign key (post_id) references `post`(post_id) ON DELETE CASCADE
);
 
