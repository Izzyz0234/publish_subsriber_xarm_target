import rclpy, random, pygame, xarm
from rclpy.node import Node
from std_msgs.msg import String

global score_counter
score_counter = 0


pygame.init()                                  # start pygame's internals
screen = pygame.display.set_mode((800, 600))   # open an 800 × 600 window

pygame.display.set_caption("Click a target")

# Load and display the image
image = pygame.image.load("archery_target2.png").convert_alpha()
scaled_image = pygame.transform.scale(image, (600, 600))
image_rect = image.get_rect(center=(320, 220))  # get the rectangle of the image and center it
screen.blit(scaled_image, image_rect)

# Load and display the text
font = pygame.font.Font(None, 48)
text_surface = font.render(f"Score: {score_counter}", True, (0, 0, 0))
text_rect = text_surface.get_rect(center=(180, 30))
screen.blit(text_surface, text_rect)


def check_pixel_color(x, y):
    global score_counter
    # Get the color of the pixel at (x, y)
    pixel_color = screen.get_at((x, y))
    
    # Define the target color (red in this case)
    white = (255, 255, 255, 255)
    black = (0, 0, 0, 255)
    blue = (104, 191, 233, 255)
    red = (222, 18, 6, 255)
    yellow = (255, 221, 0, 225)

    
    # Check if the pixel color matches the target color
    if pixel_color == white:
        score_counter += 2
    elif pixel_color == black:
        score_counter += 4
    elif pixel_color == blue:
        score_counter += 6
    elif pixel_color == red:
        score_counter += 8
    elif pixel_color == yellow:
        score_counter += 10

    # 3. Clear the screen so old text doesn't stay behind
    screen.blit(scaled_image, image_rect)
    text_surface = font.render(f"Score: {score_counter}", True, (0, 0, 0))


    # 4. Blit the current text surface and update the display
    text_rect = text_surface.get_rect(center=(180, 30))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()



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

                    check_pixel_color(positionX, positionY)                    
                    
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
