from setuptools import find_packages, setup

package_name = "policy_runtime"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Maoxu Gao",
    maintainer_email="maogao623@gmail.com",
    description="Mock VLA policy publisher for ROS2 control-learning exercises.",
    license="MIT",
    entry_points={"console_scripts": ["mock_policy = policy_runtime.mock_policy:main"]},
)
