# ============================================================
# memory_monitor.py - Project 3: System Health Monitor
# Provided module - do not modify
# ============================================================

from exceptions import DataCorruptionError


def get_memory_metrics(simulate_error=False):
    """
    Returns memory health metrics as a dictionary.
    Raises DataCorruptionError when simulate_error is True.

    Parameters:
        simulate_error (bool): If True, simulates a data corruption failure.

    Returns:
        dict: A dictionary with keys usage_percent, total_gb, and available_gb.
    """
    if simulate_error:
        raise DataCorruptionError("Memory monitor data is corrupted.")
    return {
        "usage_percent": 58.2,
        "total_gb": 16.0,
        "available_gb": 6.7
    }
