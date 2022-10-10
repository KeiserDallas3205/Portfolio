/* 7-3: Triggers and Actions */


/* 1. Write a trigger to update the salary of an employee with an average salary of the department where
he/she works BEFORE INSERT(ing) the record in the employee table IF the salary is empty or NULL */


DELIMITER $$
CREATE TRIGGER emp_addr_trig
BEFORE INSERT ON employee
FOR EACH ROW
BEGIN

	IF (NEW.salary = '' OR NEW.salary IS NULL)
	THEN
		SET NEW.salary =(SELECT AVG(salary)
						FROM employee e
						WHERE e.dno = NEW.dno);
	END IF;

END$$

DELIMITER ;


/* 2. Dependent relationship must be either spouse, son, or daughter. If anything else, then display message –
“Please, provide valid relationship (Spouse, Son or Daughter). */

DELIMITER $$
CREATE TRIGGER dependent_relationship
BEFORE INSERT ON dependent
FOR EACH ROW
BEGIN

	DECLARE msg VARCHAR(255);
	IF NEW.relationship NOT IN ('Spouse', 'Daughter', 'Son')
	THEN /* Cause Error Message */
		SET msg = 'Please, provide correct relationship (Spouse, Son or Daughter).';
	SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = msg;
	END IF;
	
END$$
DELIMITER ;

/* 3. Write a trigger to create a default project for each new department inserted into database. */

DELIMITER $$
CREATE TRIGGER new_dept
AFTER INSERT ON department
FOR EACH ROW
BEGIN

	INSERT INTO project
	VALUES(CONCAT(NEW.dname, ' - Initialization'), CONCAT(NEW.dnumber, '1'), 'Houston', NEW.dnumber);
	
END$$
DELIMITER ;