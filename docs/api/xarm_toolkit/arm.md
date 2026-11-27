Module xarm_toolkit.arm
=======================
Adapters for sending target commands to an xArm controller.

Classes
-------

`ArmController(controller: typing.Any | None = None, controller_factory: collections.abc.Callable[..., typing.Any] | None = None)`
:   Control an xArm through a small, hardware-independent interface.
    
    Initialize the arm adapter.
    
    Args:
        controller: An existing controller-compatible object. Use this for tests.
        controller_factory: Create a controller when ``controller`` is omitted.
    
    Raises:
        RuntimeError: Raised when no controller can be created.

    ### Methods

    `is_available(self) ‑> bool`
    :   Return whether a controller instance is currently attached.
        
        Returns:
            True when the adapter has a controller; otherwise False.

    `move_to(self, positions: Sequence[Sequence[int]]) ‑> None`
    :   Move the requested channels to the supplied positions.
        
        Args:
            positions: Channel/position pairs, such as ``[[6, 500], [4, 500]]``.
        
        Raises:
            ValueError: Raised when a channel or position is outside 0--1000.
            RuntimeError: Raised when the HID controller rejects the command.

    `set_servo(self, channel: int, position: int) ‑> None`
    :   Move one servo to a position.
        
        Args:
            channel: Integer servo channel.
            position: Target position between 0 and 1000.
        
        Raises:
            ValueError: Raised when channel or position is outside the valid range.
            RuntimeError: Raised when the HID controller rejects the command.