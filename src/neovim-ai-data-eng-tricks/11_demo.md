# 2025-01-05

Cleaning up this CSV
```
customer_id,name,age,email,city,purchase_amount,date,status,category,loyalty_points
1,John Smith,35,john@email.com,New York,150.50,2023-01-15,active,electronics,500
2,Mary Johnson,,mary@email.com,Chicago,75.25,2023-01-16,inactive,clothing,100
3,Bob Wilson,42,bob@invalid,Los Angeles,200.00,2023-01-17,active,home goods,750
4,Sarah Brown,29,sarah@email.com,Houston,50.75,,active,groceries,250
5,,31,james@email.com,Phoenix,125.00,2023-01-19,active,electronics,1000
6,Lisa Davis,38,lisa@email.com,Philadelphia,-50.25,2023-01-20,inactive,clothing,150
7,Mike Taylor,abc,mike@email.com,San Antonio,175.50,2023-01-21,active,home goods,600
8,Jennifer Martin,45,,Dallas,225.75,2023-01-22,active,groceries,800
9,David Anderson,33,david@email.com,San Diego,90.25,2023-01-23,,electronics,450
```

```python
import pandas as pd
import re

# Read the CSV data
df = pd.read_csv('customer_data.csv')

# Handle missing values
df['name'] = df['name'].fillna('Unknown')
df['age'] = pd.to_numeric(df['age'], errors='coerce')  # Convert non-numeric ages to NaN
df['age'] = df['age'].fillna(df['age'].mean())  # Fill missing ages with mean
df['email'] = df['email'].fillna('no_email@example.com')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['date'] = df['date'].fillna(method='ffill')  # Forward fill missing dates
df['status'] = df['status'].fillna('unknown')

# Validate and clean email addresses
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

df['email'] = df['email'].apply(lambda x: 'invalid@example.com' if not is_valid_email(x) else x)

# Fix negative purchase amounts
df['purchase_amount'] = df['purchase_amount'].abs()

# Clean up status values
df['status'] = df['status'].str.lower()

# Export cleaned data
df.to_csv('cleaned_customer_data.csv', index=False)

print("Data cleaning completed. Summary of changes:")
print(f"- Fixed {df['age'].isna().sum()} missing age values")
print(f"- Standardized {len(df[df['status'] == 'unknown'])} missing status values")
print(f"- Corrected {len(df[df['email'] == 'invalid@example.com'])} invalid email addresses")
print(f"- Fixed {len(df[df['purchase_amount'] < 0])} negative purchase amounts")
