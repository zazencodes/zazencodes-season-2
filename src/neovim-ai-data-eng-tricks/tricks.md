# Neovim AI Data Engineering Tricks





# Terminal

## Intelligently Copy and Update Commands

### Scenario
You have a list of report IDs and need to duplicate a `docker compose run` command for each report ID, modifying the `--report-name-id` flag dynamically.

### Example Command
```markdown
> Duplicate this docker compose run command for each report-name-id given in the list above the command.

---

2025_01_nursing
2025_01_earth
2025_01_chemistry
2025_01_nursing_omitted
2025_01_earth_omitted
2025_01_chemistry_omitted

docker compose run --rm app python /app/scripts/fetch_serps.py \
    --report-name-id 2025_01_nursing
```







# SQL

## Create SQL Statement

### Scenario
You need to merge two tables using a regex match while ensuring only one record is joined from the dimension table.

### Example Data
```sql
-- Source table: product_urls
| url                           | revenue |
|-------------------------------|---------|
| /shoes/nike-air-max-90       | 299.99  |
| /shoes/adidas-ultraboost-21  | 179.99  |
| /clothing/nike-tech-fleece    | 129.99  |

-- Dimension table: product_categories
| pattern         | category    | priority |
|----------------|-------------|----------|
| nike.*shoes    | Nike Shoes  | 1        |
| adidas.*shoes  | Adidas Shoes| 1        |
| nike.*clothing | Nike Apparel| 1        |
```

### Example Command
```markdown
> Write SQL to merge two tables using a regex match. Only join on one record in the dimension table.
```

## Migrate SQL

### Scenario
You have a SQL query written for one database system (e.g., MySQL) and need to rewrite it for BigQuery.

### Example Command
```markdown
> Re-write this SQL for BigQuery.
```


## Optimize SQL

### Scenario
You have a SQL query written for BigQuery that needs performance optimization.

### Example Command
```markdown
> Optimize this SQL (BigQuery)
```








# Airflow/Python

## Build a DAG Template

### Scenario
You need an Airflow DAG template with a `PythonOperator`.

### Example Command
```markdown
> Create an Airflow DAG template with a PythonOperator.
```

## Build out the job

### Scenario
You need to download a file from AWS S3, read it into pandas, and save it locally.

### Example Command
```markdown
> Write a function to download a file from S3, read it with pandas, and save locally.
```


## Write a Docstring to a Function

### Scenario
You need to document a Python function with a detailed docstring and type hints.

### Example Command
```markdown
> Create a docstring and add type hints to this function.
```


## Create a Cron String

### Scenario
You need a cron expression for a job that runs twice daily at 1 AM and 1 PM.

### Example Command
```markdown
> Write a cron string for twice a day, at 1am and at 1pm.
```

## Write a Function for a Docstring

### Scenario
You have a detailed docstring and need the corresponding Python function.

### Example Command
```markdown
> Write a function for the following docstring.

"""Logs summary statistics for a pandas DataFrame.

This function calculates and logs basic summary statistics for a pandas DataFrame,
including the shape, data types, null value counts, and basic descriptive statistics
for numeric columns.

Args:
    df (pd.DataFrame): The input pandas DataFrame to analyze

Returns:
    None: This function only logs output and does not return anything
"""
```








# Documentation

## Format SQL Query Inline in Markdown Document

### Scenario
You want to format a SQL migration query directly in a markdown document.

