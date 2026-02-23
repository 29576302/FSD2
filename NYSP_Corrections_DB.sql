-- Drop data if re-executing.
/*
DROP DATABASE nysp_correction_notice_db;
DROP ROLE 'officer_role'@'localhost';
DROP ROLE 'citizen_role'@'localhost';
DROP USER 's_scott'@'localhost';
DROP USER 'j_smith'@'localhost';
DROP USER 'd_kroenke'@'localhost';
DROP USER 'j_doe_company'@'localhost';
*/
-- DDL:
-- Creating database and marking it for use.
CREATE DATABASE nysp_correction_notice_db;
USE nysp_correction_notice_db;

-- Creating the driver table.
CREATE TABLE driver (
	driver_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state CHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    drivers_licence VARCHAR(19) NOT NULL,
    drivers_licence_state CHAR(2) NOT NULL,
    birth_date DATE NOT NULL,
    height SMALLINT NOT NULL,
    weight SMALLINT NOT NULL,
    eyes VARCHAR(20) NOT NULL
    );

-- Creating the officer table.
CREATE TABLE officer (
	officer_id INT AUTO_INCREMENT PRIMARY KEY,
    personell_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    detachment VARCHAR(100) NOT NULL
    );
    
-- Creating the vehicle owner (person or company the vehicle is registered to) table.
CREATE TABLE vehicle_owner (
	vehicle_owner_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_name VARCHAR(255) NOT NULL,
    username VARCHAR(32) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state CHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL
    );

-- Creating a lookup table for violations.
CREATE TABLE violation_type (
	violation_type_id INT AUTO_INCREMENT PRIMARY KEY,
	`description` VARCHAR(255) NOT NULL UNIQUE,
	violation_code VARCHAR(20) NOT NULL
	);
        
-- Creating the vehicle table.
CREATE TABLE vehicle (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_owner_id INT NOT NULL,
    vehicles_licence VARCHAR(20) NOT NULL,
    state CHAR(2) NOT NULL,
    colour VARCHAR(30) NOT NULL,
    make VARCHAR(50) NOT NULL,
    vin VARCHAR(17) NOT NULL UNIQUE,
    `year` SMALLINT NOT NULL,
    `type` VARCHAR(50) NOT NULL,
    CONSTRAINT fk_vehicle_owner FOREIGN KEY (vehicle_owner_id) 
	REFERENCES vehicle_owner(vehicle_owner_id)
	);

-- Creating the central table for a single notice.
CREATE TABLE correction_notice (
    correction_notice_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    officer_id INT NOT NULL,
    violation_date DATE NOT NULL,
    violation_time TIME NOT NULL,
    location VARCHAR(255) NOT NULL,
    district VARCHAR(100) NOT NULL,
    warning BOOLEAN NOT NULL DEFAULT FALSE,
    repair_vehicle BOOLEAN NOT NULL DEFAULT FALSE,
    correct_immediately BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_notice_driver FOREIGN KEY (driver_id) 
	REFERENCES driver(driver_id),
    CONSTRAINT fk_notice_vehicle FOREIGN KEY (vehicle_id) 
	REFERENCES vehicle(vehicle_id),
    CONSTRAINT fk_notice_officer FOREIGN KEY (officer_id) 
	REFERENCES officer(officer_id)
	);

-- Creating a table to store violations linked to in the notice.
CREATE TABLE notice_violation (
    notice_violation_id INT AUTO_INCREMENT PRIMARY KEY,
    correction_notice_id INT NOT NULL,
    violation_type_id INT NOT NULL,
	CONSTRAINT fk_violation_notice FOREIGN KEY (correction_notice_id) 
	REFERENCES correction_notice(correction_notice_id),
    CONSTRAINT fk_violation_type FOREIGN KEY (violation_type_id) 
	REFERENCES violation_type(violation_type_id)
	);
   
