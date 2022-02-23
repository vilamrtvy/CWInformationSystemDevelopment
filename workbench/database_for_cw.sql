-- MySQL dump 10.13  Distrib 8.0.22, for macos10.15 (x86_64)
--
-- Host: 127.0.0.1    Database: Hospital
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Department`
--

DROP TABLE IF EXISTS `Department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Department` (
  `dep_id` int NOT NULL,
  `bran_name` varchar(45) NOT NULL,
  `dephead_key` int DEFAULT NULL,
  PRIMARY KEY (`dep_id`),
  KEY `doctor_idx` (`dephead_key`),
  CONSTRAINT `dephead` FOREIGN KEY (`dephead_key`) REFERENCES `Doctor` (`doc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Department`
--

LOCK TABLES `Department` WRITE;
/*!40000 ALTER TABLE `Department` DISABLE KEYS */;
INSERT INTO `Department` VALUES (101,'Кардиология',1001),(102,'Аллергология',1004),(103,'Гастроэнтерология',1009),(104,'Эндокринология',1008),(105,'Гинекология и урология',1012),(106,'Неврология',1010),(107,'Онкология',1020),(108,'Травматология и ортопедия',1015),(109,'Терапевтия',1022),(110,'Инфекционное отделение',1017),(111,'Приемное отделение',1003),(112,'Реанимация',1011),(113,'Психиатрия',1014),(114,'Анестезиология',1005),(115,'Рентгенология',1007);
/*!40000 ALTER TABLE `Department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Doctor`
--

DROP TABLE IF EXISTS `Doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Doctor` (
  `doc_id` int NOT NULL,
  `doc_name` varchar(45) NOT NULL,
  `doc_recr` date DEFAULT NULL,
  `doc_dism` date DEFAULT NULL,
  `depart_key` int NOT NULL,
  `login` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `post` varchar(45) DEFAULT NULL,
  `gender` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`doc_id`),
  KEY `depart_idx` (`depart_key`),
  CONSTRAINT `depart` FOREIGN KEY (`depart_key`) REFERENCES `Department` (`dep_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Doctor`
--

LOCK TABLES `Doctor` WRITE;
/*!40000 ALTER TABLE `Doctor` DISABLE KEYS */;
INSERT INTO `Doctor` VALUES (1000,'Копнина Дарья','2000-01-05',NULL,107,'Kopnina','K1Rn','dc','w'),(1001,'Жашуева Сабина','1996-08-20',NULL,101,'Zhashueva','qwerty','mrg','w'),(1002,'Корнеева Ольга','2008-10-01','2020-06-30',113,'Korneeva','korn123','dc','w'),(1003,'Ефремова Наталья','1998-03-25',NULL,111,'Efremova','efim000','scr','w'),(1004,'Трофимова Мария','2002-07-17',NULL,102,'Trofimova','Maria1','mrg','w'),(1005,'Бразуев Кантемир','2021-01-19',NULL,114,'Brazuev','K1nt3m','mrga','m'),(1006,'Кочетова Елена','2005-08-22',NULL,106,'Kochetova','3l3na_33','dc','w'),(1007,'Тальковский Евгений','1999-05-29',NULL,115,'Talkovskiy','zheka293','mrga','m'),(1008,'Хромов Михаил','2007-03-08',NULL,104,'Hromov','misha_hromov','mrg','m'),(1009,'Чура Иван','2013-01-13',NULL,103,'Chura','ivan_chura079','mrg','m'),(1010,'Катунова Марина','2004-08-10',NULL,106,'Katunova','marina2008','mrg','w'),(1011,'Михалева Светлана','1999-05-30',NULL,112,'Mihaleva','svetlanamihaleva','mrg','w'),(1012,'Кригер Мария','1998-04-20',NULL,105,'Kriger','Mariyakriger1967','mrg','w'),(1013,'Мистрюкова Валерия','2003-07-31','2009-02-20',109,'Mistrykova','Valeria_246','dc','w'),(1014,'Грабовская Маргарита','2003-07-15',NULL,113,'Grabovskaya','ritagrabovskaya','mrg','w'),(1015,'Траубе Мария','2010-10-01',NULL,108,'Traube','traube111','mrg','w'),(1016,'Куренкова Нинель','2013-04-19',NULL,109,'Kurenkova','ninelistvanovna','dc','w'),(1017,'Маршев Михаил','1995-09-01',NULL,110,'Marshev','mihmarshmih','mrg','m'),(1018,'Матвеев Геннадий','1987-04-02','2020-08-31',103,'Matveev','gennnnadi','dc','m'),(1019,'Мельничук Татьяна','1991-10-12','2018-04-29',104,'Melnichuk','melnichuk','dc','w'),(1020,'Осипов Валерий','1994-05-01',NULL,107,'Osipov','valeriy1960','mrg','m'),(1021,'Ткачук Андрей','2008-03-29',NULL,105,'Tkachuk','andreytkachek1950','dc','m'),(1022,'Савчук Марина','2012-07-01',NULL,109,'Savchuk','marina_sevil','mrg','w'),(1023,'Капустин Захар','2013-04-10',NULL,113,'Kapustil','Zahar!kaputsin','dc','m'),(1024,'Квасов Дмитрий','2009-09-11',NULL,110,'Kvasov','DmitriyKvasov1970','dc','m'),(1025,'Денисюк Виктория','2013-04-21',NULL,101,'Denisuk','vika276denisuk','dc','w');
/*!40000 ALTER TABLE `Doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `History`
--

