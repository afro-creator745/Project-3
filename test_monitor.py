import pytest
import os
from unittest.mock import patch

from exceptions import (
    ServiceUnavailableError,
    DataCorruptionError,
    ConnectionTimeoutError,
    ThresholdExceededError,
)
from monitor import (
    check_cpu,
    check_memory,
    check_network,
    run_checks,
    log_results,
    generate_report,
    CPU_THRESHOLD,
    MEMORY_THRESHOLD,
    NETWORK_THRESHOLD,
)


# ============================================================
# Shared mock data
# ============================================================

NORMAL_CPU    = {"usage_percent": 63.4, "core_count": 8,  "temperature": 72.1}
HIGH_CPU      = {"usage_percent": 95.0, "core_count": 8,  "temperature": 85.0}
NORMAL_MEMORY = {"usage_percent": 58.2, "total_gb": 16.0, "available_gb": 6.7}
HIGH_MEMORY   = {"usage_percent": 90.0, "total_gb": 16.0, "available_gb": 1.6}
NORMAL_NET    = {"usage_percent": 42.1, "latency_ms": 18.3, "packets_lost": 0}
HIGH_NET      = {"usage_percent": 95.0, "latency_ms": 200.0, "packets_lost": 12}


# ============================================================
# exceptions.py class definitions - 6 points
# ============================================================

class TestExceptionClasses:

    def test_service_unavailable_error_exists(self):
        """ServiceUnavailableError should be defined and instantiable."""
        e = ServiceUnavailableError("test")
        assert isinstance(e, Exception)

    def test_data_corruption_error_exists(self):
        """DataCorruptionError should be defined and instantiable."""
        e = DataCorruptionError("test")
        assert isinstance(e, Exception)

    def test_connection_timeout_error_exists(self):
        """ConnectionTimeoutError should be defined and instantiable."""
        e = ConnectionTimeoutError("test")
        assert isinstance(e, Exception)

    def test_threshold_exceeded_error_exists(self):
        """ThresholdExceededError should be defined and instantiable."""
        e = ThresholdExceededError("test")
        assert isinstance(e, Exception)

    def test_all_inherit_from_exception(self):
        """All custom exceptions should inherit from the built-in Exception class."""
        for cls in [ServiceUnavailableError, DataCorruptionError, ConnectionTimeoutError, ThresholdExceededError]:
            assert issubclass(cls, Exception)

    def test_exceptions_are_distinct_types(self):
        """All four exception classes should be distinct types."""
        types = {ServiceUnavailableError, DataCorruptionError, ConnectionTimeoutError, ThresholdExceededError}
        assert len(types) == 4


# ============================================================
# check_cpu() - 7 points
# ============================================================

class TestCheckCpu:

    def test_returns_dict_on_success(self):
        """check_cpu() should return a dictionary on success."""
        with patch("cpu_monitor.get_cpu_metrics", return_value=NORMAL_CPU):
            result = check_cpu()
        assert isinstance(result, dict)

    def test_result_has_status_key(self):
        """check_cpu() result should include a status key."""
        with patch("cpu_monitor.get_cpu_metrics", return_value=NORMAL_CPU):
            result = check_cpu()
        assert "status" in result

    def test_result_has_data_key(self):
        """check_cpu() result should include a data key."""
        with patch("cpu_monitor.get_cpu_metrics", return_value=NORMAL_CPU):
            result = check_cpu()
        assert "data" in result

    def test_handles_service_unavailable_error(self):
        """check_cpu() should handle ServiceUnavailableError without crashing."""
        with patch("cpu_monitor.get_cpu_metrics", side_effect=ServiceUnavailableError("down")):
            try:
                result = check_cpu()
            except ServiceUnavailableError:
                pytest.fail("check_cpu() did not handle ServiceUnavailableError")

    def test_raises_threshold_exceeded_on_high_usage(self):
        """check_cpu() should raise ThresholdExceededError when usage exceeds CPU_THRESHOLD."""
        with patch("cpu_monitor.get_cpu_metrics", return_value=HIGH_CPU):
            with pytest.raises(ThresholdExceededError):
                check_cpu()

    def test_does_not_raise_threshold_on_normal_usage(self):
        """check_cpu() should not raise ThresholdExceededError on normal usage."""
        with patch("cpu_monitor.get_cpu_metrics", return_value=NORMAL_CPU):
            try:
                check_cpu()
            except ThresholdExceededError:
                pytest.fail("check_cpu() raised ThresholdExceededError on normal usage")

    def test_threshold_constant_is_float(self):
        """CPU_THRESHOLD should be a float."""
        assert isinstance(CPU_THRESHOLD, float)


