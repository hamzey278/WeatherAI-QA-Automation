import statistics
import time
import pytest
from clients.weather_api_client import WeatherAPIClient
from config.settings import settings
from utils.assertions import assert_response_time, assert_status_code


@pytest.mark.performance
class TestAPIPerformance:
    """Lightweight performance test suite measuring API latency and response thresholds."""

    def test_single_request_latency(self, api_client: WeatherAPIClient):
        """Verify single request response time remains under configured performance threshold."""
        start_time = time.perf_counter()
        response = api_client.get_weather(lat=-1.2921, lon=36.8219)
        elapsed_seconds = time.perf_counter() - start_time

        assert_status_code(response, 200)
        assert_response_time(elapsed_seconds, threshold_ms=settings.PERFORMANCE_THRESHOLD_MS)

    def test_average_and_p95_latency_batch(self, api_client: WeatherAPIClient):
        """Measure average and p95 latency across a small batch of non-destructive requests."""
        sample_size = 5
        latencies_ms = []

        for _ in range(sample_size):
            start_time = time.perf_counter()
            response = api_client.get_weather(lat=-1.2921, lon=36.8219)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            assert_status_code(response, 200)
            latencies_ms.append(elapsed_ms)

        avg_latency = statistics.mean(latencies_ms)
        # Calculate p95 (95th percentile)
        sorted_latencies = sorted(latencies_ms)
        p95_index = int(0.95 * len(sorted_latencies)) - 1
        p95_latency = sorted_latencies[max(0, p95_index)]

        print(f"\n[Performance Summary] Batch Size: {sample_size} | Avg: {avg_latency:.2f}ms | P95: {p95_latency:.2f}ms")
        assert avg_latency <= settings.PERFORMANCE_THRESHOLD_MS, f"Average latency {avg_latency:.2f}ms exceeded threshold {settings.PERFORMANCE_THRESHOLD_MS}ms"
        assert p95_latency <= settings.PERFORMANCE_THRESHOLD_MS * 1.5, f"P95 latency {p95_latency:.2f}ms exceeded 1.5x threshold"
