-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 30, 2023 at 06:00 AM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `drishtiparabha1`
--

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
CREATE TABLE IF NOT EXISTS `location` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `Email` varchar(30) NOT NULL,
  `Longitude` varchar(50) NOT NULL,
  `Latitude` varchar(50) NOT NULL,
  `Flag_web` varchar(2) NOT NULL,
  `Flag_app` varchar(2) NOT NULL,
  `Hardware_Address` varchar(50) NOT NULL,
  `Time_stamp` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`id`, `Email`, `Longitude`, `Latitude`, `Flag_web`, `Flag_app`, `Hardware_Address`, `Time_stamp`) VALUES
(1, 'abc@gmail.com', '72.153557', '21.772800', '0', '0', '0', '0'),
(2, 'abd@gmail.com', '73.153557', '22.772800', '0', '0', '0', '0');

-- --------------------------------------------------------

--
-- Table structure for table `mapping`
--

DROP TABLE IF EXISTS `mapping`;
CREATE TABLE IF NOT EXISTS `mapping` (
  `id` int(10) NOT NULL,
  `Email` varchar(30) NOT NULL,
  `Hardware_Address` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `mapping`
--

INSERT INTO `mapping` (`id`, `Email`, `Hardware_Address`) VALUES
(1, 'abc@gmail.com', '0');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `Name` varchar(20) NOT NULL,
  `Email` varchar(30) NOT NULL,
  `Password` varchar(60) NOT NULL,
  `Mobile_No` varchar(10) NOT NULL,
  `Address` varchar(50) NOT NULL,
  PRIMARY KEY (`Email`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`Name`, `Email`, `Password`, `Mobile_No`, `Address`) VALUES
('Rajyaguru Aryan', 'aryanrajyaguru22@gmail.com', '12345678', '7600663667', ' sihor'),
('Rajyaguru ', 'abc@gmail.com', '12345678', '1234567890', ' sihor');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
