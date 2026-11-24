**What is a collection?** A collection is a container. It keeps many values together. In data engineering, you use collections to keep rows and records in memory.

There are 4 main collections: **list, tuple, set, dict**.

**Big-O terms:**

- **O(1):** The time is constant. The size of the data has no effect.
- **O(n):** The time increases with the size of the data.
- **O(n log n):** This is the usual time for a sort.
- **Space:** This is the quantity of memory that the collection uses.

---

### 1. List `[ ]`

- A list keeps items in order.
- You can change a list.
- A list can have duplicate items.

```python
rows = [10, 20, 20, 30]
rows.append(40)
rows[0]   # 10
```

**Note:** Use a list to keep rows before you load them into a database.

**Time:**

- `rows[i]`: O(1)
- `append()` and `pop()` at the end: O(1)
- `insert(0, x)` and `pop(0)` at the start: O(n). All the other items move.
- `x in rows`: O(n). Python examines each item, one at a time.

**Space:** O(n)

**CAUTION:** Do not use a list to find items in large data. This operation is slow.

---

### 2. Tuple `( )`

- A tuple keeps items in order.
- You cannot change a tuple after you make it.

```python
record = (1, "Prajwal", "2026-11-23")
```

**Note:** Use a tuple for data that must not change. An example is one row from a database. Database queries give rows as tuples.

**Note:** You can use a tuple as a dict key. You cannot use a list as a dict key.

**Time:**

- `record[i]`: O(1)
- `x in record`: O(n)

**Space:** O(n). A tuple uses less memory than a list.

---

### 3. Set `{ }`

- A set keeps only unique values.
- A set does not keep the order of items.

```python
ids = {1, 2, 2, 3}              # {1, 2, 3}
new = source_ids - target_ids   # IDs that are not loaded
```

**Note:** Use a set to remove duplicates.

**Note:** Use set operations (`-`, `&`, `|`) to compare source data and target data.

**Time:**

- `add()`, `remove()`, `x in ids`: O(1) (average)
- `a - b`: O(len(a))
- `a | b` and `a & b`: approximately O(len(a) + len(b))
- Make a set from a list: O(n)

**Space:** O(n). A set uses more memory than a list, because a set is a hash table.

**Note:** A set uses more memory to give more speed.

---

### 4. Dict `{key: value}`

- A dict keeps data as pairs of keys and values.
- Each key is unique.

```python
user = {"id": 1, "name": "Prajwal"}
user["name"]           # Prajwal
user.get("email")      # None. No error occurs.
```

**Note:** A dict has the same structure as a JSON record.

**Note:** Use `.get()` when a key can be missing. This prevents errors from bad data.

**Time:**

- Get, set, or delete a value by key: O(1) (average)
- `key in user`: O(1)
- Read all items in a loop: O(n)

**Space:** O(n). A dict uses more memory than a list, because a dict is a hash table.

**Note:** Make a dict one time in O(n). After that, each lookup is O(1).

---

### Comparison

- If you must keep order and change items, use a **list**.
- If the data must not change, use a **tuple**.
- If you must have unique values or fast checks, use a **set**.
- If you must find values by a key, use a **dict**.

---

### 5. Other Tools: `from collections import ...`

**defaultdict:** A defaultdict is a dict. When a key is missing, it makes the key automatically.

```python
groups = defaultdict(list)
groups["2026-11-23"].append(row)   # No KeyError occurs.
```

**Note:** Use a defaultdict to put rows into groups by date or partition.

**Time:** Same as a dict. Each operation is O(1).  
**Space:** O(n)

**Counter:** A Counter counts items.

```python
Counter(["ok", "ok", "fail"])   # {'ok': 2, 'fail': 1}
```

**Note:** Use a Counter to do data quality checks. For example, count the rows that have errors.

**Time:** Make a Counter: O(n). `most_common(k)`: O(n log k)  
**Space:** O(number of unique values)

**deque:** A deque is a list that is fast at the two ends.

```python
last5 = deque(maxlen=5)   # Keeps only the last 5 items
```

**Note:** Use a deque to keep the last N events in a stream.

**Time:** `append`, `appendleft`, `pop`, `popleft`: O(1). Access to an item in the middle: O(n).  
**Space:** O(n). If you set `maxlen`, the space is O(maxlen).

---

### 6. List of Dicts

This is the most usual data structure in data engineering.

```python
rows = [
    {"id": 1, "city": "Austin", "amount": 50},
    {"id": 2, "city": "Dallas", "amount": 30},
]
```

