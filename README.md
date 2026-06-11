# Opera-sim_ic120_teleopration

## 概要
- このパッケージは, Opera-siｍ(PhysX, AGX)内に実装されたic120(クローラダンプ)を, Dual Senseで操作を行うものである.
- Dual Senseの左右のjoy_stickがic120の左右の履帯回転量を制御し前後進・旋回を行うことができる.
- L1, R1ボタンを押下することでベゼル(荷台)をチルトさせることができる.

## 使用パッケージ
- [ps_ros2_common](https://github.com/Ar-Ray-code/ps_ros2_common/)

## ビルド・実行手順
```bash
cd ~/ros2_ws/src
```
```bash
git clone https://github.com/Ar-Ray-code/ps_ros2_common.git
```
```bash
git clone https://github.com/Ryoya1012/Opera-sim_ic120_teleopration.git
```
```bash
colcon build --packages-select joy_controller ic120_teleop
```
```bash
source install/setup.bash
```
```bash
ros2 launch ic120_teleop teleop.launch.py
```
