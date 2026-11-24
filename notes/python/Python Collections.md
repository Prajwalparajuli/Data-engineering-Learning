
**What's a collection?** A container that holds many values together. In Data Engineering, that's how rows/records are held n memory while moving data around.

There are 4 main ones: **list, tuple, set, dict**.

**Quick Big-O reminder for myself:**
- **O(1)**: instant, doesn't matter how big the data is
- **O(n)**: grows with data size (checks every item)
- **O(n log n)**: sorting speed
- **Space** = how much memory it takes
### 1. List `[ ]`

- An ordered bag of items, that can change.
- Duplicates are allowed.
- Linear Data Structure.

```python
rows = [10, 20, 20, 30]
rows.append(40)
rows[0]   # 10
```

📝 _Think of it as rows waiting to be loaded somewhere._

⏱ **Time**

- `rows[i]` → O(1)
- `append()` / `pop()` at end → O(1)
- `insert(0, x)` / `pop(0)` at front → O(n) (everything shifts)
- `x in rows` → O(n) (checks one by one)
- searching = O(n)

💾 **Space:** O(n)

⚠️ Searching a big list is slow. Don't use it for lookups.
### 2. Tuple `( )`

- Like a list, but **can't be changed** once made.

```python
record = (1, "Prajwal", "2026-11-23")
```

