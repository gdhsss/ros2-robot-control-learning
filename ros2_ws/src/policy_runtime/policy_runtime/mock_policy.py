"""Publish deterministic joint targets as a stand-in for a VLA policy."""

import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class MockPolicy(Node):
    def __init__(self) -> None:
        super().__init__("mock_policy")
        self.publisher = self.create_publisher(Float64MultiArray, "/policy_action", 10)
        self.started_ns = self.get_clock().now().nanoseconds
        self.timer = self.create_timer(0.1, self.publish_action)
        self.get_logger().info("Publishing mock 7-DoF policy actions at 10 Hz")

    def publish_action(self) -> None:
        elapsed_s = (self.get_clock().now().nanoseconds - self.started_ns) / 1e9
        msg = Float64MultiArray()
        msg.data = [0.3 * math.sin(elapsed_s + joint * 0.2) for joint in range(7)]
        self.publisher.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MockPolicy()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
