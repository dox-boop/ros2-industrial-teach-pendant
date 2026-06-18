import time

import rclpy
from rclpy.node import Node

from rclpy.action import ActionServer

from action_tutorials_interfaces.action import Fibonacci


class MoveActionServer(Node):

    def __init__(self):

        super().__init__('move_action_server')

        self._action_server = ActionServer(
            self,
            Fibonacci,
            'move_robot',
            self.execute_callback
        )

        self.get_logger().info(
            "Move Action Server Ready"
        )

    def execute_callback(self, goal_handle):

        self.get_logger().info(
            "Move Goal Received"
        )

        feedback_msg = Fibonacci.Feedback()

        sequence = [0, 1]

        for i in range(1, 11):

            time.sleep(1)

            feedback_msg.partial_sequence = sequence

            goal_handle.publish_feedback(
                feedback_msg
            )

            self.get_logger().info(
                f"Progress: {i * 10}%"
            )

            sequence.append(
                sequence[-1] + sequence[-2]
            )

        goal_handle.succeed()

        result = Fibonacci.Result()

        result.sequence = sequence

        return result


def main(args=None):

    rclpy.init(args=args)

    node = MoveActionServer()

    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == '__main__':
    main()
