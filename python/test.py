import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

PUBLISHER_PATH = Path(__file__).with_name("I_Hess_student_id_publisher.py")

class FakeScreen:
    def blit(self, *_args):
        pass

    def get_at(self, _position):
        return (255, 255, 255)

    def get_width(self):
        return 800

    def get_height(self):
        return 600


class FakeText:
    def get_rect(self, **_kwargs):
        return object()


class FakeFont:
    def render(self, *_args):
        return FakeText()


class FakePublisher:
    def __init__(self):
        self.messages = []

    def publish(self, message):
        self.messages.append(message)


class FakeNode:
    def __init__(self, _name):
        self.publisher = FakePublisher()

    def create_publisher(self, *_args):
        return self.publisher

    def create_timer(self, *_args):
        return object()

    def get_logger(self):
        return SimpleNamespace(info=lambda *_args: None)


class PublisherMessageTests(unittest.TestCase):
    def publish_click(self, position):
        click = SimpleNamespace(type="mouse-down", pos=position)
        quit_event = SimpleNamespace(type="quit")
        event_batches = [[click, quit_event]]

        pygame = ModuleType("pygame")
        screen = FakeScreen()

        pygame.QUIT = "quit"
        pygame.MOUSEBUTTONDOWN = "mouse-down"

        pygame.init = lambda: None
        pygame.quit = lambda: None

        pygame.display = SimpleNamespace(set_mode=lambda _size: screen, set_caption=lambda *_args: None, flip=lambda: None)
        pygame.image = SimpleNamespace(load=lambda _path: SimpleNamespace(convert_alpha=lambda: SimpleNamespace(get_rect=lambda **_kwargs: object())))
        pygame.transform = SimpleNamespace(scale=lambda *_args: object())
        pygame.font = SimpleNamespace(Font=lambda *_args: FakeFont())
        pygame.event = SimpleNamespace(get=lambda: event_batches.pop(0))

        rclpy = ModuleType("rclpy")
        rclpy_node = ModuleType("rclpy.node")
        rclpy_node.Node = FakeNode
        std_msgs = ModuleType("std_msgs")
        std_msgs.__path__ = []
        std_msgs_msg = ModuleType("std_msgs.msg")
        std_msgs_msg.String = type("String", (), {"__init__": lambda self: setattr(self, "data", "")})
        xarm = ModuleType("xarm")

        fake_modules = {
            "pygame": pygame,
            "rclpy": rclpy,
            "rclpy.node": rclpy_node,
            "std_msgs": std_msgs,
            "std_msgs.msg": std_msgs_msg,
            "xarm": xarm
        }
        module_name = "publisher_under_test"
        
        with patch.dict(sys.modules, fake_modules):
            spec = importlib.util.spec_from_file_location(module_name, PUBLISHER_PATH)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module

            try:
                spec.loader.exec_module(module)
                publisher = module.MinimalPublisher()
                publisher.timer_callback()
                return [message.data for message in publisher.publisher_.messages]
            finally:
                sys.modules.pop(module_name, None)

    def test_top_left_click_publishes_maximum_position(self):
        self.assertEqual(self.publish_click((0, 0)), ["[[6, 1000], [4, 1000]]"])

    def test_bottom_right_click_publishes_zero_position(self):
        self.assertEqual(
            self.publish_click((799, 599)), ["[[6, 0], [4, 0]]"])

    def test_interior_click_publishes_scaled_position(self):
        self.assertEqual(self.publish_click((200, 150)), ["[[6, 750], [4, 750]]"])

if __name__ == "__main__":
    unittest.main()
