# game_xarm_target_publisher_subscriber

This prototype lets a developer click an archery target in a Pygame window, publishes the converted coordinates through ROS 2, and has a subscriber forward them to a Hiwonder xArm over USB. It is intended for coursework and controlled bench demonstrations; it is not a tracking system and it does not provide closed-loop motion control.

## Overview

The Pygame publisher converts clicks into two channel/value pairs and publishes a `std_msgs/msg/String` on `/student_data`. The subscriber parses that payload and calls the xArm controller. The actual contract in this checkout is the string payload `[[6, x], [4, y]]`, not `/target_xy` or a typed tracking message.

The source and subscriber are separate ROS 2 nodes. The architecture, class and sequence diagrams, test evidence, and known gaps are documented in [ARCHITECTURE.md](ARCHITECTURE.md).

The course design describes interchangeable target sources (a Pygame mock and an ARI adapter), but neither a `TargetSource` interface nor an ARI adapter is present in this checkout. Pygame currently publishes directly. This README describes the implementation that exists and does not claim the source-swap test has been completed.

## Prerequisites

- Ubuntu 24.04, or Ubuntu under WSL2 / a virtual machine.
- ROS 2 Jazzy installed and sourced in each terminal.
- Python 3, `pip`, `venv`, `colcon`, and a graphical display for Pygame.
- For physical movement, a Hiwonder xArm visible to Linux as a USB HID device.

For a fresh Ubuntu 24.04 install, follow the [official ROS 2 Jazzy Ubuntu instructions](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html), then source `/opt/ros/jazzy/setup.bash` in each terminal.

Install the basic Ubuntu tools if they are not already present:

```bash
sudo apt update
sudo apt install python3-pip python3-venv python3.12-venv python3-yaml python3-colcon-common-extensions usbutils
```

### USB access

On native Ubuntu, check that the arm is listed by `lsusb`. If it needs a udev rule, obtain the vendor/product IDs and access requirements for that exact controller; this checkout does not include verified IDs. A rule file may use this template after replacing both placeholders:

```text
SUBSYSTEM=="usb", ATTR{idVendor}=="<VENDOR_ID>", ATTR{idProduct}=="<PRODUCT_ID>", MODE="0660", GROUP="plugdev"
```

Save the verified rule under `/etc/udev/rules.d/`, then reload rules and reconnect the device:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

On Windows with WSL2 and `usbipd-win`, list devices in PowerShell, bind the xArm once if needed, then attach it to the active WSL distribution:

```powershell
usbipd list
usbipd bind --busid <BUS_ID>
usbipd attach --wsl --busid <BUS_ID>
```

In WSL, verify with:

```bash
lsusb
```

Do not infer that USB visibility proves that channel mapping or movement is safe. Confirm the device and movement in a restricted workspace before running the subscriber.

## Installation

From the workspace root, create a virtual environment that can see ROS 2's system Python packages, then install the pip-only runtime and test dependencies:

```bash
cd /path/to/capstone_ws
source /opt/ros/jazzy/setup.bash
python3 -m venv --system-site-packages src/publish_subsriber_xarm_target/.venv
source src/publish_subsriber_xarm_target/.venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pygame xarm hidapi pytest
python -c "import rclpy, yaml, pygame"
```

The ROS Python modules come from the sourced Jazzy installation, while packages such as `yaml` may come from Ubuntu's system Python. The virtual environment must therefore be created with `--system-site-packages`. An existing venv created without that option will not see `/usr/lib/python3/dist-packages`; create the project venv above and use its interpreter. If an isolated venv is required instead, install `PyYAML` into that venv with pip.

The ROS package manifest is `src/game_xarm_target_publisher_subscriber/package.xml`. Build and source the workspace:

```bash
colcon build --packages-select game_xarm_target_publisher_subscriber
source install/setup.bash
```

If an existing venv reports `ModuleNotFoundError: yaml`, it may be isolated from ROS's system Python packages. After sourcing Jazzy, check the system interpreter:

```bash
python3 -c "import rclpy, yaml, pygame"
```

In this workspace that check succeeds with `/usr/bin/python3`. Use it for the direct-script commands below, or create and activate the `--system-site-packages` venv above; do not use an older venv created without that option.

**Current checkout limitation:** the ROS package has no installed console-script entry points, so `ros2 run ... click_publisher` and `ros2 run ... xarm_node` are not available. The publisher and subscriber source files are currently standalone scripts in `src/publish_subsriber_xarm_target/python/`; the commands below run those scripts directly. The old nested `python/setup.py` is not a working install for the ROS package.

## Running

Open three terminals. In each, source ROS and activate the environment from the workspace root:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
cd src/publish_subsriber_xarm_target
```

Terminal 1 — start the Pygame publisher:

```bash
/usr/bin/python3 python/I_Hess_student_id_publisher.py
```

Terminal 2 — start the xArm subscriber **only after checking the USB device and safe workspace**:

```bash
/usr/bin/python3 python/I_Hess_student_id_subscriber.py
```

Terminal 3 — inspect the graph and messages:

```bash
ros2 node list
ros2 topic echo /student_data
```

Click the target window. A click at the top-left maps to `[[6, 1000], [4, 1000]]`; a click at the bottom-right maps to `[[6, 0], [4, 0]]`. The subscriber also sends `[[5, 300]]` after each target command. Treat that extra command as a hardware-specific behavior and verify it is safe before connecting the arm.

## Testing

Run the focused, hardware-free publisher tests:

```bash
cd /path/to/capstone_ws/src/publish_subsriber_xarm_target
python -m pytest -v python/test.py
```

These tests replace Pygame and ROS modules with fakes, simulate clicks, and inspect the published string. They verify the tested coordinate conversions and message payload without opening a display, starting ROS, connecting an xArm, or exercising the subscriber. They do **not** prove hardware calibration, subscriber parsing, or physical movement.

The current tests are also runnable directly with `python python/test.py`. The `game_xarm_target_publisher_subscriber` package's `colcon test` checks its ament template tests; it does not replace the focused publisher tests.

## API documentation

This checkout does not contain the requested `xarm_toolkit` package, `ArmController`, `TargetSource`, or either target-source implementation, so `pdoc src/xarm_toolkit/` cannot be run against it. The existing public methods have not been comprehensively audited to the requested API-docstring standard. Do not treat generated API docs as available until those APIs are added.

## Demo

The checked-in recording is [Xarm_demo_video.mov](videos/Xarm_demo_video.mov) (17.6 seconds by file metadata). It is shorter than the requested 20–30 seconds, and the repository does not establish that it records a complete, verified click-to-topic-to-physical-arm run.

## Licence

The project is licensed under MIT; see [LICENSE](LICENSE). `pygame`, `xarm`, and `hidapi` are installed separately and are not vendored here. Their exact versions, licences, and maintenance status have not been recorded in the supplied Part A evaluation; check each package's metadata before redistribution.
