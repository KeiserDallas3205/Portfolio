/*
Name: Keiser Dallas
Date: 10/10/2022
Desc: These are examples of some complex queries using SQL.
*/



/*
 Query 2 - Make a list of all project numbers for projects that involve an employee whose last name is ‘Smith’, either as a
	worker or as a manager of the department that controls the project 

*/


SELECT pnumber
FROM project
WHERE pnumber IN  
		(SELECT w.pno
		FROM works_on as w, employee as e
		WHERE w.essn = e.ssn AND e.lname = 'Smith')
	OR pnumber IN
		(SELECT p.pnumber
		FROM project as p, department as d, employee as e 
		WHERE p.dnum = d.dnumber AND d.mgr_ssn = e.ssn AND e.lname = 'Smith');

/*
Query 3.1 - Retrieve all employees whose address is in Houston, Texas

*/

SELECT fname, lname, address
FROM employee as  e
WHERE e.address LIKE '%Houston, TX';


/*
Query 4 - Show the resulting salaries if every employee working on the ‘Product’ project is given a 10% raise.

*/ 

SELECT e.fname, e.lname, 1.1*e.salary as increased_salary
FROM employee as e, works_on as w, project as p
WHERE e.ssn = w.essn AND w.pno = p.pnumber AND p.pname = 'ProductX';


/*
Query 5 - Retrieve all employees in department 5 whose salary is between $30,000 and $40,000
*/
SELECT *
FROM employee as e
WHERE (salary BETWEEN 30000 and 40000) AND e.dno = 5;


/*
• Query 6 - Retrieve a list of employees and the projects they are working on, ordered by department and, within each
	department, ordered alphabetically by last name, then first name
*/

SELECT d.dname, e.lname, e.fname, p.pname
FROM employee as e, works_on as w, project as p, department as d 
WHERE e.ssn = w.essn AND w.pno = p.pnumber AND d.dnumber = e.dno
ORDER BY d.dname, e.lname, e.fname ;


/*
• Query 7 - Retrieve the names of all employees who do not have supervisors.

*/

SELECT e.fname, e.lname
FROM employee as e 
WHERE e.super_ssn is NULL;


/*
Query 9 - Retrieve the name of each employee who has a dependent with the same first name and is the same sex as the
employee
*/

SELECT e.fname, e.lname, e.sex
FROM employee as e 
WHERE e.ssn IN 
			(SELECT d.essn
			FROM dependent as d
			WHERE e.fname = d.dependent_name AND e.sex = d.sex);


/*
Query 10 - List of managers that have a dependent using two nested queries 

*/

SELECT e.fname, e.lname
FROM employee as e
WHERE EXISTS 
		(SELECT *
		FROM department as d
		WHERE e.ssn = d.mgr_ssn)
	AND
	EXISTS
		(select * 
		FROM dependent as d 
		WHERE e.ssn = d.essn);
		
/*
Retrieve names of employees w/ at least 2 dependent 
*/

SELECT e.lname, e.fname
FROM employee as e 
WHERE (SELECT COUNT(*)
	FROM dependent as d
	WHERE e.ssn = d.essn) >= 2;
	
	
	
/* Query 22 - Retrieve the names of all employees who have two or more dependents */ 
SELECT e.fname, e.lname
FROM employee as e 
WHERE  (SELECT COUNT(*)
		FROM dependent as d 
		WHERE e.ssn = d.essn)>= 2;
		
/* • Query 23 - For each department, retrieve the department number, the number of employees in the department, and their
average salary */

SELECT e.dno, COUNT(*) as employee_count, AVG(e.salary) as average_salary
FROM employee as e
GROUP BY e.dno

/* Query 24 - For each project, retrieve the project number, the project name, the number of employees who work on
that project, and the total hours worked. */

SELECT w.pno, p.pname, COUNT(*) as num_of_emp, SUM(w.hours) as total_hours 
FROM works_on as w, project as p
WHERE w.pno = p.pnumber 
GROUP BY w.pno;


/* Query 25 - For each project on which more than two employees work, retrieve the project number, the project name, 
	the number of employees who work on the project. */
	




		
