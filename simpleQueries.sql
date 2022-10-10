
/*
Name: Keiser Dallas
Date: 10/10/2022
Desc: These are examples of simple SQL queries.
*/


/*Query 0. Retrieve birth date and address of the employee(s) whose name is ‘John B. Smith’.*/
SELECT bdate, address
FROM employee
WHERE fname = 'John' AND minit = 'B' AND lname = 'Smith';

/*Query 1. Retrieve name and address of all employees who work for the ‘Research’ department.*/
SELECT fname, lname, address
FROM employee, department
WHERE dname = 'Research' AND dnumber = dno;

SELECT employee.fname, employee.lname, employee.address
FROM employee, department
WHERE department.dname = 'Research' AND department.dnumber = employee.dno;

SELECT e.fname, e.lname, e.address
FROM employee AS e, department AS d
WHERE d.dname = 'Research' AND d.dnumber = e.dno;

/*Query 2. For every project located in ‘Stafford’, list project number, controlling department number, 
and department manager’s last name, address, and birth date.*/
SELECT p.pnumber, p.dnum, e.lname, e.address, e.bdate
FROM project p, department d, employee e
WHERE p.dnum = d.dnumber AND d.mgr_ssn = e.ssn AND p.plocation = 'Stafford';

/* Query 3. For each employee, retrieve employee’s first and last name and first and last name of his or her 
immediate supervisor.*/
SELECT e.fname, e.lname, s.fname, s.lname
FROM employee AS e, employee AS s
WHERE e.super_ssn = s.ssn;

/*Query 4. Select ssns of all employees*/
SELECT ssn
FROM employee;

/*Query 5. Select all combinations of employee ssns and department names in the database.*/
SELECT e.ssn, d.dname
FROM employee e, department d;

/*Query 6. Select all attributes of employees who work in department number 5.*/
SELECT *
FROM employee
WHERE dno = 5;

/*Query 7. Select all the attributes of an employee and the attributes of the department in which he/she works for
every employee of the ‘Research’ department.*/
SELECT *
FROM employee e, department d
WHERE d.dname = 'Research' AND e.dno = d.dnumber;

/*Query 8. CROSS PRODUCT of the employee and department relations.*/
SELECT *
FROM employee, department;
