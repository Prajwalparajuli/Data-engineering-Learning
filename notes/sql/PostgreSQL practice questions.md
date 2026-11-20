## About the dataset

This SQL practice set uses a small retail sales dataset running in PostgreSQL 13 inside Docker. It models customers placing orders, the products included in each order, and the categories those products belong to.

The tables are in the `public` schema of the `postgres` database. At the time of inspection, the dataset contained 830 orders spanning July 4, 2021 through May 6, 2023.

## Database schema

Each table’s primary key uniquely identifies a row.

| Table | Rows | Primary key | Other columns |
| --- | ---: | --- | --- |
| `customers` | 91 | `customer_id` | `customer_name`, `contact_name`, `address`, `city`, `postal_code`, `country` |
| `orders` | 830 | `order_id` | `customer_id`, `order_date` |
| `order_details` | 2,155 | `order_detail_id` | `order_id`, `product_id`, `quantity` |
| `products` | 77 | `product_id` | `product_name`, `category_id`, `unit`, `price` |
| `categories` | 8 | `category_id` | `category_name`, `description` |
| `testproducts` | 10 | `testproduct_id` | `product_name`, `category_id` |

IDs and quantities use integer types, `order_date` uses the date type, `price` uses a numeric type, and names, addresses, descriptions, and unit information use character varying types.

## How the tables connect

- A customer can place multiple orders. Join `customers.customer_id` to `orders.customer_id`.
- An order can contain multiple line items. Join `orders.order_id` to `order_details.order_id`.
- A product can appear in multiple line items. Join `products.product_id` to `order_details.product_id`.
- A category can contain multiple products. Join `categories.category_id` to `products.category_id`.
- `testproducts` is an additional product table used in comparison and data quality exercises. Its `category_id` can also be matched to `categories.category_id`.

These relationships are inferred from the columns and data. The database defines primary keys, with no foreign key constraints enforcing the relationships.

Each row in `order_details` represents a product line within an order. To estimate an order’s value, multiply each line’s `quantity` by the matching product’s `price`, then sum those amounts. These calculations use current catalog prices because historical sale prices are absent from the order details.

The dataset also includes two customers without orders and six test products whose category IDs have no matching category, providing examples for practicing joins and finding missing relationships.

## Beginner

1. **Most expensive products.** Return the ID, name, and price of the 10 highest-priced products. Exclude missing prices. Sort by price descending, then by product ID ascending.

```sql
SELECT product_id, product_name, price
FROM products
ORDER BY price DESC
LIMIT 10;
```

2. **Countries represented.** List the unique countries in `customers`, excluding missing countries. Sort alphabetically.

```sql
SELECT DISTINCT(country)
FROM customers
WHERE country IS NOT NULL;

```

3. **Search by name and price.** Find products whose names contain `ch` anywhere, ignoring case, and whose prices are between 10 and 30 inclusive. Return product ID, name, and price, ordered by name and then ID.

```sql
SELECT product_id, product_name, price
FROM products
WHERE price BETWEEN 10 AND 30 AND 
		product_name ILIKE '%ch%'
ORDER BY product_name, product_id;
```

4. **January orders.** Return the order ID, customer ID, and order date of every order placed in January 2023. Sort by date, then order ID.

```sql
SELECT order_id, customer_id, order_date
FROM orders
WHERE order_date >= DATE '2023-01-01' AND
	  order_date < DATE '2023-02-01'
ORDER BY order_date, order_id;
```

5. **Large line items.** Find line items with a quantity of at least 60. Return line item ID, order ID, product ID, and quantity. Sort by quantity descending, then line item ID ascending.

```sql
SELECT order_detail_id, order_id, product_id, quantity
FROM order_details
WHERE quantity >= 60
ORDER BY quantity DESC, order_detail_id ASC;
```

6. **Catalog price summary.** Return one row with the number of products with a price, the lowest price, the highest price, and the average price rounded to two decimal places.

```sql
SELECT DISTINCT COUNT(product_id) AS Number_of_products, 
	   MIN(price) AS Lowest_price, 
	   MAX(price) AS Highest_price,
	   ROUND(AVG(price),2) AS Average_price
FROM products;
```

7. **Countries with at least five customers.** Count customers by country, excluding missing countries. Keep only countries with at least five customers. Sort by count descending, then country alphabetically.

```sql
SELECT country, 
	   COUNT(customer_id) AS Number_of_customers
FROM customers
GROUP BY country
HAVING COUNT(customer_id) >= 5 AND country IS NOT NULL
ORDER BY Number_of_customers DESC, country ASC;
```

8. **Above-average prices.** Return the product ID, name, and price for all products priced strictly above the overall catalog average. Sort by price descending, then product ID ascending.

```sql
SELECT product_id, product_name, price 
FROM products
WHERE price > (SELECT AVG(price) FROM products)
ORDER BY price DESC, product_id ASC;
```

## Intermediate

9. **Products with category names.** Return the ID, name, category name, and price of each product that matches a category. Sort by category name, then product ID.

```sql
SELECT p.product_id, p.product_name, c.category_name, p.price  
FROM products p
JOIN categories c 
ON p.category_id = c.category_id
ORDER BY c.category_name, p.product_id;
```