**Note:** You get this structure from an API, a JSON file, or `csv.DictReader`.

**Time:**

- Read all rows in a loop: O(n)
- Find one row by ID with a loop: O(n). This is slow.
- Better procedure: Make the dict `{r["id"]: r for r in rows}` one time. This is O(n). After that, each lookup is O(1).

**Space:** O(n × number of fields)

---

### 7. Comprehensions

A comprehension makes a collection in one line.

```python
ids     = [r["id"] for r in rows]                # list
cities  = {r["city"] for r in rows}              # set (unique values)
by_id   = {r["id"]: r for r in rows}             # dict (lookup)
big     = [r for r in rows if r["amount"] > 40]  # filter
```

**Note:** A comprehension replaces a loop and `append()`. It is also a little faster than a loop.

**Time:** O(n)  
**Space:** O(n). The full result is in memory.

---

### 8. Generators

A generator gives one item at a time. It does not keep all items in memory.

```python
ids = (r["id"] for r in rows)   # Use ( ), not [ ]
```

**Note:** Use a generator for large files and streams.

**CAUTION:** You can read a generator one time only. After that, the generator is empty.

**Time:** O(n) to read all items. This is the same as a list.  
**Space:** O(1). This is the main advantage of a generator.

---

### 9. namedtuple

A namedtuple is a tuple that has names for its fields.

```python
from collections import namedtuple
Row = namedtuple("Row", ["id", "name"])
r = Row(1, "Prajwal")
r.name   # Use this, not r[1]
```

**Note:** Field names are easier to read than index numbers.

**Time:** Access to a field: O(1)  
**Space:** O(n). A namedtuple uses the same memory as a tuple. It uses less memory than a dict, because it does not keep the keys in each row.

**Note:** For millions of records, a namedtuple uses less memory than a dict.

---

### 10. Sort

```python
sorted(rows, key=lambda r: r["amount"])                 # Makes a new list
sorted(rows, key=lambda r: r["amount"], reverse=True)   # High to low
rows.sort(key=lambda r: r["amount"])                    # Sorts the same list
```

**Note:** The `key=` parameter tells Python which value to sort by.

**Time:** O(n log n)  
**Space:** `sorted()` makes a new list, so it is O(n). `.sort()` does not make a new list. It uses less memory.

---

### 11. Copy

```python
a = [{"x": 1}]
b = a.copy()          # Shallow copy. a and b share the inner dict.
b[0]["x"] = 99        # This also changes a.

import copy
c = copy.deepcopy(a)  # Deep copy. c is fully separate from a.
```

**Note:** For nested data, use `deepcopy` to make a fully separate copy.

**Time:** Shallow copy: O(n). Deep copy: O(all nested items). A deep copy is much slower.  
**Space:** Shallow copy: O(n). Deep copy: it duplicates all the data.

**CAUTION:** Do not use `deepcopy` on large data unless it is necessary.

---

### 12. Batches

Send data in small groups.

```python
from itertools import batched     # Python 3.12 or later
for chunk in batched(rows, 500):
    load(chunk)
```

**Note:** Databases and APIs do not accept 1 million rows at one time. Send 500 or 1000 rows at a time.

**Time:** O(n) in total  
**Space:** O(batch size). Only one batch is in memory at a time, if the source is a generator.

---

### 13. Speed Comparison

|Operation|list|tuple|set|dict|deque|
|---|---|---|---|---|---|
|Access by index|O(1)|O(1)|n/a|n/a|O(n)|
|`x in ...`|O(n)|O(n)|**O(1)**|**O(1)**|O(n)|
|Add at the end|O(1)|n/a|O(1)|O(1)|O(1)|
|Add or remove at the start|O(n)|n/a|n/a|n/a|**O(1)**|
|Memory|normal|lowest|high|high|normal|

**Note:** If you check 1 million rows against a list, the operation is very slow. If you check them against a set, it takes only seconds.

---

### 14. When Collections Are Not Sufficient

- For millions of rows with many calculations, use **pandas** or **Polars**.
- For data that is larger than memory, use **Spark** or **DuckDB**.

**Time:** Most operations are still O(n). But these tools are much faster in practice, because they use optimized C or Rust code, not Python loops.  
**Space:** pandas must keep all data in memory. Spark and DuckDB can move data to disk or divide it between many computers.

**Note:** You still use collections in pipelines for configurations, small lookups, and connection code.
