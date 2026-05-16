# 🚗 Autonomous Vehicle Simulation — ROS 2 & Gazebo

A full-featured **4-wheel autonomous vehicle simulation** built with ROS 2 and Gazebo Classic. The robot uses an **Ackermann steering** model, is equipped with a **2D LiDAR** and **RGB camera**, and is controlled via the `ros2_control` framework.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Sensors](#sensors)
- [Controller Configuration](#controller-configuration)
- [License](#license)

---

## Overview

This package (`four_wheel_car`) simulates a golf-cart style autonomous vehicle in a custom Gazebo world. The vehicle model is defined using modular **Xacro** files and is fully integrated with `ros2_control` for hardware abstraction and controller management.

The simulation is designed as a foundation for autonomous driving research — perception, planning, and control algorithms can be layered on top of the provided sensor topics.

---

## ✨ Features

- ⚙️ **Ackermann Steering Controller** via `ros2_control`
- 📡 **2D LiDAR** sensor (360°, 20m range)
- 📷 **RGB Camera** (640×480, 10 Hz)
- 🏎️ **Realistic vehicle mesh** modelled in Blender (golf cart body + wheels)
- 🌍 **Custom Gazebo world**
- 📐 **Physically accurate inertia** calculations (box, cylinder, sphere macros)
- 🔁 **Odometry** publishing with TF support

---

## 🏗️ System Architecture

```
                      ┌─────────────────────────────┐
                      │     Robot State Publisher   │
                      │  (robot_description / URDF) │
                      └──────────────┬──────────────┘
                                     │
              ┌──────────────────────▼───────────────────────┐
              │               ros2_control                   │
              │   ┌──────────────────────────────────────┐   │
              │   │  joint_state_broadcaster             │   │
              │   │  ackermann_steering_controller       │   │
              │   └──────────────────────────────────────┘   │
              └──────────────────────┬───────────────────────┘
                                     │
              ┌──────────────────────▼──────────────────────┐
              │              Gazebo Classic                 │
              │   ┌───────────┐  ┌──────────┐  ┌────────┐   │
              │   │  Vehicle  │  │  LiDAR   │  │ Camera │   │
              │   │  Model    │  │ /scan    │  │/image  │   │
              │   └───────────┘  └──────────┘  └────────┘   │
              └─────────────────────────────────────────────┘
```

**Key Topics:**

| Topic | Type | Description |
|---|---|---|
| `/cmd_vel_ack_stamped` | `geometry_msgs/TwistStamped` | Velocity command input |
| `/odom` | `nav_msgs/Odometry` | Wheel odometry |
| `/scan` | `sensor_msgs/LaserScan` | LiDAR scan data |
| `/camera/image_raw` | `sensor_msgs/Image` | RGB camera feed |
| `/joint_states` | `sensor_msgs/JointState` | Joint positions & velocities |
| `/tf` | `tf2_msgs/TFMessage` | Transform tree |

---

## 📁 Project Structure

```
four_wheel_car/
├── config/
│   └── ackermann_controllers_config.yaml   # ros2_control parameters
├── launch/
│   └── gazebo_launch.py                    # Main launch file
├── meshes/
│   ├── golf_car.dae                        # Vehicle body (Blender)
│   └── wheel.dae                           # Wheel mesh (Blender)
├── urdf/
│   ├── main.xacro                          # Entry point
│   ├── car.urdf.xacro                      # Chassis & wheel joints
│   ├── camera.xacro                        # Camera sensor
│   ├── lidar.xacro                         # LiDAR sensor
│   ├── inertial.xacro                      # Inertia macros
│   └── robot_ros2_control.xacro            # ros2_control hardware interface
├── worlds/
│   ├── my_world.world                      # Gazebo world file
│   └── world/
│       ├── model.config
│       └── model.sdf
├── CMakeLists.txt
└── package.xml
```

---

## 🛠️ Prerequisites

- **OS:** Ubuntu 22.04 (Jammy)
- **ROS 2:** Humble Hawksbill
- **Gazebo:** Classic (Gazebo 11)

Required ROS 2 packages:

```bash
sudo apt install \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-ackermann-steering-controller \
  ros-humble-robot-state-publisher \
  ros-humble-xacro
```

---

## 📦 Installation

```bash
# 1. Create or navigate to your ROS 2 workspace
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src

# 2. Clone the repository
git clone https://github.com/MuhammedlFatih/Autonomous-Vehicle.git

# 3. Build the package
cd ~/ros2_ws
colcon build --packages-select four_wheel_car

# 4. Source the workspace
source install/setup.bash
```

---

## 🚀 Usage

### Launch the Simulation

```bash
ros2 launch four_wheel_car gazebo_launch.py
```

This will start:
- Gazebo Classic with the custom world
- Robot State Publisher
- `joint_state_broadcaster`
- `ackermann_steering_controller`

### Send Velocity Commands

```bash
ros2 topic pub /cmd_vel_ack_stamped geometry_msgs/msg/TwistStamped \
  '{header: {stamp: {sec: 0}}, twist: {linear: {x: 1.0}, angular: {z: 0.3}}}'
```

### Visualize in RViz

```bash
rviz2
```

Add the following displays: `RobotModel`, `LaserScan` (`/scan`), `Camera` (`/camera/image_raw`), `TF`.

---

## 🔭 Sensors

### 2D LiDAR

| Parameter | Value |
|---|---|
| Type | Ray sensor |
| Samples | 360 |
| Field of View | 360° (−π to π) |
| Min Range | 0.5 m |
| Max Range | 20 m |
| Update Rate | 10 Hz |
| Output Topic | `/scan` |

### RGB Camera

| Parameter | Value |
|---|---|
| Resolution | 640 × 480 |
| Horizontal FOV | ~62.4° |
| Near Clip | 0.05 m |
| Far Clip | 15.0 m |
| Update Rate | 10 Hz |
| Output Topic | `/camera/image_raw` |

---

## ⚙️ Controller Configuration

The Ackermann Steering Controller is configured in `config/ackermann_controllers_config.yaml`.

**Key parameters:**

| Parameter | Value |
|---|---|
| Wheelbase | 1.3 m |
| Front/Rear Track Width | 0.8 m |
| Wheel Radius | 0.175 m |
| Max Steering Angle | ±45° (±0.785 rad) |
| Controller Update Rate | 1000 Hz |
| Odometry Publish Rate | 50 Hz |

---

## 📄 License

This project is currently unlicensed. A license will be added in a future release.

---

## 👤 Author

**Muhammed Fatih**
- GitHub: [@MuhammedlFatih](https://github.com/MuhammedlFatih)

---

> *Built with ROS 2 Humble · Gazebo Classic · ros2_control*
