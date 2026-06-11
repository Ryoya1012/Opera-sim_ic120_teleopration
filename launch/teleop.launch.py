import os
from launch import LaunchDescription
from launch_ros.actions import Node

# ROS2のLaunchファイルは, 必ずこの関数から始まる
def generate_launch_description():
    # ---ブロック1: joy_nodeび起動設定 ---
    joy_node = Node(
                package = 'joy',    # パッケージ名
                executable = 'joy_node',    # 実行ファイル名
                name = 'joy_node'   # 起動した時のノード名
            )

    # --- ブロック2: ic120_teleop_nodeの起動設定 ---
    teleop_node = Node(
                package = 'ic120_teleop',
                executable = 'ic120_teleop_node',
                name = 'ic120_teleop_node'
            )

    # ---ブロック3: まとめて実行
    return LaunchDescription([
            joy_node,
            teleop_node
        ])
