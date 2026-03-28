"""
Protocol definition for dependency parsers.

This module defines the structural interface that all parser implementations
(e.g., Pip, NPM, Poetry) must follow to be compatible with the stalecheck
checker logic.
"""
from typing import Protocol, runtime_checkable

from packaging.requirements import Requirement


@runtime_checkable
class Parser(Protocol):
    """
    Structural interface for dependency file parsers.
    
    Any class implementing this protocol must provide a `get_packages` 
    method that returns a list of PEP 508 Requirement objects.
    """
    def get_packages(self) -> list[Requirement]:
        ...
