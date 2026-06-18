import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from action_tutorials_interfaces.action import Fibonacci
from std_msgs.msg import String
from std_srvs.srv import Trigger


class TeachPendant(Node):

    def __init__(self):

        super().__init__('teach_pendant')

        self.robot_status = "UNKNOWN"

        # Jog Command Publisher
        self.publisher = self.create_publisher(
            String,
            '/jog_command',
            10
        )

        # Robot Status Subscriber
        self.status_subscription = self.create_subscription(
            String,
            '/robot_status',
            self.status_callback,
            10
        )

        # Home Robot Service Client
        self.home_client = self.create_client(
            Trigger,
            '/home_robot'
        )

        while not self.home_client.wait_for_service(
            timeout_sec=1.0
        ):
            self.get_logger().info(
                'Waiting for /home_robot service...'
            )

        # Action Client
        self.move_client = ActionClient(
            self,
            Fibonacci,
            'move_robot'
        )

    def status_callback(self, msg):

        self.robot_status = msg.data

    def send_jog(self, command):

        msg = String()
        msg.data = command

        self.publisher.publish(msg)

    def home_robot(self):

        request = Trigger.Request()

        future = self.home_client.call_async(
            request
        )

        rclpy.spin_until_future_complete(
            self,
            future
        )

        response = future.result()

        print("\nResponse:")
        print(response.message)

    def feedback_callback(self, feedback_msg):

        feedback = feedback_msg.feedback

        progress = len(feedback.partial_sequence) * 10

        if progress > 100:
            progress = 100

        print(f"Progress: {progress}%")

    def move_robot(self):

        self.get_logger().info(
            "Sending move goal..."
        )

        goal_msg = Fibonacci.Goal()

        goal_msg.order = 10

        self.move_client.wait_for_server()

        send_goal_future = self.move_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        rclpy.spin_until_future_complete(
            self,
            send_goal_future
        )

        goal_handle = send_goal_future.result()

        if not goal_handle.accepted:

            print("Goal Rejected")
            return

        print("Goal Accepted")

        result_future = goal_handle.get_result_async()

        rclpy.spin_until_future_complete(
            self,
            result_future
        )

        result = result_future.result().result

        print("\nMotion Complete")
        print("Result Sequence:")
        print(result.sequence)


def main(args=None):

    rclpy.init(args=args)

    pendant = TeachPendant()

    try:

        while True:

            rclpy.spin_once(
                pendant,
                timeout_sec=0.1
            )

            print("\n====================")
            print("   Teach Pendant")
            print("====================")
            print(f"Robot Status: {pendant.robot_status}")
            print("====================")
            print("1. Home Robot")
            print("2. Move J1+")
            print("3. Move J1-")
            print("4. Stop Robot")
            print("5. Move Robot (Action)")
            print("6. Exit")

            choice = input("\nSelect: ")

            if choice == "1":

                pendant.home_robot()

            elif choice == "2":

                pendant.send_jog("j1+")

            elif choice == "3":

                pendant.send_jog("j1-")

            elif choice == "4":

                pendant.send_jog("stop")

            elif choice == "5":

                pendant.move_robot()

            elif choice == "6":

                break

            else:

                print("Invalid selection")

    except KeyboardInterrupt:
        pass

    pendant.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
