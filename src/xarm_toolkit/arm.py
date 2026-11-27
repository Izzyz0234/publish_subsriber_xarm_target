"""Adapters for sending target commands to an xArm controller."""

from collections.abc import Callable, Sequence
from typing import Any


class ArmController:
    """Control an xArm through a small, hardware-independent interface."""

    def __init__(self, controller: Any | None = None, controller_factory: Callable[..., Any] | None = None):
        """Initialize the arm adapter.

        Args:
            controller: An existing controller-compatible object. Use this for tests.
            controller_factory: Create a controller when ``controller`` is omitted.

        Raises:
            RuntimeError: Raised when no controller can be created.
        """
        if controller is not None:
            self._controller = controller
            return

        if controller_factory is None:
            try:
                import xarm

                controller_factory = lambda: xarm.Controller("USB")
            except ImportError as exc:
                raise RuntimeError("The xarm package is not installed.") from exc

        try:
            self._controller = controller_factory()
        except Exception as exc:
            raise RuntimeError("Unable to create the xArm controller.") from exc

    def move_to(self, positions: Sequence[Sequence[int]]) -> None:
        """Move the requested channels to the supplied positions.

        Args:
            positions: Channel/position pairs, such as ``[[6, 500], [4, 500]]``.

        Raises:
            ValueError: Raised when a channel or position is outside 0--1000.
            RuntimeError: Raised when the HID controller rejects the command.
        """
        normalized = []
        for pair in positions:
            if len(pair) != 2:
                raise ValueError("Each position must contain a channel and a value.")
            channel, position = pair
            if not 0 <= int(channel) <= 999:
                raise ValueError("The channel must be between 0 and 999.")
            if not 0 <= int(position) <= 1000:
                raise ValueError("The position must be between 0 and 1000.")
            normalized.append([int(channel), int(position)])

        try:
            self._controller.setPosition(normalized)
        except Exception as exc:
            raise RuntimeError("The xArm rejected the move command.") from exc

    def set_servo(self, channel: int, position: int) -> None:
        """Move one servo to a position.

        Args:
            channel: Integer servo channel.
            position: Target position between 0 and 1000.

        Raises:
            ValueError: Raised when channel or position is outside the valid range.
            RuntimeError: Raised when the HID controller rejects the command.
        """
        self.move_to([[channel, position]])

    def is_available(self) -> bool:
        """Return whether a controller instance is currently attached.

        Returns:
            True when the adapter has a controller; otherwise False.
        """
        return self._controller is not None

