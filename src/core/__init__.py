"""
Core Module - Portfolio Version

Central exports for tender automation system.
Demonstrates modular architecture without implementation details.

Note: Concrete implementations hidden.
Full version available to customer after payment.
"""
from __future__ import annotations

# Re-exports with NotImplementedError in source files
from core.async_config import (
    PortalConfig,
    KeyConfig,
    BeneficiaryConfig,
    ApplicationConfig,
    AsyncInstruction,
    load_async_instruction,
    load_async_instruction_with_paths,
    load_cookies_async,
    save_cookies_async,
)
from core.path_resolver import (
    ProjectPaths,
    ConfigLoader,
    initialize_project_paths,
    get_project_paths,
    get_config_loader,
)
from core.async_session import AsyncSessionManager
from core.async_api import GoszakupApiClient, ApiStep, PreviewRedirectError
from core.async_logger import InMemoryLogger, LoggerContext, setup_utf8_logging

__all__ = [
    # Configuration dataclasses
    "PortalConfig",
    "KeyConfig",
    "BeneficiaryConfig",
    "ApplicationConfig",
    "AsyncInstruction",
    # Config loading functions
    "load_async_instruction",
    "load_async_instruction_with_paths",
    "load_cookies_async",
    "save_cookies_async",
    # Path resolution
    "ProjectPaths",
    "ConfigLoader",
    "initialize_project_paths",
    "get_project_paths",
    "get_config_loader",
    # Session and API
    "AsyncSessionManager",
    "GoszakupApiClient",
    "ApiStep",
    # Logging
    "InMemoryLogger",
    "LoggerContext",
    "setup_utf8_logging",
    # Exceptions
    "PreviewRedirectError",
]