DROP TABLE IF EXISTS `History`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `History` (
  `his_id` int NOT NULL AUTO_INCREMENT,
  `rec_date` date NOT NULL,
  `rec_diag` varchar(45) DEFAULT NULL,
  `dis_date` date DEFAULT NULL,
  `dis_diag` varchar(45) DEFAULT NULL,
  `pat_key` int NOT NULL,
  `doc_key` int NOT NULL,
  `ward_key` int DEFAULT NULL,
  PRIMARY KEY (`his_id`),
  KEY `patient_idx` (`pat_key`),
  KEY `doctor_idx` (`doc_key`),
  KEY `ward_idx` (`ward_key`),
  CONSTRAINT `doc` FOREIGN KEY (`doc_key`) REFERENCES `Doctor` (`doc_id`) ON UPDATE CASCADE,
  CONSTRAINT `pat` FOREIGN KEY (`pat_key`) REFERENCES `Patient` (`pat_id`) ON UPDATE CASCADE,
  CONSTRAINT `ward` FOREIGN KEY (`ward_key`) REFERENCES `Ward` (`ward_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10103 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `History`
--

LOCK TABLES `History` WRITE;
/*!40000 ALTER TABLE `History` DISABLE KEYS */;
INSERT INTO `History` VALUES (10011,'2020-01-19','Аллергия','2020-01-24',NULL,6,1016,147),(10012,'2020-01-31','Инсульт','2020-03-05',NULL,24,1001,115),(10013,'2020-02-14','Ангина','2020-02-23',NULL,19,1017,149),(10014,'2020-02-25','Гастрит','2020-03-08',NULL,4,1018,126),(10015,'2020-03-16','Коронавирусная инфекция','2020-04-01',NULL,17,1017,152),(10016,'2020-03-18','Язва желудка','2020-05-13',NULL,23,1009,123),(10017,'2020-03-29','Диабет','2020-04-24',NULL,16,1018,125),(10018,'2020-04-15','Перелом руки','2020-04-18',NULL,2,1015,146),(10019,'2020-05-18','Эндометрит','2020-05-30',NULL,11,1012,134),(10020,'2020-06-13','Психоз','2020-07-10',NULL,3,1006,155),(10021,'2020-06-27','Дисбактериоз','2020-07-04',NULL,5,1018,124),(10022,'2020-07-18','Коронавирусная инфекция','2020-08-02',NULL,9,1024,151),(10023,'2020-08-03','Варикоцеле','2020-08-13',NULL,14,1021,132),(10024,'2020-09-19','Диабет','2020-10-03',NULL,21,1025,118),(10025,'2020-10-02','Травма головного мозга','2020-10-10',NULL,18,1010,137),(10026,'2020-11-16','Трихомониаз','2020-12-03',NULL,8,1024,149),(10027,'2020-12-14','Ангина','2021-01-06',NULL,20,1017,152),(10028,'2021-01-13','Атеросклероз','2021-01-19',NULL,7,1001,116),(10029,'2021-01-19','Ветряная оспа','2021-02-15',NULL,5,1017,150),(10030,'2021-02-04','Неврозы','2021-03-29',NULL,4,1010,136),(10031,'2021-02-19','Аденома ','2021-03-04',NULL,13,1012,131),(10032,'2021-02-28','Коронавирусная инфекция','2021-04-01',NULL,22,1024,149),(10033,'2021-03-05','Аллергия','2021-03-17',NULL,6,1022,148),(10034,'2021-03-09','Ангина','2021-03-19',NULL,23,1024,151),(10035,'2021-03-16','Мононуклеоз','2021-04-02',NULL,14,1017,152),(10036,'2021-03-24','Перелом ключицы','2021-04-04',NULL,15,1015,144),(10037,'2021-03-26','Гипертония','2021-04-05',NULL,24,1001,118),(10038,'2021-03-27','Колит','2021-12-14',NULL,2,1009,126),(10039,'2021-03-29','Инсульт',NULL,NULL,25,1025,131),(10040,'2021-04-03','Биполярное расстройство',NULL,NULL,12,1006,156),(10041,'2021-04-05','Астма',NULL,NULL,10,1022,147),(10042,'2021-04-07','Киста',NULL,NULL,11,1021,132),(10045,'2021-12-12','Киста яичников',NULL,NULL,4,1012,132),(10046,'2021-12-12','Пиелонефрит','2021-12-16',NULL,48,1012,133),(10049,'2021-12-12','Цистит',NULL,NULL,51,1012,131),(10051,'2021-12-12','Нарколепсия',NULL,NULL,5,1006,136),(10052,'2021-12-12','Биполярное расстройство',NULL,NULL,3,1014,154),(10053,'2021-12-12','Тревожное расстройство',NULL,NULL,7,1014,154),(10054,'2021-12-12','Бронхиальная астма','2021-12-14',NULL,47,1004,120),(10061,'2021-12-12',NULL,NULL,NULL,54,1010,NULL),(10065,'2021-12-13',NULL,NULL,NULL,58,1020,NULL),(10083,'2021-12-13','Язва дв-ой кишки',NULL,NULL,76,1009,124),(10085,'2021-12-13','Поллиноз','2021-12-14',NULL,78,1004,120),(10086,'2021-12-13','Дуоденит','2021-12-14',NULL,6,1009,124),(10087,'2021-12-14','Колит','2021-12-14',NULL,13,1009,123),(10088,'2021-12-14','Панкреатит','2021-12-14',NULL,6,1009,123),(10089,'2021-12-14','Конъюктивит',NULL,NULL,79,1004,119),(10090,'2021-12-15','Тревожное расстройство',NULL,NULL,80,1014,153),(10091,'2021-12-15','Панкреатит',NULL,NULL,1,1009,126),(10092,'2021-12-15',' ',NULL,NULL,15,1014,154),(10093,'2021-12-15',NULL,NULL,NULL,19,1014,NULL),(10094,'2021-12-16','Киста яичников',NULL,NULL,81,1012,133),(10095,'2021-12-17',NULL,NULL,NULL,13,1021,NULL),(10096,'2021-12-17','Уреоплазмоз',NULL,NULL,8,1012,131),(10097,'2021-12-17',NULL,NULL,NULL,18,1021,NULL),(10098,'2021-12-17',NULL,NULL,NULL,9,1004,NULL),(10099,'2021-12-30','Психоз','2022-01-13',NULL,6,1002,154),(10100,'2022-01-13','Шизофрения',NULL,NULL,21,1002,153),(10101,'2022-01-13',NULL,NULL,NULL,82,1002,NULL),(10102,'2022-01-13','Деменция',NULL,NULL,83,1002,153);
/*!40000 ALTER TABLE `History` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Patient`
--

DROP TABLE IF EXISTS `Patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Patient` (
  `pat_id` int NOT NULL AUTO_INCREMENT,
  `pat_name` varchar(45) NOT NULL,
  `pat_passport` varchar(11) DEFAULT NULL,
  `pat_birthday` date DEFAULT NULL,
  `pat_address` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`pat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Patient`
--

LOCK TABLES `Patient` WRITE;
/*!40000 ALTER TABLE `Patient` DISABLE KEYS */;
INSERT INTO `Patient` VALUES (1,'Титова Камилла','4515246000','2001-10-06','Москва, Окская, 25, 75'),(2,'Ворошилина Милена','4515246001','2001-08-20','Москва, Полетаева, 105, 13'),(3,'Лахири Максим','4515246002','2001-06-05','Москва, Полетаева, 21, 105'),(4,'Зиновьева Софья','4515246003','2001-05-23','Москва, Полетаева, 21, 103'),(5,'Куликова Олеся','4515246004','2001-09-08','Москва, Есенинская, 5, 59'),(6,'Никулеску Денис','4515246005','2001-01-19','Москва, Шумилова, 9, 22'),(7,'Никулеску Арина','4515246006','2001-03-08','Москва, Шумилова, 9, 22'),(8,'Вальгер Денис','4515246007','2000-12-23','Москва, Шумилова, 13, 18'),(9,'Аширова Альбина','4515246008','2000-11-29','Москва, Зеленодольская, 5, 108'),(10,'Смоленова Ксения','4515246009','2000-12-05','Москва, Скрябина, 4, 89'),(11,'Донченко Мария','4515246010','1999-02-20','Ульяновск, Ленина, 43'),(12,'Вольк Дарья','4515246011','2001-06-26','Нижний Новгород, Мажковская, 37, 198'),(13,'Аксенов Михаил','4515246023','1998-06-26','Воронеж, Жуковская, 19'),(14,'Нифилим Роман','4515246023','1996-08-10','Москва, Стахановская, 10, 117'),(15,'Боженко Дмитрий','4515246024','1999-10-29','Курск, Маршала Жукова, 25, 119'),(16,'Качалинский Георгий','4515246025','1995-04-04','Химки, Малая Юрская, 29'),(17,'Денисов Владимир','4515246026','1991-07-25','Москва, Коновалова, 4, 12'),(18,'Сероштан Кирилл','4515246027','1998-03-31','Москва, Рассветная, 14'),(19,'Спилов Егор','4515246028','1989-05-16','Москва, Перовская, 24, 254'),(20,'Манукян Арсений','4515246029','1993-04-11','Москва, Новокузьминская, 19, 44'),(21,'Богдан Брага','4515246030','1998-04-13','Балашиха, Левонская, 13'),(22,'Королев Александр','4515246031','1982-02-03','Москва, Старая Басманная, 19, 1'),(23,'Ефремов Виктор','4515246032','1974-11-30','Омск, Металлургов, 34'),(24,'Нестеров Кирилл','4515246033','1960-09-12','Новосибирск, Зеленый проспект, 12'),(25,'Кузьмина Мария','4515246034','1957-03-08','Владивосток, Лапина, 17, 198'),(47,'Барышев Артем','3781 924734','1989-03-07','Москва, Кустанаевская, 18, 256'),(48,'Верзина Елизавета','4505 247134','1998-10-02','Москва, Окская, 17, 36'),(51,'Филина Александра','4502 361298','1992-02-02','Москва, Большая Черкизовская, 11, 198'),(53,'Зайцев Денис','3798 129091','1980-11-05','Москва, Береговой проезд, 17, 191'),(54,'Веленчук Алина','4500 287132','1980-11-02','Химки, Брюллова, 3, 271'),(58,'Борисов Михаил','4519 241781','1999-04-18','Подольск, Маршала Жукова, 14'),(76,'Складченко Виктория','4501 131894','1987-07-07','Москва, Мелиховская, 18, 101'),(78,'Созонов Георгий','4507 190987','1982-03-24','Можайск, проезд 1905 года, 35'),(79,'Поленчук Мария','4502 371824','1989-05-07','Москва, Бульвар Рокоссовского, 31, 74'),(80,'Козлов Алексей','4518 376541','1998-09-07','Москва, Солнечная, 14, 78'),(81,'Бакунина Маргарита','4501 241423','1964-12-16','Москва, Пресненский Вал, 37, 13'),(82,'Сурков Максим','',NULL,''),(83,'Сурков Максим','','2001-04-06','');
/*!40000 ALTER TABLE `Patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ward`
--

DROP TABLE IF EXISTS `Ward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Ward` (
  `ward_id` int NOT NULL,
  `ward_cat` varchar(45) NOT NULL,
  `ward_number` int NOT NULL,
  `ward_places` varchar(45) NOT NULL,
  `bran_key` int NOT NULL,
  PRIMARY KEY (`ward_id`),
  KEY `bran_idx` (`bran_key`),
  CONSTRAINT `bran` FOREIGN KEY (`bran_key`) REFERENCES `Department` (`dep_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ward`
--

LOCK TABLES `Ward` WRITE;
/*!40000 ALTER TABLE `Ward` DISABLE KEYS */;
INSERT INTO `Ward` VALUES (115,'Econom',1,'4',101),(116,'Econom',2,'4',101),(117,'Comfort',3,'2',101),(118,'Luxe',4,'1',101),(119,'Econom',1,'4',102),(120,'Econom',2,'4',102),(121,'Comfort',3,'2',102),(122,'Luxe',4,'1',102),(123,'Econom',1,'4',103),(124,'Econom',2,'4',103),(125,'Comfort',3,'2',103),(126,'Luxe',4,'1',103),(127,'Econom',1,'4',104),(128,'Econom',2,'4',104),(129,'Comfort',3,'2',104),(130,'Luxe',4,'1',104),(131,'Econom',1,'4',105),(132,'Econom',2,'4',105),(133,'Comfort',3,'2',105),(134,'Luxe',4,'1',105),(135,'Econom',1,'4',106),(136,'Econom',2,'4',106),(137,'Comfort',3,'2',106),(138,'Luxe',4,'1',106),(139,'Econom',1,'4',107),(140,'Econom',2,'4',107),(141,'Comfort',3,'2',107),(142,'Luxe',4,'1',107),(143,'Econom',1,'4',108),(144,'Econom',2,'4',108),(145,'Comfort',3,'2',108),(146,'Luxe',4,'1',108),(147,'Econom',1,'6',109),(148,'Econom',2,'6',109),(149,'Econom',1,'4',110),(150,'Econom',2,'4',110),(151,'Comfort',3,'2',110),(152,'Luxe',4,'1',110),(153,'Econom',1,'4',113),(154,'Econom',2,'4',113),(155,'Comfort',3,'2',113),(156,'Luxe',4,'1',113),(157,'Double',1,'2',114),(158,'Double',2,'2',114),(159,'Single',3,'1',114),(160,'Single',4,'1',114);
/*!40000 ALTER TABLE `Ward` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'Hospital'
--
/*!50003 DROP PROCEDURE IF EXISTS `new` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `new`(in usl date, in big date)
begin
	declare time1, time2 date;
    set time1 = usl;
    set time2 = big;
	select * from history
	where time1 <= rec_date
    and time2 >= dis_date;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-23 18:46:02
