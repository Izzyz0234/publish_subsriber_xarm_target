Module xarm_toolkit
===================
Public API for the xarm_toolkit package.

Sub-modules
-----------
* xarm_toolkit.arm
* xarm_toolkit.sources

Classes
-------

`ARIPersonTracker(message_source: Callable[[], typing.Any])`
:   Adapt mocked ARI ROS messages to the TargetSource contract.
    
    Initialize an ARI tracking adapter.
    
    Args:
        message_source: Callable that returns the next tracking message or None.
    
    Raises:
        ValueError: Raised when ``message_source`` is not callable.

    ### Ancestors (in MRO)

    * xarm_toolkit.sources.TargetSource
    * abc.ABC

    ### Methods

    `close(self) ‑> None`
    :   Close the ARI adapter.
        
        The adapter owns no external resources because message polling is injected.

    `get_target(self) ‑> tuple[float, float] | None`
    :   Read one ARI message and return its normalized person position.
        
        Returns:
            The first person's ``(x, y)`` center in 0--1000, or None without a target.
        
        Raises:
            RuntimeError: Raised when message fields cannot be reconciled.

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

`PygameTargetSource(pygame_module: typing.Any | None = None, width: int = 800, height: int = 600)`
:   Generate normalized targets from Pygame mouse clicks.
    
    Initialize the Pygame mock source.
    
    Args:
        pygame_module: Pygame module or compatible test double.
        width: Pygame window width in pixels.
        height: Pygame window height in pixels.
    
    Raises:
        ValueError: Raised when width or height is zero or negative.

    ### Ancestors (in MRO)

    * xarm_toolkit.sources.TargetSource
    * abc.ABC

    ### Methods

    `close(self) ‑> None`
    :   Quit Pygame and release its display resources.

    `get_target(self) ‑> tuple[float, float] | None`
    :   Poll Pygame and return the next mouse click as normalized coordinates.
        
        Returns:
            An ``(x, y)`` tuple from 0--1000, or None when no click is queued.
        
        Raises:
            RuntimeError: Raised when Pygame event processing fails.

`TargetSource()`
:   Provide normalized two-dimensional targets to downstream code.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * xarm_toolkit.sources.ARIPersonTracker
    * xarm_toolkit.sources.PygameTargetSource

    ### Methods

    `close(self) ‑> None`
    :   Release resources held by the target source.

    `get_target(self) ‑> tuple[float, float] | None`
    :   Get the next target.
        
        Returns:
            An ``(x, y)`` tuple in the 0--1000 contract, or None when unavailable.
        
        Raises:
            RuntimeError: Raised when the source cannot provide source data.