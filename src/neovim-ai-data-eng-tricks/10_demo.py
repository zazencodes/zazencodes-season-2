SELECT
    CONCAT(UPPER(SUBSTRING(c.customer_name, 1, 1)),
           LOWER(SUBSTRING(c.customer_name, 2))) AS formatted_customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.price * oi.quantity * (1 - COALESCE(o.discount, 0))), 2) AS total_spent,
    AVG(p.price) AS avg_order_value,
    MAX(o.order_date) AS last_order_date,
    DATEDIFF(NOW(), MIN(o.order_date)) AS days_since_first_order,
    SUM(CASE
        WHEN p.category = 'Premium' THEN p.price * oi.quantity
        ELSE 0
    END) AS premium_purchases,
    COUNT(DISTINCT p.category) AS unique_categories_bought,
    DENSE_RANK() OVER (
        PARTITION BY EXTRACT(YEAR FROM o.order_date)
        ORDER BY SUM(p.price * oi.quantity) DESC
    ) AS yearly_spending_rank
FROM
    customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN products p ON oi.product_id = p.product_id
    LEFT JOIN customer_segments cs ON c.customer_id = cs.customer_id
WHERE
    c.signup_date > '2022-01-01'  -- Only customers who signed up after 2022
    AND c.status = 'Active'
    AND o.order_status NOT IN ('Cancelled', 'Rejected')
    AND EXISTS (
        SELECT 1
        FROM customer_preferences cp
        WHERE cp.customer_id = c.customer_id
        AND cp.preference_type = 'Newsletter'
    )
GROUP BY
    c.customer_name,
    EXTRACT(YEAR FROM o.order_date)
HAVING
    total_spent > 500
    AND COUNT(DISTINCT o.order_id) >= 3
    AND AVG(p.price) > (
        SELECT AVG(price)
        FROM products
    )
ORDER BY
    total_spent DESC,
    last_order_date DESC
LIMIT 100;

/*
This query analyzes customer purchasing behavior by:
1. Joining customer data with their orders, items, and products
2. Filtering for active customers who signed up after 2022 and subscribed to newsletter
3. Calculating various metrics like total spent, order counts, and premium purchases
4. Showing only high-value customers (spent >500, ≥3 orders)
5. Ranking customers by yearly spending
6. Returns top 100 customers sorted by spending and recency
*/
