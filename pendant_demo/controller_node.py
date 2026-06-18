import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Trigger


class ControllerNode(Node):

    def __init__(self):
        super().__init__('controller_node')

        self.robot_status = "READY"

        # Jog Command Subscriber
        self.subscription = self.create_subscription(
            String,
            '/jog_command',
            self.command_callback,
            10
        )

        # Home Service
        self.home_service = self.create_service(
            Trigger,
            '/home_robot',
            self.home_callback
        )

        # Status Publisher
        self.status_publisher = self.create_publisher(
            String,
            '/robot_status',
            10
        )

        self.status_timer = self.create_timer(
            2.0,
            self.publish_status
        )

        self.get_logger().info(
            "🤖 Robot Controller Ready. Waiting for commands or services..."
        )

    def command_callback(self, msg):

        command = msg.data.strip().lower()

        if command == 'j1+':

            self.robot_status = "MOVING"

            self.get_logger().info(
                "⚙️ Moving Joint 1 Positive"
            )

        elif command == 'j1-':

            self.robot_status = "MOVING"

            self.get_logger().info(
                "⚙️ Moving Joint 1 Negative"
            )

        elif command == 'stop':

            self.robot_status = "STOPPED"

            self.get_logger().warn(
                "🛑 Robot Stopped"
            )

        else:

            self.get_logger().info(
                f"❓ Unknown command received: {command}"
            )

    def home_callback(self, request, response):

        self.robot_status = "HOMING"

        self.get_logger().info(
            "🏠 Homing sequence initiated..."
        )

        # Simulated homing process
        self.robot_status = "READY"

        self.get_logger().info(
            "✅ Homing complete!"
        )

        response.success = True
        response.message = "Robot successfully homed."

        return response

    def publish_status(self):

        msg = String()
        msg.data = self.robot_status

        self.status_publisher.publish(msg)

    def destroy_node(self):

        self.get_logger().info(
            "Shutting down controller..."
        )

        super().destroy_node()


def main(args=None):

    rclpy.init(args=args)

    node = ControllerNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