-- DCL:
-- Creating officer role and granting permissions.
CREATE ROLE 'officer_role'@'localhost';
GRANT USAGE ON nysp_correction_notice_db.* TO 'officer_role'@'localhost';
GRANT SELECT ON nysp_correction_notice_db.* TO 'officer_role'@'localhost';
GRANT INSERT ON nysp_correction_notice_db.correction_notice TO 'officer_role'@'localhost';
GRANT INSERT ON nysp_correction_notice_db.notice_violation TO 'officer_role'@'localhost';
GRANT INSERT ON nysp_correction_notice_db.driver TO 'officer_role'@'localhost';
GRANT INSERT ON nysp_correction_notice_db.vehicle TO 'officer_role'@'localhost';
GRANT INSERT ON nysp_correction_notice_db.vehicle_owner TO 'officer_role'@'localhost';

-- Creating a citizen view to appropriately restrict access.
CREATE VIEW citizen_view AS
SELECT 
	correction_notice.violation_date,
    correction_notice.violation_time,
    correction_notice.location,
    correction_notice.district,
    vehicle.`type` AS vehicle_type,
    vehicle.make AS vehicle_make,
    vehicle.vehicles_licence,
    violation_type.`description` AS violation_description,
    violation_type.violation_code,
    driver.first_name,
    driver.last_name,
    vehicle_owner.owner_name AS vehicle_owner
FROM correction_notice
JOIN vehicle ON correction_notice.vehicle_id = vehicle.vehicle_id
JOIN vehicle_owner ON vehicle.vehicle_owner_id = vehicle_owner.vehicle_owner_id
JOIN driver ON correction_notice.driver_id = driver.driver_id
JOIN notice_violation ON correction_notice.correction_notice_id = notice_violation.correction_notice_id
JOIN violation_type ON notice_violation.violation_type_id = violation_type.violation_type_id
WHERE vehicle_owner.username = USER();
-- Creating a citizen role and granting permissions.
CREATE ROLE 'citizen_role'@'localhost';
GRANT USAGE ON nysp_correction_notice_db.* TO 'citizen_role'@'localhost';
GRANT SELECT ON nysp_correction_notice_db.citizen_view TO 'citizen_role'@'localhost';

-- Creating sample users.
-- Officers:
CREATE USER 's_scott'@'localhost' IDENTIFIED BY 'password';
GRANT 'officer_role'@'localhost' TO 's_scott'@'localhost';
SET DEFAULT ROLE 'officer_role'@'localhost' TO 's_scott'@'localhost';
CREATE USER 'j_smith'@'localhost' IDENTIFIED BY 'password';
GRANT 'officer_role'@'localhost' TO 'j_smith'@'localhost';
SET DEFAULT ROLE 'officer_role'@'localhost' TO 'j_smith'@'localhost';
-- Citizens:
CREATE USER 'd_kroenke'@'localhost' IDENTIFIED BY 'password';
GRANT 'citizen_role'@'localhost' TO 'd_kroenke'@'localhost';
SET DEFAULT ROLE 'citizen_role'@'localhost' TO 'd_kroenke'@'localhost';
CREATE USER 'j_doe_company'@'localhost' IDENTIFIED BY 'password';
GRANT 'citizen_role'@'localhost' TO 'j_doe_company'@'localhost';
SET DEFAULT ROLE 'citizen_role'@'localhost' TO 'j_doe_company'@'localhost';
-- Applying permission changes.
FLUSH PRIVILEGES;

