import cpu_monitor
import memory_monitor
import network_monitor

from exceptions import (
    ServiceUnavailableError,
    DataCorruptionError,
    ConnectionTimeoutError,
    ThresholdExceededError
)

CPU_THRESHOLD = 80.0
MEMORY_THRESHOLD = 75.0
NETWORK_THRESHOLD = 90.0

def check_cpu():
    """
       Retrieves CPU metrics, handles service availability errors,
       and checks whether CPU usage exceeds the allowed threshold.

       Returns:
        dict: A dictionary containing the status and CPU data or error message.
       """
    try:
        data = cpu_monitor.get_cpu_metrics()

        if data["usage_percent"] > CPU_THRESHOLD:
            raise ThresholdExceededError("CPU usage exceeded threshold")

        return {
            "status": "OK",
            "data": data
        }

    except ServiceUnavailableError as error:
        return {
            "status": "ERROR",
            "data": str(error)
        }

    except ThresholdExceededError as error:
        return {
            "status": "ERROR",
            "data": str(error)
        }


def check_memory():
    """
    Retrieves memory metrics, handles data corruption errors,
    and checks whether memory usage exceeds the allowed threshold.

    Returns:
        dict: A dictionary containing the status and memory data or error message.
    """
    try:
        data = memory_monitor.get_memory_metrics()

        if data["usage_percent"] > MEMORY_THRESHOLD:
            raise ThresholdExceededError("Memory usage exceeded threshold")

        return {
            "status": "OK",
            "data": data
        }

    except DataCorruptionError as error:
        return {
            "status": "ERROR",
            "data": str(error)
        }

    except ThresholdExceededError as error:
        return {
            "status": "ERROR",
            "data": str(error)
        }



def check_network():
    """
    Retrieves network metrics, handles connection timeout errors,
    and checks whether network usage exceeds the allowed threshold.

    Returns:
        dict: A dictionary containing the status and network data or error message.
    """
    try:
        data = network_monitor.get_network_metrics()

        if data["usage_percent"] > NETWORK_THRESHOLD:
            raise ThresholdExceededError("Network usage exceeded threshold")

        return {
            "status": "OK",
            "data": data
        }

    except ConnectionTimeoutError as error:
        return {
            "status": "ERROR",
            "data": str(error)
        }

    except ThresholdExceededError as error:
        return {
            "status": "ERROR",
            "data": str(error)
        }