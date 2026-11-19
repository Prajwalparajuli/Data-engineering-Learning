SELECT Statement
- Selects the columns from the designated table.

```SQL
SELECT ID, Name, Salary
FROM employee;
```

SELECT selects all the rows when there is no condition.
In order to limit the number of rows, WHERE clause is used.

```SQL
SELECT ID, Name, Salary
FROM employee
WHERE Salary > 10000;
```

WHERE is used with expression which generate True/False within the table for the selected columns with rows that satisfy the expression or condition. 

```SQL
SELECT ID, Name, Salary
FROM employee
WHERE Salary != 20000 AND ID > 1
```
With AND statement between 2 or more conditions or expressions, the rows are returned when both conditions are satisfied, if any one or both of the conditions are not satisfied (FALSE), that row is excluded. 

**If the first expression is False then the second expression is not going to be evaluated.**

If Salary != 20000 Takes 100 sec for evaluation
And ID > 1 Takes 1 sec for evaluation.

It is better to use the WHERE clause as
```SQL
WHERE ID > 1 AND SALARY != 20000
```
so that the condition returns False faster saving compute time.

```SQL
SELECT ID, Name, Salary
FROM employee
WHERE Salary <= 10000 OR Name = 'John'
```
With OR statement between 2 or more conditions or expression, if any one of the expression is TRUE or satisfied, then those rows are returned, only the rows with both condition to be FALSE are excluded. 

**OR tries to find the first TRUE in expression of 2 or more expressions.**
Similarly keeping the condition that returns TRUE faster is better to be used before OR clause. 

When there is Data that might not match exactly we use regular expression matching (regex)

```SQL
# Find the exployee name that starts with e.
SELECT *
FROM employee
WHERE Name LIKE 'e%' 
```

LIKE clause in WHERE
- LIKE 'e%' = Starts with e
- LIKE '%e' =  Ends with e
- LIKE '%e%' =  Contains e anywhere 

Exact matching is faster than Regex matching. 

**When the Regex matching is needed along with the Exact matching then always use the Exact matching expression before the Regex matching expression.**

## SQL Joins

> **Key Principle:** SQL Joins combine rows from two or more tables based on a related column between them (typically a Primary Key and a Foreign Key).

### Sample Reference Tables
All query examples and resulting tables below are based on these two tables:

**Table A (`Employees`)**

| emp_id | name | dept_id |
| :--- | :--- | :--- |
| 1 | Alice | 10 |
| 2 | Bob | 20 |
| 3 | Charlie | NULL |

**Table B (`Departments`)**

| dept_id | dept_name |
| :--- | :--- |
| 10 | HR |
| 20 | Engineering |
| 30 | Marketing |

---

### 1. INNER JOIN
Returns **only** the rows where there is a match in **both** tables.

