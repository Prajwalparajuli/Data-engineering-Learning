## SQL Window Functions

> **Key Principle:** Unlike `GROUP BY` (which collapses rows into a single summary row), **Window Functions** perform calculations across a set of related rows **while keeping every individual row intact**.

### Anatomy of a Window Function
Every window function uses the `OVER()` clause to define the "window" of rows it looks at:

```sql
FUNCTION_NAME(column) OVER (
    PARTITION BY group_column   -- Optional: Divides rows into buckets (like GROUP BY, without collapsing)
    ORDER BY sort_column        -- Optional: Sets the order of rows inside each bucket
)
````

### Sample Reference Table

All query examples and resulting tables below use this `Employee_Salaries` table:

  **Table (`Employee_Salaries`)**

|**emp_id**|**name**|**dept**|**salary**|
|---|---|---|---|
|1|Alice|Engineering|120000|
|2|Bob|Engineering|100000|
|3|Charlie|Engineering|100000|
|4|Diana|Sales|90000|
|5|Evan|Sales|80000|

### 1. Ranking Functions

Used to assign a rank or row number to each record within a partition. (`ORDER BY` inside `OVER()` is **required**).
- **`ROW_NUMBER()`:** Assigns a unique sequential number (`1, 2, 3...`). Ties get arbitrary numbers.  
- **`RANK()`:** Assigns the same rank to ties, then **skips** the next number (`1, 2, 2, 4`).
- **`DENSE_RANK()`:** Assigns the same rank to ties, with **no gaps** (`1, 2, 2, 3`).

```sql
SELECT 
    name,
    dept,
    salary,
    ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS row_num,
    RANK()       OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS dense_rnk
FROM Employee_Salaries;
```

**Result:**

|**name**|**dept**|**salary**|**row_num**|**rnk**|**dense_rnk**|
|---|---|---|---|---|---|
|Alice|Engineering|120000|1|1|1|
|Bob|Engineering|100000|2|2|2|
|Charlie|Engineering|100000|3|2|2|
|Diana|Sales|90000|1|1|1|
|Evan|Sales|80000|2|2|2|

### 2. Value / Offset Functions (`LAG` & `LEAD`)
Used to access data from a **previous** or **subsequent** row without needing a `SELF JOIN`.
- **`LAG(col, offset)`:** Looks **backward** `N` rows (defaults to `1` row back).
- **`LEAD(col, offset)`:** Looks **forward** `N` rows (defaults to `1` row ahead).
```sql
SELECT 
    name,
    dept,
    salary,
    LAG(salary, 1)  OVER (PARTITION BY dept ORDER BY salary DESC) AS prev_higher_salary,
    LEAD(salary, 1) OVER (PARTITION BY dept ORDER BY salary DESC) AS next_lower_salary
FROM Employee_Salaries;
```

**Result:**

|**name**|**dept**|**salary**|**prev_higher_salary**|**next_lower_salary**|
|---|---|---|---|---|
|Alice|Engineering|120000|NULL|100000|
|Bob|Engineering|100000|120000|100000|
|Charlie|Engineering|100000|100000|NULL|
|Diana|Sales|90000|NULL|80000|
|Evan|Sales|80000|90000|NULL|

### 3. Aggregate Window Functions

Standard aggregates (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`) paired with `OVER()` allow you to display group totals or running totals alongside raw row data.
- **Without `ORDER BY`:** Calculates the total across the **entire partition** (useful for % of total).
- **With `ORDER BY`:** Calculates a **running (cumulative) total** row-by-row.

```sql
SELECT 
    name,
    dept,
    salary,
    SUM(salary) OVER (PARTITION BY dept) AS dept_total,
    SUM(salary) OVER (PARTITION BY dept ORDER BY emp_id) AS running_dept_total
FROM Employee_Salaries;
```

**Result:**

|**name**|**dept**|**salary**|**dept_total**|**running_dept_total**|
|---|---|---|---|---|
|Alice|Engineering|120000|320000|120000|
|Bob|Engineering|100000|320000|220000|
|Charlie|Engineering|100000|320000|320000|
|Diana|Sales|90000|170000|90000|
|Evan|Sales|80000|170000|170000|

### 4. Filtering Window Function Results

Window functions run **after** `WHERE` and `GROUP BY`, which means you **cannot** put a window function directly inside a `WHERE` clause. Wrap the query in a **CTE (`WITH` clause)** first, then filter.

```sql
WITH RankedSalaries AS (
    SELECT 
        name,
        dept,
        salary,
        DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC) AS rnk
    FROM Employee_Salaries
)
SELECT name, dept, salary
FROM RankedSalaries
WHERE rnk = 1;
```

**Result (Highest earner per department):**

|**name**|**dept**|**salary**|
|---|---|---|
|Alice|Engineering|120000|
|Diana|Sales|90000|

### Quick Summary Cheat Sheet

|**Category**|**Function**|**Purpose**|
|---|---|---|
|**Ranking**|`ROW_NUMBER()`|Unique sequential numbering (`1, 2, 3, 4`)|
|**Ranking**|`RANK()`|Ranking with gaps on ties (`1, 2, 2, 4`)|
|**Ranking**|`DENSE_RANK()`|Ranking without gaps on ties (`1, 2, 2, 3`)|
|**Offset**|`LAG()` / `LEAD()`|Fetch values from preceding or following rows|
|**Aggregate**|`SUM() OVER (...)`|Partition totals or cumulative running totals|