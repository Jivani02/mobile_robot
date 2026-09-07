# Mobile Robot — 4-Wheel Skid-Steer Robot with LiDAR, SLAM & Navigation

A mobile robot project built end-to-end: mechanical design → URDF → physics simulation → differential drive control → LiDAR sensing → SLAM mapping → autonomous navigation. Built as a hands-on learning and portfolio project covering the full robotics development pipeline in ROS1.

## Screenshots

**RViz — Robot model and TF frames**
![RViz view](docs/Rviz.png)

**Gazebo — Physics simulation**
![Gazebo view](docs/gazebo_1.png)

**LiDAR scan visualization**
![Gazebo scan](docs/gazebo_scan.png)

## Current Status

✅ **Mechanical design** — chassis and wheels designed in Fusion 360, assembled and mated in Onshape
✅ **URDF model** — generated via `onshape-to-robot`, validated in RViz
✅ **Physics simulation** — stable in Gazebo (tuned collision geometry and friction for realistic wheel-ground contact)
✅ **Differential drive** — 4-wheel skid-steer control via `libgazebo_ros_skid_steer_drive`, tested with keyboard teleop
✅ **LiDAR sensing** — simulated 360° 2D LiDAR publishing to `/scan`, verified in a realistic house environment
✅ **SLAM** — mapped the environment using `slam_toolbox`, saved as a reusable occupancy grid map
✅ **Navigation stack** — `move_base` + `amcl` configured with custom costmaps and local planner; autonomous goal-sending is functional

⚠️ **Known issue** — the `libgazebo_ros_skid_steer_drive` plugin's odometry reports a consistent ~90° yaw offset for this 4-wheel configuration (linear motion is correct; heading tracking is not). This affects `amcl` localization accuracy and `move_base` goal execution. A software correction node is planned; alternatively, migrating to `ros_control`'s `diff_drive_controller` (which has more standard odometry math) is a candidate fix.

🚧 **Planned next:**
- Odometry correction (software patch or controller migration)
- Autonomous frontier exploration (`explore_lite`)
- Stereo camera integration
- Independent 4-wheel drive (upgrade from skid-steer)

## Tech Stack

- **ROS1 (Noetic)**
- **Gazebo** (physics simulation)
- **Fusion 360** + **Onshape** (mechanical design, via `onshape-to-robot`)
- **slam_toolbox**, **move_base**, **amcl** (mapping and navigation)
- **Python** (ROS nodes)

## Repository Structure

```
mobile_robot/
├── urdf/         # Robot description (URDF)
├── meshes/       # STL mesh files for visual/collision geometry
├── launch/       # Launch files (Gazebo spawn, SLAM, navigation, RViz display)
├── config/       # Controller and navigation configuration YAML
├── worlds/       # Gazebo world files
├── maps/         # Saved SLAM maps
└── scripts/      # Python nodes
```

## Running the Simulation

```bash
# Spawn the robot in the house environment with LiDAR active
roslaunch mobile_robot gazebo.launch

# Drive it manually with the keyboard
rosrun teleop_twist_keyboard teleop_twist_keyboard.py

# Build a map with SLAM
roslaunch mobile_robot slam.launch

# Or navigate autonomously on a saved map
rosrun map_server map_server maps/house_map.yaml
roslaunch mobile_robot move_base.launch

#Spawn robot in Rviz
roslaunch mobile_robot mobile_robot.launch
```

## Key Engineering Challenges Solved

- **Unit scale mismatch**: diagnosed and fixed a 10x scale discrepancy introduced during the Fusion 360 → Onshape export pipeline, which had been causing unstable, exploding physics in simulation.
- **Collision geometry optimization**: replaced detailed mesh-based wheel collisions with simplified cylinder primitives to eliminate contact-point jitter and drift.
- **Friction tuning**: identified and resolved a friction/turning tradeoff specific to 4-wheel skid-steer geometry — high friction prevented in-place turning due to wheel scrubbing.
- **Navigation frame chain**: debugged a broken `map → odom → body1` TF chain by correctly configuring `amcl` alongside `move_base`, after discovering `move_base` reads several parameters from its own namespace independent of the individual costmap configs.

## Roadmap

Six of ten planned project phases complete. See commit history for detailed progress.