### Example Command
```markdown
> Format the following SQL inline for a markdown document.

---

WITH user_metrics AS (SELECT user_id,DATE_TRUNC('month', login_date) as login_month,COUNT(*) AS monthly_logins,MAX(login_date) AS last_login,MIN(login_date) AS first_login FROM user_logins WHERE login_date >= '2023-01-01' GROUP BY user_id, DATE_TRUNC('month', login_date)),user_rankings AS (SELECT user_id,login_month,monthly_logins,ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY monthly_logins DESC) as top_months,AVG(monthly_logins) OVER (PARTITION BY user_id) as avg_monthly_logins,LAG(monthly_logins, 1) OVER (PARTITION BY user_id ORDER BY login_month) as prev_month_logins,LEAD(monthly_logins, 1) OVER (PARTITION BY user_id ORDER BY login_month) as next_month_logins FROM user_metrics)SELECT u.user_id,SUM(u.monthly_logins) AS total_logins,COUNT(DISTINCT u.login_month) AS active_months,MAX(u.last_login) AS most_recent_login,MIN(u.first_login) AS earliest_login,MAX(CASE WHEN r.top_months = 1 THEN r.monthly_logins END) AS best_month_logins,ROUND(AVG(r.avg_monthly_logins), 2) AS avg_logins_per_month,SUM(CASE WHEN r.monthly_logins > COALESCE(r.prev_month_logins, 0) THEN 1 ELSE 0 END) AS months_with_growth FROM user_metrics u LEFT JOIN user_rankings r ON u.user_id = r.user_id AND u.login_month = r.login_month GROUP BY u.user_id HAVING total_logins > 10 ORDER BY total_logins DESC;
```


## Markdown Table

### Scenario
You want to create a two-column markdown table from a schema definition.

### Example Command
```markdown
> Make this into a markdown table.

---

[{"name":"dt","type":"DATE","mode":"NULLABLE"},{"name":"page_type_example_client","type":"STRING","mode":"NULLABLE"},{"name":"url","type":"STRING","mode":"NULLABLE"},{"name":"device_name","type":"STRING","mode":"NULLABLE"},{"name":"country_cd","type":"STRING","mode":"NULLABLE"},{"name":"sessions","type":"INTEGER","mode":"NULLABLE"},{"name":"bounce_sessions","type":"INTEGER","mode":"NULLABLE"},{"name":"orders","type":"INTEGER","mode":"NULLABLE"},{"name":"sales","type":"FLOAT","mode":"NULLABLE"},{"name":"page_type","type":"STRING","mode":"NULLABLE"},{"name":"fiscal_week","type":"STRING","mode":"NULLABLE"},{"name":"fiscal_date","type":"DATE","mode":"NULLABLE"},{"name":"fob","type":"RECORD","mode":"NULLABLE","fields":[{"name":"category","type":"STRING"},{"name":"subcategory","type":"STRING"},{"name":"subcategory_type","type":"STRING"}]}]
```










# Plan

## Summary

### Scenario
You want to create a task list in a markdown document that Neovim can toggle with `<leader>ti`.

### Example Command

```markdown
> Create a task list section with checkboxes at the bottom of this page.

---

website_20241111_v3.zip
data starting from 2022-10-31

Confirmed:
In [5]: df.dt.min()
Out[5]: 20221031

I need to update the existing `adobe_website_page` data going back to 20221031.
I will persist a "final v2 snapshot" before ingesting the new data.

I'll have to update the schema:
Existing schema is:
[{"name":"dt","type":"DATE","mode":"NULLABLE"},{"name":"page_type_example_client","type":"STRING","mode":"NULLABLE"},{"name":"url","type":"STRING","mode":"NULLABLE"},{"name":"device_name","type":"STRING","mode":"NULLABLE"},{"name":"country_cd","type":"STRING","mode":"NULLABLE"},{"name":"sessions","type":"INTEGER","mode":"NULLABLE"},{"name":"bounce_sessions","type":"INTEGER","mode":"NULLABLE"},{"name":"orders","type":"INTEGER","mode":"NULLABLE"},{"name":"sales","type":"FLOAT","mode":"NULLABLE"},{"name":"page_type","type":"STRING","mode":"NULLABLE"},{"name":"fiscal_week","type":"STRING","mode":"NULLABLE"},{"name":"fiscal_date","type":"DATE","mode":"NULLABLE"},{"name":"fob","type":"RECORD","mode":"NULLABLE","fields":[{"name":"category","type":"STRING"},{"name":"subcategory","type":"STRING"},{"name":"subcategory_type","type":"STRING"}]}]

The new schema will need additional columns:
instances INTEGER
site_type STRING

I will apply filtering at ingestion time to remove `site_type="microsite"`.
I will need to add `site_type` to downstream tables:
- adobe_website_page_agg
- adobe_website_page_fiscal
- adobe_website_page_fiscal_agg
```





