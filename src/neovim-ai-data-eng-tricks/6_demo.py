# Buggy function
def process_data(data):
    result = []
    for item in data:
        if item["value"] > 10:  # Assuming item always has 'value' key
            result.append(item.get("name", "").upper())
    print(result)
    return result


# Example input
data = [
    {"value": 15, "name": "Alice"},
    {"value": 5, "name": "Bob"},
    {"value": 20},  # Missing 'name' key
]

process_data(data)
