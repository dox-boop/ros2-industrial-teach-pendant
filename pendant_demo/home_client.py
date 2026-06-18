import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class HomeClient(Node):

    def __init__(self):
        super().__init__('home_client')

        self.client = self.create_client(
            Trigger,
            '/home_robot'
        )

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                'Waiting for home service...'
            )

    def send_request(self):

        request = Trigger.Request()

        future = self.client.call_async(request)

        rclpy.spin_until_future_complete(
            self,
            future
        )

        return future.result()


def main(args=None):

    rclpy.init(args=args)

    node = HomeClient()

    response = node.send_request()

    node.get_logger().info(
        f"{response.message}"
    )

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
