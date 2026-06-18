import rclpy

from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import JointState


class JointStateController(Node):

    def __init__(self):

        super().__init__('joint_state_controller')

        # Current joint positions

        self.joint1 = 0.0
        self.joint2 = 0.0
        self.joint3 = 0.0

        # Target joint positions

        self.target_j1 = self.joint1
        self.target_j2 = self.joint2
        self.target_j3 = self.joint3

        self.motion_active = False

        # Publish joint states

        self.publisher = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        # Publish joint values for GUI

        self.status_publisher = self.create_publisher(
            String,
            '/robot_joints',
            10
        )

        self.reached_publisher = self.create_publisher(
            String,
            '/target_reached',
            10
        )

        self.motion_status_publisher = self.create_publisher(
            String,
            '/motion_status',
            10
        )

        # Jog commands

        self.subscription = self.create_subscription(
            String,
            '/jog_command',
            self.command_callback,
            10
        )

        # Go-to-point commands

        self.goto_subscription = self.create_subscription(
            String,
            '/goto_point',
            self.goto_callback,
            10
        )

        # Publish timer

        self.timer = self.create_timer(
            0.1,
            self.publish_joint_state
        )

        self.get_logger().info(
            "Joint State Controller Ready"
        )

    def command_callback(self, msg):

        command = msg.data

        if command == "j1+":

            self.joint1 += 0.1
            self.target_j1 = self.joint1

        elif command == "j1-":

            self.joint1 -= 0.1
            self.target_j1 = self.joint1

        elif command == "j2+":

            self.joint2 += 0.1
            self.target_j2 = self.joint2

        elif command == "j2-":

            self.joint2 -= 0.1
            self.target_j2 = self.joint2

        elif command == "j3+":

            self.joint3 += 0.1
            self.target_j3 = self.joint3

        elif command == "j3-":

            self.joint3 -= 0.1
            self.target_j3 = self.joint3
            
        elif command == "home":

            self.target_j1 = 0.0
            self.target_j2 = 0.0
            self.target_j3 = 0.0

            self.motion_active = True

            self.get_logger().info(
                "Going Home"
            )

        elif command == "stop":

            self.target_j1 = self.joint1
            self.target_j2 = self.joint2
            self.target_j3 = self.joint3

            self.motion_active = False

            self.get_logger().info(
                "Motion Stopped"
            )

    def goto_callback(self, msg):

        values = msg.data.split(',')

        self.target_j1 = float(values[0])
        self.target_j2 = float(values[1])
        self.target_j3 = float(values[2])

        self.motion_active = True

        self.get_logger().info(
            f"Going to point: {values}"
        )

        self.get_logger().info(
            f"NEW TARGET: {values}"
        )
    def move_towards_target(self):

        step = 0.02

        # Joint 1

        if abs(self.target_j1 - self.joint1) > step:

            if self.joint1 < self.target_j1:
                self.joint1 += step
            else:
                self.joint1 -= step

        else:

            self.joint1 = self.target_j1

        # Joint 2

        if abs(self.target_j2 - self.joint2) > step:

            if self.joint2 < self.target_j2:
                self.joint2 += step
            else:
                self.joint2 -= step

        else:

            self.joint2 = self.target_j2

        # Joint 3

        if abs(self.target_j3 - self.joint3) > step:

            if self.joint3 < self.target_j3:
                self.joint3 += step
            else:
                self.joint3 -= step

        else:

            self.joint3 = self.target_j3

        if (
            self.motion_active and
            abs(self.target_j1 - self.joint1) < 0.01 and
            abs(self.target_j2 - self.joint2) < 0.01 and
            abs(self.target_j3 - self.joint3) < 0.01
        ):

            msg = String()
            msg.data = "REACHED"

            self.reached_publisher.publish(
                msg
            )

            self.motion_active = False

            self.get_logger().info(
                "Target Reached"
            )

    def publish_joint_state(self):

        self.move_towards_target()

        msg = JointState()

        msg.header.stamp = (
            self.get_clock().now().to_msg()
        )

        msg.name = [
            'joint1',
            'joint2',
            'joint3'
        ]

        msg.position = [
            self.joint1,
            self.joint2,
            self.joint3
        ]

        self.publisher.publish(msg)

        status_msg = String()

        status_msg.data = (
            f"{self.joint1:.2f},"
            f"{self.joint2:.2f},"
            f"{self.joint3:.2f}"
        )

        self.status_publisher.publish(
            status_msg
        )

        motion_msg = String()

        if (
            abs(self.joint1 - self.target_j1) < 0.01 and
            abs(self.joint2 - self.target_j2) < 0.01 and
            abs(self.joint3 - self.target_j3) < 0.01
        ):

            motion_msg.data = "IDLE"

        else:

            motion_msg.data = "MOVING"

        self.motion_status_publisher.publish(
            motion_msg
        )


def main(args=None):

    rclpy.init(args=args)

    node = JointStateController()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':

    main()
