/*
 Navicat Premium Data Transfer

 Source Server         : 本地连接
 Source Server Type    : MySQL
 Source Server Version : 80015
 Source Host           : localhost:3306
 Source Schema         : practice

 Target Server Type    : MySQL
 Target Server Version : 80015
 File Encoding         : 65001

 Date: 04/05/2019 04:24:42
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for staff
-- ----------------------------
DROP TABLE IF EXISTS `staff`;
CREATE TABLE `staff` (
  `user_name` varchar(20) NOT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(11) NOT NULL,
  `int_time` datetime DEFAULT NULL,
  PRIMARY KEY (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of staff
-- ----------------------------
BEGIN;
INSERT INTO `staff` VALUES ('tanhao', 'male', '', '10000000000', '2019-05-04 04:23:31');
INSERT INTO `staff` VALUES ('wankang', 'male', 'wankcn@icloud.com', '13520562678', '2019-05-04 04:23:31');
INSERT INTO `staff` VALUES ('yupeng', 'male', 'qin@lukseun.com', '15310568888', '2019-05-04 04:23:31');
INSERT INTO `staff` VALUES ('houyao', 'male', '', '88888888888', '2019-05-04 04:23:31');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
