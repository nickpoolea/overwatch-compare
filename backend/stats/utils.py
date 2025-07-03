"""
Utility functions for the stats app.
"""

def format_battletag(battletag):
    """Format a BattleTag for API usage."""
    return battletag.replace("#", "-")

def format_stat_value(stat_key, value):
    """Format a stat value for display."""
    if value is None:
        return "N/A"
    if stat_key == 'time_played' and isinstance(value, (int, float)):
        hours = int(value // 3600)
        minutes = int((value % 3600) // 60)
        return f"{hours}h {minutes}m"
    return str(value)

def calculate_difference(stat_key, value1, value2):
    """Calculate the difference between two stat values."""
    if not isinstance(value1, (int, float)) or not isinstance(value2, (int, float)):
        return "N/A"
    diff = value1 - value2
    if stat_key == 'time_played':
        diff_hours = int(abs(diff) // 3600)
        diff_minutes = int((abs(diff) % 3600) // 60)
        sign = "+" if diff >= 0 else "-"
        return f"{sign}{diff_hours}h {diff_minutes}m"
    return f"+{diff}" if diff >= 0 else str(diff)
