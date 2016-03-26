-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- 主機: localhost
-- 建立日期: 2016 年 03 月 26 日 20:55
-- 伺服器版本: 5.5.46-0ubuntu0.14.04.2
-- PHP 版本: 5.5.9-1ubuntu4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 資料庫: `lwc1503`
--

-- --------------------------------------------------------

--
-- 資料表結構 `pythonResult`
--

CREATE TABLE IF NOT EXISTS `pythonResult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `station1` int(11) NOT NULL,
  `station2` int(11) NOT NULL,
  `startDate` date NOT NULL,
  `p1` double NOT NULL,
  `p2` double NOT NULL,
  `p3` double NOT NULL,
  `p4` double NOT NULL,
  `p5` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3718083 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
