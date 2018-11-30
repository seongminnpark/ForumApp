drop database if exists test1;
create database test1;
use test1;

drop table if exists `user`;
create table IF NOT EXISTS `user` (
	user_id int(10) NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    email varchar(255) NOT NULL unique,
    password_hash varchar(255) NOT NULL,
    token varchar(255) NOT NULL,
    is_admin int(1) NOT NULL,
    avatar_id int(10) NOT NULL,
    date_joined datetime default now(),
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

drop table if exists `report`;
create table IF NOT EXISTS `report` (
	report_id int(10) NOT NULL AUTO_INCREMENT,
	reporter_id int(10) NOT NULL,
    post_id int(10) ,
	report_time datetime NOT NULL,
    content TEXT,
    active int(1) default 1 NOT NULL,
    primary key (report_id),
    foreign key (reporter_id) references `user`(user_id),
    foreign key (post_id) references `post`(post_id) ON DELETE CASCADE
);

drop table if exists `ban`;
create table IF NOT EXISTS `ban` (
    ban_id int(10) NOT NULL AUTO_INCREMENT, 
	banned_id int(10) NOT NULL unique,
    banner_id int(10) NOT NULL,
    report_id int(10) NOT NULL,
    ban_time datetime NOT NULL,
    active int(1) default 1 NOT NULL,
    primary key (ban_id),
    foreign key (banned_id) references `user`(user_id),
	foreign key (banner_id) references `user`(user_id),
    foreign key (report_id) references `report`(report_id)
);

drop table if exists `report_reason`;
create table IF NOT EXISTS `report_reason` (
    reason_id int(10) NOT NULL AUTO_INCREMENT,
    description varchar(255) NOT NULL unique,
    primary key (reason_id)
);

drop table if exists `report_has_reason`;
create table IF NOT EXISTS `report_has_reason` (
	report_id int(10) NOT NULL,
    reason_id int(10) NOT NULL,
    primary key (report_id, reason_id),
    unique(report_id, reason_id),
    foreign key (report_id) references `report`(report_id) ON DELETE CASCADE,
    foreign key (reason_id) references `report_reason`(reason_id)
);
    
-- Add post categories.
INSERT INTO category (name)
VALUES ("Announcement");

INSERT INTO category (name)
VALUES ("Discussion");

INSERT INTO category ( name)
VALUES ("Question");

INSERT INTO category ( name)
VALUES ("Guide");

-- Add report reasons.
INSERT INTO report_reason (description)
VALUES ("Vulgar");

INSERT INTO report_reason (description)
VALUES ("Advertising");

INSERT INTO report_reason (description)
VALUES ("Irrelevant");

-- Add initial users.
INSERT INTO user (name, email, password_hash, token, is_admin, avatar_id)
VALUES ('Ad Min', 'admin@admin.com', 'admin', 'admin', 1, 0);

INSERT INTO user (name, email, password_hash, token, is_admin, avatar_id)
VALUES ('User One', 'user1@user1.com', 'user1', 'user1', 0, 1);

INSERT INTO user (name, email, password_hash, token, is_admin, avatar_id)
VALUES ('User Two', 'user2@user2.com', 'user2', 'user2', 0, 2);

INSERT INTO user (name, email, password_hash, token, is_admin, avatar_id)
VALUES ('User Three', 'user3@user3.com', 'user3', 'user3', 0, 5);

-- Add initial posts.
INSERT INTO post (poster_id, category_id, title, content, post_time)
VALUES (1, 1, 'Forum is officially open!', "Write away!", "2018-10-27 12:11:12");

INSERT INTO post (poster_id, category_id, title, content, post_time)
VALUES (2, 2, 'The weather is 40 degrees', "I hope it gets warm", "2018-10-27 12:11:12");

INSERT INTO post (poster_id, category_id, title, content, post_time)
VALUES (4, 3, 'Close this forum', "Close it!", "2018-11-17 12:11:12");

-- Add initial reports.
INSERT INTO report (reporter_id, post_id, report_time, content, active)
VALUES (2, 3, '2018-08-19 12:19:28', "Stupid post", 1);

INSERT INTO report (reporter_id, post_id, report_time, content, active)
VALUES (2, 2, '2017-08-19 12:19:28', "Stupid post", 0);

-- Add initial report reasons belonging to reports.
INSERT INTO report_has_reason (report_id, reason_id)
VALUES (1, 1);

INSERT INTO report_has_reason (report_id, reason_id)
VALUES (1, 2);

INSERT INTO report_has_reason (report_id, reason_id)
VALUES (1, 3);

INSERT INTO report_has_reason (report_id, reason_id)
VALUES (2, 1);

INSERT INTO report_has_reason (report_id, reason_id)
VALUES (2, 2);

-- Add initial bans.
INSERT INTO ban (banned_id, banner_id, report_id, ban_time, active)
VALUES (3, 1, 2, "2018-10-19 10:19:28", 1);

INSERT INTO ban (banned_id, banner_id, report_id, ban_time, active)
VALUES (2, 1, 2, "2018-10-19 12:19:28", 0);