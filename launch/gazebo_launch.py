from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.substitutions import Command

def generate_launch_description():
    # URDF dosya yolu
    urdf_path = PathJoinSubstitution(
        [FindPackageShare('four_wheel_car'), 'urdf', 'main.xacro']
    )

    # Robot State Publisher node'u
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', urdf_path])}]
    )

    world_path = PathJoinSubstitution([
        FindPackageShare('four_wheel_car'),
        'worlds',
        'my_world.world'
    ])

    # Gazebo başlatma
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([FindPackageShare('gazebo_ros'), 'launch', 'gazebo.launch.py'])
        ]),
        launch_arguments={
            'world': world_path
        }.items()
    )

    # Robotu Gazebo'da spawn etme
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'four_wheel_car']
    )

    joint_state_broadcaster =Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster']

    )
    ackermann_steering_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['ackermann_steering_controller']
    )

    # Launch description döndürme
    return LaunchDescription([
        robot_state_publisher,
        gazebo_launch,
        spawn_entity,
        joint_state_broadcaster,
        ackermann_steering_controller,
    ])
