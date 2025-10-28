import os
from ament_index_python.packages import get_package_share_directory
import xacro
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch import LaunchDescription
from launch.actions import TimerAction, ExecuteProcess
from launch.substitutions import PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command


def generate_launch_description():
    # Paketin share dizinini al
    pkg_share = get_package_share_directory("btkamr_description")
    urdf_path = os.path.join(pkg_share, "urdf", "mobile_base/main.urdf.xacro")
    robot_desc = ParameterValue(Command(["xacro ", urdf_path]), value_type=str) # boşluk önemli xacro' '

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gz', 'sim', 'empty.sdf', '-v', '4'],
            output='screen'
        ),
        Node( 
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]
        ),
        Node( # Gazebo'ya spawn et
            package='ros_gz_sim',
            executable='create',
            output='screen',
            parameters=[{'topic': 'robot_description'}]
        )
    ])