# ============================================================
# check_memory() - 7 points
# ============================================================

class TestCheckMemory:

    def test_returns_dict_on_success(self):
        """check_memory() should return a dictionary on success."""
        with patch("memory_monitor.get_memory_metrics", return_value=NORMAL_MEMORY):
            result = check_memory()
        assert isinstance(result, dict)

    def test_result_has_status_key(self):
        """check_memory() result should include a status key."""
        with patch("memory_monitor.get_memory_metrics", return_value=NORMAL_MEMORY):
            result = check_memory()
        assert "status" in result

    def test_result_has_data_key(self):
        """check_memory() result should include a data key."""
        with patch("memory_monitor.get_memory_metrics", return_value=NORMAL_MEMORY):
            result = check_memory()
        assert "data" in result

    def test_handles_data_corruption_error(self):
        """check_memory() should handle DataCorruptionError without crashing."""
        with patch("memory_monitor.get_memory_metrics", side_effect=DataCorruptionError("corrupt")):
            try:
                result = check_memory()
            except DataCorruptionError:
                pytest.fail("check_memory() did not handle DataCorruptionError")

    def test_raises_threshold_exceeded_on_high_usage(self):
        """check_memory() should raise ThresholdExceededError when usage exceeds MEMORY_THRESHOLD."""
        with patch("memory_monitor.get_memory_metrics", return_value=HIGH_MEMORY):
            with pytest.raises(ThresholdExceededError):
                check_memory()

    def test_does_not_raise_threshold_on_normal_usage(self):
        """check_memory() should not raise ThresholdExceededError on normal usage."""
        with patch("memory_monitor.get_memory_metrics", return_value=NORMAL_MEMORY):
            try:
                check_memory()
            except ThresholdExceededError:
                pytest.fail("check_memory() raised ThresholdExceededError on normal usage")

    def test_threshold_constant_is_float(self):
        """MEMORY_THRESHOLD should be a float."""
        assert isinstance(MEMORY_THRESHOLD, float)


# ============================================================
# check_network() - 7 points
# ============================================================

class TestCheckNetwork:

    def test_returns_dict_on_success(self):
        """check_network() should return a dictionary on success."""
        with patch("network_monitor.get_network_metrics", return_value=NORMAL_NET):
            result = check_network()
        assert isinstance(result, dict)

    def test_result_has_status_key(self):
        """check_network() result should include a status key."""
        with patch("network_monitor.get_network_metrics", return_value=NORMAL_NET):
            result = check_network()
        assert "status" in result

    def test_result_has_data_key(self):
        """check_network() result should include a data key."""
        with patch("network_monitor.get_network_metrics", return_value=NORMAL_NET):
            result = check_network()
        assert "data" in result

    def test_handles_connection_timeout_error(self):
        """check_network() should handle ConnectionTimeoutError without crashing."""
        with patch("network_monitor.get_network_metrics", side_effect=ConnectionTimeoutError("timeout")):
            try:
                result = check_network()
            except ConnectionTimeoutError:
                pytest.fail("check_network() did not handle ConnectionTimeoutError")

    def test_raises_threshold_exceeded_on_high_usage(self):
        """check_network() should raise ThresholdExceededError when usage exceeds NETWORK_THRESHOLD."""
        with patch("network_monitor.get_network_metrics", return_value=HIGH_NET):
            with pytest.raises(ThresholdExceededError):
                check_network()

    def test_does_not_raise_threshold_on_normal_usage(self):
        """check_network() should not raise ThresholdExceededError on normal usage."""
        with patch("network_monitor.get_network_metrics", return_value=NORMAL_NET):
            try:
                check_network()
            except ThresholdExceededError:
                pytest.fail("check_network() raised ThresholdExceededError on normal usage")

    def test_threshold_constant_is_float(self):
        """NETWORK_THRESHOLD should be a float."""
        assert isinstance(NETWORK_THRESHOLD, float)


