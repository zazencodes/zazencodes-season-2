# 2025-01-01

Existing table schema:
id INT PRIMARY KEY,
name VARCHAR(100),
email VARCHAR(100)

Changes to apply:
1. Add a new column `age` (INT).
2. Add a NOT NULL constraint to `email`.
3. Add a UNIQUE constraint on `email`.

```sql
ALTER TABLE table_name
ADD COLUMN age INT,
MODIFY email VARCHAR(100) NOT NULL,
ADD UNIQUE (email);
```


