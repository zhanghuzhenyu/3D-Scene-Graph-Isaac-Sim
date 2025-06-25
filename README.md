# 3D-Scene-Graph-Isaac-Sim

A Python script for inspecting prims in a USD scene within Isaac Sim, extracting and displaying their properties including transforms, bounding boxes, and semantic information.

## Features

- Reads specified prim paths from a USD scene file
- Extracts and displays for each prim:
  - World position
  - Orientation (as quaternion)
  - 3D bounding box dimensions
  - Semantic information (type and data)
- Periodic output during simulation runtime

## Requirements

- NVIDIA Isaac Sim (tested with version 4.0.0)


## Usage

1. Modify the following variables in the script:
   - `asset_path`: Path to your USD scene file
   - `prim_paths`: List of prim paths to inspect

2. Run the script within Isaac Sim's Python environment:

```bash
./python.sh gt-sg.py