# ============================================================
# run_checks() - 6 points
# ============================================================

class TestRunChecks:

    def test_returns_dict(self):
        """run_checks() should return a dictionary."""
        with patch("cpu_monitor.get_cpu_metrics", return_value=NORMAL_CPU), \
             patch("memory_monitor.get_memory_metrics", return_value=NORMAL_MEMORY), \
             patch("network_monitor.get_network_metrics", return_value=NORMAL_NET):
            result = run_checks()
        assert isinstance(result, dict)

    def test_result_contains_cpu(self):
        """run_checks() result should contain a cpu key."""
        with patch("cpu_monitor.get_cpu_metrics", return_value=NORMAL_CPU), \
             patch("memory_monitor.get_memory_metrics", return_value=NORMAL_MEMORY), \
             patch("network_monitor.get_network_metrics", return_value=NORMAL_NET):
            result = run_checks()
        assert "cpu" in result

    def test_result_contains_memory(self):
        """run_checks() result should contain a memory key."""
        with patch("cpu_monitor.get_cpu_metrics", return_value=NORMAL_CPU), \
             patch("memory_monitor.get_memory_metrics", return_value=NORMAL_MEMORY), \
             patch("network_monitor.get_network_metrics", return_value=NORMAL_NET):
            result = run_checks()
        assert "memory" in result

    def test_result_contains_network(self):
        """run_checks() result should contain a network key."""
        with patch("cpu_monitor.get_cpu_metrics", return_value=NORMAL_CPU), \
             patch("memory_monitor.get_memory_metrics", return_value=NORMAL_MEMORY), \
             patch("network_monitor.get_network_metrics", return_value=NORMAL_NET):
            result = run_checks()
        assert "network" in result

    def test_all_three_checks_run(self):
        """run_checks() should call all three check functions."""
        with patch("cpu_monitor.get_cpu_metrics", return_value=NORMAL_CPU) as mock_cpu, \
             patch("memory_monitor.get_memory_metrics", return_value=NORMAL_MEMORY) as mock_mem, \
             patch("network_monitor.get_network_metrics", return_value=NORMAL_NET) as mock_net:
            run_checks()
        assert mock_cpu.called
        assert mock_mem.called
        assert mock_net.called

    def test_returns_dict_when_one_service_fails(self):
        """run_checks() should still return a result even if one service raises an error."""
        with patch("cpu_monitor.get_cpu_metrics", side_effect=ServiceUnavailableError("down")), \
             patch("memory_monitor.get_memory_metrics", return_value=NORMAL_MEMORY), \
             patch("network_monitor.get_network_metrics", return_value=NORMAL_NET):
            try:
                result = run_checks()
                assert isinstance(result, dict)
            except ServiceUnavailableError:
                pytest.fail("run_checks() did not handle a service failure")


# ============================================================
# log_results() - 6 points
# ============================================================

