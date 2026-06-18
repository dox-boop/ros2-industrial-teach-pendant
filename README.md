<img width="799" height="953" alt="image" src="https://github.com/user-attachments/assets/e34e1cd1-8741-4021-a556-e744f187b670" />
# ROS2 Industrial Teach Pendant

A ROS2-based industrial robot teach pendant developed using Python, PyQt6, and RViz.

This project simulates the core functionality of a real industrial robot teach pendant, allowing users to jog robot joints, teach positions, create robot programs, and execute motion sequences through a graphical interface.

---

## Features

### Robot Control

* Joint Jogging (J1, J2, J3)
* Home Function
* Stop Function
* Real-time Joint State Publishing
* RViz Robot Visualization

### Point Teaching

* Teach and save robot positions
* Support for multiple saved points (P1-P10)
* Display saved coordinates directly in the point selector
* Go-To-Point functionality

### Program Management

* Add taught points to a robot program
* Delete program steps
* Clear program
* Reorder steps (Move Up / Move Down)
* Automatic program step numbering
* Save program to file
* Load program from file

### Program Execution

* Sequential robot motion execution
* Wait-until-target-reached logic
* Point-by-point execution similar to industrial robot controllers

---

## Technologies Used

* ROS2 Humble
* Python 3
* PyQt6
* RViz2
* sensor_msgs/JointState
* std_msgs/String

---

## System Architecture

<img width="194" height="553" alt="image" src="https://github.com/user-attachments/assets/2ef89cd0-575d-4d77-89de-ebcfbf494d71" />


### ROS Topics

| Topic           | Purpose                        |
| --------------- | ------------------------------ |
| /joint_states   | Robot joint positions          |
| /robot_joints   | GUI position feedback          |
| /jog_command    | Joint jogging commands         |
| /goto_point     | Point-to-point motion commands |
| /target_reached | Motion completion notification |
| /motion_status  | Robot motion state             |

---

## Current Functionality

### Teach Pendant Interface

* Save robot positions
* Select saved points
* Execute point-to-point motion
* Create robot programs
* Execute programs sequentially
* Edit program order
* Save and load programs

### Motion Controller

The robot controller:

* Receives target positions
* Interpolates joint motion
* Publishes JointState messages
* Detects target completion
* Notifies the GUI when motion is complete

---

## Screenshots

### Teach Pendant GUI

<img width="799" height="953" alt="image" src="https://github.com/user-attachments/assets/d807f8fb-6e97-4fb5-af81-129a32c0f88b" />


### RViz Robot Simulation

<img width="1199" height="822" alt="image" src="https://github.com/user-attachments/assets/e5f41f6a-58da-4eab-80e9-cb6746cf9e93" />

<img width="1199" height="822" alt="image" src="https://github.com/user-attachments/assets/a8b9500e-afae-4aef-b9a1-48f5c9763b2e" />

---

## Example Workflow

1. Jog robot to desired position
2. Save position as P1
3. Move robot to another position
4. Save as P2
5. Create program:

   * P1
   * P2
   * P1
6. Run Program
7. Robot executes each point sequentially

---

## Future Improvements

### Short Term

* Pause Program
* Resume Program
* Program Pointer Highlighting
* Speed Override Control
* Better Motion Status Display

### Long Term

* STM32H747I-DISCO Deployment
* LVGL-Based Embedded GUI
* micro-ROS Integration
* Ethernet Communication
* Real Robot Hardware Interface
* 6-Axis Robot Support
* Tool Coordinate System Support
* User Authentication

---

## Educational Value

This project demonstrates:

* Robotics Software Development
* ROS2 Application Development
* Industrial Automation Concepts
* GUI Development
* State Machine Design
* Motion Control Concepts
* Embedded System Migration Planning

---

## Commands to use:

For Configuring the Build:
* cd ~/ros2_ws
  colcon build
  source install/setup.bash

For Opening GUI:
* ros2 run pendant_demo gui_pendant

For Opening Robot State Publisher:
* source /opt/ros/jazzy/setup.bash
  source ~/ros2_ws/install/setup.bash

  ros2 run robot_state_publisher robot_state_publisher \
  ~/ros2_ws/src/robot_description/urdf/simple_robot.urdf

For Joint-State controller
* ros2 run pendant_demo joint_state_controller

For opening RViz
* rviz2
  
---

## Author

Daksh

Industrial Robot Teach Pendant Project

Built as a robotics and embedded systems learning project with future deployment planned on STM32H747I-DISCO.
