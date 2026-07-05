"""Middleware package namespace for cross-cutting HTTP concerns."""

from app.middleware.request_logging import RequestLoggingMiddleware

__all__ = ["RequestLoggingMiddleware"]
