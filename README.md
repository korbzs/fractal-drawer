# Fractal Tree Drawing Program

## 🌳 Summary
This program draws **colorful fractal trees** using the ROS 2 `turtlesim` simulator. It begins with a trunk and recursively generates branching patterns, creating vivid and diverse tree structures.

---

## 📦 Program Overview

The program leverages ROS 2 and turtlesim to simulate fractal tree generation through turtle motion commands. Branches are recursively drawn and colored based on depth and selected styles.

### Key Methods

- `__init__`: Initializes the drawer with user-specified parameters (depth, angle, colors).
- `draw_fractal`: Main method to initiate drawing of the trunk and branches.
- `draw_branch`: Recursive function that creates branches and sub-branches up to a specified depth.
- `get_color`: Determines the color of each branch based on depth and the selected scheme.
- `draw_line`, `change_pen`, `teleport_to`: Utility functions to control the turtle's movement and drawing actions.

---

## 🛠️ Command Line Options

| Option            | Description                                                       | Default |
|-------------------|-------------------------------------------------------------------|---------|
| `--depth`         | Sets recursion depth (tree complexity)                            | `7`     |
| `--length`        | Sets the initial trunk length                                     | `2.0`   |
| `--angle`         | Sets the branching angle (degrees)                                | `30`    |
| `--color`         | Color scheme: `classic`, `autumn`, `winter`, `spring`, `fire`, `random` | `classic` |
| `--rainbow`       | Enables vibrant, depth-based color transitions                    | `False` |
| `--middle-branch` | Adds a central branch for denser tree structures                  | `False` |

---

## 🚀 Getting Started

1. Ensure you have a working ROS 2 setup.
2. Launch the turtlesim node:
   ```bash
   ros2 run turtlesim turtlesim_node!
Examples:

![Képernyőkép 2025-05-13 004803](https://github.com/user-attachments/assets/49c24127-d70c-4f38-8a05-06786210e400)
![Képernyőkép 2025-05-15 072857](https://github.com/user-attachments/assets/f398f20d-6c1b-4a23-8c99-a40a4ae459ee)
![Képernyőkép 2025-05-15 074314](https://github.com/user-attachments/assets/8378a326-3ec4-4fdf-ac7d-b9f9e237db0a)
![Képernyőkép 2025-05-15 091418](https://github.com/user-attachments/assets/f17bf7e9-9428-4f4e-b456-564d4723b123)



