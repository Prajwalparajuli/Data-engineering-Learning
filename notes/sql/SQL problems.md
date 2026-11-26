## Problem 1
Table: Cinema

| Column Name | Type    |
|-------------|---------|
| id          | int     |
| movie       | varchar |
| description | varchar |
| rating      | float   |

- id is the primary key for this table.
- Each row contains information about the name of a movie, its genre, and its rating.
- rating is a 2 decimal places float in the range [0, 10]
  
**Write an SQL query to report the movies with an odd-numbered ID and a description that is not "boring".
Return the result table ordered by rating in descending order.**

The query result format is in the following example.

Example 1:

Input: 

Cinema table:

| id | movie      | description | rating |
|----|------------|-------------|--------| 
| 1  | War        | great 3D    | 8.9    |
| 2  | Science    | fiction     | 8.5    |
| 3  | irish      | boring      | 6.2    |
| 4  | Ice song   | Fantacy     | 8.6    |
| 5  | House card | Interesting | 9.1    |

Output: 

| id | movie      | description | rating |
|----|------------|-------------|--------|
| 5  | House card | Interesting | 9.1    |
| 1  | War        | great 3D    | 8.9    |

Explanation: 

We have three movies with odd-numbered IDs: 1, 3, and 5. The movie with ID = 3 is boring so we do not include it in the answer.

```sql
SELECT *
FROM Cinema
WHERE 
    id % 2 = 1 
    AND 
    description != 'boring'
ORDER BY rating DESC;
```

## Problem 2

Table: ActorDirector

| Column Name | Type |
|-------------|------|
| actor_id    | int  |
| director_id | int  |
| timestamp   | int  |

- timestamp is the primary key column for this table.
  
**Write a SQL query for a report that provides the pairs (actor_id, director_id) where the actor has cooperated with the director at least three times.
Return the result table in any order.**

The query result format is in the following example.
 
Example 1:
Input: 
ActorDirector table:

| actor_id | director_id | timestamp |
|----------|-------------|-----------|
| 1        | 1           | 0         |
| 1        | 1           | 1         |
| 1        | 1           | 2         |
| 1        | 2           | 3         |
| 1        | 2           | 4         |
| 2        | 1           | 5         |
| 2        | 1           | 6         |

Output: 

| actor_id | director_id |
|----------|-------------|
| 1        | 1           |

Explanation: The only pair is (1, 1) where they cooperated exactly 3 times.

```sql
SELECT actor_id, director_id
FROM ActorDirector
GROUP BY actor_id, director_id
HAVING COUNT(*) >= 3;
```

## Problem 3

Table: Sales

| Column Name | Type |
|-------------|------|
| sale_id     | int  |
| product_id  | int  |
| year        | int  |
| quantity    | int  |
| price       | int  |

- (sale_id, year) is the primary key of this table.
- product_id is a foreign key to Product table.
- Each row of this table shows a sale on the product product_id in a certain year.
- Note that the price is per unit.
 
Table: Product

| Column Name  | Type    |
|--------------|---------|
| product_id   | int     |
| product_name | varchar |

- product_id is the primary key of this table.
- Each row of this table indicates the product name of each product.

**Write an SQL query that reports the product_name, year, and price for each sale_id in the Sales table.
Return the resulting table in any order.**

The query result format is in the following example.
 
Example 1:
Input: 
Sales table:

| sale_id | product_id | year | quantity | price |
|---------|------------|------|----------|-------| 
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |

Product table:

| product_id | product_name |
|------------|--------------|
| 100        | Nokia        |
| 200        | Apple        |
| 300        | Samsung      |

Output: 

| product_name | year | price |
|--------------|------|-------|
| Nokia        | 2008 | 5000  |
| Nokia        | 2009 | 5000  |
| Apple        | 2011 | 9000  |

Explanation: 
- From sale_id = 1, we can conclude that Nokia was sold for 5000 in the year 2008.
- From sale_id = 2, we can conclude that Nokia was sold for 5000 in the year 2009.
- From sale_id = 7, we can conclude that Apple was sold for 9000 in the year 2011.

```sql
SELECT s.product_name, s.year, s.price 
FROM Sales s
JOIN Product p 
    ON s.product_id = p.product_id;
```

## Problem 4

Table: Project

| Column Name | Type |
|-------------|------|
| project_id  | int  |
| employee_id | int  |

- (project_id, employee_id) is the primary key of this table.
- employee_id is a foreign key to Employee table.
- Each row of this table indicates that the employee with employee_id is working on the project with project_id.
 
Table: Employee

| Column Name      | Type    |
|------------------|---------|
| employee_id      | int     |
| name             | varchar |
| experience_years | int     |

employee_id is the primary key of this table.
Each row of this table contains information about one employee.
  
**Write an SQL query that reports all the projects that have the most employees.
Return the result table in any order.**

The query result format is in the following example.
 
Example 1:
Input: 
Project table:

| project_id | employee_id |
|------------|-------------|
| 1          | 1           |
| 1          | 2           |
| 1          | 3           |
| 2          | 1           |
| 2          | 4           |

Employee table:

| employee_id | name   | experience_years |
|-------------|--------|------------------|
| 1           | Khaled | 3                |
| 2           | Ali    | 2                |
| 3           | John   | 1                |
| 4           | Doe    | 2                |

Output: 

| project_id |
|------------|
| 1          |

Explanation: The first project has 3 employees while the second one has 2.

```sql
WITH Projectcounts AS (
    SELECT project_id,
           RANK() OVER (ORDER BY COUNT(employee_id) DESC) AS rank
    FROM Project
    GROUP BY project_id
)
SELECT project_id
FROM Projectcounts
WHERE rank = 1;
```