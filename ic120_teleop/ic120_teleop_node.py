'''
 Create Date : 2026/06/11
 Author : Ryoya SATO
 License : Apach-2.0
'''

import rclpy            # ROS2の通信システムを使用するための基本機能
from rclpy.node import Node     # ROS2のプログラミングの単位である"ノード"の設計図

# 今回使用するメッセージの型(データの型)を読み込む
from com3_msgs.msg import JointCmd  # 履帯の制御用
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy     # コントローラからの入力データ用


# 新しいノードの設計図を作成
class IC120TeleopNode( Node):
    def __init__( self):
        #システムに[ic120_teleop_node]という名前で登録
        super().__init__('ic120_teleop_node')

        # --- 通信の準備 ---
        # [送信口1] 履帯(スプロケット)への指令
        self.pub_cmd_vel = self.create_publisher( Twist, '/ic120_0/cmd_vel', 10)

        # [送信口2] ベゼル(荷台)の排土指令
        self.pub_dump = self.create_publisher( JointCmd, '/ic120_0/rot_dump_cmd', 10)
        
        # [受信口] コントローラの操作データを受信
        self.sub_joy = self.create_subscription( Joy, '/joy', self.joy_callback, 10)

        # --- パラメータの定義 ---
        self.declare_parameter( 'max_linear_vel', 2.0)   # 前進の最大速度
        self.declare_parameter( 'turn_scale', 1.5)    # 旋回の切れ具合
        self.declare_parameter( 'dump_joint_name', 'dump_joint')
        self.declare_parameter( 'dump_speed', 0.05) # ベゼルが傾くスピード


        # コントローラのボタン割り当て(PlayStation 5 DualSenseを想定)
        self.axis_left_y = 1    # 左stick上下(左履帯)
        self.axis_right_y = 4   # 右stick上下(右履帯)
        self.button_r1 = 5      # R1button(ベゼルを上げる)
        self.button_l1 = 4      # L1button(ベゼルを下げる)

        # ベゼルの現在の角度を記憶しておく変数
        self.current_dump_angle = 0.0

        self.get_logger().info("--- IC120 Teleop Ready --- ")


    # データを受信した際の処理
    def joy_callback( self, msg):
        # --- 1. 足回り(履帯)の制御 ---
        max_vel = self.get_parameter( 'max_linear_vel').value
        turn_scale = self.get_parameter( 'turn_scale').value
        
        # stickの傾きから仮想的な左右クローラ速度を計算
        v_L = msg.axes[ self.axis_left_y] * max_vel
        v_R = msg.axes[ self.axis_right_y] * max_vel

        # Twist(並進と旋回)に変換して送信
        twist_msg = Twist()
        twist_msg.linear.x = ( v_R + v_L) / 2.0
        twist_msg.angular.z = ( v_R - v_L) * turn_scale
        self.pub_cmd_vel.publish( twist_msg)

        # --- 2. ベゼル(荷台)の制御
        dump_speed = self.get_parameter( 'dump_speed').value
        dump_name = self.get_parameter( 'dump_joint_name').value
        
        # R1 buttonが押下されいる間角度を増やす
        if msg.buttons[self.button_r1] == 1:
            self.current_dump_angle += dump_speed

        # L1 buttonが押下されている間角度を減らす
        elif msg.buttons[self.button_l1] == 1:
            self.current_dump_angle -= dump_speed

        # dump角度制限
        if self.current_dump_angle > 1.0:
            self.current_dump_angle = 1.0
        elif self.current_dump_angle < 0.0:
            self.current_dump_angle = 0.0

        # JointCmdメッセージを組み立てて送信
        dump_msg = JointCmd()
        dump_msg.joint_name = [dump_name]
        dump_msg.position = [self.current_dump_angle]
        self.pub_dump.publish(dump_msg)

def main( args=None):
    rclpy.init( args=args)  # ROS2を開始
    node = IC120TeleopNode()    # 設計図から実体を作る
    try:
        rclpy.spin( node)   # nodeを待機状態にする( ここでloopさせる)
    except KeyboardInterrupt:
        pass    # Ctrl+Cで終了した場合はエラーを出さない
    finally:
        node.destroy_node() # nodeを殺す
        rclpy.shutdown()    # ROS2を終了

if __name__ == '__main__':
    main()
