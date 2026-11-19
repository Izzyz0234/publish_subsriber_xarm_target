from turtle import position

import rclpy, pygame, xarm, re
from rclpy.node import Node

from std_msgs.msg import String

arm = xarm.Controller('USB')

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('student_subscriber')
        self.subscription = self.create_subscription(
            String,
            'student_data',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        position = eval(msg.data)
        self.get_logger().info(msg.data)
        # result = re.sub(r'^\[|\]$', '', position)
        # self.get_logger().info(result)
        arm.setPosition(position)
        position2 = [[5, 300]]  # Replace 300 with a safe target for your arm
        arm.setPosition(position2)
        self.get_logger().info('I heard: "%s"' % position)


def main(args=None):

    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()