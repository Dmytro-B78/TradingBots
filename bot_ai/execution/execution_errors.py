# ================================================================
# File: bot_ai/execution/execution_errors.py
# Module: execution.execution_errors
# Purpose: NT-Tech execution error classes
# Responsibilities:
#   - Provide unified exception types for execution layer
# Notes:
#   - ASCII-only
# ================================================================

class ExecutionError(Exception):
    """Base execution-layer error."""
    pass


class OrderRejectedError(ExecutionError):
    """Raised when exchange rejects an order."""
    pass


class OrderValidationError(ExecutionError):
    """Raised when order validation fails."""
    pass
