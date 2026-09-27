# ==========================================
# Helper Functions
# ==========================================

def format_number(number):
    """
    Convert numbers to K, M, B format.

    Example:
    1500 -> 1.5K
    2500000 -> 2.5M
    """

    if number >= 1_000_000_000:
        return f"{number/1_000_000_000:.2f}B"

    elif number >= 1_000_000:
        return f"{number/1_000_000:.2f}M"

    elif number >= 1_000:
        return f"{number/1_000:.2f}K"

    else:
        return f"{number:.0f}"


# ==========================================
# Currency Formatter
# ==========================================

def format_currency(amount):
    """
    Format currency values.

    Example:
    1250000 -> $1.25M
    """

    return f"${format_number(amount)}"


# ==========================================
# Percentage Formatter
# ==========================================

def format_percentage(value):
    """
    Convert decimal to percentage.

    Example:
    0.245 -> 24.50%
    """

    return f"{value:.2f}%"


# ==========================================
# Profit Color
# ==========================================

def profit_color(value):
    """
    Return color based on profit.
    """

    if value >= 0:
        return "green"

    return "red"


# ==========================================
# KPI Delta Color
# ==========================================

def delta_color(value):
    """
    Return Streamlit delta color.
    """

    if value >= 0:
        return "normal"

    return "inverse"