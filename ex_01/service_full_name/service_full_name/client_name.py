import sys
import rclpy
from rclpy.node import Node
from ex09_interface.srv import FullNameSumService


class FullNameClient(Node):
    def __init__(self):
        super().__init__('client_name')
        self.client = self.create_client(FullNameSumService, 'SummFullName')

    def call_service(self, last_name, name, first_name, timeout_sec=5.0):
        if not self.client.wait_for_service(timeout_sec=timeout_sec):
            self.get_logger().error('Service "SummFullName" not available')
            return None

        req = FullNameSumService.Request()
        req.last_name = last_name
        req.name = name
        req.first_name = first_name

        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=timeout_sec)
        if future.done() and future.result() is not None:
            return future.result().full_name
        else:
            self.get_logger().error('Service call failed or timed out')
            return None


def main(args=None):
    rclpy.init(args=args)
    node = FullNameClient()

    if len(sys.argv) < 4:
        node.get_logger().info('Usage: ros2 run service_full_name client_name LAST_NAME NAME FIRST_NAME')
        rclpy.shutdown()
        return

    last_name = sys.argv[1]
    name = sys.argv[2]
    first_name = sys.argv[3]

    result = node.call_service(last_name, name, first_name)
    if result is not None:
        print(f"Full name: {result}")
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
