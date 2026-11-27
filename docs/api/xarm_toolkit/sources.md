Module xarm_toolkit.sources
===========================
Interchangeable target sources for Pygame and PAL Robotics ARI.

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