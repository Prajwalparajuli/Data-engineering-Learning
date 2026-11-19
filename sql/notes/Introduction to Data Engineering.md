## Docker

```bash
# Change the user
su user

# See current path
pwd

# See folders and files available
ls

# Change directory to startA
cd startA

# Starting a container from downloaded yml file (Docker Compose)
docker compose up -d

# Stop and remove containers defined in the yml file
docker compose down

# List running containers
docker ps

# List all containers (including stopped ones)
docker ps -a

# List downloaded Docker images
docker images

# Download an image from Docker Hub
docker pull <image_name>

# Run a new container in detached mode (-d) with port mapping (-p)
docker run -d -p 8080:80 --name <container_name> <image_name>

# Stop a running container
docker stop <container_name_or_id>

# Start a stopped container
docker start <container_name_or_id>

# Remove a stopped container
docker rm <container_name_or_id>

# Remove an image
docker rmi <image_name_or_id>

# View logs of a container (-f to follow live output)
docker logs -f <container_name_or_id>

# Open an interactive terminal inside a running container
docker exec -it <container_name_or_id> /bin/bash

# Build a Docker image from a Dockerfile in the current directory
docker build -t <image_name>:<tag> .

# Remove unused containers, networks, and dangling images
docker system prune

```

## Data Types

> **Key Principle:** Selecting memory-efficient data types is necessary to optimize storage and performance.

### 1. Primitive Numeric Types
Ordered from smallest to largest memory footprint:

| Data Type | Size | Notes / Usage |
| :--- | :--- | :--- |
| `byte` | 1 byte (8 bits) | Smallest integer storage |
| `short` | 2 bytes | Small whole numbers |
| `int` | 4 bytes | Standard whole numbers |
| `long` | 8 bytes | Very large whole numbers |
| `float` | 4 bytes | Single-precision decimal |
| `double` | 8 bytes | Double-precision decimal |

#### Memory Efficiency Example (Storing `123`)
* `123` as `byte` = **1 byte** *(Most efficient)*
* `'123'` as `string` = **3 bytes** *(1 byte per character in standard ASCII/UTF-8)*
* `123` as `int` = **4 bytes**
* `123` as `long` = **8 bytes**

### 2. Exact Decimal Types
Syntax: `decimal(precision, scale)`
* **Precision:** Total maximum number of digits (both left and right of the decimal point).
* **Scale:** Number of digits to the right of the decimal point.
* **Rule:** Scale cannot be greater than precision (e.g., `decimal(3, 6)` will fail).

#### Example: `decimal(10, 2)`
Allows up to **10 total digits** (8 before the decimal, 2 after).

* **Valid:** `25789541.98` *(8 integer digits + 2 decimal digits = 10 total)*
* **Exceeding Scale:** `25789541.9899` $\rightarrow$ Adjusts to fit 2 decimal places *(Note: Most SQL engines **round** this to `.99`, while specific engines may truncate to `.98`)*.
* **Exceeding Precision (Overflow):** `22,789,898,875.98` $\rightarrow$ **Fails** *(Cannot truncate or round digits before the decimal point)*.

### 3. String / Character Types *(Template for future notes)*
* `char(n)` - Fixed-length string
* `varchar(n)` - Variable-length string

### 4. Boolean & Date/Time Types *(Template for future notes)*
* `boolean` - True/False
* `date` / `timestamp` - Date and time values

