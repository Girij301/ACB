from __future__ import annotations

from threading import Lock

from pydantic import BaseModel


class ExecutionMetricsSnapshot(BaseModel):
    total_executions: int
    active_executions: int
    successful_executions: int
    failed_executions: int
    total_execution_time: float
    average_execution_time: float
    fastest_execution: float
    slowest_execution: float
    success_rate: float
    failure_rate: float


class ExecutionMetrics:
    """
    Runtime execution metrics.

    These metrics are kept in memory and are intended for
    monitoring purposes only.
    """

    def __init__(self) -> None:
        self._lock = Lock()

        self._total = 0
        self._active = 0
        self._success = 0
        self._failed = 0

        self._total_time = 0.0
        self._fastest = 0.0
        self._slowest = 0.0

    def execution_started(self) -> None:
        with self._lock:
            self._total += 1
            self._active += 1

    def execution_finished(
        self,
        *,
        success: bool,
        duration: float,
    ) -> None:
        with self._lock:

            self._active -= 1

            self._total_time += duration

            if self._fastest == 0 or duration < self._fastest:
                self._fastest = duration

            if duration > self._slowest:
                self._slowest = duration

            if success:
                self._success += 1
            else:
                self._failed += 1

    def snapshot(self) -> ExecutionMetricsSnapshot:

        with self._lock:

            average = self._total_time / self._total if self._total else 0.0

            success_rate = (self._success / self._total) * 100 if self._total else 0.0

            failure_rate = (self._failed / self._total) * 100 if self._total else 0.0

            return ExecutionMetricsSnapshot(
                total_executions=self._total,
                active_executions=self._active,
                successful_executions=self._success,
                failed_executions=self._failed,
                total_execution_time=round(self._total_time, 3),
                average_execution_time=round(average, 3),
                fastest_execution=round(self._fastest, 3),
                slowest_execution=round(self._slowest, 3),
                success_rate=round(success_rate, 2),
                failure_rate=round(failure_rate, 2),
            )


execution_metrics = ExecutionMetrics()
