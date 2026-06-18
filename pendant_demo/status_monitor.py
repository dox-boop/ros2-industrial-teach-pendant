import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class StatusMonitor(Node):

    def __init__(self):

        super().__init__('status_monitor')

        self.subscription = self.create_subscription(
            String,
            '/robot_status',
            self.status_callback,
            10
        )

    def status_callback(self, msg):

        self.get_logger().info(
            f"Robot Status: {msg.data}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = StatusMonitor()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