-- DML:
-- Populating database with sample data.
INSERT INTO officer(personell_number, first_name, last_name, detachment)
VALUES ('850', 'S', 'Scott', '17'),
('900', 'John', 'Smith', '18');
INSERT INTO driver(first_name, last_name, address, city, state, zip_code, drivers_licence,
drivers_licence_state, birth_date, height, weight, eyes)
VALUES ('David M.', 'Kroenke', '5053 88 Ave SE', 'Mercer Island', "WA", "98040", 'WDL412345678', -- Washington state DL num format
'WA', '1946-02-27', 72, 165, 'Brown'),
('Jane', 'Doe', '325 Norwood Ave', 'Syracuse', 'NY', '13206', "J8543750", "NY",-- NY state DL num format
'2006-01-01', 65, 145, 'Blue'),
('John', 'Doe', '123 Main St', 'Syracuse', 'NY', '13202', 'D12345678', 'NY', '1990-05-15', 70, 180, 'Green');
INSERT INTO vehicle_owner(owner_name, username, address, city, state, zip_code)
VALUES ('David M. Kroenke', 'd_kroenke@localhost', '5053 88 Ave SE', 'Mercer Island', "WA", "98040"),
('Jane Doe\'s Company', 'j_doe_company@localhost', '325 Norwood Ave', 'Syracuse', 'NY', '13206');
INSERT INTO vehicle(vehicle_owner_id, vehicles_licence, state, colour, make, vin, `year`, `type`)
VALUES (1, 'DMK 4765', 'WA', 'Black', 'Saab', '1FABH41JXMN109186', 1990, '900'),
(2, 'JAD-5742', 'NY', 'Silver', 'Honda', '1FTEW1E40KFA49611', 2016, 'Civic');
INSERT INTO violation_type (`description`, violation_code)
VALUES ('Texting while driving', '1225(d)'),
('Speeding', '1180'),
('Reckless driving', '1212'),
('Ignoring traffic signals', '1110');
INSERT INTO correction_notice (driver_id, vehicle_id, officer_id, violation_date, violation_time, location,
district, warning, repair_vehicle, correct_immediately)
VALUES (1, 1, 1, '2003-07-28', '09:35:00', 'Enumclaw SR410', '2', TRUE, FALSE, FALSE),
(2, 2, 2, '2025-11-05', '14:30:00', 'Oswego NY104', '1', FALSE, TRUE, TRUE),
(3, 2, 1, '2025-11-1', '12:15:00', 'Syracuse NY11', '1', FALSE, FALSE, TRUE);
INSERT INTO notice_violation (correction_notice_id, violation_type_id)
VALUES (1, 1),
(2, 2),
(2, 4),
(3, 2),
(3, 3);

-- Queries:
-- Inserting a new correction notice for Jane Doe, issued by S Scott.
INSERT INTO correction_notice (driver_id, vehicle_id, officer_id, violation_date, violation_time, location, district,
warning, repair_vehicle, correct_immediately)
VALUES (2, 2, 1, '2025-12-10', '11:15:00', 'Syracuse NY690', '1', FALSE, FALSE, TRUE);
-- Linking the new notice to a violation.
INSERT INTO notice_violation (correction_notice_id, violation_type_id)
VALUES (4, 3);

-- Updating Jane Doe's violation (ID 2).
UPDATE correction_notice
SET location = 'Syracuse NY481', correct_immediately = FALSE
WHERE correction_notice_id = 2;

-- Finding all violations that include the word 'driving'.
SELECT * FROM violation_type 
WHERE `description` LIKE '%driving%';

-- Counting correction notices issued to drivers under 21.
SELECT COUNT(correction_notice.correction_notice_id)
FROM correction_notice
JOIN driver ON correction_notice.driver_id = driver.driver_id
WHERE driver.birth_date > DATE_SUB(CURDATE(), INTERVAL 21 YEAR);

-- Retrieving the number of violations recorded by an officer at each location within the last year.
SELECT officer.first_name, officer.last_name, correction_notice.location, COUNT(correction_notice.correction_notice_id)
FROM correction_notice
JOIN officer ON correction_notice.officer_id = officer.officer_id
WHERE correction_notice.violation_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY officer.first_name, officer.last_name, correction_notice.location;

