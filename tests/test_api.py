"""Hardware-free tests for the xarm_toolkit public API."""

from types import SimpleNamespace

import pytest

from xarm_toolkit import ArmController, ARIPersonTracker, PygameTargetSource


class FakeController:
    def __init__(self):
        self.commands = []

    def setPosition(self, positions):
        self.commands.append(positions)


class FakePygame:
    QUIT = "quit"
    MOUSEBUTTONDOWN = "mouse"

    def __init__(self):
        self.events = []

    def init(self):
        pass

    def quit(self):
        pass

    class event:
        pass


def test_arm_controller_moves_with_injected_controller():
    controller = FakeController()
    arm = ArmController(controller=controller)

    arm.move_to([[6, 500], [4, 250]])

    assert controller.commands == [[[6, 500], [4, 250]]]


def test_arm_controller_rejects_invalid_position():
    arm = ArmController(controller=FakeController())

    with pytest.raises(ValueError):
        arm.move_to([[6, 1001]])


def test_pygame_source_returns_normalized_click():
    pygame = FakePygame()
    pygame.event = SimpleNamespace(
        get=lambda: [SimpleNamespace(type=pygame.MOUSEBUTTONDOWN, pos=(200, 150))]
    )
    source = PygameTargetSource(pygame, width=800, height=600)

    target = source.get_target()

    assert target == (750.0, 750.0)
    source.close()


def test_ari_stub_and_pygame_share_target_contract():
    pygame = FakePygame()
    pygame.event = SimpleNamespace(
        get=lambda: [SimpleNamespace(type=pygame.MOUSEBUTTONDOWN, pos=(400, 300))]
    )
    mock_source = PygameTargetSource(pygame, width=800, height=600)
    ari_source = ARIPersonTracker(lambda: SimpleNamespace(target_x=499.0, target_y=499.0))

    assert mock_source.get_target() == (499.0, 499.0)
    assert ari_source.get_target() == (499.0, 499.0)

