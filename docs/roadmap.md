# 学习路线与验收清单

## Week 1：ROS2 通信与调试

- [ ] 创建 Python 和 C++ Package
- [ ] 掌握 Topic、Service、Action 的使用场景
- [ ] 修改 QoS 并观察丢包行为
- [ ] 使用 `ros2 topic hz`、`ros2 topic delay` 和 `rqt_graph`
- [ ] 使用 rosbag2 记录和回放状态/动作

验收：模拟策略节点发布动作，C++ 节点过滤后发布安全动作；能够解释消息频率、延迟和超时。

## Week 2：坐标变换与运动学

- [ ] 实现旋转矩阵、四元数和齐次变换
- [ ] 推导并实现 Franka 正运动学
- [ ] 数值验证 Jacobian
- [ ] 使用 TF2 发布和查询坐标变换
- [ ] 比较 joint-space 与 Cartesian-space 动作

验收：输入关节状态，输出末端位姿；输入末端速度，计算关节速度。

## Week 3：反馈控制

- [ ] 实现 PID 与 anti-windup
- [ ] 实现轨迹插值、低通滤波、速度/加速度限制
- [ ] 注入 50/100/200ms 延迟并记录跟踪误差
- [ ] 对比不同控制频率

验收：给出一份包含 overshoot、settling time、RMSE 的实验报告。

## Week 4：ros2_control

- [ ] 跑通 RRBot Demo
- [ ] 理解 controller manager 的 `read-update-write`
- [ ] 使用 joint_state_broadcaster
- [ ] 使用 joint_trajectory_controller
- [ ] 编写最小 Hardware Interface

验收：能够画出 ros2_control 架构，并解释 command/state interface。

## Week 5：MuJoCo 控制闭环

- [ ] 加载 Franka Panda
- [ ] 接入状态与动作 Topic
- [ ] 记录控制频率、动作延迟、跟踪误差
- [ ] 验证 watchdog 与异常动作保护

验收：演示仿真机械臂在延迟和异常动作下保持安全。

## Week 6：VLA Policy Runtime

- [ ] 观测同步
- [ ] Action chunk 缓冲
- [ ] 推理超时与 fallback
- [ ] Emergency stop
- [ ] 延迟与错误指标
- [ ] README、架构图、演示视频、失败分析

验收：作品集能够证明你能负责策略输出到机器人执行器之间的完整链路。
