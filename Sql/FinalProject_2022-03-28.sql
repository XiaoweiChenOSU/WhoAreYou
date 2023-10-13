# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.26)
# Database: FinalProject
# Generation Time: 2022-03-28 22:22:52 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table admin
# ------------------------------------------------------------

DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `is_super` smallint(6) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `role_id` (`role_id`),
  KEY `ix_admin_addtime` (`addtime`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;

INSERT INTO `admin` (`id`, `name`, `pwd`, `is_super`, `role_id`, `addtime`)
VALUES
	(1,'xiaowei','pbkdf2:sha256:150000$7TUnGr1L$00b980c361b2c4deb079391a9ef81302aa56489072addeaaaea320021582a940',0,1,'2019-07-07 10:50:00'),
	(2,'qing','pbkdf2:sha256:150000$aTUQhqYz$b34e7e36d050989ada1aee6dd9a570df9159a106cc2d9355d968ce9cf5db435e',1,2,'2019-07-08 12:10:13');

/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table adminlog
# ------------------------------------------------------------

DROP TABLE IF EXISTS `adminlog`;

CREATE TABLE `adminlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_adminlog_addtime` (`addtime`),
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `adminlog` WRITE;
/*!40000 ALTER TABLE `adminlog` DISABLE KEYS */;

INSERT INTO `adminlog` (`id`, `admin_id`, `ip`, `reason`, `addtime`)
VALUES
	(1,1,'127.0.0.1',NULL,'2019-07-07 21:57:35'),
	(2,1,'127.0.0.1',NULL,'2019-07-08 11:47:32'),
	(3,1,'127.0.0.1',NULL,'2019-07-08 12:00:57'),
	(4,1,'127.0.0.1',NULL,'2019-07-09 12:45:59'),
	(5,1,'127.0.0.1',NULL,'2019-07-12 12:23:07'),
	(6,1,'127.0.0.1',NULL,'2019-07-13 16:29:52'),
	(7,1,'127.0.0.1',NULL,'2019-07-16 20:50:48'),
	(8,1,'127.0.0.1','login','2019-07-17 11:12:01'),
	(9,1,'127.0.0.1','login','2019-07-18 10:07:16'),
	(10,1,'127.0.0.1','login','2019-07-18 15:22:59'),
	(11,1,'127.0.0.1','login','2019-07-18 17:07:12'),
	(12,1,'127.0.0.1','login','2019-07-19 21:58:47'),
	(13,1,'127.0.0.1','login','2019-07-19 23:16:56'),
	(14,1,'127.0.0.1','login','2019-07-20 10:37:25'),
	(15,1,'127.0.0.1','login','2019-07-24 10:22:53'),
	(16,1,'127.0.0.1','login','2019-07-24 14:32:14'),
	(17,1,'127.0.0.1','login','2019-07-25 20:36:31'),
	(18,1,'127.0.0.1','login','2019-07-26 11:39:50'),
	(19,1,'127.0.0.1','login','2019-07-27 16:39:50'),
	(20,2,'127.0.0.1','login','2019-07-28 10:29:11'),
	(21,2,'127.0.0.1','login','2019-07-28 10:29:43'),
	(22,1,'127.0.0.1','login','2019-07-28 10:31:17'),
	(23,1,'127.0.0.1','login','2019-07-29 08:56:27'),
	(24,2,'127.0.0.1','login','2022-03-28 17:04:07');

/*!40000 ALTER TABLE `adminlog` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table auth
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth`;

CREATE TABLE `auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `ix_auth_addtime` (`addtime`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `auth` WRITE;
/*!40000 ALTER TABLE `auth` DISABLE KEYS */;

INSERT INTO `auth` (`id`, `name`, `url`, `addtime`)
VALUES
	(1,'tag_add','/admin/tag/add/','2019-06-06 12:37:01'),
	(2,'tag_list','/admin/tag/list/<int:page>/','2019-06-06 12:37:01'),
	(3,'tag_del','/admin/tag/del/<int:id>/','2019-06-06 12:37:01'),
	(4,'tag_edit','/admin/tag/edit/<int:id>/','2019-06-06 12:37:01'),
	(5,'movie_add','/admin/movie/add/','2019-06-06 12:37:01'),
	(6,'movie_list','/admin/movie/list/<int:page>/','2019-06-06 12:37:01'),
	(7,'movie_del','/admin/movie/del/<int:id>/','2019-06-06 12:37:01'),
	(8,'movie_edit','/admin/movie/edit/<int:id>/','2019-06-06 12:37:01'),
	(9,'preview_add','/admin/preview/add/','2019-06-06 12:37:01'),
	(10,'preview_list','/admin/preview/list/<int:page>/','2019-06-06 12:37:01'),
	(11,'preview_del','/admin/preview/del/<int:id>/','2019-06-06 12:37:01'),
	(12,'preview_edit','/admin/preview/edit/<int:id>/','2019-06-06 12:37:01'),
	(13,'user_list','/admin/user/list/<int:page>/','2019-06-06 12:37:01'),
	(14,'user_view','/admin/user/view/<int:id>/','2019-06-06 12:37:01'),
	(15,'user_del','/admin/user/del/<int:id>/','2019-06-06 12:37:01'),
	(16,'admin_add','/admin/admin/add/','2019-06-06 12:37:01'),
	(17,'admin_list','/admin/admin/list/<int:page>/','2019-06-06 12:37:01'),
	(18,'comment_list','/admin/comment/list/<int:page>/','2019-06-06 12:37:01'),
	(19,'comment_del','/admin/comment/del/<int:id>/','2019-06-06 12:37:01'),
	(20,'moviecol_list','/admin/moviecol/list/<int:page>/','2019-06-06 12:37:01'),
	(21,'moviecol_del','/admin/moviecol/del/<int:id>/','2019-06-06 12:37:01'),
	(22,'oplog_list','/admin/oplog/list/<int:page>/','2019-06-06 12:37:01'),
	(23,'adminloginlog_list','/admin/adminloginlog/list/<int:page>/','2019-06-06 12:37:01'),
	(24,'userloginlog_list','/admin/userloginlog/list/<int:page>/','2019-06-06 12:37:01'),
	(25,'auth_add','/admin/auth/add/','2019-06-06 12:37:01'),
	(26,'auth_list','/admin/auth/list/<int:page>/','2019-06-06 12:37:01'),
	(27,'auth_del','/admin/auth/del/<int:id>/','2019-06-06 12:37:01'),
	(28,'auth_edit','/admin/auth/edit/<int:id>/','2019-06-06 12:37:01'),
	(29,'role_add','/admin/role/add/','2019-06-06 12:37:01'),
	(30,'role_list','/admin/role/list/<int:page>/','2019-06-06 12:37:01'),
	(31,'role_del','/admin/role/del/<int:id>/','2019-06-06 12:37:01'),
	(32,'role_edit','/admin/role/edit/<int:id>/','2019-06-06 12:37:01'),
	(33,'music_add','/admin/music/add/','2019-06-06 12:37:01'),
	(34,'music_list','/admin/music/list/<int:page>/','2019-06-06 12:37:01'),
	(35,'music_del','/admin/music/del/<int:id>/','2019-06-06 12:37:01'),
	(36,'music_edit','/admin/music/edit/<int:id>/','2019-06-06 12:37:01'),
	(37,'book_add','/admin/book/add/','2019-06-06 12:37:01'),
	(38,'book_list','/admin/book/list/<int:page>/','2019-06-06 12:37:01'),
	(39,'book_del','/admin/book/del/<int:id>/','2019-06-06 12:37:01'),
	(40,'book_edit','/admin/book/edit/<int:id>/','2019-06-06 12:37:01'),
	(41,'musiccol_list','/admin/musiccol/list/<int:page>/','2019-06-06 12:37:01'),
	(42,'musiccol_del','/admin/musiccol/del/<int:id>/','2019-06-06 12:37:01'),
	(43,'bookcol_list','/admin/bookcol/list/<int:page>/','2019-06-06 12:37:01'),
	(44,'bookcol_del','/admin/bookcol/del/<int:id>/','2019-06-06 12:37:01');

/*!40000 ALTER TABLE `auth` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table book
# ------------------------------------------------------------

DROP TABLE IF EXISTS `book`;

CREATE TABLE `book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `info` text,
  `logo` varchar(255) DEFAULT NULL,
  `star` smallint(6) DEFAULT NULL,
  `commentnum` bigint(20) DEFAULT NULL,
  `tags` varchar(100) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `logo` (`logo`),
  KEY `ix_book_addtime` (`addtime`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;

INSERT INTO `book` (`id`, `title`, `url`, `info`, `logo`, `star`, `commentnum`, `tags`, `author`, `release_time`, `addtime`)
VALUES
	(1,'What You Did','https://www.amazon.com/gp/product/B07KPFLD6Q/ref=s9_acsd_ri_bw_c_x_1_w?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-10&pf_rd_r=BYBDEV3YFJZT0ABV4VE1&pf_rd_t=101&pf_rd_p=b34f3048-7fa4-49b0-99af-8102f019a6c3&pf_rd_i=283155','It was supposed to be the perfect reunion: six university friends together again after twenty years. Host Ali finally has the life she always wanted, a career she can be proud of and a wonderful family with her college boyfriend, now husband. But that night her best friend makes an accusation so shocking that nothing will ever be the same again.\r\n\r\nWhen Karen staggers in from the garden, bleeding and traumatised, she claims that she has been assaulted—by Ali’s husband, Mike. Ali must make a split-second decision: who should she believe? Her horrified husband, or her best friend? With Mike offering a very different version of events, Ali knows one of them is lying—but which? And why?\r\n\r\nWhen the ensuing chaos forces her to re-examine the golden era the group shared at university, Ali realises there are darker memories too. Memories that have lain dormant for decades. Memories someone would kill to protect.','201907121352258d560065c81048898bda280026d5ab84.jpg',5,1,'54,11,64,52','Claire McGowan','2019-01-31','2019-07-12 13:49:45'),
	(2,'Self-Discipline Made Easy','https://www.amazon.com/dp/B07HJDY2S3/ref=sspa_dk_detail_6?psc=1','Self-Discipline Made Easy is the guide you’ve been waiting for. In it we discuss the science behind what makes you want to stay in your comfort zone, hint, it’s not laziness, why you get overwhelmed when you think about your goals, and most importantly how you can overcome these tendencies to become the most productive and efficient version of yourself.','20190712135716bca1e362d1a64b8e937f4a9c9b3ac066.jpg',5,1,'30,31,5,6,32,53,54,55,7,33,8,9,1,34','Basil Foster','2018-09-19','2019-07-12 13:57:16');

/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table bookcol
# ------------------------------------------------------------

DROP TABLE IF EXISTS `bookcol`;

CREATE TABLE `bookcol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `book_id` (`book_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_bookcol_addtime` (`addtime`),
  CONSTRAINT `bookcol_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
  CONSTRAINT `bookcol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `bookcol` WRITE;
/*!40000 ALTER TABLE `bookcol` DISABLE KEYS */;

INSERT INTO `bookcol` (`id`, `book_id`, `user_id`, `addtime`)
VALUES
	(1,2,1,'2019-07-12 16:18:49'),
	(2,1,1,'2019-07-24 12:23:39');

/*!40000 ALTER TABLE `bookcol` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table comment
# ------------------------------------------------------------

DROP TABLE IF EXISTS `comment`;

CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `movie_id` int(11) DEFAULT NULL,
  `music_id` int(11) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `music_id` (`music_id`),
  KEY `book_id` (`book_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_comment_addtime` (`addtime`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`music_id`) REFERENCES `music` (`id`),
  CONSTRAINT `comment_ibfk_3` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
  CONSTRAINT `comment_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;

INSERT INTO `comment` (`id`, `content`, `movie_id`, `music_id`, `book_id`, `user_id`, `addtime`)
VALUES
	(1,'hahaha',1,NULL,NULL,1,'2019-07-09 13:31:11'),
	(2,'an awesome video',1,NULL,NULL,1,'2019-07-10 09:19:18'),
	(3,'test',NULL,2,NULL,1,'2019-07-11 14:32:41'),
	(4,'good book',NULL,2,NULL,1,'2019-07-12 16:16:46'),
	(5,'Good Book',NULL,NULL,2,1,'2019-07-12 16:18:42'),
	(6,'good!!!!!!',10,NULL,NULL,1,'2019-07-19 23:20:56'),
	(7,'this is a good book',NULL,NULL,1,1,'2019-07-24 12:23:34'),
	(8,'thisi is a good video',10,NULL,NULL,4,'2019-07-24 14:40:24'),
	(9,'haha it is good',2,NULL,NULL,7,'2019-07-29 10:55:25');

/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table friends
# ------------------------------------------------------------

DROP TABLE IF EXISTS `friends`;

CREATE TABLE `friends` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `FriendId` int(11) DEFAULT NULL,
  `UserId` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `friends_ibfk_1` (`FriendId`),
  KEY `friends_ibfk_2` (`UserId`),
  KEY `ix_message_addtime` (`addtime`),
  CONSTRAINT `friends_ibfk_1` FOREIGN KEY (`FriendId`) REFERENCES `user` (`id`),
  CONSTRAINT `friends_ibfk_2` FOREIGN KEY (`UserId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `friends` WRITE;
/*!40000 ALTER TABLE `friends` DISABLE KEYS */;

INSERT INTO `friends` (`id`, `FriendId`, `UserId`, `addtime`)
VALUES
	(1,2,4,'2019-07-25 21:56:18'),
	(2,3,1,'2019-07-26 10:49:14'),
	(3,1,3,'2019-07-26 18:18:17'),
	(4,3,2,'2019-07-29 11:06:22');

/*!40000 ALTER TABLE `friends` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table know
# ------------------------------------------------------------

DROP TABLE IF EXISTS `know`;

CREATE TABLE `know` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `strengths` varchar(300) DEFAULT NULL,
  `weaknesses` varchar(300) DEFAULT NULL,
  `jobs` varchar(300) DEFAULT NULL,
  `luckNum` varchar(30) DEFAULT NULL,
  `luckColor` varchar(300) DEFAULT NULL,
  `luckFlower` varchar(300) DEFAULT NULL,
  `luckDirection` varchar(300) DEFAULT NULL,
  `likes` varchar(300) DEFAULT NULL,
  `dislikes` varchar(300) DEFAULT NULL,
  `zodiac_info` text,
  `chineseZodiac_info` text,
  `addtime` datetime DEFAULT NULL,
  `zodiac` varchar(50) DEFAULT NULL,
  `chineseZodiac` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_know_addtime` (`addtime`),
  CONSTRAINT `know_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `know` WRITE;
/*!40000 ALTER TABLE `know` DISABLE KEYS */;

INSERT INTO `know` (`id`, `user_id`, `strengths`, `weaknesses`, `jobs`, `luckNum`, `luckColor`, `luckFlower`, `luckDirection`, `likes`, `dislikes`, `zodiac_info`, `chineseZodiac_info`, `addtime`, `zodiac`, `chineseZodiac`)
VALUES
	(1,1,'Decisive, inspiring, magnanimous, sensitive, ambitious, romanticResponsible, disciplined, self-control, good managers','Eccentric, tactless, fiery, intolerant, unrealisticKnow-it-all, unforgiving, condescending, expecting the worst','quality inspectors, cashier, financier, pharmacist, electrician, politician and priest ...','1, 7, 6','Gold, silver, hoary','Bleeding heart vine, larkspur, hyacinth','West, north, northwest','Family, tradition, music, understated status, quality craftsmanship','Almost everything at some point','Your zodiac is Capricorn, which is a sign that represents time and responsibility, and its representatives are traditional and often very serious by nature. These individuals possess an inner state of independence that enables significant progress both in their personal and professional lives. You are masters of self-control and have the ability to lead the way, make solid and realistic plans, and manage many people who work for them at any time. You will learn from your mistakes and get to the top based solely on your experience and expertise.','You are usually lively, intellectual and excitable. You can clearly tell right from wrong. You are upright and frank. However, you are also a bit arrogant and impatient. Sometimes you tend to be overly confident. You hate hypocrisy, gossip and slander. You are not afraid of difficulties but hate to be used or controlled by others.','2019-07-07 16:40:50','Scorpio','Dragon'),
	(2,2,'Decisive, inspiring, magnanimous, sensitive, ambitious, romanticResponsible, disciplined, self-control, good managers','Eccentric, tactless, fiery, intolerant, unrealisticKnow-it-all, unforgiving, condescending, expecting the worst','quality inspectors, cashier, financier, pharmacist, electrician, politician and priest ...','1, 7, 6','Gold, silver, hoary','Bleeding heart vine, larkspur, hyacinth','West, north, northwest','Family, tradition, music, understated status, quality craftsmanship','Almost everything at some point','Your zodiac is Capricorn, which is a sign that represents time and responsibility, and its representatives are traditional and often very serious by nature. These individuals possess an inner state of independence that enables significant progress both in their personal and professional lives. You are masters of self-control and have the ability to lead the way, make solid and realistic plans, and manage many people who work for them at any time. You will learn from your mistakes and get to the top based solely on your experience and expertise.','You are usually lively, intellectual and excitable. You can clearly tell right from wrong. You are upright and frank. However, you are also a bit arrogant and impatient. Sometimes you tend to be overly confident. You hate hypocrisy, gossip and slander. You are not afraid of difficulties but hate to be used or controlled by others.','2019-07-08 14:42:17','Capricorn','Dragon'),
	(3,3,'Decisive, inspiring, magnanimous, sensitive, ambitious, romanticResponsible, disciplined, self-control, good managers','Eccentric, tactless, fiery, intolerant, unrealisticKnow-it-all, unforgiving, condescending, expecting the worst','quality inspectors, cashier, financier, pharmacist, electrician, politician and priest ...','1, 7, 6','Gold, silver, hoary','Bleeding heart vine, larkspur, hyacinth','West, north, northwest','Family, tradition, music, understated status, quality craftsmanship','Almost everything at some point','Your zodiac is Capricorn, which is a sign that represents time and responsibility, and its representatives are traditional and often very serious by nature. These individuals possess an inner state of independence that enables significant progress both in their personal and professional lives. You are masters of self-control and have the ability to lead the way, make solid and realistic plans, and manage many people who work for them at any time. You will learn from your mistakes and get to the top based solely on your experience and expertise.','You are usually lively, intellectual and excitable. You can clearly tell right from wrong. You are upright and frank. However, you are also a bit arrogant and impatient. Sometimes you tend to be overly confident. You hate hypocrisy, gossip and slander. You are not afraid of difficulties but hate to be used or controlled by others.','2019-07-08 15:11:19','Capricorn','Dragon'),
	(4,4,'Decisive, inspiring, magnanimous, sensitive, ambitious, romanticCourageous, determined, confident, enthusiastic, optimistic, honest, passionate','Eccentric, tactless, fiery, intolerant, unrealisticImpatient, moody, short-tempered, impulsive, aggressive','quality inspectors, cashier, financier, pharmacist, electrician, politician and priest ...','1, 7, 6','Gold, silver, hoary','Bleeding heart vine, larkspur, hyacinth','West, north, northwest','Comfortable clothes, taking on leadership roles, physical challenges, individual sports','Inactivity, delays, work that does not use one\'s talents','Your zodiac is Aries, you are continuously looking for dynamic, speed and competition, always being the first in everything - from work to social gatherings. Thanks to its ruling planet Mars and the fact it belongs to the element of Fire, Aries is one of the most active zodiac signs. It is in your nature to take action, sometimes before you think about it well. The Sun in such high dignity gives them excellent organizational skills, so you\'ll rarely meet an Aries who isn\'t capable of finishing several things at once, often before lunch break! Your challenges show when you get impatient, aggressive and vent anger pointing it to other people. Strong personalities born under this sign have a task to fight for their goals, embracing togetherness and teamwork through this incarnation.','You are usually lively, intellectual and excitable. You can clearly tell right from wrong. You are upright and frank. However, you are also a bit arrogant and impatient. Sometimes you tend to be overly confident. You hate hypocrisy, gossip and slander. You are not afraid of difficulties but hate to be used or controlled by others.','2019-07-24 14:36:58','Aries','Dragon'),
	(5,5,'Independent, capable, warm-hearted, self-respect, quick mindedResponsible, disciplined, self-control, good managers','Impatient, critical, eccentric, narrow-minded, selfishKnow-it-all, unforgiving, condescending, expecting the worst','Politicians, diplomats, public speakers, clothing designers, beauticians, tour guides, actors/ actresses, comedians, scientists','5, 7, 8','Gold, brown, brownish yellow, yellow','Gladiola, impatiens, cockscomb','West, southwest, northeast','Family, tradition, music, understated status, quality craftsmanship','Almost everything at some point','Your zodiac is Capricorn, which is a sign that represents time and responsibility, and its representatives are traditional and often very serious by nature. These individuals possess an inner state of independence that enables significant progress both in their personal and professional lives. You are masters of self-control and have the ability to lead the way, make solid and realistic plans, and manage many people who work for them at any time. You will learn from your mistakes and get to the top based solely on your experience and expertise.','You have many excellent characteristics, such as being honest, bright, communicative and ambitious. You are born pretty or handsome, and prefer to dress up. In daily life, you seldom rely on others. However, you might be enthusiastic about something quickly, but soon be impassive. Thus, you need to have enough faiths and patience to insist on one thing.','2019-07-26 11:59:12','Capricorn','Rooster'),
	(6,7,'Valiant, loyal, responsible, clever, courageous, livelyCompassionate, artistic, intuitive, gentle, wise, musical','Impatient, critical, eccentric, narrow-minded, selfishFearful, overly trusting, sad, desire to escape reality, can be a victim or a martyr','Lawyers, judges, organizers, teachers, doctors, civil servants, programmers, advertising planners, bloggers','3, 4, 9','Green, red, purple','Rose, oncidium, cymbidium orchids','East, southeast, south','Being alone, sleeping, music, romance, visual media, swimming, spiritual themes','Know-it-all, being criticized, the past coming back to haunt, cruelty of any kind','Your zodiac is Pisces, you are usually very friendly, so you often find yourselves in a company of very different people. Pisces are selfless, you are always willing to help others, without hoping to get anything back. Pisces is a Water sign and as such this zodiac sign is characterized by empathy and expressed emotional capacity.','You are usually independent, sincere, loyal and decisive. You are not afraid of difficulties in daily life. These shining characteristics make you have harmonious relationship with people around.','2019-07-29 08:59:15','Pisces','Dog');

/*!40000 ALTER TABLE `know` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table message
# ------------------------------------------------------------

DROP TABLE IF EXISTS `message`;

CREATE TABLE `message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` text,
  `FromUserId` int(11) DEFAULT NULL,
  `ToUserId` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `message_ibfk_1` (`FromUserId`),
  KEY `message_ibfk_2` (`ToUserId`),
  KEY `ix_message_addtime` (`addtime`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`FromUserId`) REFERENCES `user` (`id`),
  CONSTRAINT `message_ibfk_2` FOREIGN KEY (`ToUserId`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table movie
# ------------------------------------------------------------

DROP TABLE IF EXISTS `movie`;

CREATE TABLE `movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `info` text,
  `logo` varchar(255) DEFAULT NULL,
  `star` smallint(6) DEFAULT NULL,
  `playnum` bigint(20) DEFAULT NULL,
  `commentnum` bigint(20) DEFAULT NULL,
  `tags` varchar(100) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `length` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `logo` (`logo`),
  KEY `ix_movie_addtime` (`addtime`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `movie` WRITE;
/*!40000 ALTER TABLE `movie` DISABLE KEYS */;

INSERT INTO `movie` (`id`, `title`, `url`, `info`, `logo`, `star`, `playnum`, `commentnum`, `tags`, `area`, `release_time`, `length`, `addtime`)
VALUES
	(1,'Spring','201907081059239719b8bad7524713ad3fbf692eaf428a.mp4','So Beautiful','20190708105924b76030352d3b420e81abe55cb90c236d.jpg',5,79,2,'1,2','china','2019-01-31','13','2019-07-07 11:10:14'),
	(2,'Star','20190709111232e514118224d84d23bb9cd7111dccd7c6.mp4','This is a star movie','20190709111232c76edd4290024052b33954147a6c25ec.jpg',5,21,1,'1','USA','1989-01-19','12','2019-07-07 22:10:28'),
	(3,'Winter','20190709130508f5194f93f0c24ce1959f5dbc4c0436a5.mp4','Winter is about snow, which is the most beautiful season.','201907091305083b416ccd77834c908f7133ea12733147.jpg',5,9,0,'1','Canada','2016-06-21','13','2019-07-09 12:30:01'),
	(4,'Flowers','201907091254266c8a3c0d82bb4b19a2d4fc074eb16165.mp4','This is a awesome video, which can make you peaceful.','201907091254263d4b31eac3914fecb44117624bc1a4ad.jpg',5,12,0,'4','USA','2015-06-23','20','2019-07-09 12:48:19'),
	(5,'Friends','20190709125727ee8ab4092669406cae8299245ea04461.mp4','People always need friends','20190709125727894792e2d8bc4b7f96f833d6a49b1201.jpg',5,8,0,'4','Japan','2019-01-31','21','2019-07-09 12:57:27'),
	(6,'Book','20190709130254addbc2984ff64803b132abae4425d419.mp4','Books','20190709130254cafbd91408384f25a5e7205302bc11d6.jpg',5,12,0,'3','Canada','2019-01-31','15','2019-07-09 13:02:54'),
	(7,'A Chinese singer concert.','201907162119474e236ff8ed0b48a9bc1553c7a3613aef.mp4','A Chinese singer concert.','20190716211947812be636b7f647d0b58e04c6e8c2d2d9.jpg',1,0,0,'17','china','2019-03-03','103','2019-07-16 21:19:48'),
	(8,'Qiu YiNong','2019071621262289897b3507404afd9f094a938641a2b4.mp4','A song make me sad.','20190716212622a5bd1895e35b4528b4130b7229478cc0.jpg',1,0,0,'17','china','2012-08-12','5','2019-07-16 21:26:22'),
	(9,'Running Man','20190716213500fbbc54d1315d485dbdb89b4780e376f4.mp4',' - \"Tears\" by So Chan Whee [Running Man Ep 459]','20190716213500a8ed7f748c894f549a583d9517e512db.jpg',5,2,0,'30','Korea','2015-06-23','3','2019-07-16 21:35:01'),
	(10,'Why You Never Forget Anything','2019071622043296fc409954f5455a982147d8f312d1dd.mp4','Introduce the working of the brain.','20190716220432629a72ad205d4942952649a214a51897.jpg',4,10,2,'14,38,24','USA','2019-07-05','15','2019-07-16 22:04:32'),
	(11,'Ugly Duck','201907162256202e9212c9cf0340ad90fb3a13aa3bebbd.mp4','the story of the ugly duck.','2019071622562056ff525c60d24558aa894aad22a17da5.jpg',4,2,0,'6,37,18,52','china','2011-01-23','11','2019-07-16 22:56:21');

/*!40000 ALTER TABLE `movie` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table moviecol
# ------------------------------------------------------------

DROP TABLE IF EXISTS `moviecol`;

CREATE TABLE `moviecol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_moviecol_addtime` (`addtime`),
  CONSTRAINT `moviecol_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `moviecol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `moviecol` WRITE;
/*!40000 ALTER TABLE `moviecol` DISABLE KEYS */;

INSERT INTO `moviecol` (`id`, `movie_id`, `user_id`, `addtime`)
VALUES
	(1,1,1,'2019-07-10 09:39:22'),
	(2,3,1,'2019-07-11 21:51:52'),
	(3,2,7,'2019-07-29 10:55:59');

/*!40000 ALTER TABLE `moviecol` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table music
# ------------------------------------------------------------

DROP TABLE IF EXISTS `music`;

CREATE TABLE `music` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `info` text,
  `logo` varchar(255) DEFAULT NULL,
  `star` smallint(6) DEFAULT NULL,
  `playnum` bigint(20) DEFAULT NULL,
  `commentnum` bigint(20) DEFAULT NULL,
  `tags` varchar(100) DEFAULT NULL,
  `singer` varchar(255) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `length` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  UNIQUE KEY `logo` (`logo`),
  KEY `ix_music_addtime` (`addtime`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `music` WRITE;
/*!40000 ALTER TABLE `music` DISABLE KEYS */;

INSERT INTO `music` (`id`, `title`, `url`, `info`, `logo`, `star`, `playnum`, `commentnum`, `tags`, `singer`, `release_time`, `length`, `addtime`)
VALUES
	(1,'when we were young','20190710180818c4e35918cdb84e4f829e2891e3a0dd7c.mp3','this is a very beautiful song','20190710180818a63826e7c6f04e54b1faafdef3d1c46d.jpg',1,0,0,'4,18','Adele','2015-07-23','5','2019-07-10 18:08:18'),
	(2,'Someone like you','2019071023063024b54c12298148569f510c3338bcf12f.mp3','Beautiful video','20190710230630dc3542dd45c44fa0918c4dda3e1ef243.jpg',5,28,1,'4,18','Adele','2016-12-15','4','2019-07-10 23:06:30'),
	(3,'Lemon Tree','2019071622113070f7da5db9574c81a6c65c453c9b130d.mp4','a song of Lemon Tree','201907162211307f8c50eed7a046eca98f775a09be8468.jpg',5,3,0,'7','mi jin xuan shi','2019-07-11','5','2019-07-16 22:11:31'),
	(4,'YiShengHeQiu','<FileStorage: \'\' (\'application/octet-stream\')>','a song for love.','20190716230147dccaa7640b504a7587a6b16204e6a7a0.jpg',5,1,0,'36,17','ChenBaiQiang','2017-10-17','5','2019-07-16 23:01:48');

/*!40000 ALTER TABLE `music` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table musiccol
# ------------------------------------------------------------

DROP TABLE IF EXISTS `musiccol`;

CREATE TABLE `musiccol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `music_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `music_id` (`music_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_musiccol_addtime` (`addtime`),
  CONSTRAINT `musiccol_ibfk_1` FOREIGN KEY (`music_id`) REFERENCES `music` (`id`),
  CONSTRAINT `musiccol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `musiccol` WRITE;
/*!40000 ALTER TABLE `musiccol` DISABLE KEYS */;

INSERT INTO `musiccol` (`id`, `music_id`, `user_id`, `addtime`)
VALUES
	(1,2,1,'2019-07-11 21:56:57');

/*!40000 ALTER TABLE `musiccol` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table oplog
# ------------------------------------------------------------

DROP TABLE IF EXISTS `oplog`;

CREATE TABLE `oplog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_oplog_addtime` (`addtime`),
  CONSTRAINT `oplog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `oplog` WRITE;
/*!40000 ALTER TABLE `oplog` DISABLE KEYS */;

INSERT INTO `oplog` (`id`, `admin_id`, `ip`, `reason`, `addtime`)
VALUES
	(1,1,'127.0.0.1','Add the movie: Spring','2019-07-07 11:10:14'),
	(2,1,'127.0.0.1','Add the movie: Star','2019-07-07 22:10:28'),
	(3,1,'127.0.0.1','Add the movie: Winter','2019-07-09 12:30:01'),
	(4,1,'127.0.0.1','Add tag:Romantic ','2019-07-09 12:44:33'),
	(5,1,'127.0.0.1','Add the movie: Flowers','2019-07-09 12:48:19'),
	(6,1,'127.0.0.1','Add the movie: Friends','2019-07-09 12:57:27'),
	(7,1,'127.0.0.1','Add the movie: Book','2019-07-09 13:02:54'),
	(8,1,'127.0.0.1','Add tag:Alternative','2019-07-10 17:00:54'),
	(9,1,'127.0.0.1','Add tag:Anime','2019-07-10 17:04:18'),
	(10,1,'127.0.0.1','Add tag:Blues','2019-07-10 17:04:26'),
	(11,1,'127.0.0.1','Add tag:Children','2019-07-10 17:04:44'),
	(12,1,'127.0.0.1','Add tag:Classical','2019-07-10 17:04:57'),
	(13,1,'127.0.0.1','Add tag:Commercial','2019-07-10 17:05:11'),
	(14,1,'127.0.0.1','Add tag:Country','2019-07-10 17:05:21'),
	(15,1,'127.0.0.1','Add tag:Dance','2019-07-10 17:05:32'),
	(16,1,'127.0.0.1','Add tag:Disney','2019-07-10 17:05:44'),
	(17,1,'127.0.0.1','Add tag:Easy Listening','2019-07-10 17:05:51'),
	(18,1,'127.0.0.1','Add tag:Electronic','2019-07-10 17:05:58'),
	(19,1,'127.0.0.1','Add tag:Enka','2019-07-10 17:28:30'),
	(20,1,'127.0.0.1','Add tag:Folk','2019-07-10 17:28:41'),
	(21,1,'127.0.0.1','Add tag:Pop','2019-07-10 17:28:51'),
	(22,1,'127.0.0.1','Add tag:Hip-Hop/Rap','2019-07-10 17:29:08'),
	(23,1,'127.0.0.1','Add tag:Fitness & Workout','2019-07-10 17:29:15'),
	(24,1,'127.0.0.1','Add tag:Holiday','2019-07-10 17:29:25'),
	(25,1,'127.0.0.1','Add tag:Industrial','2019-07-10 17:29:34'),
	(26,1,'127.0.0.1','Add tag:Instrumental','2019-07-10 17:29:48'),
	(27,1,'127.0.0.1','Add tag:Jazz','2019-07-10 17:29:58'),
	(28,1,'127.0.0.1','Add tag:Latin','2019-07-10 17:30:08'),
	(29,1,'127.0.0.1','Add tag:Opera','2019-07-10 17:30:46'),
	(30,1,'127.0.0.1','Add tag:R&B/Soul','2019-07-10 17:31:00'),
	(31,1,'127.0.0.1','Add tag:Reggae','2019-07-10 17:31:12'),
	(32,1,'127.0.0.1','Add tag:Rock','2019-07-10 17:31:25'),
	(33,1,'127.0.0.1','Add the music: when we were young','2019-07-10 18:08:18'),
	(34,1,'127.0.0.1','Add the music: Someone like you','2019-07-10 23:06:30'),
	(35,1,'127.0.0.1','Add tag:Action and adventure','2019-07-12 12:29:26'),
	(36,1,'127.0.0.1','Add tag:Alternate history','2019-07-12 12:29:46'),
	(37,1,'127.0.0.1','Add tag:Anthology','2019-07-12 12:29:58'),
	(38,1,'127.0.0.1','Add tag:Chick lit','2019-07-12 12:32:17'),
	(39,1,'127.0.0.1','Add tag:Coming-of-age','2019-07-12 12:36:59'),
	(40,1,'127.0.0.1','Add tag:Crime','2019-07-12 12:37:09'),
	(41,1,'127.0.0.1','Add tag:Drama','2019-07-12 12:37:15'),
	(42,1,'127.0.0.1','Add tag:Fairytale','2019-07-12 12:37:21'),
	(43,1,'127.0.0.1','Add tag:Fantasy','2019-07-12 12:37:31'),
	(44,1,'127.0.0.1','Add tag:Graphic novel','2019-07-12 12:37:42'),
	(45,1,'127.0.0.1','Add tag:Historical fiction','2019-07-12 12:37:48'),
	(46,1,'127.0.0.1','Add tag:Horror','2019-07-12 12:37:57'),
	(47,1,'127.0.0.1','Add tag:Mystery','2019-07-12 12:38:05'),
	(48,1,'127.0.0.1','Add tag:Paranormal romance','2019-07-12 12:40:32'),
	(49,1,'127.0.0.1','Add tag:Picture book','2019-07-12 12:42:22'),
	(50,1,'127.0.0.1','Add tag:Poetry','2019-07-12 12:42:29'),
	(51,1,'127.0.0.1','Add tag:Political thriller','2019-07-12 12:42:38'),
	(52,1,'127.0.0.1','Add tag:Satire','2019-07-12 12:43:12'),
	(53,1,'127.0.0.1','Add tag:Science fiction','2019-07-12 12:43:17'),
	(54,1,'127.0.0.1','Add tag:Short story','2019-07-12 12:43:22'),
	(55,1,'127.0.0.1','Add tag:Suspense','2019-07-12 12:43:31'),
	(56,1,'127.0.0.1','Add tag:Thriller','2019-07-12 12:43:36'),
	(57,1,'127.0.0.1','Add tag:Young adult','2019-07-12 12:43:44'),
	(58,1,'127.0.0.1','Add tag:Art','2019-07-12 12:44:00'),
	(59,1,'127.0.0.1','Add tag:Autobiography','2019-07-12 12:44:04'),
	(60,1,'127.0.0.1','Add tag:Biography','2019-07-12 12:44:10'),
	(61,1,'127.0.0.1','Add tag:Book review','2019-07-12 12:44:18'),
	(62,1,'127.0.0.1','Add tag:Cookbook','2019-07-12 12:44:23'),
	(63,1,'127.0.0.1','Add tag:Diary','2019-07-12 12:44:31'),
	(64,1,'127.0.0.1','Add tag:Dictionary','2019-07-12 12:44:38'),
	(65,1,'127.0.0.1','Add tag:Encyclopedia','2019-07-12 12:44:45'),
	(66,1,'127.0.0.1','Add tag:Guide','2019-07-12 12:44:49'),
	(67,1,'127.0.0.1','Add tag:Health','2019-07-12 12:44:59'),
	(68,1,'127.0.0.1','Add tag:History','2019-07-12 12:45:07'),
	(69,1,'127.0.0.1','Add tag:Journal','2019-07-12 12:45:17'),
	(70,1,'127.0.0.1','Add tag:Math','2019-07-12 12:45:41'),
	(71,1,'127.0.0.1','Add tag:Memoir','2019-07-12 12:45:53'),
	(72,1,'127.0.0.1','Add tag:Prayer','2019-07-12 12:45:59'),
	(73,1,'127.0.0.1','Add tag:Religion, spirituality, and new age','2019-07-12 12:46:23'),
	(74,1,'127.0.0.1','Add tag:Textbook','2019-07-12 12:46:34'),
	(75,1,'127.0.0.1','Add tag:Review','2019-07-12 12:46:40'),
	(76,1,'127.0.0.1','Add tag:Science','2019-07-12 12:46:46'),
	(77,1,'127.0.0.1','Add tag:Self help','2019-07-12 12:46:53'),
	(78,1,'127.0.0.1','Add tag:Travel','2019-07-12 12:46:59'),
	(79,1,'127.0.0.1','Add tag:True crime','2019-07-12 12:47:05'),
	(80,1,'127.0.0.1','Add tag:Religion, spirituality, and new age','2019-07-12 13:25:29'),
	(81,1,'127.0.0.1','Add tag:Textbook','2019-07-12 13:25:49'),
	(82,1,'127.0.0.1','Add tag:Review','2019-07-12 13:25:57'),
	(83,1,'127.0.0.1','Add tag:Science','2019-07-12 13:26:06'),
	(84,1,'127.0.0.1','Add tag:Travel','2019-07-12 13:27:35'),
	(85,1,'127.0.0.1','Add the book: What You Did','2019-07-12 13:49:45'),
	(86,1,'127.0.0.1','Add the book: Self-Discipline Made Easy','2019-07-12 13:57:16'),
	(87,1,'127.0.0.1','Add the movie: A Chinese singer concert.','2019-07-16 21:19:48'),
	(88,1,'127.0.0.1','Add the movie: Qiu YiNong','2019-07-16 21:26:22'),
	(89,1,'127.0.0.1','Add the movie: Running Man','2019-07-16 21:35:01'),
	(90,1,'127.0.0.1','Add the movie: Why You Never Forget Anything','2019-07-16 22:04:32'),
	(91,1,'127.0.0.1','Add the music: Lemon Tree','2019-07-16 22:11:31'),
	(92,1,'127.0.0.1','Add the movie: Ugly Duck','2019-07-16 22:56:21'),
	(93,1,'127.0.0.1','Add the music: YiShengHeQiu','2019-07-16 23:01:48'),
	(94,1,'127.0.0.1','Delete tag:Prayer','2019-07-17 09:42:59'),
	(95,1,'127.0.0.1','Delete tag:Book review','2019-07-17 09:43:53'),
	(96,1,'127.0.0.1','Add tag:xiaowei','2019-07-18 15:43:16'),
	(97,1,'127.0.0.1','Delete tag:xiaowei','2019-07-18 15:43:23'),
	(98,1,'127.0.0.1','Add tag:Sports','2019-07-18 15:46:17'),
	(99,1,'127.0.0.1','Add tag:War','2019-07-18 17:09:31'),
	(100,1,'127.0.0.1','Add tag:test','2019-07-18 17:26:10'),
	(101,1,'127.0.0.1','Delete tag:test','2019-07-18 17:26:19');

/*!40000 ALTER TABLE `oplog` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table preview
# ------------------------------------------------------------

DROP TABLE IF EXISTS `preview`;

CREATE TABLE `preview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `logo` (`logo`),
  KEY `ix_preview_addtime` (`addtime`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `preview` WRITE;
/*!40000 ALTER TABLE `preview` DISABLE KEYS */;

INSERT INTO `preview` (`id`, `title`, `logo`, `addtime`)
VALUES
	(1,'Spring','20190625161310ea88f7f50f9a4bba83e7c4f6b5702b19.jpg','2019-06-25 16:13:11'),
	(2,'Star','20190625161349a6755e6a6b984336b86ee16768aa154e.jpg','2019-06-25 16:13:11'),
	(3,'Winter','20190625161400201574cbbd6341b0982cdb7d6a212cd4.jpg','2019-06-25 16:13:11'),
	(4,'Flowers','201906251614148742208c906d4d73951e9ce2274dd8a3.jpg','2019-06-25 16:13:11'),
	(5,'Friends','20190625161432a792516e53c24b8aabdba8a550649add.jpg','2019-06-25 16:13:11'),
	(6,'Book','201906251615322e9f2899568c4f4999eb8366a25f9962.jpg','2019-06-25 16:13:11');

/*!40000 ALTER TABLE `preview` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table role
# ------------------------------------------------------------

DROP TABLE IF EXISTS `role`;

CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `auths` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_addtime` (`addtime`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;

INSERT INTO `role` (`id`, `name`, `auths`, `addtime`)
VALUES
	(1,'Super Admin','1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44','2019-07-07 10:50:00'),
	(2,'Tag Manager','1,2,3,4','2019-07-08 11:47:06'),
	(3,'Movie Manager','5,6,7,8','2019-07-08 11:58:00'),
	(4,'Music Manager','33,34,35,36','2019-07-08 12:00:10');

/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table tag
# ------------------------------------------------------------

DROP TABLE IF EXISTS `tag`;

CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `zodiac` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_tag_addtime` (`addtime`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;

INSERT INTO `tag` (`id`, `name`, `addtime`, `zodiac`)
VALUES
	(1,'comedy','2019-07-07 10:50:00','1'),
	(2,'tragedy','2019-07-07 10:50:00','1'),
	(3,'fiction','2019-07-07 10:50:00','1'),
	(4,'Romantic ','2019-07-09 12:44:33','1'),
	(5,'Alternative','2019-07-10 17:00:54','1,10'),
	(6,'Anime','2019-07-10 17:04:18','1'),
	(7,'Blues','2019-07-10 17:04:26','1'),
	(8,'Children','2019-07-10 17:04:44','1'),
	(9,'Classical','2019-07-10 17:04:57','1'),
	(10,'Commercial','2019-07-10 17:05:11','1'),
	(11,'Country','2019-07-10 17:05:21','1'),
	(12,'Dance','2019-07-10 17:05:32','1'),
	(13,'Disney','2019-07-10 17:05:44','1'),
	(14,'Easy Listening','2019-07-10 17:05:51','1'),
	(15,'Electronic','2019-07-10 17:05:58','1'),
	(16,'Enka','2019-07-10 17:28:30','1'),
	(17,'Folk','2019-07-10 17:28:41','1'),
	(18,'Pop','2019-07-10 17:28:51','1'),
	(19,'Hip-Hop/Rap','2019-07-10 17:29:08','1'),
	(20,'Fitness & Workout','2019-07-10 17:29:15','1'),
	(21,'Holiday','2019-07-10 17:29:25','1'),
	(22,'Industrial','2019-07-10 17:29:34','1'),
	(23,'Instrumental','2019-07-10 17:29:48','1'),
	(24,'Jazz','2019-07-10 17:29:58','1'),
	(25,'Latin','2019-07-10 17:30:08','1'),
	(26,'Opera','2019-07-10 17:30:46','1'),
	(27,'R&B/Soul','2019-07-10 17:31:00','1'),
	(28,'Reggae','2019-07-10 17:31:12','1'),
	(29,'Rock','2019-07-10 17:31:25','1'),
	(30,'Action and adventure','2019-07-12 12:29:26','1,10'),
	(31,'Alternate history','2019-07-12 12:29:46','1,10'),
	(32,'Anthology','2019-07-12 12:29:58','1'),
	(33,'Chick lit','2019-07-12 12:32:17','1'),
	(34,'Coming-of-age','2019-07-12 12:36:59','1'),
	(35,'Crime','2019-07-12 12:37:09','1'),
	(36,'Drama','2019-07-12 12:37:15','1'),
	(37,'Fairytale','2019-07-12 12:37:21','1'),
	(38,'Fantasy','2019-07-12 12:37:31','1'),
	(39,'Graphic novel','2019-07-12 12:37:42','1'),
	(40,'Historical fiction','2019-07-12 12:37:48','1'),
	(41,'Horror','2019-07-12 12:37:57','1'),
	(42,'Mystery','2019-07-12 12:38:04','1'),
	(43,'Paranormal romance','2019-07-12 12:40:32','1'),
	(44,'Picture book','2019-07-12 12:42:22','1'),
	(45,'Poetry','2019-07-12 12:42:29','1'),
	(46,'Political thriller','2019-07-12 12:42:38','1'),
	(47,'Satire','2019-07-12 12:43:12','1'),
	(48,'Science fiction','2019-07-12 12:43:17','1'),
	(49,'Short story','2019-07-12 12:43:22','1'),
	(50,'Suspense','2019-07-12 12:43:31','1'),
	(51,'Thriller','2019-07-12 12:43:36','1'),
	(52,'Young adult','2019-07-12 12:43:44','1'),
	(53,'Art','2019-07-12 12:44:00','1'),
	(54,'Autobiography','2019-07-12 12:44:04','1,10,12'),
	(55,'Biography','2019-07-12 12:44:10','1'),
	(57,'Cookbook','2019-07-12 12:44:23','1'),
	(58,'Diary','2019-07-12 12:44:31','1'),
	(59,'Dictionary','2019-07-12 12:44:38','1'),
	(60,'Encyclopedia','2019-07-12 12:44:45','1'),
	(61,'Guide','2019-07-12 12:44:49','1'),
	(62,'Health','2019-07-12 12:44:59','1'),
	(63,'History','2019-07-12 12:45:07','1'),
	(64,'Journal','2019-07-12 12:45:17','1'),
	(65,'Math','2019-07-12 12:45:41','1'),
	(66,'Memoir','2019-07-12 12:45:53','1'),
	(75,'Religion, spirituality, and new age','2019-07-12 13:25:29','1'),
	(76,'Textbook','2019-07-12 13:25:49','1'),
	(77,'Review','2019-07-12 13:25:57','1'),
	(79,'Sports','2019-07-18 15:46:17','1'),
	(80,'War','2019-07-18 17:09:31','1,2,3');

/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `gender` int(11) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `info` text,
  `face` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  `facebook` varchar(255) DEFAULT NULL,
  `instagram` varchar(255) DEFAULT NULL,
  `twitter` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_user_addtime` (`addtime`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;

INSERT INTO `user` (`id`, `name`, `gender`, `pwd`, `DOB`, `email`, `phone`, `info`, `face`, `addtime`, `uuid`, `facebook`, `instagram`, `twitter`)
VALUES
	(1,'xiaowei',2,'pbkdf2:sha256:150000$yAu8MYFT$f777bd86bdb54d6e0f6b78a44616100849ddac4ee4fa22936fe249d3765cb4cf','1998-12-25','xchen8897@gmail.com','9293009291','test','2022032815232640056ddfcf814fea82721d88f26ce68b.jpeg','2019-07-07 16:39:26','f26d7ad5ccd04a809825ec4ecfc57e36','https://www.facebook.com/xiaowei.chen.3705','https://www.facebook.com/xiaowei.chen.3705','https://twitter.com/WEI16090918'),
	(2,'yuan',1,'pbkdf2:sha256:150000$gwh3hQ8W$87fbf4e48d651620016fb886aa3a51c0911b563af5b0f1afb4f6a60c5e42786a','1988-12-25','yuan@gmail.com','9293009295','I like playing video games, singing, and reading books','20190715111228f3c13540def94c39ab2c99ab178ed3c7.jpg','2019-07-08 14:41:49','c6b45001a1d54c8c9352184715a67d56','https://www.facebook.com/xiaowei.chen.3705','https://www.facebook.com/xiaowei.chen.3705','https://www.facebook.com/xiaowei.chen.3705'),
	(3,'heng',1,'pbkdf2:sha256:150000$08zG7ta6$34edd353fdf9eb0ecd1d9ba0adb8dc145930c33c79b3382cbb0fd98a7f82c465','1988-12-25','heng@gmail.com','3472061111','I am a foodie, I like all kinds of food','201907151112553a9426b361d1496eb3016f1d19b3b461.jpg','2019-07-08 15:10:41','e439c81d24fe4fe8901a6c6302da0efc','https://www.facebook.com/xiaowei.chen.3705','https://www.facebook.com/xiaowei.chen.3705','https://www.facebook.com/xiaowei.chen.3705'),
	(4,'shah',1,'pbkdf2:sha256:150000$BcxI3cqy$a8c2916b27b2c00e4a4e81e9ce195edebe0b59d564f86ddbd79af0f680a698d5','1976-04-15','shah@gmail.com','3472061112','hahaha','2019072414404998d746603db145d3b4e5a16a0ef77341.jpg','2019-07-24 14:34:47','3a8d8789f483471f9be7141c90555815','https://www.facebook.com/xiaowei.chen.3705','https://www.instagram.com/','https://twitter.com/WEI16090918'),
	(5,'Rumi',2,'pbkdf2:sha256:150000$4IjZT2XO$3209be1803238650f347c9467cd79558629eac3c3b86cda4f4a4df3663046416','2005-01-12','rumi@gmail.com','9293009201','I do not want to tell you everything','2019072611591170ada7815e5449a2a34616020344efa8.png','2019-07-26 11:36:14','78b894f31c2345298a231e8a3ec4217c','https://www.facebook.com/xiaowei.chen.3705','https://www.instagram.com/drsebiscellfood/','https://twitter.com/WEI16090918'),
	(6,'Alexandra',NULL,'pbkdf2:sha256:150000$znwgD3Do$719f61119010f964f3ce2ecdd9bee53bedd97c845c41d9ecb6b7d8469f21697e',NULL,'Alexandra@gmail.com','9293009202',NULL,NULL,'2019-07-26 13:39:54','2cf713a244714e5cbb34e4032afb6664',NULL,NULL,NULL),
	(7,'Breanna',2,'pbkdf2:sha256:150000$LT1MPZUa$d417e644b2acfd0262d2cef3b819e2465d19476b28ac381b2e73cf9ed25cb025','1994-03-18','breanna@gmail.com','9293009203','I want to be friend with you','2019072908591558aa96a72d3a449abd275bcd6477decc.png','2019-07-29 08:58:18','2c441f297f1946abbbe254d67d68ff2f','https://www.facebook.com/xiaowei.chen.3705','https://www.instagram.com/nathanwpylestrangeplanet/','https://twitter.com/WEI16090918');

/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table userlog
# ------------------------------------------------------------

DROP TABLE IF EXISTS `userlog`;

CREATE TABLE `userlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_userlog_addtime` (`addtime`),
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `userlog` WRITE;
/*!40000 ALTER TABLE `userlog` DISABLE KEYS */;

INSERT INTO `userlog` (`id`, `user_id`, `ip`, `addtime`)
VALUES
	(1,1,'127.0.0.1','2019-07-07 16:39:44'),
	(2,1,'127.0.0.1','2019-07-07 17:09:40'),
	(3,1,'127.0.0.1','2019-07-08 10:49:28'),
	(4,1,'127.0.0.1','2019-07-08 14:23:38'),
	(5,2,'127.0.0.1','2019-07-08 14:41:55'),
	(6,3,'127.0.0.1','2019-07-08 15:10:48'),
	(7,1,'127.0.0.1','2019-07-08 15:21:30'),
	(8,1,'127.0.0.1','2019-07-09 10:55:16'),
	(9,1,'127.0.0.1','2019-07-10 09:43:28'),
	(10,1,'127.0.0.1','2019-07-13 16:26:33'),
	(11,1,'127.0.0.1','2019-07-15 10:18:28'),
	(12,2,'127.0.0.1','2019-07-15 11:11:06'),
	(13,3,'127.0.0.1','2019-07-15 11:12:38'),
	(14,1,'127.0.0.1','2019-07-19 21:43:37'),
	(15,1,'127.0.0.1','2019-07-19 23:12:59'),
	(16,1,'127.0.0.1','2019-07-21 16:20:40'),
	(17,1,'127.0.0.1','2019-07-24 10:23:28'),
	(18,1,'127.0.0.1','2019-07-24 12:04:40'),
	(19,4,'127.0.0.1','2019-07-24 14:34:54'),
	(20,1,'127.0.0.1','2019-07-25 12:22:51'),
	(21,4,'127.0.0.1','2019-07-25 12:23:57'),
	(22,1,'127.0.0.1','2019-07-26 10:42:34'),
	(23,5,'127.0.0.1','2019-07-26 11:36:22'),
	(24,1,'127.0.0.1','2019-07-26 11:54:38'),
	(25,6,'127.0.0.1','2019-07-26 13:40:01'),
	(26,1,'127.0.0.1','2019-07-26 13:40:49'),
	(27,3,'127.0.0.1','2019-07-26 17:24:06'),
	(28,3,'127.0.0.1','2019-07-26 17:31:56'),
	(29,7,'127.0.0.1','2019-07-29 08:58:23'),
	(30,1,'127.0.0.1','2019-07-29 11:03:10'),
	(31,2,'127.0.0.1','2019-07-29 11:06:18'),
	(32,1,'127.0.0.1','2019-07-29 11:07:08'),
	(33,3,'127.0.0.1','2019-07-29 11:11:04'),
	(34,1,'127.0.0.1','2022-03-28 15:14:59'),
	(35,1,'127.0.0.1','2022-03-28 15:27:14');

/*!40000 ALTER TABLE `userlog` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
