# ============================================================
# cpu_monitor.py - Project 3: System Health Monitor
# Provided module - do not modify
# ============================================================

from exceptions import ServiceUnavailableError


def get_cpu_metrics(simulate_error=False):
    """
    Returns CPU health metrics as a dictionary.
    Raises ServiceUnavailableError when simulate_error is True.

    Parameters:
        simulate_error (bool): If True, simulates a service failure.

    Returns:
        dict: A dictionary with keys usage_percent, core_count, and temperature.
    """
    if simulate_error:
        raise ServiceUnavailableError("CPU monitor service is unavailable.")
    return {
        "usage_percent": 63.4,
        "core_count": 8,
        "temperature": 72.1
    }