```sql
SELECT e.name, d.dept_name
FROM Employees e
INNER JOIN Departments d ON e.dept_id = d.dept_id;
````

**Result:**

|**name**|**dept_name**|
|---|---|
|Alice|HR|
|Bob|Engineering|

### 2. LEFT JOIN (or LEFT OUTER JOIN)

Returns **all** rows from the left table (`Employees`), and the matched rows from the right table (`Departments`). Unmatched right-side columns return `NULL`.
 
```SQL
SELECT e.name, d.dept_name
FROM Employees e
LEFT JOIN Departments d ON e.dept_id = d.dept_id;
```

**Result:**

| **name** | **dept_name** |
| -------- | ------------- |
| Alice    | HR            |
| Bob      | Engineering   |
| Charlie  | NULL          |

### 3. RIGHT JOIN (or RIGHT OUTER JOIN)

Returns **all** rows from the right table (`Departments`), and the matched rows from the left table (`Employees`). Unmatched left-side columns return `NULL`.

```sql
SELECT e.name, d.dept_name
FROM Employees e
RIGHT JOIN Departments d ON e.dept_id = d.dept_id;
```

**Result:**

|**name**|**dept_name**|
|---|---|
|Alice|HR|
|Bob|Engineering|
|NULL|Marketing|
### 4. FULL JOIN (or FULL OUTER JOIN)

Returns **all** rows when there is a match in **either** the left or right table. Unmatched sides are filled with `NULL`.

```sql
SELECT e.name, d.dept_name
FROM Employees e
FULL OUTER JOIN Departments d ON e.dept_id = d.dept_id;
```

**Result:**

|**name**|**dept_name**|
|---|---|
|Alice|HR|
|Bob|Engineering|
|Charlie|NULL|
|NULL|Marketing|
### 5. Anti-Joins (Filtering Unmatched Rows)

Used to isolate records in one table that have **no** corresponding record in the other table.
#### Left Anti-Join (Only in Left Table)

```sql
SELECT e.name
FROM Employees e
LEFT JOIN Departments d ON e.dept_id = d.dept_id
WHERE d.dept_id IS NULL;
```

**Result:**

|**name**|
|---|
|Charlie|
#### Right Anti-Join (Only in Right Table)

```sql
SELECT d.dept_name
FROM Employees e
RIGHT JOIN Departments d ON e.dept_id = d.dept_id
WHERE e.dept_id IS NULL;
```

**Result:**

|**dept_name**|
|---|
|Marketing|
### 6. CROSS JOIN

Produces a **Cartesian Product**—every row from the left table is combined with every row from the right table (no `ON` condition required).

```sql
SELECT e.name, d.dept_name
FROM Employees e
CROSS JOIN Departments d;
```

**Result (3 rows × 3 rows = 9 rows):**

| **name** | **dept_name** |
| -------- | ------------- |
| Alice    | HR            |
| Alice    | Engineering   |
| Alice    | Marketing     |
| Bob      | HR            |
| Bob      | Engineering   |
| Bob      | Marketing     |
| Charlie  | HR            |
| Charlie  | Engineering   |
| Charlie  | Marketing     |

### 7. SELF JOIN

A regular join where a table is joined **with itself**. Useful for hierarchical data (e.g., an employee and their manager in the same table).

  **Reference Table (`Employees_Hierarchy`)**

|**emp_id**|**name**|**manager_id**|
|---|---|---|
|1|Alice|NULL|
|2|Bob|1|
|3|Charlie|2|


```sql
SELECT e1.name AS Employee, e2.name AS Manager
FROM Employees_Hierarchy e1
LEFT JOIN Employees_Hierarchy e2 ON e1.manager_id = e2.emp_id;
```

**Result:**

|**Employee**|**Manager**|
|---|---|
|Alice|NULL|
|Bob|Alice|
|Charlie|Bob|

### Quick Summary Cheat Sheet

|**Join Type**|**Keeps Left Unmatched?**|**Keeps Right Unmatched?**|**Common Use Case**|
|---|---|---|---|
|**INNER JOIN**|No|No|Get records that exist in both tables|
|**LEFT JOIN**|**Yes**|No|Get all primary records + optional details|
|**RIGHT JOIN**|No|**Yes**|Less common (usually rewritten as a `LEFT JOIN`)|
|**FULL JOIN**|**Yes**|**Yes**|Merge two datasets completely / audit mismatches|
|**CROSS JOIN**|N/A|N/A|Generate all possible combinations (e.g., sizes × colors)|
|**SELF JOIN**|Depends|Depends|Organizational charts, parent-child categories|

## SQL Set Operators: UNION & UNION ALL

> **Key Principle:** Unlike `JOIN` (which combines columns horizontally), `UNION` and `UNION ALL` stack result sets **vertically** by appending rows from one query onto another.

### Strict Rules for Combining Queries
Before using `UNION` or `UNION ALL`, all `SELECT` statements must follow three rules:
1. **Same Number of Columns:** Every `SELECT` statement must have the exact same column count.
2. **Compatible Data Types:** Corresponding columns must have matching or compatible data types in the same order.
3. **Column Naming:** The final output inherits its column headers from the **first** `SELECT` statement.

### Sample Reference Tables
All query examples and resulting tables below use these two tables:

**Table A (`US_Customers`)**

| customer_id | name | city |
| :--- | :--- | :--- |
| 1 | Alice | New York |
| 2 | Bob | Chicago |
| 3 | Charlie | Austin |

**Table B (`EU_Customers`)**

| customer_id | name | city |
| :--- | :--- | :--- |
| 2 | Bob | Chicago |
| 4 | Diana | London |
| 5 | Evan | Berlin |

*(Note: **Bob** exists in both tables).*

### 1. UNION
Combines the result sets of two or more `SELECT` statements and **removes duplicate rows**.

```sql
SELECT name, city FROM US_Customers
UNION
SELECT name, city FROM EU_Customers;
````

