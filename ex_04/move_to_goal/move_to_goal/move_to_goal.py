import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class MoveToGoalNode(Node):
    def __init__(self):
        super().__init__('move_to_goal')
        
        # Declare parameters
        self.declare_parameter('x', 0.0)
        self.declare_parameter('y', 0.0)
        self.declare_parameter('theta', 0.0)
        
        # Get parameters
        self.goal_x = self.get_parameter('x').get_parameter_value().double_value
        self.goal_y = self.get_parameter('y').get_parameter_value().double_value
        self.goal_theta = self.get_parameter('theta').get_parameter_value().double_value
        
        # Initialize pose
        self.current_pose = Pose()
        self.at_position = False  # Flag to track if position is reached
        
        # Create publisher and subscriber
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscriber = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
        # Control parameters
        self.linear_speed = 1.5
        self.angular_speed = 1.0
        self.linear_tolerance = 0.1  # Distance tolerance (meters)
        self.angular_tolerance = 0.01  # Angle tolerance (radians)
        
        self.get_logger().info(f'Moving to goal: x={self.goal_x}, y={self.goal_y}, theta={self.goal_theta}')

    def pose_callback(self, msg):
        self.current_pose = msg
        
        # Create velocity command
        cmd = Twist()
        
        if not self.at_position:
            # Calculate distance to goal
            distance = math.sqrt((self.goal_x - self.current_pose.x) ** 2 + 
                               (self.goal_y - self.current_pose.y) ** 2)
            
            # Calculate angle to goal
            angle_to_goal = math.atan2(self.goal_y - self.current_pose.y, 
                                     self.goal_x - self.current_pose.x)
            angle_diff = self.normalize_angle(angle_to_goal - self.current_pose.theta)
            
            # Move to position
            if distance > self.linear_tolerance:
                # Turn towards goal
                if abs(angle_diff) > self.angular_tolerance:
                    cmd.angular.z = self.angular_speed * min(1.0, abs(angle_diff)) * (1 if angle_diff > 0 else -1)
                else:
                    cmd.linear.x = self.linear_speed * min(1.0, distance)
            else:
                self.at_position = True
                self.get_logger().info('Position reached, adjusting orientation')
        else:
            # Adjust orientation
            angle_diff = self.normalize_angle(self.goal_theta - self.current_pose.theta)
            if abs(angle_diff) > self.angular_tolerance:
                cmd.angular.z = self.angular_speed * min(1.0, abs(angle_diff)) * (1 if angle_diff > 0 else -1)
            else:
                self.get_logger().info('Goal reached!')
                rclpy.shutdown()
                return
        
        self.publisher.publish(cmd)

    def normalize_angle(self, angle):
        """Normalize angle to [-pi, pi]"""
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle

def main(args=None):
    rclpy.init(args=args)
    node = MoveToGoalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()