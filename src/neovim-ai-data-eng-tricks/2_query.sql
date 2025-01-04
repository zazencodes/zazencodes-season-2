-- Recommended indexes for optimization:
-- CREATE INDEX idx_orders_user_id ON orders(user_id);
-- CREATE INDEX idx_order_items_order_id ON order_items(order_id);
-- CREATE INDEX idx_order_items_product_id ON order_items(product_id);
-- CREATE INDEX idx_products_price ON products(price);

SELECT
    u.name AS user_name,
    o.order_id,
    order_total.total_price
FROM
    users u
    INNER JOIN orders o ON u.user_id = o.user_id
    INNER JOIN (
        SELECT
            oi.order_id,
            SUM(p.price) AS total_price
        FROM
            order_items oi
            INNER JOIN products p ON oi.product_id = p.product_id
        GROUP BY
            oi.order_id
        HAVING
            SUM(p.price) > 100
    ) order_total ON o.order_id = order_total.order_id
ORDER BY
    order_total.total_price DESC;
