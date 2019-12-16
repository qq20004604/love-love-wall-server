CREATE DATABASE `love_love_wall` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
use love_love_wall;
CREATE TABLE `user_auth` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL COMMENT '注册邮箱',
  `pw` varchar(32) NOT NULL DEFAULT '' COMMENT '密码，以sha1存储，加盐',
  `phone` varchar(11) DEFAULT NULL COMMENT '手机号码（选填）',
  `permission` tinyint(1) NOT NULL DEFAULT '0' COMMENT '权限，0未验证用户，1普通用户，2被封禁用户，10管理员',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '账号状态，0启用，1禁用',
  `create_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `lastlogin_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '最近一次登录时间',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `用户名` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT COMMENT='用户表';
CREATE TABLE `verify_email` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '邮箱地址',
  `verify_key` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '验证的key',
  `ctime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '发起验证的时间',
  `last_vtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '上一次进行验证的时间（无论是否通过）',
  `is_pass` tinyint(3) NOT NULL DEFAULT '0' COMMENT '验证是否通过：0待验证1验证失败2验证通过',
  `is_invalid` tinyint(3) NOT NULL DEFAULT '0' COMMENT '0有效1无效，默认有效。同一邮箱创建新的后，将之前的设置为无效',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮箱验证。每创建一次验证，则插入一条数据。同一个邮箱验证可以插入多条数据';
create table reset_pw_list
(
    Id         int auto_increment
        primary key,
    email      varchar(100) default ''                    not null comment '邮箱地址',
    verify_key varchar(50)  default ''                    not null comment '验证的key',
    ctime      datetime     default '0000-00-00 00:00:00' not null comment '发起重置密码申请的时间',
    last_vtime datetime     default '0000-00-00 00:00:00' null comment '上一次进行验证的时间（无论是否通过）',
    is_pass    tinyint(3)   default 0                     null comment '验证是否通过：0待验证，1验证通过',
    is_invalid tinyint(3)   default 0                     null comment '0有效1无效，默认有效。同一邮箱创建新的后，将之前的设置为无效'
)
    comment '重置密码。每创建一次重置密码的请求，则插入一条数据，同时使之前的那一次请求失效';