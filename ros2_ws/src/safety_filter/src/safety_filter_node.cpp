#include <algorithm>
#include <chrono>
#include <functional>
#include <memory>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64_multi_array.hpp"

using namespace std::chrono_literals;

class SafetyFilterNode : public rclcpp::Node {
 public:
  SafetyFilterNode() : Node("safety_filter"), previous_action_(7, 0.0) {
    action_limit_ = declare_parameter("action_limit", 1.0);
    max_delta_ = declare_parameter("max_delta_per_message", 0.08);
    timeout_ms_ = declare_parameter("timeout_ms", 200);
    publisher_ = create_publisher<std_msgs::msg::Float64MultiArray>("/safe_action", 10);
    subscription_ = create_subscription<std_msgs::msg::Float64MultiArray>(
        "/policy_action", 10, std::bind(&SafetyFilterNode::on_action, this, std::placeholders::_1));
    watchdog_ = create_wall_timer(50ms, std::bind(&SafetyFilterNode::check_timeout, this));
    last_action_time_ = now();
    RCLCPP_INFO(get_logger(), "Safety filter ready for 7-DoF actions");
  }

 private:
  void on_action(const std_msgs::msg::Float64MultiArray::SharedPtr message) {
    if (message->data.size() != previous_action_.size()) {
      RCLCPP_ERROR(get_logger(), "Rejected action with dimension %zu", message->data.size());
      return;
    }
    std_msgs::msg::Float64MultiArray safe_message;
    safe_message.data.reserve(message->data.size());
    for (std::size_t joint = 0; joint < message->data.size(); ++joint) {
      const double position_limited = std::clamp(message->data[joint], -action_limit_, action_limit_);
      const double delta = std::clamp(position_limited - previous_action_[joint], -max_delta_, max_delta_);
      safe_message.data.push_back(previous_action_[joint] + delta);
    }
    previous_action_ = safe_message.data;
    last_action_time_ = now();
    timed_out_ = false;
    publisher_->publish(safe_message);
  }

  void check_timeout() {
    const auto elapsed_ms = (now() - last_action_time_).nanoseconds() / 1000000;
    if (elapsed_ms > timeout_ms_ && !timed_out_) {
      timed_out_ = true;
      RCLCPP_WARN(get_logger(), "Policy action timeout after %ld ms; holding position", elapsed_ms);
      std_msgs::msg::Float64MultiArray hold_message;
      hold_message.data = previous_action_;
      publisher_->publish(hold_message);
    }
  }

  double action_limit_;
  double max_delta_;
  int64_t timeout_ms_;
  bool timed_out_{false};
  std::vector<double> previous_action_;
  rclcpp::Time last_action_time_;
  rclcpp::Publisher<std_msgs::msg::Float64MultiArray>::SharedPtr publisher_;
  rclcpp::Subscription<std_msgs::msg::Float64MultiArray>::SharedPtr subscription_;
  rclcpp::TimerBase::SharedPtr watchdog_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SafetyFilterNode>());
  rclcpp::shutdown();
  return 0;
}
