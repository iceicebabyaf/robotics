import rclpy
from rclpy.node import Node
from ex09_interface.srv import FullNameSumService


class FullNameService(Node):
    def __init__(self):
        super().__init__('service_name')
        self.srv = self.create_service(FullNameSumService, 'SummFullName', self.handle_sum)
        self.get_logger().info('Service "SummFullName" is ready')

    def handle_sum(self, request, response):
        response.full_name = f"{request.last_name} {request.name} {request.first_name}"
        self.get_logger().info(f"Request: {request.last_name}, {request.name}, {request.first_name} -> {response.full_name}")
        return response


def main(args=None):
    rclpy.init(args=args)
    node = FullNameService()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
