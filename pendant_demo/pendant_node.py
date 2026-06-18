import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PendantNode(Node):

    def __init__(self):
        super().__init__('pendant_node')

        self.publisher = self.create_publisher(
            String,
            '/jog_command',
            10
        )

    def send_command(self, command):

        msg = String()
        msg.data = command

        self.publisher.publish(msg)

        self.get_logger().info(
            f"Sent: {msg.data}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = PendantNode()

    try:
        while rclpy.ok():

            command = input(
                "\nEnter command (j1+, j1-, home, stop): "
            )

            node.send_command(command)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
