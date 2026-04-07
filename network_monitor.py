# ============================================================
# network_monitor.py - Project 3: System Health Monitor
# Provided module - do not modify
# ============================================================

from exceptions import ConnectionTimeoutError


def get_network_metrics(simulate_error=False):
    """
    Returns network health metrics as a dictionary.
    Raises ConnectionTimeoutError when simulate_error is True.

    Parameters:
        simulate_error (bool): If True, simulates a connection timeout.

    Returns:
        dict: A dictionary with keys usage_percent, latency_ms, and packets_lost.
    """
    if simulate_error:
        raise ConnectionTimeoutError("Network monitor connection timed out.")
    return {
        "usage_percent": 42.1,
        "latency_ms": 18.3,
        "packets_lost": 0
    }
