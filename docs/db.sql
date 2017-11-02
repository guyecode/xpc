CREATE DATABASE IF NOT EXISTS `xpc`;
USE `xpc`;


CREATE TABLE IF NOT EXISTS `posts` (
	`pid` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '作品表主键',
	`title` VARCHAR(256) NOT NULL COMMENT '作品标题',
	`preview` VARCHAR(512) COMMENT '视频预览图',
	`video` VARCHAR(512) COMMENT '视频链接',
	`video_format` VARCHAR(32) COMMENT '视频格式：4K 等',
	`category` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '作品分类',
	`created_at` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '发表时间',
	`description` text COMMENT '作品描述',
	`play_counts` INT(8) NOT NULL DEFAULT 0 COMMENT '播放次数',
	`like_counts` INT(8) NOT NULL DEFAULT 0 COMMENT '被点赞次数',
	PRIMARY KEY (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '作品表';

CREATE TABLE IF NOT EXISTS `composers` (
	`cid` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '创作者表主键',
	`banner` VARCHAR(512) NOT NULL COMMENT '用户主页banner图片',
	`avatar` VARCHAR(512) NOT NULL DEFAULT '' COMMENT '用户头像',
	`verified` int(1) NOT NULL DEFAULT 0 COMMENT '是否加V',
	`name`  VARCHAR(128) NOT NULL COMMENT '名字',
	`intro` TEXT COMMENT '自我介绍',
	`like_counts` INT(8) NOT NULL DEFAULT 0 COMMENT '被点赞次数',
	`fans_counts` INT(8) NOT NULL DEFAULT 0 COMMENT '被关注数量',
	`follow_counts` INT(8) NOT NULL DEFAULT 0 COMMENT '关注数量',
	PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '用户表';


CREATE TABLE IF NOT EXISTS `comments` (
	`commentid` int(11) NOT NULL COMMENT '评论表主键',
	`pid` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '评论的作品ID',
	`cid` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '评论人ID',
	`avatar` VARCHAR(512) COMMENT '评论人头像',
	`uname` VARCHAR(512) COMMENT '评论人名称',
	`created_at` VARCHAR(128) NOT NULL DEFAULT '' COMMENT '发表时间',
	`content` TEXT COMMENT '评论内容',
	`like_counts` INT(8) NOT NULL DEFAULT 0 COMMENT '被点赞次数',
	`reply` INT(8) NOT NULL DEFAULT 0 COMMENT '回复其他评论的ID，如果不是则为0',
	PRIMARY KEY (`commentid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '评论表';


CREATE TABLE IF NOT EXISTS `copyrights` (
	`pcid` VARCHAR(32) NOT NULL COMMENT '主键，由pid_cid组成',
	`pid` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '对应作品表主键',
	`cid` BIGINT UNSIGNED NOT NULL DEFAULT 0 COMMENT '对应作者表主键',
	`roles` VARCHAR(32) NOT NULL DEFAULT '' COMMENT '担任角色',
	PRIMARY KEY (`pcid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT '著作权关系表';