**Result (5 rows — duplicate "Bob" is removed):**

|**name**|**city**|
|---|---|
|Alice|New York|
|Bob|Chicago|
|Charlie|Austin|
|Diana|London|
|Evan|Berlin|

### 2. UNION ALL

Combines the result sets of two or more `SELECT` statements and **keeps all duplicate rows**.

```sql
SELECT name, city FROM US_Customers
UNION ALL
SELECT name, city FROM EU_Customers;
```

**Result (6 rows — duplicate "Bob" is preserved):**

|**name**|**city**|
|---|---|
|Alice|New York|
|Bob|Chicago|
|Charlie|Austin|
|Bob|Chicago|
|Diana|London|
|Evan|Berlin|
### 3. Sorting & Tagging Combined Results

- **Sorting (`ORDER BY`):** Must be placed at the **very end** of the final `SELECT` statement; it sorts the entire combined result.  
- **Source Tracking:** You can add a hardcoded string column to track which table each row originated from.

```sql
SELECT name, city, 'US' AS region FROM US_Customers
UNION ALL
SELECT name, city, 'EU' AS region FROM EU_Customers
ORDER BY name ASC;
```

**Result:**

|**name**|**city**|**region**|
|---|---|---|
|Alice|New York|US|
|Bob|Chicago|US|
|Bob|Chicago|EU|
|Charlie|Austin|US|
|Diana|London|EU|
|Evan|Berlin|EU|

### Quick Comparison Cheat Sheet

|**Feature**|**UNION**|**UNION ALL**|
|---|---|---|
|**Duplicate Rows**|**Removed** (Distinct values only)|**Kept** (All rows returned)|
|**Performance**|**Slower** (Requires sorting/hashing to find duplicates)|**Faster** (Simply appends data without checking)|
|**Best Use Case**|Creating a clean master list without repeats|Merging partitioned logs/tables or when duplicates are impossible/needed|

## SQL Aggregation: GROUP BY & HAVING

> **Key Principle:** `GROUP BY` collapses rows that share identical values in specified columns into single summary rows, allowing you to run aggregate calculations (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) on each group.

### Golden Rule of `GROUP BY`
Every column in your `SELECT` clause must be **either**:
1. Listed inside the `GROUP BY` clause, **OR**
2. Wrapped inside an aggregate function (e.g., `SUM(amount)`).

*(Violating this rule will throw a syntax/grouping error in standard SQL).*

### Sample Reference Table
All query examples and resulting tables below use this `Sales` table:

**Table (`Sales`)**

| sale_id | region | category | amount |
| :--- | :--- | :--- | :--- |
| 1 | North | Electronics | 500 |
| 2 | North | Electronics | 300 |
| 3 | North | Furniture | 200 |
| 4 | South | Electronics | 400 |
| 5 | South | Furniture | NULL |

### 1. Basic `GROUP BY` (Single Column)
Groups rows by one column and calculates summary metrics per group. Note that aggregate functions like `COUNT(column)` and `SUM(column)` automatically **ignore `NULL` values**, whereas `COUNT(*)` counts all rows including `NULL`s.

```sql
SELECT 
    region,
    COUNT(*) AS total_transactions,
    COUNT(amount) AS paid_transactions,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_sale
FROM Sales
GROUP BY region;
````

**Result:**

|**region**|**total_transactions**|**paid_transactions**|**total_revenue**|**avg_sale**|
|---|---|---|---|---|
|North|3|3|1000|333.33|
|South|2|1|400|400.00|

_(Notice: For `South`, `AVG(amount)` divides `400` by `1` paid transaction, not `2`, because `NULL` is ignored)._

### 2. Multi-Column `GROUP BY`

Creates a unique group for every distinct combination of the specified columns.

```sql
SELECT 
    region,
    category,
    SUM(amount) AS category_revenue
