# 2025-01-10

Ran SQL query:

```sql
WITH user_metrics AS (
  SELECT
    user_id,
    DATE_TRUNC('month', login_date) as login_month,
    COUNT(*) AS monthly_logins,
    MAX(login_date) AS last_login,
    MIN(login_date) AS first_login
  FROM user_logins
  WHERE login_date >= '2023-01-01'
  GROUP BY user_id, DATE_TRUNC('month', login_date)
),
user_rankings AS (
  SELECT
    user_id,
    login_month,
    monthly_logins,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY monthly_logins DESC) as top_months,
    AVG(monthly_logins) OVER (PARTITION BY user_id) as avg_monthly_logins,
    LAG(monthly_logins, 1) OVER (PARTITION BY user_id ORDER BY login_month) as prev_month_logins,
    LEAD(monthly_logins, 1) OVER (PARTITION BY user_id ORDER BY login_month) as next_month_logins
  FROM user_metrics
)
SELECT
  u.user_id,
  SUM(u.monthly_logins) AS total_logins,
  COUNT(DISTINCT u.login_month) AS active_months,
  MAX(u.last_login) AS most_recent_login,
  MIN(u.first_login) AS earliest_login,
  MAX(CASE WHEN r.top_months = 1 THEN r.monthly_logins END) AS best_month_logins,
  ROUND(AVG(r.avg_monthly_logins), 2) AS avg_logins_per_month,
  SUM(CASE WHEN r.monthly_logins > COALESCE(r.prev_month_logins, 0) THEN 1 ELSE 0 END) AS months_with_growth
FROM user_metrics u
LEFT JOIN user_rankings r
  ON u.user_id = r.user_id
  AND u.login_month = r.login_month
GROUP BY u.user_id
HAVING total_logins > 10
ORDER BY total_logins DESC;
```


Schema for the new table, after migration:

| Field Name | Type | Mode | Description |
|------------|------|------|-------------|
| dt | DATE | NULLABLE | |
| page_type_example_client | STRING | NULLABLE | |
| url | STRING | NULLABLE | |
| device_name | STRING | NULLABLE | |
| country_cd | STRING | NULLABLE | |
| sessions | INTEGER | NULLABLE | |
| bounce_sessions | INTEGER | NULLABLE | |
| orders | INTEGER | NULLABLE | |
| sales | FLOAT | NULLABLE | |
| page_type | STRING | NULLABLE | |
| fiscal_week | STRING | NULLABLE | |
| fiscal_date | DATE | NULLABLE | |
| fob.category | STRING | NULLABLE | |
| fob.subcategory | STRING | NULLABLE | |
| fob.subcategory_type | STRING | NULLABLE | |



# 2025-01-04

Running bulk scripts on docker app

```
2025_01_nursing
2025_01_earth
2025_01_chemistry
2025_01_nursing_omitted
2025_01_earth_omitted
2025_01_chemistry_omitted

docker compose run --rm app python /app/scripts/fetch_serps.py \
    --report-name-id 2025_01_nursing
```


```
docker compose run --rm app python /app/scripts/fetch_serps.py \
    --report-name-id 2025_01_nursing

docker compose run --rm app python /app/scripts/fetch_serps.py \
    --report-name-id 2025_01_earth

docker compose run --rm app python /app/scripts/fetch_serps.py \
    --report-name-id 2025_01_chemistry

docker compose run --rm app python /app/scripts/fetch_serps.py \
    --report-name-id 2025_01_nursing_omitted

docker compose run --rm app python /app/scripts/fetch_serps.py \
    --report-name-id 2025_01_earth_omitted

docker compose run --rm app python /app/scripts/fetch_serps.py \
    --report-name-id 2025_01_chemistry_omitted
```


# 2024-04-03

Created docker app

Does xyz....
