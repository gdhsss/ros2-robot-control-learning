cmake_minimum_required(VERSION 3.8)
project(safety_filter)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(safety_filter_node src/safety_filter_node.cpp)
target_compile_features(safety_filter_node PUBLIC cxx_std_17)
ament_target_dependencies(safety_filter_node rclcpp std_msgs)
install(TARGETS safety_filter_node DESTINATION lib/${PROJECT_NAME})
ament_package()