FROM Sales
GROUP BY region, category
ORDER BY region, category;
```

**Result:**

|**region**|**category**|**category_revenue**|
|---|---|---|
|North|Electronics|800|
|North|Furniture|200|
|South|Electronics|400|
|South|Furniture|NULL|

### 3. Filtering Groups: `WHERE` vs. `HAVING`

Because `WHERE` filters rows **before** grouping occurs, it cannot filter based on aggregate results (like `SUM(amount) > 500`). Use `HAVING` to filter **after** groups are created.

```sql
SELECT 
    region,
    SUM(amount) AS total_revenue
FROM Sales
WHERE category = 'Electronics'     -- Step 1: Filter individual rows first
GROUP BY region                    -- Step 2: Group remaining rows
HAVING SUM(amount) > 500;          -- Step 3: Filter the grouped results
```

**Result:**

|**region**|**total_revenue**|
|---|---|
|North|800|

_(Explanation: `WHERE` removes Furniture rows. `GROUP BY` sums Electronics for North (800) and South (400). `HAVING` eliminates South because 400 is not greater than 500)._

### 4. SQL Execution Order (Why `HAVING` Exists)

Understanding the order in which the database processes a query prevents most `GROUP BY` errors:

1. `FROM` (Fetch the table)
2. `WHERE` (Filter raw rows)    
3. `GROUP BY` (Form the groups)
4. `HAVING` (Filter the groups)
5. `SELECT` (Compute aggregations & assign column aliases)
6. `ORDER BY` (Sort the final output)

### Quick Comparison Cheat Sheet: `WHERE` vs. `HAVING`

|**Feature**|**WHERE**|**HAVING**|
|---|---|---|
|**When it runs**|**Before** `GROUP BY`|**After** `GROUP BY`|
|**What it filters**|Individual, raw rows|Summarized groups|
|**Can use `SUM()`, `COUNT()`, etc.?**|**No** (Throws an error)|**Yes**|
|**Performance Tip**|Filter as much as possible in `WHERE` first to shrink the data before grouping|Use only for conditions that depend on aggregate values|
## SQL Commands: DDL & DML

> **Key Principle:** **DDL** (Data Definition Language) defines and modifies the *structure* of database objects (tables, columns, schemas), while **DML** (Data Manipulation Language) manages the *data* inside those tables.

---

### Part 1: DDL (Data Definition Language)
DDL commands alter the blueprint of the database and are typically auto-committed (cannot be undone with a standard `ROLLBACK` in most SQL engines).

#### 1. `CREATE`
Builds a new table from scratch, defining column names, data types, and constraints (`PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `DEFAULT`).

```sql
CREATE TABLE Employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dept VARCHAR(50) DEFAULT 'General',
    salary DECIMAL(10, 2)
);
````

**Result (Empty `Employees` table structure created):**

| **emp_id** | **name**  | **dept**  | **salary** |
| ---------- | --------- | --------- | ---------- |
| _(empty)_  | _(empty)_ | _(empty)_ | _(empty)_  |

#### 2. `ALTER`

Modifies the structure of an **existing** table (adding, dropping, or renaming columns, or changing data types).

```sql
-- Add a new column
ALTER TABLE Employees ADD email VARCHAR(150);

-- Modify an existing column's data type
ALTER TABLE Employees MODIFY COLUMN salary DECIMAL(12, 2);