📝 _Use it when data shouldn't change, like one DB row._ DB queries return rows as tuples.  
📝 It can be used as a dict key (a list can't).

⏱ **Time**

- `record[i]` → O(1)
- `x in record` → O(n)

💾 **Space:** O(n), slightly **less** memory than a list (fixed size, no room for growth)
### 3. Set `{ }`

- Only **unique** values, with **no order**.

```python
ids = {1, 2, 2, 3}   # {1, 2, 3}
new = source_ids - target_ids   # ids not loaded yet
```

📝 _Easiest way to remove duplicates._  
📝 Set math (`-`, `&`, `|`) is great for comparing source and target.

⏱ **Time**

- `add()`, `remove()`, `x in ids` → O(1) average
- `a - b` → O(len(a))
- `a | b`, `a & b` → about O(len(a) + len(b))
- Building a set from a list → O(n)
- Searching = O(n)

💾 **Space:** O(n), uses **more** memory than a list (it's a hash table underneath)

📝 _I'm trading memory for speed._
### 4. Dict `{key: value}`

- Stores data as key → value pairs. Keys are unique.

```python
user = {"id": 1, "name": "Prajwal"}
user["name"]           # Prajwal
user.get("email")      # None, no error
```

📝 _This is basically a JSON record._  
📝 Use `.get()` when a key might be missing (messy data!).

⏱ **Time**

- Get / set / delete by key → O(1) average
- `key in user` → O(1)
- Looping over all items → O(n)

💾 **Space:** O(n), more than a list (hash table)

📝 _Build a dict once in O(n), then every lookup is instant._
### Quick comparison (my cheat line)

- Need order + changes → **list**
- Fixed data → **tuple**
- Unique values / fast checking → **set**
- Look up by a key → **dict**
### 5. Extra tools: `from collections import ...`

**defaultdict**: a dict that doesn't crash on missing keys.

```python
groups = defaultdict(list)
groups["2026-11-23"].append(row)   # no KeyError
```

📝 Useful for grouping rows by date/partition.  
⏱ Same as dict, O(1) per operation | 💾 O(n)

**Counter**: counts things for me.

```python
Counter(["ok", "ok", "fail"])   # {'ok': 2, 'fail': 1}
```

📝 Quick data-quality check, e.g. how many failed rows.  
⏱ Building → O(n) | `most_common(k)` → O(n log k)  
💾 O(number of unique values)

**deque**: a list that's fast at both ends.

```python
last5 = deque(maxlen=5)   # keeps only the last 5
```

📝 Good for "last N events" in a stream.  
⏱ `append`, `appendleft`, `pop`, `popleft` → O(1) | access in the middle → O(n)  
💾 O(n), or O(maxlen) if I set a limit
### 6. List of dicts: the most common DE shape

```python
rows = [
    {"id": 1, "city": "Austin", "amount": 50},
    {"id": 2, "city": "Dallas", "amount": 30},
]
```

📝 _This is what I get from an API, a JSON file, or `csv.DictReader`._

⏱ **Time**

- Loop through all rows → O(n)
- Find a row by id (looping) → O(n) ❌
- Better: build `{r["id"]: r for r in rows}` once (O(n)), then each lookup is O(1) ✅

💾 **Space:** O(n × number of fields)
### 7. Comprehensions: short way to build collections

```python
ids     = [r["id"] for r in rows]                # list
cities  = {r["city"] for r in rows}              # set (unique)
by_id   = {r["id"]: r for r in rows}             # dict (lookup)
big     = [r for r in rows if r["amount"] > 40]  # filter
```

📝 _One line instead of a loop + append._ A bit faster than a normal loop too.

⏱ **Time:** O(n)  
💾 **Space:** O(n), since it builds the whole result in memory
### 8. Generators: for big data

```python
ids = (r["id"] for r in rows)   # ( ) not [ ]
```

- Gives one item at a time and doesn't store everything.

📝 _Use it for big files and streams._  
⚠️ It can only be looped through **once**.

⏱ **Time:** O(n) to go through everything (same as a list)  
💾 **Space:** **O(1)**. That's the whole point!
### 9. namedtuple: a tuple with names

```python
from collections import namedtuple
Row = namedtuple("Row", ["id", "name"])
r = Row(1, "Prajwal")
r.name   # instead of r[1]
```

📝 _Easier to read than `row[3]`._

⏱ **Time:** field access → O(1)  
💾 **Space:** O(n), same as a tuple and **lighter than a dict** (no keys stored per row)

📝 _Millions of records? namedtuple uses less memory than dicts._
### 10. Sorting

```python
sorted(rows, key=lambda r: r["amount"])                 # new list
sorted(rows, key=lambda r: r["amount"], reverse=True)   # high to low
rows.sort(key=lambda r: r["amount"])                    # sorts in place
```

📝 _`key=` tells Python what to sort by._

⏱ **Time:** O(n log n)  
💾 **Space:** `sorted()` → O(n) (makes a new list) | `.sort()` → no new list, saves memory
### 11. Copying: this trips people up

```python
a = [{"x": 1}]
b = a.copy()          # shallow: inner dict is SHARED
b[0]["x"] = 99        # a changes too! 😬

import copy
c = copy.deepcopy(a)  # fully separate
```

📝 _Nested data needs `deepcopy` if I want a true copy._

⏱ **Time:** shallow → O(n) | deep → O(every nested item), much slower  
💾 **Space:** shallow → O(n) | deep → duplicates **everything**

⚠️ Don't deepcopy huge data unless I really need to.
### 12. Batching: send data in chunks

```python
from itertools import batched     # Python 3.12+
for chunk in batched(rows, 500):
    load(chunk)
```

📝 _Databases/APIs don't like 1M rows at once._

⏱ **Time:** O(n) total  
💾 **Space:** O(batch size), only one chunk in memory at a time (if reading from a generator)
### 13. Speed: the full picture

|Operation|list|tuple|set|dict|deque|
|---|---|---|---|---|---|
|Access by index|O(1)|O(1)|n/a|n/a|O(n)|
|`x in ...`|O(n)|O(n)|**O(1)**|**O(1)**|O(n)|
|Add at end|O(1)|n/a|O(1)|O(1)|O(1)|
|Add/remove at front|O(n)|n/a|n/a|n/a|**O(1)**|
|Memory|normal|lowest|high|high|normal|

📝 _1M rows checked against a list = very slow. Against a set = seconds._
### 14. When collections aren't enough

- Millions of rows with lots of math → **pandas / Polars**
- Bigger than memory → **Spark / DuckDB**

⏱ Still O(n) for most operations, but **much faster in practice** (they run optimized C/Rust code instead of Python loops)  
💾 pandas needs everything in memory. Spark and DuckDB can spill to disk or spread across machines.

📝 _Collections are still used everywhere for configs, small lookups, and glue code in pipelines._
