import rclpy, random
from rclpy.node import Node

from std_msgs.msg import String



class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('student_publisher')
        self.publisher_ = self.create_publisher(String, 'student_data', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.message_count = 0
        self.average_number = 0
        self.numbers = []

    def timer_callback(self):
        random_number = random.randint(1, 1000)
        self.numbers += [random_number]
        self.average_number = sum(self.numbers) / len(self.numbers)

        msg = String()
        msg2 = String()
        msg3 = String()
        msg.data = 'STUD_9369:%d' % random_number
        msg2.data = 'Message Count:%d' % self.message_count 
        msg3.data = 'Average Number:%d' % self.average_number
        self.publisher_.publish(msg)
        self.publisher_.publish(msg2)
        self.publisher_.publish(msg3)
        self.get_logger().info('1 Publishing: "%s"' % msg.data)
        self.get_logger().info('2 Publishing: "%s"' % msg2.data)
        self.get_logger().info('3 Publishing: "%s"' % msg3.data)
        
        self.message_count += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