-- Remove a column
ALTER TABLE Employees DROP COLUMN dept;
```

**Result (Updated `Employees` structure):**

|**emp_id**|**name**|**salary**|**email**|
|---|---|---|---|
|_(empty)_|_(empty)_|_(empty)_|_(empty)_|

#### 3. `TRUNCATE`

Instantly deletes **all rows** from a table while keeping the table structure intact. It is much faster than `DELETE` because it deallocates data pages instead of logging individual row deletions.
```sql
TRUNCATE TABLE Employees;
```

#### 4. `DROP`

Completely deletes the entire table—both its data **and** its structure—from the database.
```sql
DROP TABLE Employees;
```

### Part 2: DML (Data Manipulation Language)

DML commands manipulate the actual records inside existing tables. _(Note: `SELECT` is also often grouped under DML/DQL)._
#### Sample Reference Table (`Employees`)

All DML examples below start with this state:

|**emp_id**|**name**|**dept**|**salary**|
|---|---|---|---|
|1|Alice|Engineering|100000.00|
|2|Bob|Sales|80000.00|

#### 1. `INSERT`

```sql
INSERT INTO Employees (emp_id, name, dept, salary)
VALUES 
    (3, 'Charlie', 'Marketing', 75000.00),
    (4, 'Diana', DEFAULT, 70000.00);
```

**Result (`Employees` table after `INSERT`):**

|**emp_id**|**name**|**dept**|**salary**|
|---|---|---|---|
|1|Alice|Engineering|100000.00|
|2|Bob|Sales|80000.00|
|3|Charlie|Marketing|75000.00|
|4|Diana|General|70000.00|

#### 2. `UPDATE`

Modifies existing column values for specific rows. **Always use a `WHERE` clause**, otherwise every row in the table will be overwritten.

```sql
UPDATE Employees
SET salary = 85000.00, dept = 'Enterprise Sales'
WHERE emp_id = 2;
```

**Result (`Employees` table after `UPDATE`):**

|**emp_id**|**name**|**dept**|**salary**|
|---|---|---|---|
|1|Alice|Engineering|100000.00|
|2|Bob|Enterprise Sales|85000.00|
|3|Charlie|Marketing|75000.00|
|4|Diana|General|70000.00|

#### 3. `DELETE`

Removes specific rows from a table based on a condition. Omitting `WHERE` deletes all rows (slower than `TRUNCATE`, as every row deletion is logged).

```sql
DELETE FROM Employees
WHERE emp_id = 4;
```

**Result (`Employees` table after `DELETE`):**

|**emp_id**|**name**|**dept**|**salary**|
|---|---|---|---|
|1|Alice|Engineering|100000.00|
|2|Bob|Enterprise Sales|85000.00|
|3|Charlie|Marketing|75000.00|

#### 4. `MERGE` (or `UPSERT`)

Synchronizes a target table with a source table in a single statement: **updates** rows if a match exists, and **inserts** new rows if no match is found.

**Source Table (`Salary_Updates`)**

|**emp_id**|**name**|**dept**|**salary**|
|---|---|---|---|
|1|Alice|Engineering|110000.00|
|5|Evan|HR|65000.00|

```sql
MERGE INTO Employees target
USING Salary_Updates source
ON target.emp_id = source.emp_id
WHEN MATCHED THEN
    UPDATE SET target.salary = source.salary
WHEN NOT MATCHED THEN
    INSERT (emp_id, name, dept, salary)
    VALUES (source.emp_id, source.name, source.dept, source.salary);
```

**Result (`Employees` table after `MERGE`):**

|**emp_id**|**name**|**dept**|**salary**|
|---|---|---|---|
|1|Alice|Engineering|110000.00|
|2|Bob|Enterprise Sales|85000.00|
|3|Charlie|Marketing|75000.00|
|5|Evan|HR|65000.00|

### Quick Summary Cheat Sheet: `DELETE` vs. `TRUNCATE` vs. `DROP`

|**Feature**|**DELETE (DML)**|**TRUNCATE (DDL)**|**DROP (DDL)**|
|---|---|---|---|
|**What it removes**|Specific rows (via `WHERE`) or all rows|**All rows** only|**All rows + table structure**|
|**`WHERE` clause allowed?**|**Yes**|No|No|
|**Speed**|Slower (Row-by-row logging)|Fast (Page deallocation)|Instant|
|**Auto-Increment / Identity**|Keeps current counter|Resets counter back to `1`|Destroyed with the table|
|**Rollback possible?**|**Yes** (inside a transaction)|No (in most SQL engines)|No|
