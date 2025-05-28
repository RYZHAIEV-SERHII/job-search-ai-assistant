"""Platform adapters for job search."""

from .base import PlatformAdapter, PlatformConfig, SelectorConfig
from .djinni import DjinniAdapter
from .dou import DOUAdapter
from .linkedin import LinkedInAdapter
from .workua import WorkUaAdapter

__all__ = [
    "DOUAdapter",
    "DjinniAdapter",
    "LinkedInAdapter",
    "PlatformAdapter",
    "PlatformConfig",
    "SelectorConfig",
    "WorkUaAdapter",
]
