CREATE DATABASE `love_love_wall` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
use love_love_wall;
CREATE TABLE `user_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户id，对应user_auth的信息',
  `nickname` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户昵称，唯一',
  `avatar` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像的url链接',
  `qq` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'QQ',
  `wechat` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '微信号',
  `other` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '其他联系方式',
  `gender` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '性别。可以自己填，不校验。前端给默认的男、女、以及自定义',
  `target_gender` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '期待另一半的性别',
  `age` tinyint(3) DEFAULT NULL COMMENT '年龄',
  `target_age` varchar(5) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '期望另一半的年龄，5位长度，例如 20~30，也可以是 25 这样',
  `tag` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '标签。可以由多个标签组成，中间英文句号，例如：LOL,桌游,爬山',
  `ideal` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '理想',
  `company` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '公司。可以填公司名称，或公司类型，或公司描述',
  `city` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '城市',
  `income` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '收入，可以填具体数字，也可以填描述',
  `target_income` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '期待另一半的收入',
  `college` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '学校',
  `profession` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '行业/职业。例如：IT、互联网、财务等',
  `summary` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '一句话介绍',
  `is_hidden` int(11) DEFAULT '0' COMMENT '是否全部隐藏。0显示，1隐藏',
  `hidden_columns` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '非隐藏模式下，这里的值是隐藏的列的字段名，以逗号分隔。例如 age,tag 表示隐藏年龄和标签列',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_info_nickname_uindex` (`nickname`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户信息表';
CREATE TABLE `verify_email` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '邮箱地址',
  `verify_key` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '验证的key',
  `ctime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '发起验证的时间',
  `last_vtime` datetime DEFAULT '0000-00-00 00:00:00' COMMENT '上一次进行验证的时间（无论是否通过）',
  `is_pass` tinyint(3) DEFAULT '0' COMMENT '验证是否通过：0待验证，1验证通过',
  `is_invalid` tinyint(3) DEFAULT '0' COMMENT '0有效1无效，默认有效。同一邮箱创建新的后，将之前的设置为无效',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='邮箱验证。每创建一次验证，则插入一条数据。同一个邮箱验证可以插入多条数据';
CREATE TABLE `user_auth` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL COMMENT '注册邮箱',
  `pw` varchar(32) NOT NULL DEFAULT '' COMMENT '密码，以sha1存储，加盐',
  `phone` varchar(11) DEFAULT NULL COMMENT '手机号码（选填）',
  `permission` tinyint(1) NOT NULL DEFAULT '0' COMMENT '权限，0未验证用户，1普通用户，2被封禁用户，10管理员',
  `status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '账号状态，0启用，1禁用',
  `create_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `lastlogin_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '最近一次登录时间',
  `role` varchar(100) DEFAULT NULL COMMENT '发布人身份，手动修改表格填写，默认为空',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `用户名` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT COMMENT='用户权限表';
CREATE TABLE `reset_pw_list` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '邮箱地址',
  `verify_key` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '验证的key',
  `ctime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '发起重置密码申请的时间',
  `last_vtime` datetime DEFAULT '0000-00-00 00:00:00' COMMENT '上一次进行验证的时间（无论是否通过）',
  `is_pass` tinyint(3) DEFAULT '0' COMMENT '验证是否通过：0待验证，1验证通过',
  `is_invalid` tinyint(3) DEFAULT '0' COMMENT '0有效1无效，默认有效。同一邮箱创建新的后，将之前的设置为无效',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='重置密码。每创建一次重置密码的请求，则插入一条数据，同时使之前的那一次请求失效';
