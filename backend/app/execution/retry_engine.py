from app.core.config import settings
from app.schemas.failure import FailureAnalysis


class RetryEngine:
    """
    Decides whether a failed step should be retried.
    """

    def __init__(
        self,
        max_retries: int | None = None,
    ) -> None:
        self.max_retries = (
            max_retries if max_retries is not None else settings.MAX_RETRIES
        )

    def should_retry(
        self,
        analysis: FailureAnalysis,
        attempt: int,
    ) -> bool:
        """
        Decide whether a step should be retried.
        """

        if attempt >= self.max_retries:
            return False

        return analysis.retryable
