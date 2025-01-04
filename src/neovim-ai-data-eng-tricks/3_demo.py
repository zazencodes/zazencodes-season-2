def calculate_retention(user_logins: list[list[str]], days: int) -> float:
    """
    Calculate user retention rate based on login activity over a period of time.

    Args:
        user_logins: A list of daily user logins, where each inner list contains user IDs
        days: Number of initial days to consider for active user base

    Returns:
        float: Retention rate (0.0 to 1.0) of users who logged in after the initial period
    """
    active_users = set()    # Users who logged in during initial period
    retained_users = set()  # Users who logged in after initial period

    for day, logins in enumerate(user_logins):
        for user in logins:
            if day < days:
                active_users.add(user)
            if user in active_users:
                retained_users.add(user)

    return len(retained_users) / len(active_users) if active_users else 0