class TestLogResults:

    def test_creates_file(self, tmp_path):
        """log_results() should create the log file if it does not exist."""
        filepath = str(tmp_path / "monitor.log")
        results = {"cpu": {"status": "ok"}, "memory": {"status": "ok"}, "network": {"status": "ok"}}
        log_results(results, filepath)
        assert os.path.exists(filepath)

    def test_appends_on_second_call(self, tmp_path):
        """log_results() should append to the file on subsequent calls."""
        filepath = str(tmp_path / "monitor.log")
        results = {"cpu": {"status": "ok"}, "memory": {"status": "ok"}, "network": {"status": "ok"}}
        log_results(results, filepath)
        size_after_first = os.path.getsize(filepath)
        log_results(results, filepath)
        size_after_second = os.path.getsize(filepath)
        assert size_after_second > size_after_first

    def test_file_not_empty(self, tmp_path):
        """log_results() should write content to the file."""
        filepath = str(tmp_path / "monitor.log")
        results = {"cpu": {"status": "ok"}, "memory": {"status": "ok"}, "network": {"status": "ok"}}
        log_results(results, filepath)
        assert os.path.getsize(filepath) > 0

    def test_returns_none(self, tmp_path):
        """log_results() should not return a value."""
        filepath = str(tmp_path / "monitor.log")
        results = {"cpu": {"status": "ok"}, "memory": {"status": "ok"}, "network": {"status": "ok"}}
        result = log_results(results, filepath)
        assert result is None

    def test_does_not_crash_on_empty_results(self, tmp_path):
        """log_results() should handle an empty results dictionary without crashing."""
        filepath = str(tmp_path / "monitor.log")
        try:
            log_results({}, filepath)
        except Exception as e:
            pytest.fail(f"log_results() raised an exception on empty results: {e}")

    def test_multiple_runs_accumulate(self, tmp_path):
        """log_results() called three times should produce a larger file than once."""
        filepath = str(tmp_path / "monitor.log")
        results = {"cpu": {"status": "ok"}, "memory": {"status": "ok"}, "network": {"status": "ok"}}
        log_results(results, filepath)
        size_after_one = os.path.getsize(filepath)
        log_results(results, filepath)
        log_results(results, filepath)
        assert os.path.getsize(filepath) > size_after_one


# ============================================================
# generate_report() - 6 points
# ============================================================

class TestGenerateReport:

    def test_returns_string(self):
        """generate_report() should return a string."""
        results = {"cpu": {"status": "ok", "data": NORMAL_CPU},
                   "memory": {"status": "ok", "data": NORMAL_MEMORY},
                   "network": {"status": "ok", "data": NORMAL_NET}}
        report = generate_report(results)
        assert isinstance(report, str)

    def test_report_not_empty(self):
        """generate_report() should return a non-empty string."""
        results = {"cpu": {"status": "ok", "data": NORMAL_CPU},
                   "memory": {"status": "ok", "data": NORMAL_MEMORY},
                   "network": {"status": "ok", "data": NORMAL_NET}}
        report = generate_report(results)
        assert len(report) > 0

    def test_report_contains_cpu(self):
        """generate_report() output should reference cpu."""
        results = {"cpu": {"status": "ok", "data": NORMAL_CPU},
                   "memory": {"status": "ok", "data": NORMAL_MEMORY},
                   "network": {"status": "ok", "data": NORMAL_NET}}
        report = generate_report(results).lower()
        assert "cpu" in report

    def test_report_contains_memory(self):
        """generate_report() output should reference memory."""
        results = {"cpu": {"status": "ok", "data": NORMAL_CPU},
                   "memory": {"status": "ok", "data": NORMAL_MEMORY},
                   "network": {"status": "ok", "data": NORMAL_NET}}
        report = generate_report(results).lower()
        assert "memory" in report

    def test_report_contains_network(self):
        """generate_report() output should reference network."""
        results = {"cpu": {"status": "ok", "data": NORMAL_CPU},
                   "memory": {"status": "ok", "data": NORMAL_MEMORY},
                   "network": {"status": "ok", "data": NORMAL_NET}}
        report = generate_report(results).lower()
        assert "network" in report

    def test_report_is_multiline(self):
        """generate_report() should return a multi-line string."""
        results = {"cpu": {"status": "ok", "data": NORMAL_CPU},
                   "memory": {"status": "ok", "data": NORMAL_MEMORY},
                   "network": {"status": "ok", "data": NORMAL_NET}}
        report = generate_report(results)
        assert "\n" in report
