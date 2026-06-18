import sys
import rclpy
import json

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QComboBox,
    QListWidget
)

from PyQt6.QtCore import QTimer

from rclpy.node import Node

from std_msgs.msg import String
from std_srvs.srv import Trigger



class PendantROS(Node):

    def __init__(self):

        super().__init__('gui_pendant')

        self.robot_status = "UNKNOWN"
        self.motion_status = "IDLE"

        self.publisher = self.create_publisher(
            String,
            '/jog_command',
            10
        )

        self.status_subscriber = self.create_subscription(
            String,
            '/motion_status',
            self.status_callback,
            10
        )

        self.home_client = self.create_client(
            Trigger,
            '/home_robot'
        )
        
        self.joint_positions = [
            0.0,
            0.0,
            0.0
        ]
        
        self.saved_points = {
            f"P{i}": None
            for i in range(1, 11)
        }

        self.program = []
        
        self.joint_subscription = self.create_subscription(
            String,
            '/robot_joints',
            self.joint_callback,
            10
        )
        
        self.goto_publisher = self.create_publisher(
            String,
            '/goto_point',
            10
        )

        self.motion_subscriber = self.create_subscription(
            String,
            '/motion_status',
            self.motion_callback,
            10
        )

        self.target_reached = False

        self.reached_subscriber = self.create_subscription(
            String,
            '/target_reached',
            self.reached_callback,
            10
        )
        

    def status_callback(self, msg):

        self.robot_status = msg.data

    def send_jog(self, command):

        msg = String()
        msg.data = command

        self.publisher.publish(msg)

    def home_robot(self):

        if not self.home_client.wait_for_service(
            timeout_sec=1.0
        ):
            print("Home service unavailable")
            return

        request = Trigger.Request()

        future = self.home_client.call_async(
            request
        )

        rclpy.spin_until_future_complete(
            self,
            future
        )

        response = future.result()

        if response is not None:

            print("Response:")
            print(response.message)

        else:

            print("Service call failed")
        
    def joint_callback(self, msg):

        print(
            "CALLBACK ID:",
            id(self)
        )

        print("JOINT MSG:", msg.data)

        values = msg.data.split(',')

        self.joint_positions = [
            float(values[0]),
            float(values[1]),
            float(values[2])
        ]
        
    def save_point(self, point_name):

        self.saved_points[point_name] = (
            self.joint_positions.copy()
        )

        print(
            f"{point_name} Saved:"
        )

        print(
            self.saved_points[point_name]
        )


    def goto_point(self, point_name):

        point = self.saved_points.get(
            point_name
        )

        if point is None:

            print(
                f"{point_name} not saved yet"
            )

            return

        msg = String()

        msg.data = (
            f"{point[0]},"
            f"{point[1]},"
            f"{point[2]}"
        )

        self.goto_publisher.publish(
            msg
        )

        print(
            f"Going to {point_name}"
        )
        
    def run_program(self):

        if self.saved_points["P1"] is None:

            print("P1 not saved")

            return

        if self.saved_points["P2"] is None:

            print("P2 not saved")

            return

        import time

        print("Running Program")

        self.goto_point("P1")

        time.sleep(3)

        self.goto_point("P2")

        time.sleep(3)

        self.goto_point("P1")

        time.sleep(3)

        self.goto_point("P2")

        print("Program Complete")
            
    def save_program(self):

        data = {}

        for key, value in self.saved_points.items():

            data[key] = value

        with open(
            "program.json",
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        print(
            "Program Saved"
        )


    def load_program(self):

        try:

            with open(
                "program.json",
                "r"
            ) as file:

                self.saved_points = json.load(
                    file
                )

                for key, value in self.saved_points.items():

                    if value is not None:

                        self.saved_points[key] = [
                            float(value[0]),
                            float(value[1]),
                            float(value[2])
                        ]

            print(
                "Program Loaded"
            )

            print(
                self.saved_points
            )

        except FileNotFoundError:

            print(
                "No saved program found"
            )

    def execute_program(self):

        if len(self.program) == 0:

            print(
                "Program Empty"
            )

            return

        print(
            "Executing Program"
        )

        for point_name in self.program:

            if self.saved_points.get(
                point_name
            ) is None:

                print(
                    f"{point_name} not saved"
                )

                continue

            print(
                f"Moving to {point_name}"
            )

            self.target_reached = False

            self.goto_point(
                point_name
            )

            while not self.target_reached:

                rclpy.spin_once(
                    self,
                    timeout_sec=0.1
                )

            print(
                f"{point_name} reached"
            )

        print(
            "Program Complete"
        )
            
    def motion_callback(self, msg):

        print("MOTION:", msg.data)

        self.motion_status = msg.data

    def reached_callback(self, msg):

        self.target_reached = True

class PendantWindow(QWidget):

    def __init__(self, ros_node):

        super().__init__()

        self.ros_node = ros_node

        self.setWindowTitle(
            "STM32 Teach Pendant"
        )

        self.resize(800,480)

        layout = QVBoxLayout()
        
        status_group = QGroupBox(
            "STATUS"
        )

        jog_group = QGroupBox(
            "JOG CONTROL"
        )

        points_group = QGroupBox(
            "TEACH POINTS"
        )

        program_group = QGroupBox(
            "PROGRAM"
        )

        self.status_label = QLabel(
            "Status: UNKNOWN"
        )
        
        self.j1_label = QLabel(
            "J1: 0.00"
        )

        self.j2_label = QLabel(
            "J2: 0.00"
        )

        self.j3_label = QLabel(
            "J3: 0.00"
        )
        
        self.status_label.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        self.j1_label.setStyleSheet(
            "font-size: 20px;"
        )

        self.j2_label.setStyleSheet(
            "font-size: 20px;"
        )

        self.j3_label.setStyleSheet(
            "font-size: 20px;"
        )

        self.home_button = QPushButton(
            "HOME"
        )

        self.j1_plus_button = QPushButton(
            "J1+"
        )

        self.j1_minus_button = QPushButton(
            "J1-"
        )

        self.j2_plus_button = QPushButton(
            "J2+"
        )

        self.j2_minus_button = QPushButton(
            "J2-"
        )

        self.j3_plus_button = QPushButton(
            "J3+"
        )

        self.j3_minus_button = QPushButton(
            "J3-"
        )

        self.stop_button = QPushButton(
            "STOP"
        )
        
        self.run_program_button = QPushButton(
            "RUN PROGRAM"
        )
        
        self.save_program_button = QPushButton(
            "SAVE PROGRAM"
        )

        self.load_program_button = QPushButton(
            "LOAD PROGRAM"
        )
        
        self.point_selector = QComboBox()

        self.refresh_point_selector()
        
        self.save_point_button = QPushButton(
            "SAVE POINT"
        )

        self.goto_point_button = QPushButton(
            "GO TO POINT"
        )

        self.program_list = QListWidget()

        self.add_point_button = QPushButton(
            "ADD TO PROGRAM"
        )

        self.clear_program_button = QPushButton(
            "CLEAR PROGRAM"
        )

        self.delete_step_button = QPushButton(
            "DELETE STEP"
        )

        self.move_up_button = QPushButton(
            "MOVE UP"
        )

        self.move_down_button = QPushButton(
            "MOVE DOWN"
        )

        for button in [
            self.home_button,
            self.stop_button,
            self.run_program_button,
            self.save_program_button,
            self.load_program_button,
            self.j1_plus_button,
            self.j1_minus_button,
            self.j2_plus_button,
            self.j2_minus_button,
            self.j3_plus_button,
            self.j3_minus_button,
        ]:

            button.setMinimumHeight(50)

        layout.addWidget(
            self.status_label
        )
        
        layout.addWidget(
            self.j1_label
        )

        layout.addWidget(
            self.j2_label
        )

        layout.addWidget(
            self.j3_label
        )

        layout.addWidget(
            self.home_button
        )
        
        layout.addWidget(
            self.point_selector
        )

        layout.addWidget(
            self.save_point_button
        )

        layout.addWidget(
            self.goto_point_button
        )

        layout.addWidget(
            self.program_list
        )

        layout.addWidget(
            self.add_point_button
        )

        layout.addWidget(
            self.clear_program_button
        )

        layout.addWidget(
            self.delete_step_button
        )

        layout.addWidget(
            self.move_up_button
        )

        layout.addWidget(
            self.move_down_button
        )

        # J1 Row

        j1_layout = QHBoxLayout()

        j1_layout.addWidget(
            self.j1_plus_button
        )

        j1_layout.addWidget(
            self.j1_minus_button
        )

        layout.addLayout(
            j1_layout
        )

        # J2 Row

        j2_layout = QHBoxLayout()

        j2_layout.addWidget(
            self.j2_plus_button
        )

        j2_layout.addWidget(
            self.j2_minus_button
        )

        layout.addLayout(
            j2_layout
        )

        # J3 Row

        j3_layout = QHBoxLayout()

        j3_layout.addWidget(
            self.j3_plus_button
        )

        j3_layout.addWidget(
            self.j3_minus_button
        )

        layout.addLayout(
            j3_layout
        )

        layout.addWidget(
            self.stop_button
        )
        
        layout.addWidget(
            self.run_program_button
        )
        layout.addWidget(
            self.save_program_button
        )
        layout.addWidget(
            self.load_program_button
        )
        self.save_program_button.clicked.connect(
            self.save_program_pressed
        )

        self.load_program_button.clicked.connect(
            self.load_program_pressed
        )

        self.setLayout(layout)

        self.home_button.clicked.connect(
            self.home_pressed
        )

        self.j1_plus_button.clicked.connect(
            lambda: self.ros_node.send_jog("j1+")
        )

        self.j1_minus_button.clicked.connect(
            lambda: self.ros_node.send_jog("j1-")
        )

        self.j2_plus_button.clicked.connect(
            lambda: self.ros_node.send_jog("j2+")
        )

        self.j2_minus_button.clicked.connect(
            lambda: self.ros_node.send_jog("j2-")
        )

        self.j3_plus_button.clicked.connect(
            lambda: self.ros_node.send_jog("j3+")
        )

        self.j3_minus_button.clicked.connect(
            lambda: self.ros_node.send_jog("j3-")
        )

        self.stop_button.clicked.connect(
            lambda: self.ros_node.send_jog("stop")
        )
        
        self.run_program_button.clicked.connect(
            self.run_program_pressed
        )
        
        self.save_point_button.clicked.connect(
            self.save_selected_point
        )

        self.goto_point_button.clicked.connect(
            self.goto_selected_point
        )

        self.add_point_button.clicked.connect(
            self.add_point_to_program
        )

        self.clear_program_button.clicked.connect(
            self.clear_program
        )

        self.delete_step_button.clicked.connect(
            self.delete_program_step
        )

        self.move_up_button.clicked.connect(
            self.move_step_up
        )

        self.move_down_button.clicked.connect(
            self.move_step_down
        )

    def home_pressed(self):

        self.ros_node.send_jog("home")

    def move_pressed(self):

        self.ros_node.run_program()
        
    def save_selected_point(self):

        point_name = (
            self.point_selector.currentText()
            .split()[0]
        )

        self.ros_node.save_point(
            point_name
        )

        self.refresh_point_selector()


    def goto_selected_point(self):

        point = (
            self.point_selector.currentText()
            .split()[0]
        )

        self.ros_node.goto_point(
            point
        )

    def run_program_pressed(self):

        self.ros_node.execute_program()
    # def update_status(self):

    #     print(
    #         self.ros_node.motion_status,
    #         self.ros_node.joint_positions
    #     )

    #     self.status_label.setText(
    #         f"Status: {self.ros_node.motion_status}"
    #     )

    #     self.j1_label.setText(
    #         f"J1: {self.ros_node.joint_positions[0]:.2f}"
    #     )

    #     self.j2_label.setText(
    #         f"J2: {self.ros_node.joint_positions[1]:.2f}"
    #     )

    #     self.j3_label.setText(
    #         f"J3: {self.ros_node.joint_positions[2]:.2f}"
    #     )
    
    def update_status(self):

        self.status_label.setText(
            self.ros_node.motion_status
        )

        self.j1_label.setText(
            str(self.ros_node.joint_positions[0])
        )

        self.j2_label.setText(
            str(self.ros_node.joint_positions[1])
        )

        self.j3_label.setText(
            str(self.ros_node.joint_positions[2])
        )

    def save_program_pressed(self):

        self.ros_node.save_program()

    def load_program_pressed(self):

        self.ros_node.load_program()

        self.refresh_point_selector()

    def add_point_to_program(self):

        point = (
            self.point_selector.currentText()
            .split()[0]
        )

        self.ros_node.program.append(
            point
        )

        self.refresh_program_list()

    def clear_program(self):

        self.program_list.clear()

        self.ros_node.program.clear()

    def delete_program_step(self):

        row = (
            self.program_list.currentRow()
        )

        if row >= 0:

            self.program_list.takeItem(
                row
            )

            self.ros_node.program.pop(
                row
            )

    def move_step_up(self):

        row = self.program_list.currentRow()

        if row <= 0:

            return

        self.ros_node.program[row], \
        self.ros_node.program[row - 1] = \
        self.ros_node.program[row - 1], \
        self.ros_node.program[row]

        self.refresh_program_list()

        self.program_list.setCurrentRow(
            row - 1
        )

    def move_step_down(self):

        row = self.program_list.currentRow()

        if (
            row < 0 or
            row >= len(
                self.ros_node.program
            ) - 1
        ):

            return

        self.ros_node.program[row], \
        self.ros_node.program[row + 1] = \
        self.ros_node.program[row + 1], \
        self.ros_node.program[row]

        self.refresh_program_list()

        self.program_list.setCurrentRow(
            row + 1
        )
    
    def refresh_program_list(self):

        self.program_list.clear()

        for index, point in enumerate(
            self.ros_node.program,
            start=1
        ):

            self.program_list.addItem(
                f"{index}. {point}"
            )

    def refresh_point_selector(self):

        self.point_selector.clear()

        for point_name, point in (
            self.ros_node.saved_points.items()
        ):

            if point is None:

                text = (
                    f"{point_name} "
                    "(NOT SAVED)"
                )

            else:

                text = (
                    f"{point_name} "
                    f"[{point[0]:.2f}, "
                    f"{point[1]:.2f}, "
                    f"{point[2]:.2f}]"
                )

            self.point_selector.addItem(
                text
            )
        
def main():

    rclpy.init()

    ros_node = PendantROS()

    app = QApplication(sys.argv)

    window = PendantWindow(
        ros_node
    )

    window.show()

    timer = QTimer()

    timer.timeout.connect(
        lambda: (
            rclpy.spin_once(
                ros_node,
                timeout_sec=0
            ),
            window.update_status()
        )
    )

    timer.start(100)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
