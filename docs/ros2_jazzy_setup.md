# Ubuntu 24.04 + ROS2 Jazzy 环境

建议在 Apple Silicon Mac 上使用 Ubuntu 24.04 ARM64 虚拟机。

## 安装 ROS2 Jazzy

以 ROS2 官方 Jazzy Ubuntu 安装文档为准。安装完成后确认：

```bash
source /opt/ros/jazzy/setup.bash
ros2 doctor --report
```

## 安装学习所需组件

```bash
sudo apt update
sudo apt install \
  python3-colcon-common-extensions \
  python3-rosdep \
  ros-jazzy-ros2-control \
  ros-jazzy-ros2-controllers \
  ros-jazzy-rqt-graph
```

## 构建本仓库 ROS2 Workspace

```bash
cd ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```
