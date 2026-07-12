from enum import Enum


class ExecutionEventType(str, Enum):
    """
    Types of events emitted during execution.
    """

    EXECUTION_STARTED = "execution_started"
    EXECUTION_FINISHED = "execution_finished"

    STEP_STARTED = "step_started"
    STEP_COMPLETED = "step_completed"

    RETRY_STARTED = "retry_started"
    RETRY_COMPLETED = "retry_completed"

    DEBUG_STARTED = "debug_started"
    DEBUG_COMPLETED = "debug_completed"

    VALIDATION_STARTED = "validation_started"
    VALIDATION_COMPLETED = "validation_completed"
