import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class TextToCmdVel(Node):
    def __init__(self):
        super().__init__('text_to_cmd_vel')
        self.subscription = self.create_subscription(String, 'cmd_text', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.linear_speed = 1.0    # м/с
        self.angular_speed = 1.5   # рад/с
        self.get_logger().info('text_to_cmd_vel node started, listening on "cmd_text"')

    def listener_callback(self, msg: String):
        cmd = msg.data.strip()
        twist = Twist()

        if cmd == "move_forward":
            twist.linear.x = self.linear_speed
            twist.angular.z = 0.0
        elif cmd == "move_backward":
            twist.linear.x = -self.linear_speed
            twist.angular.z = 0.0
        elif cmd == "turn_left":
            twist.linear.x = 0.0
            twist.angular.z = self.angular_speed
        elif cmd == "turn_right":
            twist.linear.x = 0.0
            twist.angular.z = -self.angular_speed
        else:
            self.get_logger().warn(f'Unknown command received: "{cmd}"')
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        self.publisher_.publish(twist)
        self.get_logger().info(f'Published Twist for command "{cmd}": linear.x={twist.linear.x}, angular.z={twist.angular.z}')

def main(args=None):
    rclpy.init(args=args)
    node = TextToCmdVel()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
