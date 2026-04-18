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
    Checks CPU health metrics from the cpu_monitor module.

    Returns:
        dict: A dictionary containing the status of the check and the
        CPU metric data or an error message.

    Raises:
        ThresholdExceededError: If CPU usage exceeds CPU_THRESHOLD.
    """
    try:
        data = cpu_monitor.get_cpu_metrics()

        if data["usage_percent"] > CPU_THRESHOLD:
            raise ThresholdExceededError("CPU usage exceeded threshold")

        return {"status": "OK", "data": data}

    except ServiceUnavailableError as error:
        return {"status": "ERROR", "data": str(error)}


def check_memory():
    """
    Checks memory health metrics from the memory_monitor module.

    Returns:
        dict: A dictionary containing the status of the check and the
        memory metric data or an error message.

    Raises:
        ThresholdExceededError: If memory usage exceeds MEMORY_THRESHOLD.
    """
    try:
        data = memory_monitor.get_memory_metrics()

        if data["usage_percent"] > MEMORY_THRESHOLD:
            raise ThresholdExceededError("Memory usage exceeded threshold")

        return {"status": "OK", "data": data}

    except DataCorruptionError as error:
        return {"status": "ERROR", "data": str(error)}


def check_network():
    """
    Checks network health metrics from the network_monitor module.

    Returns:
        dict: A dictionary containing the status of the check and the
        network metric data or an error message.

    Raises:
        ThresholdExceededError: If network usage exceeds NETWORK_THRESHOLD.
    """
    try:
        data = network_monitor.get_network_metrics()

        if data["usage_percent"] > NETWORK_THRESHOLD:
            raise ThresholdExceededError("Network usage exceeded threshold")

        return {"status": "OK", "data": data}

    except ConnectionTimeoutError as error:
        return {"status": "ERROR", "data": str(error)}

def run_checks():
    """
    Runs CPU, memory, and network checks.

    Returns:
        dict: A dictionary containing the results of all three checks.
    """
    results = {
        "cpu": check_cpu(),
        "memory": check_memory(),
        "network": check_network()
    }
    return results

def log_results(results, filepath):
    """
    Appends monitoring results to a log file.

    Parameters:
        results (dict): The results dictionary from run_checks().
        filepath (str): The path to the log file.

    Returns:
        None
    """
    try:
        with open(filepath, "a") as log_file:
            log_file.write(generate_report(results))
            log_file.write("\n")
    finally:
        with open(filepath, "a") as log_file:
            log_file.write("Logging complete.\n")



def generate_report(results):
    """
    Generates a formatted report string from monitoring results.

    Parameters:
        results (dict): The results dictionary from run_checks().

    Returns:
        str: A formatted multi-line report.
    """
    report = "System Health Report\n"
    report += "CPU: " + str(results.get("cpu", {})) + "\n"
    report += "Memory: " + str(results.get("memory", {})) + "\n"
    report += "Network: " + str(results.get("network", {})) + "\n"
    return report


def main():
    """
    Runs all system checks, prints the report, and logs results.

    Returns:
        None
    """
    results = run_checks()
    report = generate_report(results)
    print(report)
    log_results(results, "monitor.log")




if __name__ == "__main__":
    main()