-- Creating a full report for notice ID 2.
SELECT correction_notice.violation_date, driver.first_name AS driver_first, driver.last_name AS driver_last_name,
vehicle.make, officer.last_name AS officer_last, violation_type.`description`
FROM correction_notice
JOIN driver ON correction_notice.driver_id = driver.driver_id
JOIN vehicle ON correction_notice.vehicle_id = vehicle.vehicle_id
JOIN officer ON correction_notice.officer_id = officer.officer_id
JOIN notice_violation ON correction_notice.correction_notice_id = notice_violation.correction_notice_id
JOIN violation_type ON notice_violation.violation_type_id = violation_type.violation_type_id
WHERE correction_notice.correction_notice_id = 2;

-- Creating a list of repeat offenders ordered by number of violations.
SELECT driver.first_name, driver.last_name, COUNT(notice_violation.notice_violation_id) AS violation_count
FROM driver
JOIN correction_notice ON driver.driver_id = correction_notice.driver_id
JOIN notice_violation ON correction_notice.correction_notice_id = notice_violation.correction_notice_id
GROUP BY driver.driver_id, driver.first_name, driver.last_name
HAVING violation_count > 1
ORDER BY violation_count DESC;

-- Creating a list of drivers and their violations.
SELECT driver.first_name, driver.last_name, correction_notice.violation_date, violation_type.`description`
FROM driver
JOIN correction_notice ON driver.driver_id = correction_notice.driver_id
JOIN notice_violation ON correction_notice.correction_notice_id = notice_violation.correction_notice_id
JOIN violation_type ON notice_violation.violation_type_id = violation_type.violation_type_id
ORDER BY driver.last_name, correction_notice.violation_date;

-- Creating a list of vehicles with registered owners and addresses.
SELECT vehicle.make, vehicle.`type`, vehicle.`year`, vehicle.vehicles_licence, vehicle_owner.owner_name,
vehicle_owner.address, vehicle_owner.city, vehicle_owner.state
FROM vehicle
JOIN vehicle_owner ON vehicle.vehicle_owner_id = vehicle_owner.vehicle_owner_id
ORDER BY vehicle_owner.owner_name;

-- Creating a list of citizens with violations that they must correct immediately.
SELECT driver.first_name, driver.last_name, correction_notice.violation_date, violation_type.`description`
FROM driver
JOIN correction_notice ON driver.driver_id = correction_notice.driver_id
JOIN notice_violation ON correction_notice.correction_notice_id = notice_violation.correction_notice_id
JOIN violation_type ON notice_violation.violation_type_id = violation_type.violation_type_id
WHERE correction_notice.correct_immediately = TRUE;

-- Generating a list of violation incident reports, displaying the location, driver, officer, date and time.
SELECT correction_notice.location, correction_notice.violation_date, correction_notice.violation_time,
CONCAT(officer.first_name, ' ', officer.last_name) AS officer_name, CONCAT(driver.first_name, ' ', driver.last_name) AS driver_name
FROM correction_notice
JOIN officer ON correction_notice.officer_id = officer.officer_id
JOIN driver ON correction_notice.driver_id = driver.driver_id
ORDER BY correction_notice.violation_date DESC, correction_notice.violation_time DESC;

-- Finding all drivers from Syracuse who were given a notice for speeding.
SELECT DISTINCT driver.first_name, driver.last_name, driver.address
FROM driver
JOIN correction_notice ON driver.driver_id = correction_notice.driver_id
JOIN notice_violation ON correction_notice.correction_notice_id = notice_violation.correction_notice_id
JOIN violation_type ON notice_violation.violation_type_id = violation_type.violation_type_id
WHERE driver.city = 'Syracuse' AND violation_type.`description` = 'Speeding';

-- Viewing citizen view. Must be executed by a citizen user.
SELECT * FROM citizen_view;

-- Removing the ignoring traffic signal violation from Jane Doe's notice (ID 2).
DELETE FROM notice_violation
WHERE correction_notice_id = 2 AND violation_type_id = 4;