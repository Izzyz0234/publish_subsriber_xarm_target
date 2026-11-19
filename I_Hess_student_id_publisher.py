import rclpy, random, pygame, xarm
from rclpy.node import Node
from std_msgs.msg import String


pygame.init()                                  # start pygame's internals
screen = pygame.display.set_mode((800, 600))   # open an 800 × 600 window

pygame.display.set_caption("Click a target")

# Load and display the image
image = pygame.image.load("archery_target2.png").convert_alpha()
scaled_image = pygame.transform.scale(image, (600, 600))
image_rect = image.get_rect(center=(320, 220))  # get the rectangle of the image and center it
screen.blit(scaled_image, image_rect)

pygame.display.flip()                           # make the changes visible

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
        xarmMsg = String()

        running = True
        while running:
            for event in pygame.event.get():           # poll the event queue
                if event.type == pygame.QUIT:          # user closed the window
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("clicked at", event.pos)     # ← this is your (x, y)
                    positionX = event.pos[0]
                    positionY = event.pos[1]
                    xarmMsg.data = f'[[6, {positionX}], [4, {positionY}]]'

                    
                    self.publisher_.publish(xarmMsg)
                    self.get_logger().info('Publishing to Xarm: "%s"' % xarmMsg.data)
            
        pygame.quit()


        # msg = String()
        # msg2 = String()
        # msg3 = String()
        # msg.data = 'STUD_9369:%d' % random_number
        # msg2.data = 'Message Count:%d' % self.message_count 
        # msg3.data = 'Average Number:%d' % self.average_number
        # self.publisher_.publish(msg)
        # self.publisher_.publish(msg2)
        # self.publisher_.publish(msg3)
        # self.get_logger().info('1 Publishing: "%s"' % msg.data)
        # self.get_logger().info('2 Publishing: "%s"' % msg2.data)
        # self.get_logger().info('3 Publishing: "%s"' % msg3.data)
        
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
