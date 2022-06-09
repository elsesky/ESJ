-- 导出 esj 的数据库结构
CREATE DATABASE IF NOT EXISTS `esj` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `esj`;

-- 导出  表 esj.chapters 结构
CREATE TABLE IF NOT EXISTS `chapters` (
  `id` bigint(12) NOT NULL AUTO_INCREMENT,
  `nid` bigint(12) NOT NULL,
  `chapter_name` varchar(500) DEFAULT 'UNKNOWN',
  `order_num` bigint(12) DEFAULT NULL,
  `orgcontent` longtext DEFAULT NULL,
  `content` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `nid` (`nid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;

-- 数据导出被取消选择。

-- 导出  表 esj.novels 结构
CREATE TABLE IF NOT EXISTS `novels` (
  `id` bigint(12) NOT NULL AUTO_INCREMENT,
  `name` mediumtext NOT NULL,
  `Author` text DEFAULT NULL COMMENT '作者',
  `ImageUrl` mediumtext DEFAULT NULL,
  `Introduction` mediumtext DEFAULT NULL,
  `lastupdate` bigint(20) NOT NULL DEFAULT 0,
  `count` bigint(12) NOT NULL DEFAULT 0,
  `ViewCount` bigint(12) NOT NULL DEFAULT 0,
  `rcount` bigint(12) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `lastupdate` (`lastupdate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

