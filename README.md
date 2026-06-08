# ROS2 Robot Control Learning

面向 VLA / 机器人学习算法工程师的 ROS2 与机器人控制学习仓库。

目标不是只会运行 ROS2 Demo，而是能够实现并解释完整执行链路：

```text
observation -> policy -> action safety filter -> controller -> robot
```

## 当前环境

- 本机：Apple Silicon Mac，可直接运行 `control_foundations`
- ROS2：推荐 Ubuntu 24.04 ARM64 + ROS2 Jazzy
- 后续仿真：MuJoCo + Franka Panda

## 仓库结构

```text
.
├── control_foundations/       # 可直接在 macOS 运行的控制基础
│   ├── pid.py
│   ├── safety_filter.py
│   ├── trajectory.py
│   └── tests/
├── ros2_ws/src/
│   ├── policy_runtime/        # Python ROS2 模拟策略节点
│   └── safety_filter/         # C++ ROS2 动作安全过滤节点
└── docs/
    ├── roadmap.md
    └── ros2_jazzy_setup.md
```

## 在本机开始

```bash
python3 -m unittest discover -s control_foundations/tests -v
python3 -m control_foundations.demo
```

Demo 会模拟策略以较低频率输出 action chunk，控制循环进行插值、限幅和超时保护。

## 在 Ubuntu ROS2 Jazzy 中运行

安装 ROS2 后：

```bash
cd ros2_ws
colcon build --symlink-install
source install/setup.bash

# Terminal 1: 模拟策略，每 100ms 发布一个动作
ros2 run policy_runtime mock_policy

# Terminal 2: C++ 安全过滤器，限幅、限速并监测超时
ros2 run safety_filter safety_filter_node

# Terminal 3: 查看安全动作
ros2 topic echo /safe_action
```

## 六周目标

| 周次 | 主题 | 可验收成果 |
|---|---|---|
| 1 | ROS2 Topic、Service、Action、QoS、rosbag2 | 多节点通信与录包 |
| 2 | 坐标变换、正逆运动学、Jacobian | Panda 运动学 Notebook/脚本 |
| 3 | PID、轨迹插值、安全过滤 | 本仓库控制基础 Demo |
| 4 | ros2_control | RRBot 与自定义 Hardware Interface |
| 5 | MuJoCo + ROS2 控制闭环 | 仿真机械臂策略执行链路 |
| 6 | VLA Policy Runtime | 延迟统计、watchdog、故障恢复 |

详细任务见 [docs/roadmap.md](docs/roadmap.md)。

## 每次实验必须记录

- 控制频率和实际周期抖动
- 策略推理/消息传输延迟
- 过期动作数量
- 动作被限幅比例
- 跟踪误差
- 故障现象、定位过程和修复结果

## 学习原则

1. 每周提交一个可运行成果。
2. 每个节点都必须考虑时间戳、超时和异常输入。
3. 每次优化必须用指标验证。
4. 优先解释问题为什么发生，而不只是让 Demo 跑起来。
