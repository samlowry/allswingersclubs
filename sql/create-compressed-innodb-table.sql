SET GLOBAL innodb_file_per_table=1;
SET GLOBAL innodb_file_format=Barracuda;

-- Create new compressed table

CREATE TABLE i_events (
    event_id INT(11) NOT NULL AUTO_INCREMENT,
    src_event_id INT(6) NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    date_time VARCHAR(255) NOT NULL,
    date_time_html VARCHAR(70) NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    cost VARCHAR(255) NOT NULL,
    dresscode TEXT NOT NULL,
    created_by_id INT(11) NOT NULL,
    src_created_by_id INT(6) NOT NULL,
    src_going_ids VARCHAR(500) NOT NULL,
    src_maybe_going VARCHAR(500) NOT NULL,
    PRIMARY KEY (event_id),
    UNIQUE INDEX event_id (src_event_id),
    INDEX created_by_id (created_by_id)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
ROW_FORMAT=COMPRESSED
KEY_BLOCK_SIZE=8;

INSERT INTO i_events SELECT * FROM events;
DROP TABLE events;
RENAME TABLE i_events TO events;

----------------------------------------------------------------

CREATE TABLE `i_groups` (
    `group_id` INT(11) NOT NULL,
    `src_group_id` INT(5) NOT NULL,
    `group_name` VARCHAR(255) NOT NULL,
    `description` TEXT NOT NULL,
    `rules` TEXT NOT NULL,
    `restricted_to` TEXT NOT NULL,
    `comments_cnt` INT(10) NOT NULL,
    `started_on` VARCHAR(25) NOT NULL,
    `src_group_leaders_ids` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`group_id`),
    UNIQUE INDEX `src_group_id` (`src_group_id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
ROW_FORMAT=COMPRESSED
KEY_BLOCK_SIZE=8;

INSERT INTO i_groups SELECT * FROM groups;
DROP TABLE groups;
RENAME TABLE i_groups TO groups;

----------------------------------------------------------------

CREATE TABLE `i_group_categories` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
ROW_FORMAT=COMPRESSED
KEY_BLOCK_SIZE=8;

INSERT INTO i_group_categories SELECT * FROM group_categories;
DROP TABLE group_categories;
RENAME TABLE i_group_categories TO group_categories;

----------------------------------------------------------------

CREATE TABLE `group_posts` (
    `topic_id` INT(11) NOT NULL AUTO_INCREMENT,
    `src_group_post_id` INT(11) NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `group_id` INT(11) NOT NULL,
    `src_group_id` INT(10) NOT NULL,
    `post_text` TEXT NOT NULL,
    `author_id` INT(11) NOT NULL,
    `src_author_id` INT(10) NOT NULL,
    `time` VARCHAR(30) NOT NULL,
    `comments_cnt` INT(10) NOT NULL,
    PRIMARY KEY (`topic_id`),
    UNIQUE INDEX `src_group_post_id` (`src_group_post_id`),
    INDEX `group_id` (`src_group_id`),
    INDEX `group_id_2` (`group_id`),
    INDEX `author_id` (`author_id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
ROW_FORMAT=COMPRESSED
KEY_BLOCK_SIZE=8;

INSERT INTO i_group_posts SELECT * FROM group_posts;
DROP TABLE group_posts;
RENAME TABLE i_group_posts TO group_posts;

----------------------------------------------------------------

CREATE TABLE `i_group_posts_comments` (
    `topic_comment_id` INT(11) NOT NULL AUTO_INCREMENT,
    `src_topic_comment_id` INT(10) NOT NULL,
    `comment_text` TEXT NOT NULL,
    `time` VARCHAR(30) NOT NULL,
    `commenter_id` INT(11) NOT NULL,
    `src_commenter_id` INT(10) NOT NULL,
    `topic_id` INT(11) NOT NULL,
    `src_topic_id` INT(10) NOT NULL,
    PRIMARY KEY (`topic_comment_id`),
    UNIQUE INDEX `src_group_post_comment_id` (`src_topic_comment_id`),
    INDEX `commenter_id` (`commenter_id`),
    INDEX `topic_id` (`topic_id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
ROW_FORMAT=COMPRESSED
KEY_BLOCK_SIZE=8;

INSERT INTO i_group_posts_comments SELECT * FROM group_posts_comments;
DROP TABLE group_posts_comments;
RENAME TABLE i_group_posts_comments TO group_posts_comments;

----------------------------------------------------------------

CREATE TABLE `i_posts` (
    `post_id` INT(11) NOT NULL AUTO_INCREMENT,
    `src_post_id` INT(11) NOT NULL,
    `post_title` VARCHAR(255) NOT NULL,
    `post_body` TEXT NOT NULL,
    `author_id` INT(11) NOT NULL,
    `src_author_id` INT(7) NOT NULL,
    `time` VARCHAR(30) NOT NULL,
    `comments_cnt` INT(3) NOT NULL,
    PRIMARY KEY (`post_id`),
    UNIQUE INDEX `src_post_id` (`src_post_id`),
    INDEX `author_id` (`author_id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
ROW_FORMAT=COMPRESSED
KEY_BLOCK_SIZE=8;

INSERT INTO i_posts SELECT * FROM posts;
DROP TABLE posts;
RENAME TABLE i_posts TO posts;

----------------------------------------------------------------

CREATE TABLE `i_posts_comments` (
    `comment_id` INT(11) NOT NULL AUTO_INCREMENT,
    `comment` TEXT NOT NULL,
    `commenter_id` INT(11) NOT NULL,
    `src_commenter_id` INT(7) NOT NULL,
    `post_id` INT(11) NOT NULL,
    `src_post_id` INT(10) NOT NULL,
    `time` VARCHAR(30) NOT NULL,
    `src_comment_id` INT(8) NOT NULL,
    PRIMARY KEY (`comment_id`),
    UNIQUE INDEX `src_comment_id` (`src_comment_id`),
    INDEX `user_id` (`src_commenter_id`),
    INDEX `post_id` (`src_post_id`),
    INDEX `commenter_id` (`commenter_id`),
    INDEX `post_id_2` (`post_id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
ROW_FORMAT=COMPRESSED
KEY_BLOCK_SIZE=8;

INSERT INTO i_posts_comments SELECT * FROM posts_comments;
DROP TABLE posts_comments;
RENAME TABLE i_posts_comments TO posts_comments;

----------------------------------------------------------------

CREATE TABLE `i_users` (
    `user_id` INT(11) NOT NULL AUTO_INCREMENT,
    `src_user_id` INT(11) NOT NULL,
    `src_nickname` VARCHAR(100) NOT NULL,
    `fake_nickname` VARCHAR(100) NOT NULL,
    `gender` VARCHAR(1) NOT NULL,
    `age` VARCHAR(2) NOT NULL,
    `role` VARCHAR(100) NOT NULL,
    `relationship` VARCHAR(500) NOT NULL,
    `ds_relationship` VARCHAR(500) NOT NULL,
    `active` VARCHAR(100) NOT NULL,
    `userpic` VARCHAR(255) NOT NULL,
    `city` VARCHAR(5) NOT NULL,
    `region` VARCHAR(5) NOT NULL,
    `country` VARCHAR(5) NOT NULL,
    `orientation` VARCHAR(100) NOT NULL,
    `groups_member` VARCHAR(500) NOT NULL,
    `about me` TEXT NOT NULL,
    `is_looking_for` TEXT NOT NULL,
    `friends_ids` VARCHAR(500) NOT NULL,
    `following_ids` VARCHAR(1000) NOT NULL,
    `followers_ids` VARCHAR(1000) NOT NULL,
    `events_org` VARCHAR(500) NOT NULL,
    `events_going_to` VARCHAR(500) NOT NULL,
    `events_maybe_going` VARCHAR(500) NOT NULL,
    `fetishes_into` VARCHAR(500) NOT NULL,
    `fetishes_curious` VARCHAR(500) NOT NULL,
    `images_cnt` VARCHAR(5) NOT NULL,
    `posts_ids` VARCHAR(1000) NOT NULL,
    `groups_lead` VARCHAR(500) NOT NULL,
    `video_cnt` VARCHAR(5) NOT NULL,
    PRIMARY KEY (`user_id`),
    UNIQUE INDEX `src_user_id` (`src_user_id`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
ROW_FORMAT=COMPRESSED
KEY_BLOCK_SIZE=8;

INSERT INTO i_users SELECT * FROM users;
DROP TABLE users;
RENAME TABLE i_users TO users;