10. **German customers’ 2022 orders.** Return order ID, order date, customer ID, and customer name for all orders placed in 2022 by customers based in Germany. Sort by date, then order ID.

```sql
SELECT o.order_id, o.order_date, c.customer_id, c.customer_name
FROM customers c
JOIN orders o 
ON c.customer_id = o.customer_id
WHERE c.country = 'Germany' 
      AND o.order_date >= DATE '2022-01-01' 
	  AND o.order_date < DATE '2023-01-01'
ORDER BY o.order_date, o.order_id;
```

11. **Orders per customer.** Return each customer’s ID, name, and number of orders, including customers with zero orders. Sort by order count descending, then customer ID ascending.

```sql
SELECT c.customer_id, c.customer_name, COUNT(order_id) AS Number_of_orders
FROM customers c
LEFT JOIN orders o 
ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY Number_of_orders DESC, c.customer_id; 
```

12. **Customers without orders.** Use `NOT EXISTS` to list customer ID, name, and country for customers who have never placed an order. Sort by customer ID.

```sql
SELECT  c.customer_id, customer_name, country 
FROM customers c
WHERE NOT EXISTS (SELECT o.customer_id 
				  FROM orders o
				  WHERE o.customer_id = c.customer_id);
```

13. **Ten highest-value orders.** Sum the estimated line values for each order, using lines with a matching product, a price, and a quantity. Return order ID, order date, and estimated value rounded to two decimal places for the 10 highest-valued orders. Rank by the unrounded total, with smaller order IDs first when totals tie.

```sql
SELECT od.order_id, 
	   o.order_date, 
	   ROUND(SUM(od.quantity * p.price)) AS line_value
FROM order_details od 
JOIN orders o ON od.order_id = o.order_id
JOIN products p ON od.product_id = p.product_id
GROUP BY od.order_id, o.order_date
ORDER BY line_value DESC
LIMIT 10
```

14. **Units ordered by category.** Sum the quantities recorded in `order_details` for each catalog category. Include all categories and show zero when there are no quantities to sum. Return category ID, name, and total units. Sort by units descending, then category ID ascending.

```sql
SELECT c.category_id, c.category_name, SUM(quantity) AS total_units
FROM order_details od
JOIN products p ON od.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_id, c.category_name
ORDER BY total_units DESC, c.category_id ASC
```

15. **Price bands.** Classify priced products as Budget (below 10), Standard (10 up to but excluding 30), or Premium (30 or above). Return the number of products in each populated band. Sort alphabetically by band name.

```sql
SELECT product_name, price,
	CASE
		WHEN price < 10 THEN 'Budget'
		WHEN price >= 10 AND price < 30 THEN 'Standard'
		ELSE
		'Premium'
	END
FROM products
ORDER BY product_name
```

16. **Test products with unknown categories.** Use `EXCEPT` to find the non-null category IDs used by `testproducts` that are missing from `categories`. Return each of those IDs and the number of test products using it. Sort by category ID.

```sql
WITH unknown_categories AS 
	(SELECT category_id
	FROM testproducts
	WHERE category_id IS NOT NULL
	EXCEPT
	SELECT category_id
	FROM categories)

SELECT uc.category_id, COUNT(*) AS Number_of_products
FROM unknown_categories uc
JOIN testproducts ts ON uc.category_id = ts.category_id
GROUP BY uc.category_id
ORDER BY uc.category_id
```

## Advanced

17. **Average order value by country.** First compute one estimated value per order with at least one line that has a matching product, price, and quantity. Then group these orders by the customer’s country. For countries with at least 10 such orders, return the country, order count, and average order value rounded to two decimal places. Skip missing countries. Sort by unrounded average descending, then country alphabetically.

```sql
WITH country_order AS
	(SELECT od.order_id, 
		   p.product_id, 
		   p.product_name, 
		   c.country,
		   SUM(od.quantity * p.price) AS value
	FROM order_details od 
	JOIN orders o ON od.order_id = o.order_id
	JOIN customers c ON o.customer_id = c.customer_id
	JOIN products p ON od.product_id = p.product_id
	GROUP BY od.order_id, p.product_id, c.country)
SELECT country, 
	   COUNT(order_id) AS order_count,
	   ROUND(AVG(value), 2) AS avg_value
FROM country_order
GROUP BY country
ORDER BY AVG(value) DESC, country
```

18. **Top three price ranks per category.** Within each category, assign rank 1 to the highest price and give equal prices the same rank without leaving gaps. Return category ID, category name, product ID, product name, price, and rank for the first three ranks. Use only priced products with a matching category. Sort by category ID, rank, then product ID.

```sql
WITH ranked_products AS(
	SELECT 
		  p.category_id, 
		  c.category_name, 
		  p.product_id,
		  p.product_name,
		  p.price,
		  DENSE_RANK() OVER (PARTITION BY p.category_id ORDER BY p.price DESC) AS rank
	FROM products p
	JOIN categories c ON p.category_id = c.category_id
	WHERE p.price IS NOT NULL)
SELECT category_id, 
	   category_name,
	   product_id,
	   product_name,
	   price,
	   rank
FROM ranked_products
WHERE rank <= 3
ORDER BY category_id, rank, product_id
```

