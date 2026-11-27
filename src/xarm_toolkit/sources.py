"""Interchangeable target sources for Pygame and PAL Robotics ARI."""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class TargetSource(ABC):
    """Provide normalized two-dimensional targets to downstream code."""

    @abstractmethod
    def get_target(self) -> tuple[float, float] | None:
        """Get the next target.

        Returns:
            An ``(x, y)`` tuple in the 0--1000 contract, or None when unavailable.

        Raises:
            RuntimeError: Raised when the source cannot provide source data.
        """

    @abstractmethod
    def close(self) -> None:
        """Release resources held by the target source."""


class PygameTargetSource(TargetSource):
    """Generate normalized targets from Pygame mouse clicks."""

    def __init__(self, pygame_module: Any | None = None, width: int = 800, height: int = 600):
        """Initialize the Pygame mock source.

        Args:
            pygame_module: Pygame module or compatible test double.
            width: Pygame window width in pixels.
            height: Pygame window height in pixels.

        Raises:
            ValueError: Raised when width or height is zero or negative.
        """
        if width <= 0 or height <= 0:
            raise ValueError("Window dimensions must be positive.")

        if pygame_module is None:
            import pygame

            pygame_module = pygame

        self._pygame = pygame_module
        self._width = width
        self._height = height
        self._pygame.init()

    def get_target(self) -> tuple[float, float] | None:
        """Poll Pygame and return the next mouse click as normalized coordinates.

        Returns:
            An ``(x, y)`` tuple from 0--1000, or None when no click is queued.

        Raises:
            RuntimeError: Raised when Pygame event processing fails.
        """
        try:
            for event in self._pygame.event.get():
                if event.type == self._pygame.MOUSEBUTTONDOWN:
                    pixel_x, pixel_y = event.pos
                    x = round((1 - pixel_x / (self._width - 1)) * 1000)
                    y = round((1 - pixel_y / (self._height - 1)) * 1000)
                    return (
                        max(0.0, min(1000.0, float(x))),
                        max(0.0, min(1000.0, float(y))),
                    )
        except Exception as exc:
            raise RuntimeError("Pygame event polling failed.") from exc
        return None

    def close(self) -> None:
        """Quit Pygame and release its display resources."""
        self._pygame.quit()


class ARIPersonTracker(TargetSource):
    """Adapt mocked ARI ROS messages to the TargetSource contract."""

    def __init__(self, message_source: Callable[[], Any]):
        """Initialize an ARI tracking adapter.

        Args:
            message_source: Callable that returns the next tracking message or None.

        Raises:
            ValueError: Raised when ``message_source`` is not callable.
        """
        if not callable(message_source):
            raise ValueError("message_source must be callable.")
        self._message_source = message_source

    def get_target(self) -> tuple[float, float] | None:
        """Read one ARI message and return its normalized person position.

        Returns:
            The first person's ``(x, y)`` center in 0--1000, or None without a target.

        Raises:
            RuntimeError: Raised when message fields cannot be reconciled.
        """
        message = self._message_source()
        if message is None:
            return None

        for field_name in ("target_x", "target_y"):
            if not hasattr(message, field_name):
                raise RuntimeError(f"ARI message is missing '{field_name}'.")

        x = getattr(message, "target_x")
        y = getattr(message, "target_y")
        try:
            x = float(x)
            y = float(y)
        except (TypeError, ValueError) as exc:
            raise RuntimeError("ARI target coordinates must be numeric.") from exc

        if not 0 <= x <= 1000 or not 0 <= y <= 1000:
            raise RuntimeError("ARI target coordinates are outside 0--1000.")
        return x, y

    def close(self) -> None:
        """Close the ARI adapter.

        The adapter owns no external resources because message polling is injected.
        """
